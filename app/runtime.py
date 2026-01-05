from .db import duckdb_connection, table_registration
from .graph import create_app_graph

# Initializing duckdb, data table and building graph
def init_graph():
    conn = duckdb_connection()
    table_registration(conn)
    graph = create_app_graph(conn)
    return graph

# Run user question through graph and return route, result
def run_question(graph, question):
    state = {"input": question}
    final_state = graph.invoke(state)
    route = final_state.get("route", "analysis")
    if route == "analysis":
        output = final_state.get("analyst_result", "") or ""
        image_path = None
        steps = final_state.get("analyst_steps", []) or []
    elif route == "analysis_with_chart":
        output = final_state.get("chart_result", "") or ""
        image_path = final_state.get("image_path")
        steps = final_state.get("chart_steps", []) or []
    elif route == "definition":
        output = final_state.get("glossary_result", "") or ""
        image_path = None
        steps = []
    else:
        output = "I only handle questions about Apple's financials."
        image_path = None
        steps = []
    return route, {"output": output, "image_path": image_path, "intermediate_steps": steps}