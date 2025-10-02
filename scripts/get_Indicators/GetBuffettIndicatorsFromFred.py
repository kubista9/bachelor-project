import time
from pathlib import Path
import requests

#```
# Gets :
# US GDP - Gross Domestic Product, Billions of Dollars, Quarterly, Seasonally Adjusted Annual Rate 
# us_total_assets - Assets: Total Assets: Total Assets (Less Eliminations from Consolidation): Wednesday Level, Millions of U.S. Dollars, Weekly, Not Seasonally Adjusted
#```

# -------- Settings --------
OUTDIR = Path("data/fred")
OUTDIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "us_gdp_fred.xlsx": "https://fred.stlouisfed.org/graph/fredgraph.xls?g=1AJNd",
    "us_total_assets_fred.xlsx": "https://fred.stlouisfed.org/graph/fredgraph.xls?g=1AJMI",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
TIMEOUT = 30
RETRIES = 3
# --------------------------

def download_file(url: str, outpath: Path):
    for attempt in range(1, RETRIES + 1):
        try:
            with requests.get(url, headers=HEADERS, stream=True, timeout=TIMEOUT) as r:
                r.raise_for_status()
                with open(outpath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            print(f"Saved: {outpath.resolve()}")
            return
        except Exception as e:
            print(f"[Attempt {attempt}/{RETRIES}] Error downloading {url}: {e}")
            if attempt < RETRIES:
                time.sleep(2)
    raise RuntimeError(f"Failed to download after {RETRIES} attempts: {url}")

def main():
    for filename, url in FILES.items():
        outpath = OUTDIR / filename
        download_file(url, outpath)

if __name__ == "__main__":
    main()
