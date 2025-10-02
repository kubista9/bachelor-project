import requests
import pandas as pd

#```
# Gets :
# Warren Buffett Indicator
#```

DIR = "data/buffett"
FILENAME = "BuffettIndicatorHistory.csv"

outpath = DIR+"/"+FILENAME


url = "https://buffettindicator.net/wp-content/themes/flashmag/data/history.json"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Referer": "https://buffettindicator.net/"
}

resp = requests.get(url, headers=headers, timeout=30)
resp.raise_for_status()
data = resp.json()

df = pd.DataFrame(data)
df = df.rename(columns={
    "DateTime": "date",
    "Wilshire 5000 to GDP Ratio": "buffett_ratio"
})


df.to_csv(outpath, index=False)
#df.to_excel("buffett_indicator_history.xlsx", index=False)

print("Saved " + outpath)
