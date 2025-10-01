Ticker info 
    time.sleep(2)

    stock = yf.Ticker("AAPL")
    print(stock.info.keys())

Stocks

1. Company Information
longName, shortName, displayName
industry, industryKey, industryDisp
sector, sectorKey, sectorDisp
longBusinessSummary
fullTimeEmployees, executiveTeam, companyOfficers
website, irWebsite, address1, city, state, zip, country, phone

2. Market/Exchange Information
symbol, exchange, market, quoteType, quoteSourceName, fullExchangeName
exchangeTimezoneName, exchangeTimezoneShortName, gmtOffSetMilliseconds
language, region, typeDisp, messageBoardId
marketState, tradeable, triggerable, cryptoTradeable

3. Price & Trading Data
currentPrice, previousClose, open, dayLow, dayHigh
regularMarketPrice, regularMarketOpen, regularMarketDayLow, regularMarketDayHigh, regularMarketPreviousClose
regularMarketChange, regularMarketChangePercent, regularMarketDayRange
preMarketPrice, preMarketChange, preMarketChangePercent, preMarketTime
regularMarketTime
bid, ask, bidSize, askSize

4. Volume & Liquidity
volume, regularMarketVolume
averageVolume, averageVolume10days, averageDailyVolume10Day, averageDailyVolume3Month

5. Market Valuation
marketCap, enterpriseValue
floatShares, sharesOutstanding, impliedSharesOutstanding
sharesShort, sharesShortPriorMonth, sharesShortPreviousMonthDate, sharesPercentSharesOut, shortRatio, shortPercentOfFloat
heldPercentInsiders, heldPercentInstitutions

6. Dividends
dividendRate, dividendYield, payoutRatio
fiveYearAvgDividendYield
trailingAnnualDividendRate, trailingAnnualDividendYield
lastDividendValue, lastDividendDate, dividendDate
exDividendDate

7. Valuation Ratios
trailingPE, forwardPE, trailingPegRatio
priceToBook, bookValue
priceToSalesTrailing12Months
enterpriseToRevenue, enterpriseToEbitda

8. Growth & Profitability
netIncomeToCommon, earningsQuarterlyGrowth, earningsGrowth, revenueGrowth
profitMargins, grossMargins, ebitdaMargins, operatingMargins
returnOnAssets, returnOnEquity
grossProfits, ebitda, operatingCashflow, freeCashflow
totalRevenue, revenuePerShare
totalCash, totalCashPerShare, totalDebt, debtToEquity
quickRatio, currentRatio

9. Earnings & Analysts
trailingEps, forwardEps, epsTrailingTwelveMonths, epsForward, epsCurrentYear, priceEpsCurrentYear
earningsTimestamp, earningsTimestampStart, earningsTimestampEnd, earningsCallTimestampStart, earningsCallTimestampEnd, isEarningsDateEstimate
recommendationMean, recommendationKey, numberOfAnalystOpinions, averageAnalystRating
targetHighPrice, targetLowPrice, targetMeanPrice, targetMedianPrice

10. Price History / Technicals
fiftyTwoWeekLow, fiftyTwoWeekHigh, fiftyTwoWeekRange
fiftyTwoWeekChange, SandP52WeekChange, 52WeekChange, fiftyTwoWeekChangePercent
fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent
fiftyDayAverage, twoHundredDayAverage
fiftyDayAverageChange, fiftyDayAverageChangePercent, twoHundredDayAverageChange, twoHundredDayAverageChangePercent
allTimeHigh, allTimeLow

11. Risk & Governance
auditRisk, boardRisk, compensationRisk, shareHolderRightsRisk, overallRisk
governanceEpochDate, compensationAsOfEpochDate

12. Miscellaneous
priceHint, beta
financialCurrency
corporateActions
customPriceAlertConfidence
firstTradeDateMilliseconds
sourceInterval, exchangeDataDelayedBy
esgPopulated, hasPrePostMarketData
maxAge

Ticker info
    time.sleep(2)

    stock = yf.Ticker("XLE")
    print(stock.info.keys())

# ETFs

1. Fund Information
longName, shortName
fundFamily (e.g. iShares, Vanguard)
fundInceptionDate (when the ETF/fund launched)
category (fund category: Equity, Bond, etc.)
legalType (ETF, mutual fund, etc.)
longBusinessSummary
companyOfficers, executiveTeam

