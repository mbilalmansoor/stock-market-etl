import pipeline as pipe

if __name__ == "__main__":
    # Define the assets you want to maintain automatically
    tickers_to_watch = ["AAPL", "MSFT", "NVDA", "GOOG"]
    
    print("🚀 Starting Automated Database Synchronization Flow...")
    for ticker in tickers_to_watch:
        pipe.execute_automatic_daily_sync(ticker)
    print("🏁 Automation pipeline run finished successfully.")