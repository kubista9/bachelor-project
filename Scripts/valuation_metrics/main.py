import os
from scripts.valuation_metrics.process_stocks import process_stocks
from scripts.valuation_metrics.process_efs import process_etfs
from scripts.valuation_metrics.process_commodities import process_commodities
from scripts.valuation_metrics.save_tickers import save_all_tickers
import time
import pandas as pd

if __name__ == "__main__":
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    DATA_PATH = os.path.join(ROOT_DIR, "data", "tickers", "stocks.csv")
    
    stocks = pd.read_csv(DATA_PATH)
    stock_results, etf_results, commodity_results = [], [], []
    delay = 8

    # stocks
    stocks = pd.read_csv("data/tickers/stocks.csv")
    stock_results = process_stocks(stocks['Ticker'].tolist(), delay)
    save_all_tickers(stock_results, "Stocks")
    print("\nWaiting 30 seconds before processing ETFs...")
    time.sleep(30)
    
    # etfs
    etfs = pd.read_csv("data/tickers/etfs.csv") 
    etf_results = process_etfs(etfs['Ticker'].tolist(), delay)
    save_all_tickers(etf_results, "ETFs")
    print("\nWaiting 30 seconds before processing commodities...")
    time.sleep(30)
    
    # commodities
    commodities = pd.read_csv("data/tickers/commodities.csv")
    commodity_results = process_commodities(commodities['Ticker'].tolist(), delay)
    save_all_tickers(commodity_results, "Commodities")
    print("Scan is completed")