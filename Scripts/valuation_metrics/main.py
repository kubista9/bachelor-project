from scripts.valuation_metrics.process_commodities import process_commodities
from scripts.valuation_metrics.process_stocks import process_stocks
from scripts.valuation_metrics.process_efs import process_etfs
from scripts.constants.constants import TICKERS_DATA_PATH
from scripts.utils.save_to_csv import save_to_csv
import pandas as pd
import time
import os

if __name__ == "__main__":
    dir = base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/valuation_metrics"))
    stocks = pd.read_csv(TICKERS_DATA_PATH)
    stock_results, etf_results, commodity_results = [], [], []
    delay = 2
    time_asleep = 60

    # stocks
    stocks = pd.read_csv("data/tickers/stocks.csv")
    stock_results = process_stocks(stocks['Ticker'].tolist(), delay)
    save_to_csv(stock_results, "Stocks", dir)
    print("\nWaiting 30 seconds before processing ETFs...")
    time.sleep(time_asleep)
    
    # etfs
    etfs = pd.read_csv("data/tickers/etfs.csv") 
    etf_results = process_etfs(etfs['Ticker'].tolist(), delay)
    save_to_csv(etf_results, "ETFs", dir)
    print("\nWaiting 30 seconds before processing commodities...")
    time.sleep(time_asleep)
    
    # commodities
    commodities = pd.read_csv("data/tickers/commodities.csv")
    commodity_results = process_commodities(commodities['Ticker'].tolist(), delay)
    save_to_csv(commodity_results, "Commodities", dir)
    print("Scan is completed")