import os
import sys

# Force Python to switch its execution focus to your project directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)
os.chdir(SCRIPT_DIR)

import pipeline as pipe

if __name__ == "__main__":
    # Define the assets you want to maintain automatically
    tickers_to_watch = ["AAPL", "MSFT", "NVDA", "GOOG"]
            
    print("🚀 Starting Automated Database Synchronization Flow...")
    print(f"📁 Running script inside system directory workspace: {os.getcwd()}")
        
    for ticker in tickers_to_watch:
        pipe.execute_automatic_daily_sync(ticker)
            
    print("🏁 Automation pipeline run finished successfully.")