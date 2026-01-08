import re
from typing import TypedDict, Any, List, Optional
from langgraph.graph import StateGraph, END
from .db import get_table_columns
from .tools import create_glossary_rag_tool, create_metric_over_time_tool, create_multi_metrics_over_time_tool, create_sql_query_tool, create_plot_metric_over_time_tool, create_schema_info_tool, create_plot_multi_metrics_over_time_tool
from .agents import create_glossary_agent, create_analyst_agent, create_chart_agent, create_router_chain
from .config import data_dir

# Graph state ( basically my state definition, memory going to be shared on the run)
class GraphState(TypedDict, total = False):
    input: str
    route: str
    analyst_result: str
    analyst_steps: List[Any]
    chart_result: str
    chart_steps: List[Any]
    image_path: Optional[str]
    glossary_result: str
    
def extract_year_bounds(question: str):             # fallback 1 if chart doesnt show image
    years = [int(year) for year in re.findall(r"\b(19\d{2}|20\d{2})\b", question)]
    if not years:
        return None, None
    if len(years) == 1:
        return years[0], None
    return min(years), max(years)

def resolve_metrics_from_question(question: str, available_columns: List[str]) -> List[str]: #fallback 1 functioon to hardcode aliases
    q = question.lower()
    available = set(available_columns)
    aliases = {
        "operating income": "operating_income_millions",
        "op income": "operating_income_millions",
        "net income": "net_income_millions",
        "revenue": "revenue_millions",
        "gross profit": "gross_profit_millions",
        "ebitda": "ebitda_millions",
        "gross margin": "gross_margin",
        "net profit margin": "net_profit_margin",
        "operating margin": "operating_margin",
        "cash": "cash_on_hand_millions",
        "cash on hand": "cash_on_hand_millions",
        "long term debt": "long_term_debt_millions",
        "total assets": "total_assets_millions",
        "total liabilities": "total_liabilities_millions",
        "shares outstanding": "shares_outstanding",
        "employees": "employees",
        "eps": "eps",
        "pe ratio": "pe_ratio",
    }
    metrics = []
    for phrase, column in aliases.items():
        if phrase in q and column in available:
            metrics.append(column)
    for column in available:
        if column in q and column not in metrics:
            metrics.append(column)
    return metrics


# ------------- Graph factory -------------
def create_app_graph(conn):
    persist_dir = str((data_dir / "chroma_glossary").resolve())     # persist chroma save memory?
    # tools -
    glossary_tool = create_glossary_rag_tool(persist_directory=persist_dir)
    metric_tool = create_metric_over_time_tool(conn)
    multi_metric_tool = create_multi_metrics_over_time_tool(conn)
    sql_tool = create_sql_query_tool(conn)
    plot_tool = create_plot_metric_over_time_tool(conn)
    plot_multi_tool = create_plot_multi_metrics_over_time_tool(conn)
    schema_tool = create_schema_info_tool(conn)
    # tool sets per agent -
    analyst_tools = [schema_tool, metric_tool, multi_metric_tool, sql_tool]
    chart_tools = [schema_tool, metric_tool, multi_metric_tool, sql_tool, plot_tool, plot_multi_tool]
    glossary_tools = [glossary_tool]
    
    # router + agents -
    router_chain = create_router_chain()
    glossary_agent = create_glossary_agent(glossary_tools)
    analyst_agent = create_analyst_agent(analyst_tools)
    chart_agent = create_chart_agent(chart_tools)
    
    # nodes - 
    def glossary_node(state: GraphState):
        question = state["input"]
        result = glossary_agent.invoke({"input": question})
        out = result.get("output")
        if isinstance(out, list):
            out = "\n".join([x.get("text","") for x in out if isinstance(x, dict)])
        return {"glossary_result": out}
    
    def router_node(state: GraphState):
        question = state["input"]
        route_label = router_chain.run(input=question).strip().lower().strip("`'\" .,\n\t")
        route_label = route_label.split()[0]
        q = question.lower()
        chart_triggers = ("plot", "chart", "graph", "visualize", "trend", "over time", "line chart", "bar chart", "compare", "versus", " vs ")
        definition_triggers = ("define", "definition", "meaning of", "what is ", "what does ")
        if any(t in q for t in definition_triggers) and "what was" not in q and not any(t in q for t in chart_triggers):
            route_label = "definition"
        elif any(t in q for t in chart_triggers):
            route_label = "analysis_with_chart"
        else:
            route_label = "analysis"
        allowed = {"analysis", "analysis_with_chart", "definition", "other"}
        if route_label not in allowed:
            route_label = "analysis"
        return {"route": route_label}
    
    def analyst_node(state: GraphState):
        question = state["input"]
        result = analyst_agent.invoke({"input": question})
        out = result.get("output")
        if isinstance(out, list):
            out = "\n".join([x.get("text","") for x in out if isinstance(x, dict)])
        return {
            "analyst_result": out,
            "analyst_steps": result.get("intermediate_steps", [])
            }
    
    def chart_node(state: GraphState):
        question = state["input"]
        result = chart_agent.invoke({"input": question})
        out = result.get("output")
        if isinstance(out, list):
            out = "\n".join([x.get("text","") for x in out if isinstance(x, dict)])
        steps = result.get("intermediate_steps", [])
        image_path = None
        for action, obs in steps:
            if isinstance(obs, dict) and "image_path" in obs:
                image_path = obs["image_path"]
        if image_path is None:                                  ###### main fallback path image failure bug?
            available_columns = get_table_columns(conn)
            metrics = resolve_metrics_from_question(question, available_columns)
            start_year, end_year = extract_year_bounds(question)
            if len(metrics) >= 2:
                fallback = plot_multi_tool.invoke({
                    "metrics": metrics[:3],
                    "start_year": start_year,
                    "end_year": end_year,
                    "title": "Financial Comparison",
                })
                if isinstance(fallback, dict):
                    image_path = fallback.get("image_path")
            elif len(metrics) == 1:
                fallback = plot_tool.invoke({
                    "metric": metrics[0],
                    "start_year": start_year,
                    "end_year": end_year,
                    "title": None,
                })
                if isinstance(fallback, dict):
                    image_path = fallback.get("image_path")
        return {
            "chart_result": out,
            "chart_steps": steps,
            "image_path": image_path,
            }

    # graph topology -
    workflow = StateGraph(GraphState)
    workflow.add_node("glossary", glossary_node)
    workflow.add_node("router", router_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("chart", chart_node)
    workflow.set_entry_point("router")
    
    # control flow & edge logic - 
    def route_decider(state: GraphState):
        route = state.get("route", "analysis")
        if route == "analysis":
            return "analyst"
        if route == "analysis_with_chart":
            return "chart"
        if route == "definition":
            return "glossary"
        return "end"
    
    # orchestration logic -
    workflow.add_conditional_edges(
        "router",
        route_decider,
        {
            "analyst": "analyst",
            "chart": "chart",
            "glossary": "glossary",
            "end": END
            })
    
    workflow.add_edge("analyst", END)
    workflow.add_edge("chart", END)
    workflow.add_edge("glossary", END)
    app = workflow.compile()
    return app