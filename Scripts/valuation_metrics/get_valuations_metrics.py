import yfinance as yf

def get_valuation_metrics(ticker: str, start: str = None, end: str = None):
    try:
        stock = yf.Ticker(ticker)  # create Ticker object

        if start and end:
            history = stock.history(start=start, end=end, interval="1d")
        else:
            history = stock.history(period="1y", interval="1d")

        if history .empty:
            return []

        info = stock.get_info()
        name = info.get("shortName") or info.get("longName")
        eps = info.get("trailingEps", None)

        results = []
        for date, row in history.iterrows():
            price_open = row["Open"]
            price_close = row["Close"]
            price_average = (price_open + price_close) / 2

            pe_ratio = None
            if eps and eps > 0:
                pe_ratio = price_average / eps

            results.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Ticker": ticker,
                "Name": name,
                "Price_Open": price_open,
                "Price_Close": price_close,
                "Price_Avg": price_average,
                "EPS": eps,
                "PE_Ratio": pe_ratio
            })

        return results

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return []
