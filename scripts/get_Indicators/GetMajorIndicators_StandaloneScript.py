# pip install yfinance pandas numpy
import math
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

START = "1998-01-01"

#```
# Script for downloading and calculating financial indicators
#```

# -----------------------------
# Helpers: technical indicators
# -----------------------------

# Simple Moving Average (SMA).
# Average of past x days at closing time
def sma(series, window):
    return series.rolling(window).mean()

# Exponential Moving Average (EMA)
# exponential weights (yesterday counts more than 2 days ago, which counts more than 3 days ago, etc.). 
# (sum of weights is geometric series that adds up to 1, so gives back the original scale)
# ratios: 10-day 0.82 ; 20-day 0.905 ; 100-day 0.98 
def ema(series, window):
    return series.ewm(span=window, adjust=False).mean()

# Weighted Moving Average (WMA)
# Uses linearly increasing weights/ also gives more weight to recent closes, but via exponential decay instead of linear weights.
# last day in list gets weight of 1, next last day gets weight 1+n
# divides weighted sum by sum of weights to get average
def wma(series, window):
    # Linear weights: 1..window
    weights = np.arange(1, window + 1)
    return series.rolling(window).apply(lambda x: np.dot(x, weights)/weights.sum(), raw=True)

# Financial Momentum tools
def macd(close, fast=12, slow=26, signal=9):
    # macd_line = EMA(12) − EMA(26) difference between short-term and long-term trend 
    # Positive -> short-term trend stronger than long-term (bullish)
    # Negative -> long-term trend stronger than short-term (bearish)
    macd_line = ema(close, fast) - ema(close, slow) 

    # signal_line = EMA(9) of macd_line
    # smoothed version of macd_line
    # Used for crossovers (when MACD crosses above signal -> bullish, below -> bearish).
    signal_line = ema(macd_line, signal)

    # hist = MACD line − Signal line
    # The histogram
    # Positive histogram = upward momentum increasing.
    # Negative histogram = downward momentum increasing.
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

# Relative Strength Index (RSI)
# Gives information about “pressure buildup” in the last 14 days.
# RSI 70-100 -> price rising a lot recently (often labeled "Overbought") 
# RSI 50 -> neutral/balance point
# RSI 0-30 -> price falling a lot recently (often labeled "Oversold") 
def rsi(close, period=14):
    delta = close.diff() # Daily change in closing price
    gain = (delta.clip(lower=0)).ewm(alpha=1/period, adjust=False).mean() # Average only up movements
    loss = (-delta.clip(upper=0)).ewm(alpha=1/period, adjust=False).mean() # Average only down movements
    rs = gain / loss # Relative strength = ratio of average gains to average losses.
    return 100 - (100 / (1 + rs)) # Scales the ratio into 0-100

# Stochastic Oscillator (Stoch)
# %K or %D > 80 -> considered “Overbought”.
# %K or %D < 20 -> considered “Oversold”.
# When %K crosses above %D from below -> bullish signal.
# When %K crosses below %D from above -> bearish signal.
# Compares closes to the recent high–low band, it’s very good at picking up short-term momentum shifts.
def stochastic_osc(high, low, close, k_window=14, d_window=3):
    lowest_low = low.rolling(k_window).min() # last 14 day lowest low
    highest_high = high.rolling(k_window).max() # Last 14 day highest high
    k = 100 * (close - lowest_low) / (highest_high - lowest_low) # Measures where today's close sits within the recent high-low range.
    d = k.rolling(d_window).mean() # 3 day mean of k
    return k, d

# Williams %R
# function returns the Williams %R oscillator, which is just another way of quantifying momentum by placing today’s close inside its recent trading range.
# Outputs values between 0 and −100.
# %R = 0 means “as strong as possible” (at the top of the range). (0-20 overbouth)
# %R = −100 means “as weak as possible” (at the bottom of the range). (-80 - -100 oversold)
# Close in the middle of the range → %R ≈ −50. (neutral)
# It measures how close today’s close is to the recent high–low range.
def williams_r(high, low, close, period=14):
    highest_high = high.rolling(period).max() # Last 14 day highest high
    lowest_low = low.rolling(period).min()  # last 14 day lowest low
    return -100 * (highest_high - close) / (highest_high - lowest_low) # Outputs values between 0 and −100.

