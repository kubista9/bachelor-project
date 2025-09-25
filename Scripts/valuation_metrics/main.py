import pandas as pd
import yfinance as yf
import time
from constants import START_DATE, END_DATE, INTERVAL
from get_valuation_metrics import get_metrics
from save_tickers import save_all_tickers

if __name__ == "__main__":
    stocks = pd.read_csv("../../data/tickers/stocks.csv")
    etfs = pd.read_csv("../../data/tickers/etfs.csv")
    commodities = pd.read_csv("../../data/tickers/commodities.csv")
    stock_results, etf_results, commodity_results = [],[],[]
    stock_tickers = stocks["Ticker"].tolist()
    etf_tickers = etfs["Ticker"].tolist()
    commodity_tickers = commodities["Ticker"].tolist()
    data = yf.download(stock_tickers, start=START_DATE, end=END_DATE, interval=INTERVAL)
    data = yf.download(etf_tickers, start=START_DATE, end=END_DATE, interval=INTERVAL)
    data = yf.download(commodity_tickers, start=START_DATE, end=END_DATE, interval=INTERVAL)

    for ticker in stocks["Ticker"].tolist():
        print(f"Fetching stock: {ticker}")
        metrics = get_metrics(ticker, "stock")
        if metrics:
            stock_results.extend(metrics)
        time.sleep(4)

    for ticker in etfs["Ticker"].tolist():
        print(f"Fetching ETF: {ticker}")
        metrics = get_metrics(ticker, "etf")
        if metrics:
            etf_results.extend(metrics)
        time.sleep(4)

    for ticker in commodities["Ticker"].tolist():
        print(f"Fetching commodity: {ticker}")
        metrics = get_metrics(ticker, "commodity")
        if metrics:
            commodity_results.extend(metrics)
        time.sleep(4)

save_all_tickers(stock_results, "Stocks")
save_all_tickers(etf_results, "ETFs")
save_all_tickers(commodity_results, "Commodities")


