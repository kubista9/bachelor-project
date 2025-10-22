from datetime import datetime
import os

START_DATE = datetime(2000,1,1) # 'YYYY-MM-DD'
END_DATE = datetime(2025,10,30) # 'YYYY-MM-DD'
INTERVAL = "1d"

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
TICKERS_DATA_PATH = os.path.join(ROOT_DIR, "data", "tickers", "stocks.csv")