# Bollinger Bands, volatility-based indicator
# Band width expands/shrinks with volatility.
#   Wide bands → volatile market.
#   Narrow bands → quiet market (sometimes before a breakout).
# Price vs. bands:
#   Touching upper band → strong upward momentum, possibly overbought.
#   Touching lower band → strong downward momentum, possibly oversold.
#   Middle band (SMA) often used as dynamic support/resistance.
# %B:
#   Instead of absolute prices, gives you a normalized 0–1 measure of where price sits inside the band.
def bollinger_bands(close, window=20, num_std=2):
    mid = sma(close, window) # moving average of 20 day close
    std = close.rolling(window).std() # Standard deviation of the closing prices over the same window. Captures volatility
    upper = mid + num_std * std # upper band
    lower = mid - num_std * std # lower band
    bbp = (close - lower) / (upper - lower)  # %B
    return upper, mid, lower, bbp

# True Range (TR)
# It captures both intra-day volatility and overnight gaps.
# In human words, calculates swings overnight and day time and gives the swing range
def true_range(high, low, close):
    prev_close = close.shift(1) # Yesterday's closing price aligned with today.
    tr = pd.concat([
        (high - low), # intraday range 
        (high - prev_close).abs(), # upwared gap
        (low - prev_close).abs() # downward gap
    ], axis=1).max(axis=1) # picks largest value ; This ensures TR always reflects the true price movement range, including both intraday swings and gaps from the prior close
    return tr

# Average True Range (ATR)
# ATR is a pure volatility measure.
# ATR is in the same units as price (e.g. dollars).
def atr(high, low, close, period=14):
    tr = true_range(high, low, close) # compute the daily True Range using your true_range function.
    return tr.ewm(alpha=1/period, adjust=False).mean() # Apply an exponentially weighted moving average (EWMA) to TR.

# annualized historical volatility (based on returns)
# Hist vol = statistical estimate of realized volatility, assuming past return variance continues.
# Is the stock currently stable (low vol) or turbulent (high vol)?
#   Moderate: 15–30% (typical for S&P 500 stocks in normal times).
#   High: 40–60%+ (growth stocks, small caps, or crisis periods).
#   Extreme: 80–100%+ (crypto, meme stocks, biotech during FDA events).
def hist_vol(log_ret, window=20, trading_days=252):
    # Annualized historical volatility
    return log_ret.rolling(window).std() * math.sqrt(trading_days)

# On-Balance Volume (OBV)
#   Rising OBV = more volume is occurring on up days than down days → buying pressure.
#   Falling OBV = more volume on down days → selling pressure.
#   Flat OBV = no strong volume bias.
# Traders often compare OBV to price:
#   If price is making new highs but OBV isn’t → weak trend (divergence).
#   If OBV breaks out before price does → could signal trend continuation.
def obv(close, volume):
    direction = np.sign(close.diff().fillna(0)) # directional flag if price rose or fell from yesterday to today [-1,0,1]
    return (direction * volume).fillna(0).cumsum()  # culmunative sum over time for volume movements 

# Chaikin Money Flow (CMF)
# gives volume-weighted positioning info: is volume flowing in on up-closes or on down-closes?
# CMF > 0 → more buying pressure (closes near highs on strong volume).
# CMF < 0 → more selling pressure (closes near lows on strong volume).
def chaikin_money_flow(high, low, close, volume, period=20):
    mfm = ((close - low) - (high - close)) / (high - low) # measures where the close sits inside the day’s high–low range
    mfm = mfm.replace([np.inf, -np.inf], np.nan).fillna(0) # division by 0 fix
    mfv = mfm * volume  # Scales that multiplier by trading volume.
    return mfv.rolling(period).sum() / volume.rolling(period).sum() # normalized rolling sum of MFV over the lookback window (20 days)

# rolling VWAP (Volume-Weighted Average Price)
# a way of tracking the average trading price, weighted by traded volume, over a rolling window.
# Gives a volume-adjusted price trend, often smoother and more “true to liquidity” than SMA/EMA.
def rolling_vwap(high, low, close, volume, window=20):
    tp = (high + low + close) / 3 # Approximate the “average” price of the day (not just the close).
    numerator = (tp * volume).rolling(window).sum() # Multiply each day’s typical price by its trading volume and rolling sum over 20 days window
    denom = volume.rolling(window).sum() # The sum of the volume over the same window
    return numerator / denom # Weighted average price = (sum of price × volume) ÷ (sum of volume).

