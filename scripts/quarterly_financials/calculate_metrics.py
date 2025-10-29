import pandas as pd
import numpy as np
from scripts.ticker_data.get_history import get_history


def calculate_all_metrics(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Combine SEC XBRL fundamentals with Yahoo Finance price data and compute metrics."""
    print(f"\n📊 Entered calculate_all_metrics for {ticker}, input shape: {df.shape}")

    if df.empty:
        print(f"⚠️ Empty DataFrame for {ticker}, skipping metric calculation.")
        return df

    # --- Ensure date column is valid ---
    df["date"] = df["date"].apply(lambda x: x[0] if isinstance(x, (list, np.ndarray)) else x)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # --- ensure numeric types ---
    df = df.apply(pd.to_numeric, errors="ignore")

    # ✅ Fetch Yahoo price history
    hist = get_history([ticker])
    if isinstance(hist.columns, pd.MultiIndex):
        hist = hist[ticker]
    close_series = hist["Close"]
    df["price"] = df["date"].apply(lambda d: close_series.asof(pd.Timestamp(d)) if not close_series.empty else np.nan)

    # ✅ Compute derived values
    # ✅ Compute key financial components safely
    if "gross_profit" not in df or df["gross_profit"].isna().all():
        if "revenue" in df and "cogs" in df:
            df["gross_profit"] = df["revenue"] - df["cogs"]
        else:
            df["gross_profit"] = np.nan

    if "operating_income" not in df or df["operating_income"].isna().all():
        if "gross_profit" in df and "operating_expenses" in df:
            df["operating_income"] = df["gross_profit"] - df["operating_expenses"]
        else:
            df["operating_income"] = np.nan

    if "ebitda" not in df or df["ebitda"].isna().all():
        if "operating_income" in df:
            dep = df.get("depreciation", 0)
            amort = df.get("amortization", 0)
            df["ebitda"] = df["operating_income"] + dep + amort
        else:
            df["ebitda"] = np.nan


    # --- Balance sheet & enterprise components ---
    df["total_debt"] = df.get("debt_current", 0).fillna(0) + df.get("debt_noncurrent", 0).fillna(0)
    df["total_cash"] = df.get("cash", 0).fillna(0)
    df["enterprise_value"] = (df["price"] * df.get("shares", np.nan)) + df["total_debt"] - df["total_cash"]
    df["market_cap"] = df["price"] * df.get("shares", np.nan)

    # --- Income statement derived metrics ---
    df["eps"] = df["net_income"] / df.get("shares", np.nan)

    # --- Valuation ratios ---
    df["pe_ratio"] = df["market_cap"] / df["net_income"]
    df["pb_ratio"] = df["market_cap"] / df["equity"]
    df["ps_ratio"] = df["market_cap"] / df["revenue"]
    df["ev_to_revenue"] = df["enterprise_value"] / df["revenue"]
    df["ev_to_ebitda"] = df["enterprise_value"] / df["ebitda"]

    # --- Profitability ratios ---
    df["gross_margin"] = df["gross_profit"] / df["revenue"]
    df["operating_margin"] = df["operating_income"] / df["revenue"]
    df["profit_margin"] = df["net_income"] / df["revenue"]
    df["roe"] = df["net_income"] / df["equity"]
    df["roa"] = df["net_income"] / df["assets"]

    # --- Financial health ratios ---
    df["current_ratio"] = df["assets_current"] / df["liabilities_current"]
    df["debt_to_equity"] = df["total_debt"] / df["equity"]

    # --- Cashflow metrics ---
    df["free_cashflow"] = df["operating_cashflow"] - df.get("capex", 0)

    # --- Growth metrics ---
    df["revenue_growth"] = df["revenue"].pct_change(fill_method=None)
    df["earnings_growth"] = df["net_income"].pct_change(fill_method=None)

    df = df.round(6)
    print(f"✅ Calculated metrics for {ticker}: {len(df)} quarters after filtering.")
    return df