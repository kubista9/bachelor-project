import yfinance as yf

def get_valuation_metrics(ticker: str, start: str = None, end: str = None):
    try:
        stock = yf.Ticker(ticker)

        if start and end:
            hist = stock.history(start=start, end=end, interval="1d")
        else:
            hist = stock.history(period="1d")

        if hist.empty:
            return []

        name = stock.info.get("shortName") or stock.info.get("longName")
        eps = stock.info.get("trailingEps", None)

        results = []
        for date, row in hist.iterrows():
            price_open = row["Open"]
            price_close = row["Close"]
            price_avg = (price_open + price_close) / 2

            pe_ratio = None
            if eps and eps > 0:
                pe_ratio = price_close / eps

            results.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Ticker": ticker,
                "Name": name,
                "Price_Open": price_open,
                "Price_Close": price_close,
                "Price_Avg": price_avg,
                "EPS": eps,
                "PE_Ratio": pe_ratio
            })

        return results

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return []