# -----------------------------
# Feature engineering pipeline
# -----------------------------
def build_features(df):
    """
    Expects a DataFrame with columns:
    ['Open','High','Low','Close','Adj Close','Volume']
    Returns df with engineered features.
    """
    out = df.copy()

    # Basic returns & spreads (use adjusted Close)
    out['ret_pct'] = out['Close'].pct_change()
    out['ret_log'] = np.log(out['Close']).diff()
    out['gap_open_prevclose'] = (out['Open'] - out['Close'].shift(1)) / out['Close'].shift(1)
    out['spread_hl'] = (out['High'] - out['Low']) / out['Close'].shift(1)
    out['spread_co'] = (out['Close'] - out['Open']) / out['Open']

    # Trend: SMA/EMA/WMA
    for w in [10, 20, 50, 100, 200]:
        out[f'sma_{w}'] = sma(out['Close'], w)
        out[f'ema_{w}'] = ema(out['Close'], w)
        out[f'wma_{w}'] = wma(out['Close'], w)

    # MACD / RSI (on adjusted Close)
    out['macd'], out['macd_signal'], out['macd_hist'] = macd(out['Close'])
    out['rsi_14'] = rsi(out['Close'], 14)

    # Momentum/Volatility using adjusted OHLC and Volume (already adjusted by yfinance)
    out['stoch_k_14'], out['stoch_d_3'] = stochastic_osc(out['High'], out['Low'], out['Close'], 14, 3)
    out['williams_r_14'] = williams_r(out['High'], out['Low'], out['Close'], 14)
    out['bb_upper_20'], out['bb_mid_20'], out['bb_lower_20'], out['bbp_20'] = bollinger_bands(out['Close'], 20, 2)
    out['atr_14'] = atr(out['High'], out['Low'], out['Close'], 14)
    out['hv_20'] = hist_vol(out['ret_log'], 20)

    # Volume-based (Volume is adjusted when auto_adjust=True)
    out['obv'] = obv(out['Close'], out['Volume'])
    out['cmf_20'] = chaikin_money_flow(out['High'], out['Low'], out['Close'], out['Volume'], 20)
    out['vwap_20'] = rolling_vwap(out['High'], out['Low'], out['Close'], out['Volume'], 20)

    out.replace([np.inf, -np.inf], np.nan, inplace=True)
    return out

# -----------------------------
# Download & assemble dataset
# -----------------------------

def fetch_yahoo(ticker, start=None, end=None):
    t = yf.Ticker(ticker)
    if start or end:
        df = t.history(start=start, end=end, interval="1d", auto_adjust=True)
    else:
        df = t.history(period="max", interval="1d", auto_adjust=True)
    df = _strip_tz_index(df)
    df.index.name = "date"
    return df

def _strip_tz_index(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    out = df.copy()
    if isinstance(out.index, pd.DatetimeIndex):
        try:
            out.index = out.index.tz_convert(None)
        except Exception:
            try:
                out.index = out.index.tz_localize(None)
            except Exception:
                pass
        out.index = out.index.normalize()
        out.index.name = "date"
    return out

# -----------------------------
# Main pipeline
# -----------------------------
def run_pipeline(tickers, output_dir="data/indicators"):
    import os
    os.makedirs(output_dir, exist_ok=True)

    per_ticker = []
    for name, tkr in tickers.items():
        raw = fetch_yahoo(tkr, START)
        if raw.empty:
            print(f"[WARN] No data for {name} ({tkr}).")
            continue

        feats = build_features(raw)
        feats['ticker'] = name
        feats['symbol'] = tkr

        out_path = os.path.join(output_dir, f"{name}_daily_features.csv")
        feats.to_csv(out_path, index=True)
        print(f"Saved: {out_path} ({len(feats)} rows)")
        per_ticker.append(feats)

    if per_ticker:
        tidy = pd.concat(per_ticker, axis=0, ignore_index=False)
        tidy.index.name = 'date'
        tidy = tidy.reset_index()

        if isinstance(tidy.columns, pd.MultiIndex):
            tidy.columns = [c[0] for c in tidy.columns]

        keep_first = ['date', 'ticker', 'symbol']
        rest = [c for c in tidy.columns if c not in keep_first]
        tidy = tidy[keep_first + rest]

        merged_path = os.path.join(output_dir, "merged_daily_features.csv")
        tidy.to_csv(merged_path, index=False)
        print(f"Saved: {merged_path} ({len(tidy)} rows)")

TICKERS = [
    "XOM","NEM","CAT","PG","AMZN","LLY","JPM","NVDA","GOOGL","NEE","WELL","SPY",
    "EXSA.DE","ISF.L",
    "XLE","XLB","XLI","XLP","XLY","XLV","XLF","XLK","XLC","XLU","XLRE",
    "GC=F","SI=F","CL=F"
]

SYMBOL_MAP = {t: t for t in TICKERS}

if __name__ == "__main__":
    run_pipeline(SYMBOL_MAP)



