from scripts.constants.constants import START_DATE, END_DATE
from scripts.utils.save_to_csv import save_to_csv
from scripts.fred.series import series_list
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd
import os

load_dotenv()
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

for series_id, filename in series_list:
    try:
        data = fred.get_series(
            series_id,
            observation_start=START_DATE,
            observation_end=END_DATE
        )
        df = pd.DataFrame({
            'observation_date': data.index,
            series_id: data.values
        })
        df = df.reset_index(drop=True)
        save_to_csv(df, filename, "data/fred")
        print(f"Successfully fetched {series_id}")
    except Exception as e:
        print(f"Failed to fetch {series_id}: {e}")

print("All series processed.")