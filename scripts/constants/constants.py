from datetime import datetime
import os

# Time configuration
START_DATE = datetime(2000, 1, 1)
END_DATE = datetime(2025, 10, 30)
INTERVAL = "1d"

# Paths
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(ROOT_DIR, "data")
TICKER_DATA_DIR = os.path.join(DATA_DIR, "ticker data")