2. Market / Exchange Information
symbol, quoteType, typeDisp
exchange, fullExchangeName
region, language, quoteSourceName
exchangeTimezoneName, exchangeTimezoneShortName, gmtOffSetMilliseconds
messageBoardId
market, marketState, triggerable, tradeable, cryptoTradeable, esgPopulated

3. Price & Trading Data
previousClose, open, dayLow, dayHigh
regularMarketPrice, regularMarketOpen, regularMarketDayLow, regularMarketDayHigh, regularMarketPreviousClose
regularMarketChange, regularMarketChangePercent, regularMarketDayRange, regularMarketTime
preMarketPrice, preMarketChange, preMarketChangePercent, preMarketTime
bid, ask, bidSize, askSize
priceHint

4. Volume & Liquidity
volume, regularMarketVolume
averageVolume, averageVolume10days, averageDailyVolume10Day, averageDailyVolume3Month

5. Fund Net Asset Data
navPrice (Net Asset Value per share)
netAssets (total AUM)
totalAssets
sharesOutstanding
marketCap

6. Returns & Performance
ytdReturn
threeYearAverageReturn
fiveYearAverageReturn
trailingThreeMonthReturns
trailingThreeMonthNavReturns

7. Dividends & Yield
dividendYield
trailingAnnualDividendRate, trailingAnnualDividendYield

8. Valuation Ratios
trailingPE (sometimes provided even for funds if equity-heavy)
priceToBook, bookValue
trailingPegRatio

9. Risk & Beta
beta3Year

10. Technicals / Price Ranges
fiftyTwoWeekLow, fiftyTwoWeekHigh, fiftyTwoWeekRange
fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent
fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent
fiftyTwoWeekChangePercent
fiftyDayAverage, twoHundredDayAverage
fiftyDayAverageChange, fiftyDayAverageChangePercent
twoHundredDayAverageChange, twoHundredDayAverageChangePercent
allTimeHigh, allTimeLow

11. Financial Metrics
epsTrailingTwelveMonths (not always meaningful for ETFs)
netExpenseRatio (expense ratio %)

12. Miscellaneous
financialCurrency
sourceInterval, exchangeDataDelayedBy
corporateActions
customPriceAlertConfidence
maxAge

ETFs
UK - no mining/materials, industrials, consumer discretionary, healthcare/pharmaceuticals, financials, Information Technology, communcation services, utilities

Ticker info 
    time.sleep(2)

    stock = yf.Ticker("GC=F")
    print(stock.info.keys())

# Commodities

1. Contract Information
contractSymbol
underlyingSymbol
underlyingExchangeSymbol
headSymbolAsString
expireDate, expireIsoDate (expiration date of the option)

2. Market / Exchange Information
symbol, shortName
quoteType, typeDisp
exchange, fullExchangeName
exchangeTimezoneName, exchangeTimezoneShortName, gmtOffSetMilliseconds
market, marketState, tradeable, cryptoTradeable, esgPopulated
quoteSourceName, triggerable, corporateActions
language, region

3. Price & Trading Data
previousClose, open, dayLow, dayHigh
regularMarketPrice, regularMarketOpen, regularMarketDayLow, regularMarketDayHigh, regularMarketPreviousClose
regularMarketChange, regularMarketChangePercent, regularMarketDayRange, regularMarketTime
bid, ask, bidSize, askSize
priceHint

4. Volume & Open Interest
volume, regularMarketVolume
averageVolume, averageVolume10days, averageDailyVolume10Day, averageDailyVolume3Month
openInterest (unique to options, # of outstanding contracts)

5. Technicals / Price Ranges
fiftyTwoWeekLow, fiftyTwoWeekHigh, fiftyTwoWeekRange
fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent
fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent
fiftyTwoWeekChangePercent
fiftyDayAverage, twoHundredDayAverage
fiftyDayAverageChange, fiftyDayAverageChangePercent
twoHundredDayAverageChange, twoHundredDayAverageChangePercent
allTimeHigh, allTimeLow

6. Miscellaneous
maxAge
customPriceAlertConfidence
sourceInterval, exchangeDataDelayedBy
hasPrePostMarketData
firstTradeDateMilliseconds
trailingPegRatio (not meaningful for options, likely inherited field)
currency