import yfinance as yf
import time

# AAPL, SIE.DE, NVDA
# SPY, XLE, EXH1.DE
# GC=F, CL=F
time.sleep(2)

stock = yf.Ticker("GC=F")
print(stock.info.keys())