import pandas as pd
import time
from datetime import datetime, timedelta
from get_valuation_metrics import get_metrics
from save_tickers import save_all_tickers

if __name__ == "__main__":
    stocks = pd.read_csv("../../data/tickers/stocks.csv")
    etfs = pd.read_csv("../../data/tickers/etfs.csv")
    commodities = pd.read_csv("../../data/tickers/commodities.csv")
    stock_results, etf_results, commodity_results = [],[],[]

    for ticker in stocks["Ticker"].tolist():
        print(f"Fetching stock: {ticker}")
        metrics = get_metrics(ticker, "stock")
        if metrics:
            stock_results.extend(metrics)
        time.sleep(1.5)

    for ticker in etfs["Ticker"].tolist():
        print(f"Fetching ETF: {ticker}")
        metrics = get_metrics(ticker, "etf")
        if metrics:
            etf_results.extend(metrics)
        time.sleep(1.5)

    for ticker in commodities["Ticker"].tolist():
        print(f"Fetching commodity: {ticker}")
        metrics = get_metrics(ticker, "commodity")
        if metrics:
            commodity_results.extend(metrics)
        time.sleep(1.5)

save_all_tickers(stock_results, "Stocks")
save_all_tickers(etf_results, "ETFs")
save_all_tickers(commodity_results, "Commodities")


