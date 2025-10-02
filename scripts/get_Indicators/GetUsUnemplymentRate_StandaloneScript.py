import requests
import pandas as pd
from pathlib import Path

OUTDIR = Path("data/unemployment")
OUTDIR.mkdir(exist_ok=True)

url_csv = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE"
out_csv = OUTDIR / "us_unemployment_rate.csv"

resp = requests.get(url_csv, timeout=30)
resp.raise_for_status()

with open(out_csv, "wb") as f:
    f.write(resp.content)

print(f"Saved: {out_csv.resolve()}")

# Optional: load into DataFrame
df = pd.read_csv(out_csv)
print(df.head())
