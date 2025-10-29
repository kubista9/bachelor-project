from scripts.ticker_data.get_history import get_history
import yfinance as yf
import time

def process_ticker(tickers):
    history = get_history(tickers)
    delay = 0.25
    results = []
    
    for i, ticker in enumerate(tickers):
        print(f"Processing {i+1}/{len(tickers)}: {ticker}")
        
        try:
            time.sleep(delay)
            stock = yf.Ticker(ticker)
            info = stock.get_info()
            time.sleep(delay)

            # Basic
            name = info.get("shortName") or info.get("longName")
            currency = info.get("currency")
            sector = info.get("sector")
            industry = info.get("industry")
            market_cap = info.get("marketCap")
            
            ticker_history = history[ticker]

            for date, row in ticker_history.iterrows():
                results.append({
                    # Basic
                    "Date": date.strftime("%Y-%m-%d"),
                    "Ticker": ticker,
                    "Name": name,
                    "Currency": currency,
                    "Sector": sector,
                    "Industry": industry,
                    "Market Cap": market_cap,

                    # Price
                    "Price Open": row["Open"],
                    "Price Close": row["Close"],
                    "Price High": row["High"],
                    "Price Low": row["Low"],
                    "Volume": row["Volume"], 
                })

        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    return results