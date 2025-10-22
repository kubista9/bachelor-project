import requests
import pandas as pd
from pathlib import Path

OUTDIR = Path("data/us_inflation")
OUTDIR.mkdir(parents=True, exist_ok=True)

SERIES_ID = "FPCPITOTLZGUSA"  # Consumer Price Index for All Urban Consumers
URL_CSV = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}"

OUT_RAW = OUTDIR / f"{SERIES_ID}_raw.csv"
OUT_TIDY = OUTDIR / f"{SERIES_ID}_tidy.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}

def download_csv(url, outpath):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    outpath.write_bytes(r.content)
    print(f"Saved: {outpath.resolve()}")

def main():
    download_csv(URL_CSV, OUT_RAW)
    df = pd.read_csv(OUT_RAW)

    # Standardize column names
    df.rename(columns={df.columns[0]: "date", df.columns[1]: "cpi_index"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    df["cpi_index"] = pd.to_numeric(df["cpi_index"], errors="coerce")

    # Compute year-over-year inflation (%)
    df["inflation_yoy_pct"] = df["cpi_index"].pct_change(periods=12) * 100

    df.to_csv(OUT_TIDY, index=False)
    print(f"Tidy CSV saved: {OUT_TIDY.resolve()}")
    print("\nPreview:")
    print(df.tail())

if __name__ == "__main__":
    main()
