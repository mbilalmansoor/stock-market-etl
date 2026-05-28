import os
import duckdb
import polars as pl

# Resolve the absolute workspace directory to keep paths uniform
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "stock_data.duckdb")

def init_db():
    """Verifies or creates the physical DuckDB storage schema."""
    with duckdb.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS historical_stocks (
                ticker TEXT,
                date DATE,
                close_price DOUBLE,
                volume BIGINT,
                PRIMARY KEY (ticker, date)
            )
        """)

def write_to_database(df_cleaned: pl.DataFrame):
    """Directly inserts or updates fresh records into DuckDB."""
    if df_cleaned.is_empty():
        return
    
    init_db()
    with duckdb.connect(DB_FILE) as conn:
        # Overwrite or insert the new market rows natively
        conn.execute("INSERT OR REPLACE INTO historical_stocks SELECT * FROM df_cleaned")
    print("💾 Fresh records successfully committed to DuckDB.")