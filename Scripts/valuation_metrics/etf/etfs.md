# ETF Data
stock = yf.Ticker("etf")
print(stock.info.keys())
## 1. Fund Information
longName, shortName, fundFamily , fundInceptionDate, category
legalType, longBusinessSummary, companyOfficers, executiveTeam

## 2. Market / Exchange Information
symbol, exchange, region, language, market

## 3. Price & Trading Data
previousClose, open, dayLow, dayHigh, regularMarketPrice, bid, ask, bidSize, askSize

## 4. Volume & Liquidity
volume, regularMarketVolume, averageVolume, averageVolume10days, averageDailyVolume10Day, averageDailyVolume3Month

## 5. Fund Net Asset Data
navPrice (Net Asset Value per share), netAssets, totalAssets, sharesOutstanding, 
marketCap

## 6. Returns & Performance
ytdReturn, threeYearAverageReturn, fiveYearAverageReturn, trailingThreeMonthReturns, trailingThreeMonthNavReturns

## 7. Dividends & Yield
dividendYield, trailingAnnualDividendRate, trailingAnnualDividendYield

## 8. Valuation Ratios
priceToBook, bookValue, trailingPegRatio

## 9. Risk & Beta
beta3Year

## 10. Technicals / Price Ranges
fiftyTwoWeekLow, fiftyTwoWeekHigh, fiftyTwoWeekRange, fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent
fiftyTwoWeekChangePercent, fiftyDayAverage, twoHundredDayAverage, fiftyDayAverageChange, fiftyDayAverageChangePercent, twoHundredDayAverageChange, twoHundredDayAverageChangePercent
allTimeHigh, allTimeLow

## 11. Financial Metrics
netExpenseRatio (expense ratio %)

## 12. Miscellaneous
financialCurrency, corporateActions