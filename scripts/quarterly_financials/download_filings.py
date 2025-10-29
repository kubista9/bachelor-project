import os
import time
import json
import requests

# Browser-like headers keep SEC happier
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36 (Jakub Kuka; jakub.kuka@student.via.dk)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.sec.gov/",
    "Connection": "keep-alive",
}

def _safe_get_json(url: str):
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code} for {url}")
    try:
        return r.json()
    except Exception:
        # Save body for debugging if SEC serves HTML
        os.makedirs("data", exist_ok=True)
        with open("data/SEC_last_response.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        raise

def download_filing_html(cik: str, accession_number: str, save_dir: str) -> str | None:
    """
    Given CIK '0000034088' and accession '0000034088-24-000058',
    downloads the main HTML file (largest .htm/.html in the filing).
    Returns saved filepath or None.
    """
    os.makedirs(save_dir, exist_ok=True)
    acc_no_clean = accession_number.replace("-", "")
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_clean}"
    index_url = f"{base}/index.json"

    try:
        index_data = _safe_get_json(index_url)
    except Exception as e:
        print(f"⚠️ Could not fetch filing index for {accession_number}: {e}")
        return None

    items = index_data.get("directory", {}).get("item", [])
    htmls = [it for it in items if it["name"].lower().endswith((".htm", ".html"))]
    if not htmls:
        print(f"⚠️ No HTML files in {accession_number}")
        return None

    # Choose the largest HTML as the primary document
    main_doc = max(htmls, key=lambda it: it.get("size", 0))
    doc_url = f"{base}/{main_doc['name']}"

    try:
        r = requests.get(doc_url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print(f"⚠️ HTTP {r.status_code} for {doc_url}")
            return None
        out_path = os.path.join(save_dir, f"{accession_number}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"✅ Saved {accession_number}.html  →  {out_path}")
    except Exception as e:
        print(f"⚠️ Failed to download {doc_url}: {e}")
        return None

    time.sleep(1.5)  # polite delay
    return out_path
