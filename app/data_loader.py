import pandas as pd
from .config import apple_csv_path

def load_data():
    if not apple_csv_path.exists():
        raise FileNotFoundError(f"File not found at {apple_csv_path}") 
    df = pd.read_csv(apple_csv_path)
    return df

def cleaned_data():
    df_cleaned = load_data().copy()
    
    if "year" not in df_cleaned.columns:
        raise ValueError("Expected timeframe not found in data.")
    df_cleaned["year"] = pd.to_numeric(df_cleaned["year"], errors = "coerce").astype("Int64")
    
    # column clean up -
    monetary_cols = [
        'ebitda_millions', 'revenue_millions', 'gross_profit_millions',
        'op_income_millions', 'net_income_millions', 'total_assets_millions',
        'cash_on_hand_millions', 'long_term_debt_millions',
        'total_liabilities_millions', 'shares_outstanding', 'employees'
        ]
    
    # int64 -
    for col in monetary_cols:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].astype(str).str.replace(r'[$,\s]', '', regex=True).astype('int64')
    
    # float64 -
    if "eps" in df_cleaned.columns:
        df_cleaned['eps'] = df_cleaned['eps'].astype(str).str.replace(r'[$,\s]', '', regex=True).astype('float64')
    if "gross_margin" in df_cleaned.columns:
        df_cleaned['gross_margin'] = (df_cleaned['gross_margin'].astype(str).str.replace(r'[%\s]', '', regex=True).astype('float64')/100)
    if "pe_ratio" in df_cleaned.columns:
        df_cleaned["pe_ratio"] = df_cleaned["pe_ratio"].astype("float64")
    
    # feature engineering for financial literacy -
    if {"net_income_millions", "revenue_millions"}.issubset(df_cleaned.columns):
        df_cleaned['net_profit_margin'] = df_cleaned['net_income_millions'] / df_cleaned['revenue_millions']
    if {"total_assets_millions", "total_liabilities_millions"}.issubset(df_cleaned.columns):
         df_cleaned['current_ratio'] = df_cleaned['total_assets_millions'] / df_cleaned['total_liabilities_millions']
    if {"long_term_debt_millions", "total_assets_millions"}.issubset(df_cleaned.columns):
         df_cleaned['debt_to_assets_ratio'] = df_cleaned['long_term_debt_millions'] / df_cleaned['total_assets_millions']
    if "op_income_millions" in df_cleaned.columns and "operating_income_millions" not in df_cleaned.columns:
        df_cleaned["operating_income_millions"] = df_cleaned["op_income_millions"]
    if {"operating_income_millions", "revenue_millions"}.issubset(df_cleaned.columns):
        df_cleaned["operating_margin"] = df_cleaned["operating_income_millions"] / df_cleaned["revenue_millions"]
    if {"gross_profit_millions", "revenue_millions"}.issubset(df_cleaned.columns):
        df_cleaned["gross_profit_margin"] = df_cleaned["gross_profit_millions"] / df_cleaned["revenue_millions"]        

    # sort by year -
    df_cleaned = df_cleaned.sort_values("year").reset_index(drop = True)
    return df_cleaned