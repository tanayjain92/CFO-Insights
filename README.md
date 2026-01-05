# CFO Insights – Apple Financials

This app answers grounded questions over Apple annual financial data (2009–2024).
It uses DuckDB for analytics, LangGraph for orchestration, and a Chroma-based glossary retriever for definitions.

## Features
- Ask metric questions (YoY, trends, comparisons)
- SQL-powered analysis via DuckDB
- “Definition” mode grounded on a finance glossary (RAG)
- Chart generation

## Requirements
- Python 3.11 recommended
- An Anthropic API key
-.env file in project root should have: ANTHROPIC_API_KEY = xx 
-run streamlit run app.py

## Setup (pip)
```bash
git clone repo url
cd finsights

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
