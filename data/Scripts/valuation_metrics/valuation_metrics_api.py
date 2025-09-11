import yfinance as yf
import time

ticker_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

for ticker in ticker_symbols:
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1d")
        print(f"Successfully fetched data for {ticker}")
        time.sleep(5) 
    except yf.exceptions.YFRateLimitError:
        print(f"Rate limited on {ticker}. Waiting for 10 minutes...")
        time.sleep(600)