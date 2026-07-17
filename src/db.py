"""
db.py
------
Small helper for connecting to the customer_success.db SQLite database
and running queries into pandas DataFrames.
"""

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "customer_success.db"


def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}.\n"
            "Run `python data/generate_data.py` first to create it."
        )
    return sqlite3.connect(DB_PATH)


def run_query(sql: str) -> pd.DataFrame:
    """Run a SQL query and return the result as a pandas DataFrame."""
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn)
