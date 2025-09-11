# Minimal World Bank downloader:
# One Excel per region; one sheet "rates" with only Year + the 4 indicators.

import requests
import pandas as pd
from pathlib import Path
import time

WB_API_BASE = "https://api.worldbank.org/v2"

COUNTRIES = {
    "USA": "USA_interest_rates_WB.xlsx",
    "GBR": "UK_interest_rates_WB.xlsx",
    "EMU": "EuroArea_interest_rates_WB.xlsx",
}

INDICATORS = {
    "FR.INR.LEND": "Lending interest rate (%)",
    "FR.INR.DPST": "Deposit interest rate (%)",
    "FR.INR.LNDP": "Interest rate spread (lending - deposit, %)",
    "FR.INR.RINR": "Real interest rate (%)",
}

# Try xlsxwriter, fall back to openpyxl
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
                "No Excel writer engine found. Install one of:\n"
                "  pip install xlsxwriter\n"
                "  or\n"
                "  pip install openpyxl"
            )

def wb_fetch_indicator(country, indicator, per_page=20000, sleep=0.1):
    """
    Fetch a single (country, indicator) series as a DataFrame with columns:
      date (int year), value (float)
    """
    url = f"{WB_API_BASE}/country/{country}/indicator/{indicator}"
    params = {"format": "json", "per_page": per_page}
    rows, page = [], 1
    while True:
        params["page"] = page
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        payload = r.json()
        if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
            break
        meta, data = payload[0], payload[1]
        for obs in data:
            year = obs.get("date")
            val = obs.get("value", None)
            try:
                val = float(val) if val is not None else None
            except Exception:
                val = None
            if year is not None:
                rows.append({"date": int(year), "value": val})
        if page >= int(meta.get("pages", 1)):
            break
        page += 1
        time.sleep(sleep)
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df

def build_rates_table(country_code):
    """
    Returns a DataFrame with columns:
      Year, Lending interest rate (%), Deposit interest rate (%),
      Interest rate spread (lending - deposit, %), Real interest rate (%)
    """
    out = None
    for code, friendly in INDICATORS.items():
        df = wb_fetch_indicator(country_code, code)
        if df.empty:
            series = pd.DataFrame(columns=["date", friendly])
        else:
            series = df.rename(columns={"value": friendly})
            series = series[["date", friendly]]
        if out is None:
            out = series
        else:
            out = out.merge(series, on="date", how="outer")
    if out is None:
        out = pd.DataFrame(columns=["date"] + list(INDICATORS.values()))
    out = out.sort_values("date").reset_index(drop=True)
    out.rename(columns={"date": "Year"}, inplace=True)
    # Optional: limit to 1960..current (WDI typical coverage). Comment out if you want all.
    # out = out[(out["Year"] >= 1960)]
    return out

def save_rates_xlsx(path, df_rates):
    engine = _pick_excel_engine()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Ensure exact column order
    ordered_cols = ["Year"] + list(INDICATORS.values())
    for col in ordered_cols:
        if col not in df_rates.columns:
            df_rates[col] = pd.NA
    df_rates = df_rates.reindex(columns=ordered_cols)
    with pd.ExcelWriter(path, engine=engine) as writer:
        df_rates.to_excel(writer, sheet_name="rates", index=False)

def main():
    for ccode, outfile in COUNTRIES.items():
        print(f"Fetching {ccode} ...")
        rates = build_rates_table(ccode)
        save_rates_xlsx(outfile, rates)
        print(f"Wrote {outfile}")

if __name__ == "__main__":
    main()
