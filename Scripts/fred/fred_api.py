from fredapi import Fred
import pandas as pd
from scripts.fred.series import series_list
from scripts.utils.save_to_csv import save_to_csv
from dotenv import load_dotenv
import os

load_dotenv()
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

for series_id, filename in series_list:
    try:
        df = fred.get_series(series_id)
        df = pd.DataFrame(df)
        save_to_csv(df, filename, "data/fred")
    except Exception as e:
        print(f"❌ Failed to fetch {series_id}: {e}")

print("All series processed.")
