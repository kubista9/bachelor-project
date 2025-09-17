import pandas as pd
from get_valuations_metrics import get_valuation_metrics
from save_tickers import save_ticker_data

if __name__ == "__main__":
    tickers_df = pd.read_csv("../..//data/tickers/Tickers.csv")
    tickers = tickers_df["Ticker"].tolist()

    for ticker in tickers[:10]:
        metrics = get_valuation_metrics(ticker)
        if metrics:
            save_ticker_data(metrics)
