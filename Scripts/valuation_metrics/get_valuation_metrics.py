import yfinance as yf
from constants import START_DATE, END_DATE, INTERVAL
import time

def get_single_ticker_data(ticker, delay=8):
    try:
        print(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)
        history = stock.history(start=START_DATE, end=END_DATE, interval=INTERVAL)
        time.sleep(delay // 2)
        info = stock.get_info()
        time.sleep(delay // 2)
        return history, info
        
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None, None

def process_stock_ticker(ticker, delay=8):
    history, info = get_single_ticker_data(ticker, delay)
    if history is None or history.empty:
        return []
    
    name = info.get("shortName") or info.get("longName") if info else None
    eps = info.get("trailingEps") if info else None
    
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

def process_etf_ticker(ticker, delay=8):
    history, info = get_single_ticker_data(ticker, delay)
    if history is None or history.empty:
        return []
    
    name = info.get("shortName") or info.get("longName") if info else None
    currency = info.get("currency") if info else None
    expense_ratio = info.get("annualReportExpenseRatio") if info else None
    nav = info.get("navPrice") if info else None
    yield_pct = info.get("yield") if info else None

    results = []
    for date, row in history.iterrows():
        results.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Ticker": ticker,
            "Name": name,
            "Currency": currency,
            "Price_Open": row["Open"],
            "Price_Close": row["Close"],
            "Dividend_Yield": yield_pct
        })
    
    return results

def process_commodity_ticker(ticker, delay=8):
    history, info = get_single_ticker_data(ticker, delay)
    if history is None or history.empty:
        return []
    
    name = info.get("shortName") or info.get("longName") if info else None
    currency = info.get("currency") if info else None

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