import pandas as pd
from pathlib import Path
from datetime import datetime

def save_all_tickers(data_list: list[dict], label: str = "All"):
    if not data_list:
        return

    timestamp = datetime.now().strftime("%Y.%d.%m")
    filepath = Path(f"../../data/valuation_metrics/{label}_Scan_{timestamp}.csv")
    df = pd.DataFrame(data_list)
    df.to_csv(filepath, index=False)
    print(f"Saved {len(data_list)} tickers to {filepath}")

