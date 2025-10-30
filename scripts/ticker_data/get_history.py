from scripts.constants.constants import START_DATE, END_DATE, INTERVAL
import yfinance as yf
import time

def get_history(tickers):
    try:
        history = yf.download(
            tickers,
            start=START_DATE,
            end=END_DATE,
            interval=INTERVAL,
            group_by='ticker',
            threads=False
        )
        return history
    except Exception as e:
        print(f"Error fetching batch history: {e}")
        return []