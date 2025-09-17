import pandas as pd
from datetime import datetime, timedelta
from get_valuations_metrics import get_valuation_metrics
from save_tickers import save_all_tickers
import time

if __name__ == "__main__":
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    tickers_df = pd.read_csv("../../data/tickers/Tickers.csv")
    tickers = tickers_df["Ticker"].tolist() # convert to list

    results = []
    for ticker in tickers[:4]:
        metrics = get_valuation_metrics(
            ticker,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d")
        )
        results.extend(metrics)
        time.sleep(1.5)
        if metrics:
            results.extend(metrics)

    save_all_tickers(results)