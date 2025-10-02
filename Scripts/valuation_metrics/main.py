from process_stocks import process_stocks
from process_efs import process_etfs
from process_commodities import process_commodities
from save_tickers import save_all_tickers
import time
import pandas as pd

if __name__ == "__main__":
    stock_results, etf_results, commodity_results = [], [], []
    delay = 8

    # stocks
    stocks = pd.read_csv("../../data/tickers/stocks.csv")
    stock_results = process_stocks(stocks['Ticker'].tolist(), delay)
    save_all_tickers(stock_results, "Stocks")
    print("\nWaiting 30 seconds before processing ETFs...")
    time.sleep(30)
    
    # etfs
    etfs = pd.read_csv("../../data/tickers/etfs.csv") 
    etf_results = process_etfs(etfs['Ticker'].tolist(), delay)
    save_all_tickers(etf_results, "ETFs")
    print("\nWaiting 30 seconds before processing commodities...")
    time.sleep(30)
    
    # commodities
    commodities = pd.read_csv("../../data/tickers/commodities.csv")
    commodity_results = process_commodities(commodities['Ticker'].tolist(), delay)
    save_all_tickers(commodity_results, "Commodities")
    print("Scan is completed")