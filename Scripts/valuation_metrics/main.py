import pandas as pd
from get_valuations_metrics import get_valuation_metrics
from save_tickers import save_all_tickers

if __name__ == "__main__":
    tickers_df = pd.read_csv("../../data/tickers/Tickers.csv")
    tickers = tickers_df["Ticker"].tolist() # conver to list

    results = []
    for ticker in tickers[:4]:
        metrics = get_valuation_metrics(ticker)
        if metrics:
            results.append(metrics)

    save_all_tickers(results)
