import yfinance as yf

def get_valuation_metrics(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        last_row = hist.iloc[-1] # last available OHLC row
        open_price = last_row["Open"]
        high_price = last_row["High"]
        low_price = last_row["Low"]
        close_price = last_row["Close"]
        average_price = (open_price + close_price) / 2
        name = stock.info.get("shortName") or stock.info.get("longName")
        eps = stock.info.get("trailingEps", None)
        pe_ratio = average_price / eps

        return {
            "Ticker": ticker,
            "Name": name,
            "Opening price": open_price,
            "High price": high_price,
            "Low price": low_price,
            "Closing price": close_price,
            "Average price": average_price,
            "EPS": eps,
            "PE ratio": pe_ratio
        }

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None
