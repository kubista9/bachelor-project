import yfinance as yf
from constants import START_DATE, END_DATE, INTERVAL
import time

def get_history(tickers, delay=8):
    try:
        history = yf.download(
            tickers,
            start=START_DATE,
            end=END_DATE,
            interval=INTERVAL,
            group_by='ticker',
            threads=True
        )
        time.sleep(delay)
        return history
    except Exception as e:
        print(f"Error fetching batch history: {e}")
        return []