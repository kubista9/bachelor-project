from scripts.ticker_data.get_history import get_history
import yfinance as yf
import time

def process_commodities(tickers, delay):
    history = get_history(tickers, delay)
    results = []

    for i, ticker in enumerate(tickers):
        print(f"Processing {i+1}/{len(tickers)}: {ticker}")
        try:
            stock = yf.Ticker(ticker)
            info = stock.get_info()
            time.sleep(delay)

            # Basic Info
            name = info.get("shortName")
            currency = info.get("currency")
            exchange = info.get("exchange")
            quote_type = info.get("quoteType")
            time.sleep(delay)
            
            # Trading Metrics
            fifty_day_average = info.get("fiftyDayAverage")
            two_hundred_day_average = info.get("twoHundredDayAverage")
            avg_volume = info.get("averageVolume")
            
            ticker_history = history[ticker]
            
            for date, row in ticker_history.iterrows():
                results.append({
                    # Basic
                    "Date": date.strftime("%Y-%m-%d"),
                    "Ticker": ticker,
                    "Name": name,
                    "Currency": currency,
                    "Quote_Type": quote_type,
                    "Exchange": exchange,
                    
                    # Price
                    "Price Open": row["Open"],
                    "Price Close": row["Close"],
                    "Price High": row["High"],
                    "Price Low": row["Low"],
                    "Volume": row["Volume"],
                    
                    # Market Performance
                    "50 MA": fifty_day_average,
                    "200 MA": two_hundred_day_average,
                    "Avg Volume": avg_volume,
                })
            
            time.sleep(delay)

        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    return results