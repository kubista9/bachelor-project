# pip install pandas openpyxl numpy
import pandas as pd
import numpy as np

# Read your worksheet (change sheet_name as needed)
df = pd.read_excel("data/indicators/NVDA_daily_features.xlsx", sheet_name="Sheet1")  # or sheet_name="Sheet1"



# Treat empty strings/whitespace and common tokens as NaN
df = df.replace(r"^\s*$", np.nan, regex=True).replace(
    ["","NaN", "nan", "NULL", "null", "None", "-"], np.nan
)

# Drop rows that are entirely null
df = df.dropna(how="any")



# (Optional) also drop columns that are entirely null
# df = df.dropna(axis=1, how="all")

df = df.drop(columns=["ticker","symbol"])


print(df.head())
# Save back out
df.to_excel("data/indicators/NVDA_daily_enriched_clean.xlsx", index=False)


