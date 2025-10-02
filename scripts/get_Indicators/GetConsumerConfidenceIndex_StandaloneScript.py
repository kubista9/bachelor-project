import requests
import pandas as pd
from pathlib import Path

#```
# gets:
# University of Michigan: Consumer Sentiment, Index 1966:Q1=100, Monthly, Not Seasonally Adjusted 
#```

# ---------- Settings ----------
OUTDIR = Path("data/consumerSentiment")
OUTDIR.mkdir(parents=True, exist_ok=True)

SERIES_ID = "UMCSENT"
URL_CSV = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}"
URL_XLSX = f"https://fred.stlouisfed.org/graph/fredgraph.xls?id={SERIES_ID}"

RAW_CSV = OUTDIR / "umich_consumer_sentiment_raw.csv"
RAW_XLSX = OUTDIR / "umich_consumer_sentiment_raw.xlsx"
TIDY_CSV = OUTDIR / "umich_consumer_sentiment_tidy.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}
TIMEOUT = 30
# -----------------------------

def download(url: str, outpath: Path):
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    outpath.write_bytes(r.content)
    print(f"Saved: {outpath.resolve()}")

def normalize_fred_csv(in_csv: Path, out_csv_tidy: Path, series_id: str):
    """
    Normalize FRED CSV to tidy format:
    - date (YYYY-MM-DD)
    - value (float / NA)
    - series_id
    Handles either 'DATE' or 'observation_date' column names.
    """
    df = pd.read_csv(in_csv)

    # Standardize date column name
    if "DATE" in df.columns:
        df = df.rename(columns={"DATE": "date"})
    elif "observation_date" in df.columns:
        df = df.rename(columns={"observation_date": "date"})
    else:
        raise ValueError("Could not find a DATE/observation_date column in FRED CSV.")

    # Identify the value column (usually equals series_id)
    value_col = series_id if series_id in df.columns else df.columns[1]
    df = df.rename(columns={value_col: "value"})[["date", "value"]]

    # Coerce values to numeric, keep NA where missing
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Add series_id for traceability
    df["series_id"] = series_id

    df.to_csv(out_csv_tidy, index=False)
    print(f"Tidy CSV saved: {out_csv_tidy.resolve()}")
    return df

def main():
    print("Downloading University of Michigan Consumer Sentiment (UMCSENT) from FRED…")
    download(URL_CSV, RAW_CSV)
    #download(URL_XLSX, RAW_XLSX)

    #df_tidy = normalize_fred_csv(RAW_CSV, TIDY_CSV, SERIES_ID)

    # Optional preview
    #print("\nPreview (tidy):")
    #print(df_tidy.head())

if __name__ == "__main__":
    main()
