import duckdb
import polars as pl

DB_FILE = "stock_data.duckdb"

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

def read_cached_data(ticker: str, start_date: str, end_date: str) -> pl.DataFrame:
    """Queries the local cache and returns a clean Polars DataFrame."""
    init_db()
    with duckdb.connect(DB_FILE) as conn:
        query = """
            SELECT * FROM historical_stocks 
            WHERE ticker = ? AND date BETWEEN ? AND ?
            ORDER BY date ASC
        """
        # .pl() tells DuckDB to hand the results straight over as a Polars DataFrame
        return conn.execute(query, [ticker, start_date, end_date]).pl()

def write_to_cache(df_cleaned: pl.DataFrame):
    """Inserts or updates structured Polars DataFrames into the storage file."""
    if df_cleaned.is_empty():
        return
        
    with duckdb.connect(DB_FILE) as conn:
        # DuckDB natively reads the Polars DataFrame variable 'df_cleaned' directly in-memory
        conn.execute("INSERT OR REPLACE INTO historical_stocks SELECT * FROM df_cleaned")