from pydantic import BaseModel, Field
from typing import Optional, List
from langchain_core.tools import StructuredTool
from .rag_glossary import get_glossary_retriever
from .metrics import metric_over_time, multi_metrics_over_time
from .db import run_sql
from .charts import plot_metric_over_time
from .config import base_dir
import os
import uuid
import matplotlib.pyplot as plt

### ---Classes---

class GlossaryRAGInput(BaseModel):
    question: str = Field(
        ...,
        description = "Natural language question asking for definitions or explanations of financial terms, KPIs, or concepts from the Apple financial glossary file.")

class MetricOverTimeInput(BaseModel):
    metric: str = Field(
        ...,
        description = "Name of the financial metric column. Examples: 'revenue_millions', 'net_income_millions', 'eps', 'net_profit_margin'.")
    start_year: Optional[int] = Field(
        None,
        description = "First year inclusive. If blank/omitted, use earliest year.")
    end_year: Optional[int] = Field(
        None,
        description = "Last year inclusive. If blank/omitted, use latest year.")

class MultiMetricsOverTimeInput(BaseModel):
    metrics: List[str] = Field(
        ...,
        description = "List of metrics to retrieve over time. Examples: ['revenue_millions', 'net_income_millions', 'eps'].")
    start_year: Optional[int] = Field(
        None,
        description = "First year inclusive. If blank/omitted, use earliest year.")
    end_year: Optional[int] = Field(
        None,
        description = "Last year inclusive. If blank/omitted, use latest year.")

class SQLQueryInput(BaseModel):
    query: str = Field(
        ...,
        description = "A valid SQL query over the data table. Example: 'SELECT year, revenue_millions FROM apple_financials WHERE year >= 2015'.")    

class PlotMetricOverTimeInput(BaseModel):
    metric: str = Field(
        ...,
        description = "Metric to plot over time. Examples: 'revenue_millions', 'net_income_millions', 'eps'.")
    start_year: Optional[int] = Field(
        None,
        description = "First year inclusive. If blank/omitted, use earliest year.")
    end_year: Optional[int] = Field(
        None,
        description = "Last year inclusive. If blank/omitted, use latest year.")
    title: Optional[str] = Field(
        None,
        description= "Optional chart title.")
    
### ---Tools---

# Glossary RAG tool
def create_glossary_rag_tool(persist_directory = None):
    retriever = get_glossary_retriever(persist_directory = persist_directory)
    def run(question: str):
        docs = retriever.invoke(question)
        if not docs:
            return []
        results = []
        for doc in docs:
            meta = doc.metadata or {}
            results.append(
                {
                    "content": doc.page_content,
                    "source": meta.get("source", ""),
                    "start_index": meta.get("start_index", None),
                    }
                )
        return results
        
    tool = StructuredTool.from_function(
        func = run,
        name = "glossary_rag_tool",
        description = ("Use this to look up definitions, explanations of Apple financial metrics and concepts from the glossary file. Return relevant glossary excerpts."),
        args_schema = GlossaryRAGInput
        )
    return tool

# MetricOverTime tool
def create_metric_over_time_tool(conn):
    if conn is None:
        raise ValueError("Connection is None. Please call duckdb_connection() and table_registration() properly.")
    def run(metric, start_year = None, end_year = None):
        df = metric_over_time(conn, metric, start_year, end_year)
        if "error" in df.columns:
            return [{"error": df.loc[0, "error"]}]
        if df.empty:
            return []
        return df.to_dict(orient="records")

    tool = StructuredTool.from_function(
        func = run,
        name = "metric_over_time_tool",
        description = ("Use to retrieve historical financial data for a metric over a range of years."),
        args_schema = MetricOverTimeInput
        )   
    return tool

# MultiMetricsOverTime tool
def create_multi_metrics_over_time_tool(conn):
    if conn is None:
        raise ValueError("Connection is None. Please call duckdb_connection() and table_registration() properly.")
    def run(metrics, start_year = None, end_year = None):
        df = multi_metrics_over_time(conn, metrics, start_year, end_year)
        if "error" in df.columns:
            return [{"error": df.loc[0, "error"]}]
        if df.empty:
            return []
        return df.to_dict(orient="records")
    
    tool = StructuredTool.from_function(
        func = run,
        name = "multi_metrics_over_time_tool",
        description = ("Use to retrieve historical financial data for multiple metrics over a range of years."),
        args_schema = MultiMetricsOverTimeInput
        )
    return tool

# SQL tool
def create_sql_query_tool(conn):
    if conn is None:
        raise ValueError("Connection is None. Please call duckdb_connection() and table_registration() properly.")
    def run(query: str):
        df = run_sql(conn, query)
        if "error" in df.columns:
            return [{"error": df.loc[0, "error"]}]
        if df.empty:
            return []
        return df.to_dict(orient="records")

    tool = StructuredTool.from_function(
        func = run,
        name = "sql_query_tool",
        description = "Use to run custom SQL queries over the data table with complex filters, conditions, joins.",
        args_schema=SQLQueryInput
        )
    return tool

# PlotMetricOverTime tool
def create_plot_metric_over_time_tool(conn, charts_dir = None):
    if charts_dir is None:
        charts_dir = str((base_dir/"charts").resolve())
    os.makedirs(charts_dir, exist_ok = True)
    if conn is None:
        raise ValueError("Connection is None. Please call duckdb_connection() and table_registration() properly.")
    os.makedirs(charts_dir, exist_ok=True)
    def run(metric, start_year = None, end_year = None, title=None):
        fig, df = plot_metric_over_time(conn, metric, start_year, end_year, title)
        if fig is None or df is None:
            return {"error": "Plot function returned no figure/data."}
        if hasattr(df, "columns") and "error" in df.columns:
            return {"error": str(df.loc[0, "error"])}
        if getattr(df, "empty", False):
            return {"error": "No data returned for that metric/year range."}
        filename = f"{metric}_{uuid.uuid4().hex}.png"
        image_path = os.path.join(charts_dir, filename)
        fig.savefig(image_path, bbox_inches="tight")
        plt.close(fig)
    
        return {
            "image_path": image_path,
            "data": df.to_dict(orient="records"),
        }

    tool = StructuredTool.from_function(
        func=run,
        name="plot_metric_over_time_tool",
        description=(
            "Generates a time-series line chart for a metric over years and return a file path to the saved chart image and the underlying data."),
        args_schema=PlotMetricOverTimeInput,
    )
    return tool