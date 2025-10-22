from scripts.constants.constants import START_DATE, END_DATE, INTERVAL
from scripts.valuation_metrics.get_history import get_history
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
            
            # Basic Info
            name = info.get("shortName")
            currency = info.get("currency")
            exchange = info.get("exchange")
            quote_type = info.get("quoteType")
            
            # Trading Metrics
            fifty_day_average = info.get("fiftyDayAverage")
            hundred_day_average = info.get("hundredDayAverage")
            hundred_fifty_day_average = info.get("hundredFiftyDayAverage")
            two_hundred_day_average = info.get("twoHundredDayAverage")
            avg_volume = info.get("averageVolume")
            
            ticker_history = history[ticker]
            
            for date, row in ticker_history.iterrows():
                results.append({
                    # Basic Info
                    "Date": date.strftime("%Y-%m-%d"),
                    "Ticker": ticker,
                    "Name": name,
                    "Currency": currency,
                    "Exchange": exchange,
                    "Quote_Type": quote_type,
                    
                    # Price
                    "Price Open": row["Open"],
                    "Price Close": row["Close"],
                    "Price High": row["High"],
                    "Price Low": row["Low"],
                    "Volume": row["Volume"],
                    
                    # Market Performance
                    "50 MA": fifty_day_average,
                    "100 MA": hundred_day_average,
                    "150 MA": hundred_fifty_day_average,
                    "200 MA": two_hundred_day_average,
                    "Avg Volume": avg_volume,
                })
            
            time.sleep(delay)

        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    return results