import yfinance as yf
from scripts.constants.constants import START_DATE, END_DATE, INTERVAL
from scripts.valuation_metrics.get_history import get_history
import time

def process_etfs(tickers, delay):
    history = get_history(tickers, delay)
    results = []

    for i, ticker in enumerate(tickers):
        print(f"Processing {i+1}/{len(tickers)}: {ticker}")
        try:
            stock = yf.Ticker(ticker)
            info = stock.get_info()
            
            # Basic Info
            name = info.get("shortName") or info.get("longName")
            currency = info.get("currency")
            category = info.get("category")
            fund_family = info.get("fundFamily")
            
            # ETF Specific Metrics
            expense_ratio = info.get("annualReportExpenseRatio")
            nav = info.get("navPrice")
            yield_pct = info.get("yield")
            ytd_return = info.get("ytdReturn")
            three_year_avg_return = info.get("threeYearAverageReturn")
            five_year_avg_return = info.get("fiveYearAverageReturn")
            
            # Holdings Info
            total_assets = info.get("totalAssets")
            holdings_count = info.get("holdingsCount")
            
            # Trading Info
            beta = info.get("beta3Year")
            avg_volume = info.get("averageVolume")
            fifty_two_week_high = info.get("fiftyTwoWeekHigh")
            fifty_two_week_low = info.get("fiftyTwoWeekLow")
            fifty_day_average = info.get("fiftyDayAverage")
            two_hundred_day_average = info.get("twoHundredDayAverage")
            
            # Get history for this specific ticker
            ticker_history = history[ticker]
            
            for date, row in ticker_history.iterrows():
                results.append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Ticker": ticker,
                    "Name": name,
                    "Currency": currency,
                    "Category": category,
                    "Fund_Family": fund_family,
                    
                    # Price Data
                    "Price_Open": row["Open"],
                    "Price_Close": row["Close"],
                    "Price_High": row["High"],
                    "Price_Low": row["Low"],
                    "Volume": row["Volume"],
                    
                    # ETF Metrics
                    "Expense_Ratio": expense_ratio,
                    "NAV": nav,
                    "Yield": yield_pct,
                    "YTD_Return": ytd_return,
                    "3_Year_Avg_Return": three_year_avg_return,
                    "5_Year_Avg_Return": five_year_avg_return,
                    
                    # Holdings
                    "Total_Assets": total_assets,
                    "Holdings_Count": holdings_count,
                    
                    # Trading Metrics
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