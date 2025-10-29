# scripts/quarterly_financials/download_filings.py
import os, time, requests

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
    r.raise_for_status()
    return r.json()

def download_filing_html(cik: str, accession_number: str, save_dir: str, primary_document: str | None = None) -> str | None:
    os.makedirs(save_dir, exist_ok=True)
    acc_no_clean = accession_number.replace("-", "")
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_clean}"
    index_url = f"{base}/index.json"

    # If we already saved .html or .htm or .txt, skip
    for ext in (".html", ".htm", ".txt"):
        existing = os.path.join(save_dir, f"{accession_number}{ext}")
        if os.path.exists(existing):
            # already have this filing saved
            return existing

    try:
        index_data = _safe_get_json(index_url)
    except Exception as e:
        print(f"⚠️ Could not fetch filing index for {accession_number}: {e}")
        return None

    items = index_data.get("directory", {}).get("item", [])
    names = [it["name"] for it in items]

    def is_index_page(name: str) -> bool:
        ln = name.lower()
        return ln.endswith("-index.html") or ln.endswith("-index-headers.html")

    # 1) Prefer the primary document if present and not an index page
    candidates = []
    if primary_document and primary_document in names and not is_index_page(primary_document):
        candidates.append(primary_document)
    # 2) Non-index HTML by largest size
    htmls = [it for it in items if it["name"].lower().endswith((".htm", ".html")) and not is_index_page(it["name"])]
    htmls.sort(key=lambda it: it.get("size", 0), reverse=True)
    candidates += [it["name"] for it in htmls]
    # 3) Fallback to .txt for very old filings
    candidates += [it["name"] for it in items if it["name"].lower().endswith(".txt")]

    for name in candidates:
        url = f"{base}/{name}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code != 200:
                print(f"⚠️ HTTP {r.status_code} for {url}")
                continue
            ext = os.path.splitext(name)[1]
            out_path = os.path.join(save_dir, f"{accession_number}{ext}")
            with open(out_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(r.text)
            print(f"✅ Saved {os.path.basename(out_path)}  →  {out_path}")
            time.sleep(1.5)
            return out_path
        except Exception as e:
            print(f"⚠️ Failed {url}: {e}")

    print(f"⚠️ No suitable document found for {accession_number}")
    return None
