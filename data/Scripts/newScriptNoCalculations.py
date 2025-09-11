# -*- coding: utf-8 -*-
# pip install yfinance pandas openpyxl --upgrade
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import yfinance as yf
from pathlib import Path

# ============================= HELPERS =============================

def _strip_tz_index(df: pd.DataFrame) -> pd.DataFrame:
    """Make DatetimeIndex timezone-naive and normalized to midnight (Excel-friendly)."""
    if df is None or df.empty:
        return df
    out = df.copy()
    if isinstance(out.index, pd.DatetimeIndex):
        try:
            out.index = out.index.tz_convert(None)
        except Exception:
            try:
                out.index = out.index.tz_localize(None)
            except Exception:
                pass
        out.index = out.index.normalize()
        out.index.name = "date"
    return out

def _pick_excel_engine():
    try:
        import xlsxwriter  # noqa: F401
        return "xlsxwriter"
    except Exception:
        try:
            import openpyxl  # noqa: F401
            return "openpyxl"
        except Exception:
            raise RuntimeError(
                "Install an Excel writer engine:\n"
                "  pip install xlsxwriter\n  or\n  pip install openpyxl"
            )

# ============================= RAW FETCH =============================

def fetch_yf_raw(ticker: str, start: str | None = None, end: str | None = None) -> dict:
    """
    Return only raw objects from yfinance for a ticker:
      - prices: OHLCV (Adj Close included)
      - dividends: cash dividends (per share)
      - splits: split ratios
      - shares: shares outstanding history (as provided by Yahoo; not modified)
    """
    t = yf.Ticker(ticker)

    # Prices (no adjustments or derived columns)
    if start or end:
        prices = t.history(start=start, end=end, interval="1d", auto_adjust=False)
    else:
        prices = t.history(period="max", interval="1d", auto_adjust=False)
    prices = _strip_tz_index(prices)

    # Dividends & splits (Series -> DataFrame)
    div = t.dividends
    div = div.to_frame("dividend") if div is not None and not div.empty else pd.DataFrame()
    div = _strip_tz_index(div)

    spl = t.splits
    spl = spl.to_frame("split_ratio") if spl is not None and not spl.empty else pd.DataFrame()
    spl = _strip_tz_index(spl)

    # Shares outstanding history (Series -> DataFrame). No forward-fill or calc.
    try:
        shares = t.get_shares_full(start=(start or "1900-01-01"))
        if shares is not None and not shares.empty:
            shares = shares.to_frame("shares_out")
            shares = _strip_tz_index(shares)
        else:
            shares = pd.DataFrame()
    except Exception:
        shares = pd.DataFrame()

    return {"prices": prices, "dividends": div, "splits": spl, "shares": shares}

# ============================= SAVE =============================

def save_raw_to_excel(ticker: str, data: dict, out_path: str | Path):
    engine = _pick_excel_engine()
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(out_path, engine=engine) as xl:
        for sheet_name in ["prices", "dividends", "splits", "shares"]:
            df = data.get(sheet_name)
            if df is not None and not df.empty:
                df.to_excel(xl, sheet_name=sheet_name, index=True)

# ============================= RUN =============================

def main():
    tickers = ["AAPL"]  # e.g. ["AAPL", "MSFT", "UPS"]
    # Optional date window; leave as None to get full available history
    start = None  # e.g. "2010-01-01"
    end   = None  # e.g. "2025-09-11"

    for tk in tickers:
        print(f"Fetching raw Yahoo data for {tk} ...")
        raw = fetch_yf_raw(tk, start=start, end=end)
        out_file = f"{tk}_raw_yf.xlsx"
        save_raw_to_excel(tk, raw, out_file)
        print(f"  Wrote {out_file}")

if __name__ == "__main__":
    main()
