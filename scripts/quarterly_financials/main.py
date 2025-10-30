import os
import csv
import pandas as pd
import yfinance as yf
import time

from .get_quarterly_reports import (
    get_all_10q_between_dates,
    _load_company_tickers,
    _find_cik,
)
from .download_filings import download_filing_html
from .extract_from_xbrl import build_quarterly_frame
from ..utils.save_to_csv import save_to_csv
from ..constants.constants import DATA_DIR, QUARTERLY_FINANCIALS_DIR, START_DATE, END_DATE


# ----------------------------- Load Tickers -----------------------------
def load_tickers():
    """Read tickers from data/tickers/stocks.csv"""
    path = os.path.join(DATA_DIR, "tickers", "stocks.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Ticker file not found at {path}")

    with open(path, newline="") as f:
        return [
            {"name": row.get("Name", ""), "ticker": row["Ticker"], "sector": row.get("Sector", "")}
            for row in csv.DictReader(f)
        ]


# ----------------------------- Yahoo Price + Valuations -----------------------------
def enrich_with_price_and_valuations(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Attach Yahoo prices & compute valuation metrics."""
    if df.empty:
        print(f"⚠️ Empty fundamentals for {ticker}, skipping price enrichment.")
        return df

    start = START_DATE.strftime("%Y-%m-%d")
    end = END_DATE.strftime("%Y-%m-%d")

    print(f"📈 Fetching Yahoo Finance data for {ticker} ({start} → {end})")

    hist = yf.download(
        ticker, start=start, end=end, interval="1d",
        progress=False, auto_adjust=True, threads=False,
    )

    if hist.empty:
        print(f"⚠️ No Yahoo Finance data found for {ticker}")
        df["price"] = None
        return df

    close_series = hist["Close"].reindex(pd.date_range(start=start, end=end, freq="D")).ffill()

    def nearest_price(d):
        d = pd.Timestamp(d).normalize()
        val = close_series.get(d)
        return float(val) if pd.notna(val) else None

    df["price"] = df["date"].apply(nearest_price)

    # --- Valuations
    shares = df.get("shares", pd.Series([None] * len(df), index=df.index)).astype(float)
    df["market_cap"] = df["price"] * shares

    debt = df.get("debt_current", 0).fillna(0) + df.get("debt_noncurrent", 0).fillna(0)
    cash = df.get("cash", 0).fillna(0)
    df["enterprise_value"] = df["market_cap"] + debt - cash

    df["eps"] = df.get("net_income") / shares
    df["book_ps"] = df.get("equity") / shares
    df["revenue_ps"] = df.get("revenue") / shares

    df["pe_ratio"] = df["price"] / df["eps"]
    df["pb_ratio"] = df["price"] / df["book_ps"]
    df["ps_ratio"] = df["price"] / df["revenue_ps"]
    df["ev_to_revenue"] = df["enterprise_value"] / df.get("revenue")

    if "ebitda" in df.columns:
        df["ev_to_ebitda"] = df["enterprise_value"] / df["ebitda"]

    return df


# ----------------------------- Core Processing -----------------------------
def process_quarterly_reports_and_metrics(ticker: str, name: str):
    """End-to-end pipeline for a single ticker."""
    print(f"\n🔎 Fetching and computing metrics for {ticker}")

    tickers_index = _load_company_tickers()
    cik = _find_cik(ticker, tickers_index)

    filings = get_all_10q_between_dates(cik, START_DATE, END_DATE)
    print(f"📥 Found {len(filings)} filings for {ticker}")

    html_dir = os.path.join(QUARTERLY_FINANCIALS_DIR, ticker, "html")
    os.makedirs(html_dir, exist_ok=True)

    for i, f in enumerate(filings, start=1):
        download_filing_html(cik=cik, accession_number=f["accessionNumber"], save_dir=html_dir)
        if i % 5 == 0:
            time.sleep(2)

    df = build_quarterly_frame(cik, START_DATE, END_DATE)
    if df.empty:
        print(f"⚠️ No data extracted for {ticker}, skipping.")
        return

    df = enrich_with_price_and_valuations(df, ticker)

    save_to_csv(df, category=f"{ticker}_quarterly_metrics", dir=QUARTERLY_FINANCIALS_DIR)
    print(f"✅ Saved metrics for {ticker} → {QUARTERLY_FINANCIALS_DIR}")


# ----------------------------- Main Pipeline -----------------------------
def main():
    print("🚀 Starting quarterly financials full pipeline...\n")

    tickers = load_tickers()
    print(f"🧾 Loaded {len(tickers)} tickers from CSV.")

    for i, t in enumerate(tickers, start=1):
        ticker = t["ticker"]
        name = t.get("name") or t.get("Name") or ticker
        print(f"\n==============================")
        print(f"({i}/{len(tickers)}) Processing {ticker} — {name}")
        print("==============================")

        try:
            process_quarterly_reports_and_metrics(ticker, name)
        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")

        time.sleep(1.5)  # prevent SEC rate-limit

    print("\n✅ All tickers processed successfully!")


# ✅ Entry point guard
if __name__ == "__main__":
    main()
