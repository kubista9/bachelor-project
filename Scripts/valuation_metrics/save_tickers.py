import pandas as pd
from pathlib import Path
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filepath = f"../../data/valuation_metrics/Scan_{timestamp}.xlsx"


def save_ticker_data(data: dict, output_path="valuation_metrics.csv"):
    if not data:
        return

    file_path = Path(output_path)
    df_new = pd.DataFrame([data])  # wrap dict into dataframe

    if file_path.exists():
        df_existing = pd.read_csv(file_path)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(file_path, index=False)
    print(f"Saved {data['Ticker']} to {file_path}")

