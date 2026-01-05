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
    conn.register("financials", df)
    conn.register("data_table", df) 
        
def run_sql(conn, query):
    try:
        output_table = conn.execute(query).df()
        return output_table
    except (duckdb.InternalError, AttributeError) as e:
        error = f"SQL query failed. Error: {str(e).splitlines()[0]}."
        print(error)
        return pd.DataFrame({"error": [error]}) 