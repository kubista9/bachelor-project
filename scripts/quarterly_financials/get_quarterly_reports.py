import requests
import os
import json

def get_filings(ticker, form_type="10-Q", limit=20):
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36 (Jakub Kuka; jakub.kuka@student.via.dk)",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.sec.gov/",
    "Origin": "https://www.sec.gov",
    "Connection": "keep-alive",
}


    tickers_file = "data/company_tickers.json"
    if os.path.exists(tickers_file):
        with open(tickers_file, "r") as f:
            cik_lookup = json.load(f)
    else:
        resp = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
        resp.raise_for_status()
        cik_lookup = resp.json()
        os.makedirs("data", exist_ok=True)
        with open(tickers_file, "w") as f:
            json.dump(cik_lookup, f, indent=2)

    cik = None
    for v in cik_lookup.values():
        if v["ticker"].lower() == ticker.lower():
            cik = v["cik_str"]
            break
    if not cik:
        raise ValueError(f"❌ Ticker {ticker} not found in SEC list")

    url = f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"
    print(f"🌐 Fetching submissions: {url}")
    resp = requests.get(url, headers=headers)

    data = None
    if resp.status_code == 200:
        try:
            data = resp.json()
            with open(f"data/submissions_CIK{int(cik):010d}.json", "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            print("⚠️ SEC returned non-JSON data, saving to HTML for inspection...")
            with open(f"data/SEC_error_{ticker}.html", "w") as f:
                f.write(resp.text)
    else:
        print(f"⚠️ SEC returned HTTP {resp.status_code}. Trying public SEC mirror...")
        mirror_url = f"https://api.sec-api.io?token=demo"
        try:
            mirror_resp = requests.get(
                f"https://api.sec-api.io?query={{'query':{{'query_string':{{'query':'ticker:{ticker} AND formType:{form_type}'}}}},'from':0,'size':{limit}}}&token=demo"
            )
            if mirror_resp.status_code == 200:
                data = mirror_resp.json()
                print(f"✅ Retrieved {len(data.get('filings', []))} filings from SEC mirror.")
            else:
                print(f"⚠️ Mirror returned HTTP {mirror_resp.status_code}.")
        except Exception as e:
            print(f"❌ Mirror fetch failed: {e}")

    if not data:
        raise Exception(f"❌ Failed to fetch or find cache for {ticker}")

    filings = []
    recent = data.get("filings", {}).get("recent", {})
    if recent:
        for form, acc_num in zip(recent.get("form", []), recent.get("accessionNumber", [])):
            if form == form_type:
                filings.append(acc_num)
                if len(filings) >= limit:
                    break

    if not filings and "filings" in data:
        # If data is from SEC-API mirror
        filings = [f.get("accessionNo") for f in data["filings"][:limit]]

    if not filings:
        print(f"⚠️ No {form_type} filings found for {ticker}")

    return filings
