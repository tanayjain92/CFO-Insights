from typing import Optional
from .db import run_sql, get_table_columns
import pandas as pd

# Metric from yearA to yearB
def metric_over_time(conn, metric, start_year: Optional[int] = None, end_year: Optional[int] = None):
    available = set(get_table_columns(conn))
    if metric not in available:
        error = (
            f"Metric '{metric}' not found in table. Available columns: "
            f"{', '.join(sorted(available))}."
            )
        return pd.DataFrame({"error": [error]})
    where_clauses = ["1=1"]
    if start_year is not None:
        where_clauses.append(f"year >= {int(start_year)}")
    if end_year is not None:
        where_clauses.append(f"year <= {int(end_year)}")
    where_sql = " AND ".join(where_clauses)

    # query string -
    query = f"""
        SELECT
            year,
            {metric}
        FROM apple_financials
        WHERE {where_sql}
        ORDER BY year
        """
    df = run_sql(conn, query)
    return df

# Metric between yearA, yearB
def metric_btwn_yrs(conn, metric, year_a, year_b):
    query = f"""
        SELECT
            year,
            {metric}
        FROM apple_financials
        WHERE year in ({year_a}, {year_b})
        ORDER BY year
        """
    df = run_sql(conn, query)
    # error, logic checks -
    if "error" in df.columns:
        return df
    if len(df) != 2:     #2-year delta 
        return df
    
    # FE metrics -
    value_a = df.loc[0, metric]
    value_b = df.loc[1, metric]
    delta_abs = value_b - value_a
    delta_pct = (delta_abs / value_a) if value_a not in (0, None) else None
    df["delta_abs"] = delta_abs
    df["delta_pct"] = delta_pct
    return df  

# MetricA, metricB + horizon
def multi_metrics_over_time(conn, metrics, start_year: Optional[int] = None, end_year: Optional[int] = None):
    available = set(get_table_columns(conn))
    missing = [metric for metric in metrics if metric not in available]
    if missing:
        error = (
            "Metrics not found in table: "
            f"{', '.join(missing)}. Available columns: {', '.join(sorted(available))}."
        )
    return pd.DataFrame({"error": [error]})
    # build SELECT list: year + each metric-
    select_cols = ["year"] + metrics
    select_sql = ", ".join(select_cols)
    where_clauses = ["1=1"]
    if start_year is not None:
        where_clauses.append(f"year >= {int(start_year)}")
    if end_year is not None:
        where_clauses.append(f"year <= {int(end_year)}")
    where_sql = " AND ".join(where_clauses)
    
    query = f"""
        SELECT
            {select_sql}
        FROM apple_financials
        WHERE {where_sql}
        ORDER BY year
    """
    df = run_sql(conn, query)
    return df

# Metric growth
def metric_with_growth(conn, metric, start_year: Optional[int] = None, end_year: Optional[int] = None):
    df = metric_over_time(conn, metric, start_year, end_year)
    # error checks -
    if "error" in df.columns or df.empty:
        return df
    df = df.sort_values("year").reset_index(drop=True)

    # using pct_change to compute YoY growth -
    df["growth_pct"] = df[metric].pct_change()
    return df