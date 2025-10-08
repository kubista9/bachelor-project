import os
import pandas as pd

def save_all_tickers(results, category):
    df = pd.DataFrame(results)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/valuation_metrics"))
    os.makedirs(base_dir, exist_ok=True) # create directory if it doesn't exist

    filepath = os.path.join(base_dir, f"{category}.csv")
    df.to_csv(filepath, index=False)
    print(f"✅ Saved {category} data to {filepath}")
