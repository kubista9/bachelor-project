import os, json, time, requests
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36 (Jakub Kuka; jakub.kuka@student.via.dk)",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.sec.gov/",
}

def _load_json(url: str, cache_path: str | None = None, sleep: float = 1.5):
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            return json.load(f)
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    if cache_path:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, "w") as f:
            json.dump(data, f, indent=2)
    time.sleep(sleep)
    return data

def _load_company_tickers(cache_path: str = "data/company_tickers.json") -> dict:
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            return json.load(f)
    url = "https://www.sec.gov/files/company_tickers.json"
    return _load_json(url, cache_path=cache_path)

def _find_cik(ticker: str, company_tickers: dict) -> str:
    for v in company_tickers.values():
        if v.get("ticker", "").lower() == ticker.lower():
            return f"{int(v['cik_str']):010d}"
    raise ValueError(f"Ticker {ticker} not found")

def get_all_10q_between_dates(cik: str, start_dt: datetime, end_dt: datetime):
    cik_padded = f"{int(cik):010d}"
    subs = _load_json(
        f"https://data.sec.gov/submissions/CIK{cik_padded}.json",
        cache_path=f"data/submissions_CIK{cik_padded}.json"
    )

    def collect(block):
        out = []
        forms = block.get("form", [])
        accs  = block.get("accessionNumber", [])
        dates = block.get("filingDate", [])
        for form, acc, dt in zip(forms, accs, dates):
            if form == "10-Q":
                try:
                    fdt = datetime.strptime(dt, "%Y-%m-%d")
                    if start_dt <= fdt <= end_dt:
                        out.append({"accessionNumber": acc, "filingDate": dt, "cik": cik_padded})
                except Exception:
                    pass
        return out

    results = collect(subs.get("filings", {}).get("recent", {}))
    for f in subs.get("filings", {}).get("files", []):
        page = _load_json(
            f"https://data.sec.gov/submissions/{f['name']}",
            cache_path=os.path.join("data", f['name'])
        )
        results += collect(page)

    results.sort(key=lambda x: x["filingDate"], reverse=True)
    return results