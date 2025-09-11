# pip install yfinance pandas numpy
import math
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# -----------------------------
# Helpers: technical indicators
# -----------------------------
def sma(series, window):
    return series.rolling(window).mean()

def ema(series, window):
    return series.ewm(span=window, adjust=False).mean()

def wma(series, window):
    # Linear weights: 1..window
    weights = np.arange(1, window + 1)
    return series.rolling(window).apply(lambda x: np.dot(x, weights)/weights.sum(), raw=True)

def macd(close, fast=12, slow=26, signal=9):
    macd_line = ema(close, fast) - ema(close, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def rsi(close, period=14):
    delta = close.diff()
    gain = (delta.clip(lower=0)).ewm(alpha=1/period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1/period, adjust=False).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def stochastic_osc(high, low, close, k_window=14, d_window=3):
    lowest_low = low.rolling(k_window).min()
    highest_high = high.rolling(k_window).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(d_window).mean()
    return k, d

def williams_r(high, low, close, period=14):
    highest_high = high.rolling(period).max()
    lowest_low = low.rolling(period).min()
    return -100 * (highest_high - close) / (highest_high - lowest_low)

def bollinger_bands(close, window=20, num_std=2):
    mid = sma(close, window)
    std = close.rolling(window).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    bbp = (close - lower) / (upper - lower)  # %B
    return upper, mid, lower, bbp

def true_range(high, low, close):
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr

def atr(high, low, close, period=14):
    tr = true_range(high, low, close)
    return tr.ewm(alpha=1/period, adjust=False).mean()

def hist_vol(log_ret, window=20, trading_days=252):
    # Annualized historical volatility
    return log_ret.rolling(window).std() * math.sqrt(trading_days)

def obv(close, volume):
    direction = np.sign(close.diff().fillna(0))
    return (direction * volume).fillna(0).cumsum()

def chaikin_money_flow(high, low, close, volume, period=20):
    mfm = ((close - low) - (high - close)) / (high - low)
    mfm = mfm.replace([np.inf, -np.inf], np.nan).fillna(0)
    mfv = mfm * volume
    return mfv.rolling(period).sum() / volume.rolling(period).sum()

def rolling_vwap(high, low, close, volume, window=20):
    tp = (high + low + close) / 3
    numerator = (tp * volume).rolling(window).sum()
    denom = volume.rolling(window).sum()
    return numerator / denom

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

    # Basic returns & spreads
    out['ret_pct'] = out['Adj Close'].pct_change()
    out['ret_log'] = np.log(out['Adj Close']).diff()
    out['gap_open_prevclose'] = (out['Open'] - out['Adj Close'].shift(1)) / out['Adj Close'].shift(1)
    out['spread_hl'] = (out['High'] - out['Low']) / out['Close'].shift(1)
    out['spread_co'] = (out['Close'] - out['Open']) / out['Open']

    # Trend: SMA/EMA/WMA
    for w in [10, 20, 50, 100, 200]:
        out[f'sma_{w}'] = sma(out['Adj Close'], w)
        out[f'ema_{w}'] = ema(out['Adj Close'], w)
        out[f'wma_{w}'] = wma(out['Adj Close'], w)

    # MACD
    out['macd'], out['macd_signal'], out['macd_hist'] = macd(out['Adj Close'])

    # Momentum: RSI, Stoch, Williams %R
    out['rsi_14'] = rsi(out['Adj Close'], 14)
    out['stoch_k_14'], out['stoch_d_3'] = stochastic_osc(out['High'], out['Low'], out['Close'], 14, 3)
    out['williams_r_14'] = williams_r(out['High'], out['Low'], out['Close'], 14)

    # Volatility: Bollinger, ATR, HistVol
    out['bb_upper_20'], out['bb_mid_20'], out['bb_lower_20'], out['bbp_20'] = bollinger_bands(out['Adj Close'], 20, 2)
    out['atr_14'] = atr(out['High'], out['Low'], out['Close'], 14)
    out['hv_20'] = hist_vol(out['ret_log'], 20)

    # Volume-based: OBV, CMF, VWAP(rolling)
    out['obv'] = obv(out['Adj Close'], out['Volume'])
    out['cmf_20'] = chaikin_money_flow(out['High'], out['Low'], out['Close'], out['Volume'], 20)
    out['vwap_20'] = rolling_vwap(out['High'], out['Low'], out['Close'], out['Volume'], 20)

    # Clean up infs
    out.replace([np.inf, -np.inf], np.nan, inplace=True)
    return out

# -----------------------------
# Download & assemble dataset
# -----------------------------
def fetch_yahoo(ticker):
    df = yf.download(
        ticker,
        period="max",      # get all available history
        interval="1d",
        auto_adjust=False,
        progress=False
    )
    # Standardize column names if needed
    df = df.rename(columns={'Adj Close': 'Adj Close'})
    return df

def main():
    tickers = {
        "WTI_OIL": "CL=F",  # Change to "BZ=F" for Brent
        "FDX": "FDX",
        "UPS": "UPS",
    }

    end = datetime.today().date()
    start = end - timedelta(days=365 * 10 + 5)  # ~10 years buffer for leap years

    per_ticker = []
    for name, tkr in tickers.items():
        raw = fetch_yahoo(tkr)
        if raw.empty:
            print(f"[WARN] No data for {name} ({tkr}).")
            continue

        feats = build_features(raw)
        # Add identifier columns
        feats['ticker'] = name
        feats['symbol'] = tkr

        # Save per-ticker xlsx
        out_path = f"{name}_daily_features.xlsx"
        feats.to_excel(out_path, index=True)  # <-- fixed
        print(f"Saved: {out_path} ({len(feats)} rows)")

        per_ticker.append(feats)

    if per_ticker:
        # Stack all tickers (they already have 'ticker' and 'symbol' columns)
        tidy = pd.concat(per_ticker, axis=0, ignore_index=False)

        # Ensure the datetime index becomes a 'date' column
        tidy.index.name = 'date'
        tidy = tidy.reset_index()

        # If columns are a MultiIndex (e.g., ('Adj Close','CL=F')), flatten them
        if isinstance(tidy.columns, pd.MultiIndex):
            tidy.columns = [
                "_".join([str(x) for x in tup if str(x) != ""]).strip("_")
                for tup in tidy.columns.to_list()
            ]

        # Some envs name the reset index 'Date' (capital D) — normalize it
        if 'Date' in tidy.columns and 'date' not in tidy.columns:
            tidy = tidy.rename(columns={'Date': 'date'})

        # Put key columns first
        keep_first = ['date', 'ticker', 'symbol']
        rest = [c for c in tidy.columns if c not in keep_first]
        tidy = tidy[keep_first + rest]

        tidy.to_excel("ALL_TICKERS_daily_features.xlsx", index=False)  # <-- fixed
        print(f"Saved: ALL_TICKERS_daily_features.xlsx ({len(tidy)} rows)")

if __name__ == "__main__":
    main()
