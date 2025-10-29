# scripts/quarterly_financials/extract_from_xbrl.py

import os, json, time, requests
from datetime import datetime
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Jakub Kuka; jakub.kuka@student.via.dk)",
    "Accept": "application/json, */*",
}

GAAP_MAP = {
    "revenue": "Revenues",
    "net_income": "NetIncomeLoss",
    "operating_income": "OperatingIncomeLoss",
    "gross_profit": "GrossProfit",
    "assets": "Assets",
    "equity": "StockholdersEquity",
    "assets_current": "AssetsCurrent",
    "liabilities_current": "LiabilitiesCurrent",
    "cash": "CashAndCashEquivalentsAtCarryingValue",
    "debt_current": "DebtCurrent",
    "debt_noncurrent": "LongTermDebtNoncurrent",
    "shares": "CommonStockSharesOutstanding",
    "ebitda": "EarningsBeforeInterestTaxesDepreciationAndAmortization",
    "operating_cashflow": "NetCashProvidedByUsedInOperatingActivities",
    "free_cashflow": None,  # will compute if we have capex
    "capex": "PaymentsToAcquirePropertyPlantAndEquipment",
}

def _load_companyfacts(cik_padded: str):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    time.sleep(1.2)
    return r.json()

def _pick_quarterly_usd(series: dict, start_dt: datetime, end_dt: datetime):
    """Return list of dicts with 'end','val' for USD duration facts within date window (quarterly)."""
    out = []
    for item in series.get("units", {}).get("USD", []):
        try:
            # duration fact: has start and end; keep by end date
            end = datetime.strptime(item["end"], "%Y-%m-%d")
        except Exception:
            continue
        if not (start_dt <= end <= end_dt):
            continue
        # keep only quarterly periods (fp=Q1,Q2,Q3) when present
        fp = item.get("fp")
        if fp and fp.startswith("Q"):
            out.append({"end": end, "val": item["val"]})
    return out

def build_quarterly_frame(cik_padded: str, start_dt: datetime, end_dt: datetime) -> pd.DataFrame:
    facts = _load_companyfacts(cik_padded)
    us_gaap = facts.get("facts", {}).get("us-gaap", {})

    cols = {"date": []}
    series = {}

    # pull each mapped concept
    for key, concept in GAAP_MAP.items():
        series[key] = {}
        if not concept or concept not in us_gaap:
            continue
        vals = _pick_quarterly_usd(us_gaap[concept], start_dt, end_dt)
        for v in vals:
            d = v["end"].date()
            series[key][d] = v["val"]
            if d not in cols["date"]:
                cols["date"].append(d)

    cols["date"].sort()
    df = pd.DataFrame({"date": cols["date"]})
    for key, dmap in series.items():
        df[key] = [dmap.get(d, None) for d in df["date"]]

    # compute derived fields where possible
    if "assets_current" in df and "liabilities_current" in df:
        df["current_ratio"] = df["assets_current"] / df["liabilities_current"]
    if "revenue" in df and "gross_profit" in df:
        df["gross_margin"] = df["gross_profit"] / df["revenue"]
    if "revenue" in df and "operating_income" in df:
        df["operating_margin"] = df["operating_income"] / df["revenue"]
    if "revenue" in df and "net_income" in df:
        df["profit_margin"] = df["net_income"] / df["revenue"]
    if "net_income" in df and "equity" in df:
        df["roe"] = df["net_income"] / df["equity"]
    if "net_income" in df and "assets" in df:
        df["roa"] = df["net_income"] / df["assets"]
    if "operating_cashflow" in df and "capex" in df:
        df["free_cashflow"] = df["operating_cashflow"] - df["capex"]

    return df