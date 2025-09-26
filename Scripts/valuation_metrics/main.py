import pandas as pd
import yfinance as yf
import time
from get_valuation_metrics import process_stock_ticker, process_etf_ticker, process_commodity_ticker
from save_tickers import save_all_tickers

if __name__ == "__main__":
    stocks = pd.read_csv("../../data/tickers/stocks.csv")
    etfs = pd.read_csv("../../data/tickers/etfs.csv") 
    commodities = pd.read_csv("../../data/tickers/commodities.csv")
    stock_results, etf_results, commodity_results = [], [], []
    
    # stocks
    for i, ticker in enumerate(stocks["Ticker"].tolist()):
        print(f"Stock {i+1}/{len(stocks)}: {ticker}")
        metrics = process_stock_ticker(ticker, delay=8)
        if metrics:
            stock_results.extend(metrics)
        else:
            print(f"⚠ No data for {ticker}")
    
    print("\nWaiting 30 seconds before processing ETFs...")
    time.sleep(30)
    
    # etfs
    for i, ticker in enumerate(etfs["Ticker"].tolist()):
        print(f"ETF {i+1}/{len(etfs)}: {ticker}")
        metrics = process_etf_ticker(ticker, delay=8)
        if metrics:
            etf_results.extend(metrics)
        else:
            print(f"⚠ No data for {ticker}")

    print("\nWaiting 30 seconds before processing commodities...")
    time.sleep(30)
    
    # commodities
    for i, ticker in enumerate(commodities["Ticker"].tolist()):
        metrics = process_commodity_ticker(ticker, delay=8)
        if metrics:
            commodity_results.extend(metrics)
            print(f"✓ Added {len(metrics)} records for {ticker}")
        else:
            print(f"⚠ No data for {ticker}")
    
    save_all_tickers(stock_results, "Stocks")
    save_all_tickers(etf_results, "ETFs")
    save_all_tickers(commodity_results, "Commodities")
    print("Scan is completed")


