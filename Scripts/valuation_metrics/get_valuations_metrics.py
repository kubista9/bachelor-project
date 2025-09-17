import yfinance as yf

def get_valuation_metrics(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        eps = stock.info.get("trailingEps", None)

        # Calculate P/E
        pe_ratio = None
        if eps and eps > 0:
            pe_ratio = price / eps

        return {
            "Ticker": ticker,
            "Price": price,
            "EPS": eps,
            "PE_Ratio": pe_ratio
        }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None
