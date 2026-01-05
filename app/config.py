import os
from pathlib import Path
from dotenv import load_dotenv

# Working directory
base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir/"data"
apple_csv_path = data_dir/"apple_2009-2024.csv"
rag_glossary_path = data_dir/"glossary_apple_finance.md"

# Claude API load 
load_dotenv(dotenv_path=base_dir / ".env")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_key:
    raise RuntimeError("ANTHROPIC_API_KEY not found. Put it in project_root/.env")