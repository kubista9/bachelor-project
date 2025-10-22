from scripts.ticker_data.get_history import get_history
import yfinance as yf
import time

def process_etfs(tickers, delay):
    history = get_history(tickers, delay)
    results = []

    for i, ticker in enumerate(tickers):
        print(f"Processing {i+1}/{len(tickers)}: {ticker}")
        try:
            stock = yf.Ticker(ticker)
            info = stock.get_info()
            time.sleep(delay)

            # Basic
            name = info.get("shortName") or info.get("longName")
            currency = info.get("currency")
            category = info.get("category")
            fund_family = info.get("fundFamily")
            time.sleep(delay)
            
            # Specifics
            nav = info.get("navPrice")
            yield_pct = info.get("yield")
            ytd_return = info.get("ytdReturn")
            three_year_avg_return = info.get("threeYearAverageReturn")
            five_year_avg_return = info.get("fiveYearAverageReturn")
            time.sleep(delay)
            
            # Holdings
            total_assets = info.get("totalAssets")
            time.sleep(delay)
            
            # Market performance
            beta = info.get("beta3Year")
            avg_volume = info.get("averageVolume")
            fifty_two_week_high = info.get("fiftyTwoWeekHigh")
            fifty_two_week_low = info.get("fiftyTwoWeekLow")
            fifty_day_average = info.get("fiftyDayAverage")
            two_hundred_day_average = info.get("twoHundredDayAverage")
            
            ticker_history = history[ticker]
            
            for date, row in ticker_history.iterrows():
                results.append({
                    # Basic
                    "Date": date.strftime("%Y-%m-%d"),
                    "Ticker": ticker,
                    "Name": name,
                    "Currency": currency,
                    "Category": category,
                    "Fund_Family": fund_family,
                    
                    # Price
                    "Price_Open": row["Open"],
                    "Price_Close": row["Close"],
                    "Price_High": row["High"],
                    "Price_Low": row["Low"],
                    "Volume": row["Volume"],
                    
                    # Specifics
                    "NAV": nav,
                    "Yield": yield_pct,
                    "YTD_Return": ytd_return,
                    "3_Year_Avg_Return": three_year_avg_return,
                    "5_Year_Avg_Return": five_year_avg_return,
                    
                    # Holdings
                    "Total_Assets": total_assets,
                    
                    # Market performance
                    "Beta_3_Year": beta,
                    "Avg_Volume": avg_volume,
                    "52_Week_High": fifty_two_week_high,
                    "52_Week_Low": fifty_two_week_low,
                    "50_Day_Avg": fifty_day_average,
                    "200_Day_Avg": two_hundred_day_average
                })
            
            time.sleep(delay)

        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    return results