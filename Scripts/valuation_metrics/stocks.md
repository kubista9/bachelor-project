# Stock Data

## 1. General 
shortName, industry, sector, longBusinessSummary, fullTimeEmployees , executiveTeam 
companyOfficers, website, city, country

## 2. Market/Exchange
symbol/ticker, exchange, market, exchangeTimezoneName, language, region, marketState

## 3. Price & Trading Data
currentPrice, previousClose, open, dayLow, dayHigh, bid, ask, bidSize, askSize

## 4. Volume & Liquidity
volume, regularMarketVolume, averageVolume, averageVolume10days, 
averageDailyVolume10Day, averageDailyVolume3Month

## 5. Market Valuation
marketCap, enterpriseValue

- Mega Cap: > $200B
- Large Cap: $10B - $200B
- Mid Cap: $2B - $10B
- Small Cap: $300M - $2B
- Micro Cap: < $300M

## 6. Share Structure
floatShares, sharesOutstanding, impliedSharesOutstanding, shortRatio, shortPercentOfFloat, sharesShort, sharesShortPriorMonth, sharesShortPreviousMonthDate, sharesPercentSharesOut 

- Low Float: Higher volatility, larger price moves
- High Short Interest: Potential for short if stock rises

## 7. Ownership
heldPercentInsiders, heldPercentInstitutions

- High Insider + High Institutional: Very bullish
- High Insider + Low Institutional: Potential growth story
- Low Insider + High Institutional: Mature, stable company
- Low Insider + Low Institutional: Speculative or troubled

## 8. Dividends
dividendRate, dividendYield, payoutRatio, fiveYearAvgDividendYield
trailingAnnualDividendRate, trailingAnnualDividendYield
lastDividendValue, lastDividendDate, dividendDate, exDividendDate

## 9. Valuation Ratios
trailingPE/forwardPE - Price-to-Earnings ratio using last/next expected 12 months
trailingPegRatio - P/E ratio divided by earnings growth rate, < 1 = potentially undervalued, > 3 potentially high growth
priceToBook - Market value relative to accounting book value 
bookValue - Net asset value per share (assets - liabilities) 
priceToSalesTrailing12Months - Market cap relative to last 12 months revenue, useful for companies with no earnings or negative earnings 1-2 = mature company
enterpriseToRevenue - Similar to P/S but includes debt

## 10. Financial Metrics
### Profitability
profitMargins, grossMargins, ebitdaMargins, operatingMargins

### Growth
netIncomeToCommon, earningsQuarterlyGrowth, earningsGrowth, revenueGrowth

### Return Metrics
returnOnAssets, returnOnEquity

### Cashflow
grossProfits, ebitda, operatingCashflow, freeCashflow

### Balancesheets
totalRevenue, revenuePerShare, totalCash, totalCashPerShare, totalDebt, 
debtToEquity, quickRatio, currentRatio

## 11. Earnings & Analysts
trailingEps, forwardEps, epsTrailingTwelveMonths, epsForward, epsCurrentYear, priceEpsCurrentYear, earningsTimestamp, earningsTimestampStart,earningsTimestampEnd, earningsCallTimestampStart, earningsCallTimestampEnd, isEarningsDateEstimate,
recommendationMean, recommendationKey, numberOfAnalystOpinions, averageAnalystRating,
targetHighPrice, targetLowPrice, targetMeanPrice, targetMedianPrice

## 12. Price History / Technicals
fiftyTwoWeekLow, fiftyTwoWeekHigh, fiftyTwoWeekRange
fiftyTwoWeekChange, SandP52WeekChange, 52WeekChange, fiftyTwoWeekChangePercent
fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent, fiftyDayAverage, twoHundredDayAverage
fiftyDayAverageChange, fiftyDayAverageChangePercent, twoHundredDayAverageChange, twoHundredDayAverageChangePercent, allTimeHigh, allTimeLow

## 13. Risk & Governance
auditRisk, boardRisk, compensationRisk, shareHolderRightsRisk, overallRisk, governanceEpochDate

## 14. Miscellaneous
beta, financialCurrency, corporateActions, sourceInterval
