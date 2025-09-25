import yfinance as yf
from constants import START_DATE, END_DATE, INTERVAL

def get_common_data(stock):
    history = stock.history(start=START_DATE, end=END_DATE, interval=INTERVAL)
    info = stock.get_info()
    name = info.get("shortName") or info.get("longName")
    currency = info.get("currency")
    return history, name, currency, info


def get_stock_metrics(ticker: str):
    stock = yf.Ticker(ticker)
    history, name, currency, info = get_common_data(stock)
    eps = info.get("trailingEps")
    results = []

    for date, row in history.iterrows():
        price_open = row["Open"]
        price_close = row["Close"]
        price_avg = (price_open + price_close) / 2
        pe_ratio = price_avg / eps if eps and eps > 0 else None

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


def get_etf_metrics(ticker: str):
    stock = yf.Ticker(ticker)
    history, name, currency, info = get_common_data(stock)

    expense_ratio = info.get("annualReportExpenseRatio")
    nav = info.get("navPrice")
    yield_pct = info.get("yield")

    results = []
    for date, row in history.iterrows():
        results.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Ticker": ticker,
            "Name": name,
            "Currency": currency,
            "Price_Open": row["Open"],
            "Price_Close": row["Close"],
            "NAV": nav,
            "Expense_Ratio": expense_ratio,
            "Dividend_Yield": yield_pct
        })

    return results


def get_commodity_metrics(ticker: str):
    stock = yf.Ticker(ticker)
    history, name, currency, info = get_common_data(stock)

    results = []
    for date, row in history.iterrows():
        results.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Ticker": ticker,
            "Name": name,
            "Currency": currency,
            "Price_Open": row["Open"],
            "Price_Close": row["Close"],
            "Price_High": row["High"],
            "Price_Low": row["Low"],
            "Volume": row["Volume"]
        })

    return results


def get_metrics(ticker: str, type_: str):
    try:
        if type_ == "stock":
            return get_stock_metrics(ticker)
        elif type_ == "etf":
            return get_etf_metrics(ticker)
        elif type_ == "commodity":
            return get_commodity_metrics(ticker)
        else:
            raise ValueError(f"Unknown type: {type_}")
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return []
