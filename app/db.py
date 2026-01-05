import duckdb
import pandas as pd
from .data_loader import cleaned_data

# Duckdb to db connection
def duckdb_connection(db_path = ":memory:"):
    conn = duckdb.connect(database = db_path, read_only = False)
    return conn

# Data2table
def table_registration(conn):
    df = cleaned_data()
    conn.register("apple_financials", df)

def get_table_columns(conn, table_name: str = "apple_financials"):
    info = conn.execute(f"PRAGMA table_info('{table_name}')").df()
    if "name" not in info.columns:
        return []
    return info["name"].tolist()
        
def run_sql(conn, query):
    try:
        output_table = conn.execute(query).df()
        return output_table
    except (duckdb.Error, AttributeError) as e:
        columns = get_table_columns(conn)
        columns_hint = f" Available columns: {', '.join(columns)}." if columns else ""
        error = f"SQL query failed. Error: {str(e).splitlines()[0]}.{columns_hint}"
        print(error)
        return pd.DataFrame({"error": [error]}) 