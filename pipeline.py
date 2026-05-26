import polars as pl
import yfinance as yf
import database as db

def execute_etl_flow(ticker: str, start_date_str: str, end_date_str: str):
    """
    Orchestrates the custom ingestion logic.
    Returns: (status_message, polars_dataframe)
    """
    ticker_clean = ticker.upper().strip()
    if not ticker_clean:
        return "⚠️ Please enter a valid stock ticker symbol.", pl.DataFrame()

    # 1. EXTRACT FROM CACHE: Check if storage already has the data
    try:
        df_cached = db.read_cached_data(ticker_clean, start_date_str, end_date_str)
        if not df_cached.is_empty():
            return f"⚡ Cache Hit! Loaded {len(df_cached)} records directly from local DuckDB.", df_cached
    except Exception as cache_err:
        print(f"Cache lookup logged an error: {cache_err}")

    # 2. EXTRACT FROM API: Cache Miss -> Query live market API
    print(f"Cache miss for {ticker_clean}. Querying yfinance API...")
    try:
        stock = yf.Ticker(ticker_clean)
        raw_pandas = stock.history(start=start_date_str, end=end_date_str)
        
        if raw_pandas.empty:
            return f"❌ Ticker '{ticker_clean}' not found or contains no data for this window.", pl.DataFrame()
            
        # 3. TRANSFORM: Wrap inside Polars and enforce structural type casting
        df_raw = pl.from_pandas(raw_pandas.reset_index())
        df_transformed = df_raw.select([
            pl.lit(ticker_clean).alias("ticker"),
            pl.col("Date").dt.replace_time_zone(None).cast(pl.Date).alias("date"),
            pl.col("Close").round(2).cast(pl.Float64).alias("close_price"),
            pl.col("Volume").cast(pl.Int64).alias("volume")
        ])

        # 4. LOAD: Push the transformed dataframe back into the storage cache layer
        db.write_to_cache(df_transformed)
        
        return f"📥 Cache Miss! Fetched fresh records from API and committed to DuckDB.", df_transformed

    except Exception as pipeline_err:
        return f"❌ Critical Pipeline Failure: {str(pipeline_err)}", pl.DataFrame()