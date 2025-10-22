from scripts.ticker_data.get_history import get_history
import yfinance as yf
import time

def process_stocks(tickers, delay):
    history = get_history(tickers, delay=0)
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
            time.sleep(delay)
            
            # Valuation
            pe_ratio = info.get("trailingPE")
            pb_ratio = info.get("priceToBook")
            ps_ratio = info.get("priceToSalesTrailing12Months")
            ev_to_revenue = info.get("enterpriseToRevenue")
            ev_to_ebitda = info.get("enterpriseToEbitda")
            time.sleep(delay)

            # Profitability
            profit_margin = info.get("profitMargins")
            operating_margin = info.get("operatingMargins")
            gross_margin = info.get("grossMargins")
            roe = info.get("returnOnEquity")
            roa = info.get("returnOnAssets")
            time.sleep(delay)
            
            # Dividend
            dividend_yield = info.get("dividendYield")
            dividend_rate = info.get("dividendRate")
            payout_ratio = info.get("payoutRatio")
            ex_dividend_date = info.get("exDividendDate")
            time.sleep(delay)

            # Financials
            current_ratio = info.get("currentRatio")
            debt_to_equity = info.get("debtToEquity")
            total_debt = info.get("totalDebt")
            total_cash = info.get("totalCash")
            free_cashflow = info.get("freeCashflow")
            operating_cashflow = info.get("operatingCashflow")
            time.sleep(delay)

            # Growth
            revenue_growth = info.get("revenueGrowth")
            earnings_growth = info.get("earningsGrowth")
            time.sleep(delay)
            
            # Market performance
            beta = info.get("beta")
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
                    "Sector": sector,
                    "Industry": industry,
                    "Market Cap": market_cap,

                    # Price
                    "Price Open": row["Open"],
                    "Price Close": row["Close"],
                    "Price High": row["High"],
                    "Price Low": row["Low"],
                    "Volume": row["Volume"],

                    # Valuation
                    "PE Ratio": pe_ratio,
                    "PB Ratio": pb_ratio,
                    "PS_Ratio": ps_ratio,
                    "EV To Revenue": ev_to_revenue,
                    "EV To EBITDA": ev_to_ebitda,
                    
                    # Profitability
                    "Net Margin": profit_margin,
                    "Operating Margin": operating_margin,
                    "Gross Margin": gross_margin,
                    "ROE": roe,
                    "ROA": roa,

                    # Dividend
                    "Dividend Yield": dividend_yield,
                    "Dividend Rate": dividend_rate,
                    "Payout Ratio": payout_ratio,
                    "Ex divident rate": ex_dividend_date,

                    # Financials
                    "Current Ratio": current_ratio,
                    "Debt To Equity": debt_to_equity,
                    "Total Debt": total_debt,
                    "Total Cash": total_cash,
                    "Free Cashflow": free_cashflow,
                    "Operating Cashflow": operating_cashflow,

                    # Growth
                    "Revenue Growth": revenue_growth,
                    "Earnings Growth": earnings_growth,
                    "Beta": beta,

                    # Market Performance
                    "50 MA": fifty_day_average,
                    "200 MA": two_hundred_day_average,
                    "Avg Volume": avg_volume,   
                })

        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    return results