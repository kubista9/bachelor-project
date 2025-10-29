from scripts.constants.constants import TICKER_DATA_DIR
from scripts.ticker_data.process_ticker import process_ticker
from scripts.utils.save_to_csv import save_to_csv
import pandas as pd

if __name__ == "__main__":

    # Stocks
    stocks = pd.read_csv("data/tickers/stocks.csv")
    stock_results = process_ticker(stocks['Ticker'].tolist())
    save_to_csv(stock_results, "Stocks", TICKER_DATA_DIR)

    # ETFs
    etfs = pd.read_csv("data/tickers/etfs.csv")
    etf_results = process_ticker(etfs['Ticker'].tolist())
    save_to_csv(etf_results, "ETFs", TICKER_DATA_DIR)

    # Commodities
    commodities = pd.read_csv("data/tickers/commodities.csv")
    commodity_results = process_ticker(commodities['Ticker'].tolist())
    save_to_csv(commodity_results, "Commodities", TICKER_DATA_DIR)

    print("Scan is completed")