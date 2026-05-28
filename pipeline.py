import polars as pl
import yfinance as yf
import database as db
from datetime import datetime, timedelta

def execute_etl_flow(ticker: str, start_date_str: str, end_date_str: str):
    """
    Directly extracts from yfinance API, transforms with Polars, 
    and saves straight to DuckDB without any caching logic.
    """
    ticker_clean = ticker.upper().strip()
    if not ticker_clean:
        return "⚠️ Please enter a valid stock ticker symbol.", pl.DataFrame()

    print(f"📡 Requesting live market records for {ticker_clean} from API...")
    try:
        stock = yf.Ticker(ticker_clean)
        raw_pandas = stock.history(start=start_date_str, end=end_date_str)
                
        if raw_pandas.empty:
            return f"❌ Ticker '{ticker_clean}' contains no data for this window.", pl.DataFrame()
                    
        # TRANSFORM: Wrap inside Polars and enforce structural type casting
        df_raw = pl.from_pandas(raw_pandas.reset_index())
        df_transformed = df_raw.select([
            pl.lit(ticker_clean).alias("ticker"),
            pl.col("Date").dt.replace_time_zone(None).cast(pl.Date).alias("date"),
            pl.col("Close").round(2).cast(pl.Float64).alias("close_price"),
            pl.col("Volume").cast(pl.Int64).alias("volume")
        ])

        # LOAD: Write straight to disk
        db.write_to_database(df_transformed)
                
        return f"🚀 Success! Fetched fresh records from API and saved to database.", df_transformed
        
    except Exception as pipeline_err:
        return f"❌ Critical Pipeline Failure: {str(pipeline_err)}", pl.DataFrame()

# --- AUTOMATION ORCHESTRATION LAYER ---
def execute_automatic_daily_sync(ticker: str):
    """Calculates dates automatically and pulls fresh data."""
    today = datetime.today()
    five_days_ago = today - timedelta(days=5)
        
    start_date_str = five_days_ago.strftime("%Y-%m-%d")
    end_date_str = today.strftime("%Y-%m-%d")
        
    print(f"🔄 Automation Engine: Syncing {ticker.upper()}...")
    status, _ = execute_etl_flow(ticker, start_date_str, end_date_str)
    print(f"📡 Engine Log Result: {status}")