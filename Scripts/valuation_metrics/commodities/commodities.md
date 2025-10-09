# Commodity Data
stock = yf.Ticker("commodity")
print(stock.info.keys())
## 1. Market / Exchange Information
symbol, shortName, exchange, market

## 2. Price & Trading Data
previousClose, open, dayLow, dayHigh regularMarketPrice, regularMarketOpen, regularMarketDayLow, regularMarketDayHigh, regularMarketPreviousClose,
regularMarketChange, regularMarketChangePercent, regularMarketDayRange, 
regularMarketTime, bid, ask, bidSize, askSize, priceHint

## 3. Volume & Open Interest
volume, regularMarketVolume, averageVolume, averageVolume10days, averageDailyVolume10Day, averageDailyVolume3Month

## 4. Technicals / Price Ranges
fiftyTwoWeekLow, fiftyTwoWeekHigh, fiftyTwoWeekRange, fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent
fiftyTwoWeekChangePercent, fiftyDayAverage, twoHundredDayAverage, fiftyDayAverageChange, fiftyDayAverageChangePercent, twoHundredDayAverageChange, twoHundredDayAverageChangePercent, allTimeHigh, allTimeLow

## 5. Miscellaneous
currency