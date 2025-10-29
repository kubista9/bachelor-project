import os
import csv
from .get_quarterly_reports import get_filings
from .extract_text_from_pdf import extract_text_from_pdf
from .extract_values import extract_number
from ..utils.save_to_csv import save_to_csv
from ..constants.constants import QUATERLY_FINANCIALS_DIR, DATA_DIR

# Optional: use your real User-Agent email to avoid SEC rate limiting
HEADERS = {"User-Agent": "yourname@example.com"}

def load_tickers():
    tickers = []
    stocks_path = os.path.join(DATA_DIR, "tickers", "stocks.csv")
    with open(stocks_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickers.append({
                "name": row["Name"],
                "ticker": row["Ticker"],
                "sector": row["Sector"]
            })
    return tickers

def process_quarterly_reports(ticker):
    """Downloads filings for a single ticker (e.g., XOM)"""
    filings = get_filings(ticker, form_type="10-Q", limit=4)
    results = []

    print(f"📥 Found {len(filings)} quarterly filings for {ticker}")

    for filing in filings:
        # For prototype, just save the accession number (we won’t download PDFs yet)
        results.append({
            "Ticker": ticker,
            "AccessionNumber": filing
        })

    # Save results to CSV
    save_to_csv(results, category=f"{ticker}_quarterly_filings", dir=QUATERLY_FINANCIALS_DIR)

def main():
    print("🚀 Starting quarterly financials pipeline...\n")

    tickers = load_tickers()
    if not tickers:
        print("❌ No tickers found in stocks.csv")
        return

    # For testing, process only the first ticker (Exxon)
    first_ticker = tickers[0]["ticker"]
    print(f"🔍 Processing first ticker: {first_ticker}\n")

    process_quarterly_reports(first_ticker)

    print("\n✅ Done!")

if __name__ == "__main__":
    main()
