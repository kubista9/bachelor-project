from scripts.constants.constants import TICKER_DATA_DIR
from scripts.ticker_data.process_commodities import process_commodities
from scripts.ticker_data.process_stocks import process_stocks
from scripts.ticker_data.process_efs import process_etfs
from scripts.utils.save_to_csv import save_to_csv
import pandas as pd

if __name__ == "__main__":
    delay = 0.25

    # Stocks
    stocks = pd.read_csv("data/tickers/stocks.csv")
    stock_results = process_stocks(stocks['Ticker'].tolist(), delay)
    save_to_csv(stock_results, "Stocks", TICKER_DATA_DIR)

    # ETFs
    etfs = pd.read_csv("data/tickers/etfs.csv")
    etf_results = process_etfs(etfs['Ticker'].tolist(), delay)
    save_to_csv(etf_results, "ETFs", TICKER_DATA_DIR)

    # Commodities
    commodities = pd.read_csv("data/tickers/commodities.csv")
    commodity_results = process_commodities(commodities['Ticker'].tolist(), delay)
    save_to_csv(commodity_results, "Commodities", TICKER_DATA_DIR)

    print("Scan is completed")