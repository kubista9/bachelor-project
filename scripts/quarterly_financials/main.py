import os
import csv
import pandas as pd
import yfinance as yf
import time

from .get_quarterly_reports import get_all_10q_between_dates, _load_company_tickers, _find_cik
from .download_filings import download_filing_html
from .extract_from_xbrl import build_quarterly_frame
from ..utils.save_to_csv import save_to_csv
from ..constants.constants import DATA_DIR, QUARTERLY_FINANCIALS_DIR, START_DATE, END_DATE


def load_tickers():
    """Read tickers from data/tickers/stocks.csv"""
    path = os.path.join(DATA_DIR, "tickers", "stocks.csv")
    with open(path, newline="") as f:
        return [
            {"name": row["Name"], "ticker": row["Ticker"], "sector": row["Sector"]}
            for row in csv.DictReader(f)
        ]


def enrich_with_price_and_valuations(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Attach Yahoo prices & valuation metrics."""
    if df.empty:
        return df

    start = START_DATE.strftime("%Y-%m-%d")
    end   = END_DATE.strftime("%Y-%m-%d")

    print(f"📈 Fetching Yahoo Finance data for {ticker} ({start} → {end})")

    hist = yf.download(
        ticker,
        start=start,
        end=end,
        interval="1d",
        progress=False,
        auto_adjust=True,
        threads=False,
    )

    # --- normalize to Series
    if isinstance(hist, pd.Series):
        close_series = hist
    else:
        if isinstance(hist.columns, pd.MultiIndex):
            if ('Close', ticker) in hist.columns:
                close_series = hist[('Close', ticker)]
            elif ('Adj Close', ticker) in hist.columns:
                close_series = hist[('Adj Close', ticker)]
            elif 'Close' in hist.columns.get_level_values(0):
                close_series = hist.xs('Close', axis=1, level=0).iloc[:, 0]
            elif 'Adj Close' in hist.columns.get_level_values(0):
                close_series = hist.xs('Adj Close', axis=1, level=0).iloc[:, 0]
            else:
                close_series = hist.iloc[:, 0]
        else:
            if 'Close' in hist.columns:
                close_series = hist['Close']
            elif 'Adj Close' in hist.columns:
                close_series = hist['Adj Close']
            else:
                close_series = hist.iloc[:, 0]

    # --- reindex to daily calendar for clean lookups
    full_idx = pd.date_range(start=start, end=end, freq="D")
    close_series = close_series.reindex(full_idx).ffill()

    def nearest_price(d):
        d = pd.Timestamp(d).normalize()
        val = close_series.get(d)
        return None if pd.isna(val) else float(val)

    df["price"] = df["date"].apply(nearest_price)

    # --- valuation metrics
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

    if "ebitda" in df:
        df["ev_to_ebitda"] = df["enterprise_value"] / df["ebitda"]

    return df


def process_quarterly_reports_and_metrics(ticker: str):
    """End-to-end pipeline for a single ticker"""
    print(f"\n🔎 Fetching and computing metrics for {ticker}")

    # 1️⃣ Get CIK
    tickers_index = _load_company_tickers()
    cik = _find_cik(ticker, tickers_index)

    # 2️⃣ Get all 10-Q filings between 2000–2025
    filings = get_all_10q_between_dates(cik, START_DATE, END_DATE)
    print(f"📥 Found {len(filings)} filings for {ticker}")

    # 3️⃣ Download some HTML filings for archival
    # 3️⃣ Download ALL quarterly HTML filings (2000–2025)
    html_dir = os.path.join(QUARTERLY_FINANCIALS_DIR, ticker, "html")
    os.makedirs(html_dir, exist_ok=True)

    for i, f in enumerate(filings, start=1):
        download_filing_html(cik=cik, accession_number=f["accessionNumber"], save_dir=html_dir)
        if i % 5 == 0:
            time.sleep(2)  # polite 2-second pause every 5 downloads


    # 4️⃣ Build quarterly fundamentals from SEC XBRL
    facts_df = build_quarterly_frame(cik, START_DATE, END_DATE)

    # 5️⃣ Enrich with prices and valuation ratios
    facts_df = enrich_with_price_and_valuations(facts_df, ticker)

    # 6️⃣ Save output CSV
    records = facts_df.assign(Ticker=ticker).to_dict(orient="records")
    save_to_csv(records, category=f"{ticker}_quarterly_metrics", dir=QUARTERLY_FINANCIALS_DIR)

    print(f"✅ Saved metrics for {ticker} → {QUARTERLY_FINANCIALS_DIR}")


def main():
    print("🚀 Starting quarterly financials full pipeline...\n")
    tickers = load_tickers()

    first = tickers[0]["ticker"]  # e.g. XOM
    process_quarterly_reports_and_metrics(first)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
