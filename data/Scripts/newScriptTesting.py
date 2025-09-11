# -*- coding: utf-8 -*-
# pip install yfinance pandas numpy openpyxl --upgrade
import warnings
warnings.filterwarnings("ignore")

import math
import numpy as np
import pandas as pd
import yfinance as yf

# ============================= TZ / DATE HELPERS =============================

def strip_tz(df: pd.DataFrame) -> pd.DataFrame:
    """Make all datetime columns/index timezone-naive (Excel can't handle tz-aware)."""
    out = df.copy()
    for c in out.select_dtypes(include=["datetimetz"]).columns:
        out[c] = out[c].dt.tz_localize(None)
    if isinstance(out.index, pd.DatetimeIndex) and out.index.tz is not None:
        try:
            out.index = out.index.tz_convert(None)
        except Exception:
            out.index = out.index.tz_localize(None)
    return out

def _normalize_daily_index(idx_like):
    di = pd.to_datetime(idx_like, errors="coerce")
    if isinstance(di, pd.DatetimeIndex):
        if di.tz is not None:
            try:
                di = di.tz_convert(None)
            except Exception:
                di = di.tz_localize(None)
        return di.normalize()
    try:
        di = di.tz_localize(None)
    except Exception:
        pass
    return pd.DatetimeIndex(di).normalize()

# ============================= TECHNICALS =============================

def sma(series, window): return series.rolling(window).mean()
def ema(series, window): return series.ewm(span=window, adjust=False).mean()
def wma(series, window):
    w = np.arange(1, window + 1)
    return series.rolling(window).apply(lambda x: np.dot(x, w) / w.sum(), raw=True)

def macd(close, fast=12, slow=26, signal=9):
    m = ema(close, fast) - ema(close, slow)
    s = ema(m, signal)
    return m, s, m - s

def rsi(close, period=14):
    d = close.diff()
    gain = d.clip(lower=0).ewm(alpha=1/period, adjust=False).mean()
    loss = (-d.clip(upper=0)).ewm(alpha=1/period, adjust=False).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def stochastic_osc(h, l, c, k_window=14, d_window=3):
    ll = l.rolling(k_window).min()
    hh = h.rolling(k_window).max()
    k = 100 * (c - ll) / (hh - ll)
    d = k.rolling(d_window).mean()
    return k, d

def williams_r(h, l, c, period=14):
    hh = h.rolling(period).max()
    ll = l.rolling(period).min()
    return -100 * (hh - c) / (hh - ll)

def bollinger_bands(close, window=20, num_std=2):
    mid = sma(close, window)
    std = close.rolling(window).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    bbp = (close - lower) / (upper - lower)
    return upper, mid, lower, bbp

def true_range(h, l, c):
    pc = c.shift(1)
    return pd.concat([(h - l), (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)

def atr(h, l, c, period=14):
    return true_range(h, l, c).ewm(alpha=1/period, adjust=False).mean()

def hist_vol(log_ret, window=20, trading_days=252):
    return log_ret.rolling(window).std() * math.sqrt(trading_days)

def obv(close, vol):
    direction = np.sign(close.diff().fillna(0))
    return (direction * vol).fillna(0).cumsum()

def chaikin_money_flow(h, l, c, v, period=20):
    mfm = ((c - l) - (h - c)) / (h - l)
    mfm = mfm.replace([np.inf, -np.inf], np.nan).fillna(0)
    return (mfm * v).rolling(period).sum() / v.rolling(period).sum()

def rolling_vwap(h, l, c, v, window=20):
    tp = (h + l + c) / 3
    return (tp * v).rolling(window).sum() / v.rolling(window).sum()

def build_price_features(df):
    out = df.copy()
    out['ret_pct'] = out['Adj Close'].pct_change()
    out['ret_log'] = np.log(out['Adj Close']).diff()
    out['gap_open_prevclose'] = (out['Open'] - out['Close'].shift(1)) / out['Close'].shift(1)
    out['spread_hl'] = (out['High'] - out['Low']) / out['Close'].shift(1)
    out['spread_co'] = (out['Close'] - out['Open']) / out['Open']

    for w in [10, 20, 50, 100, 200]:
        out[f'sma_{w}'] = sma(out['Adj Close'], w)
        out[f'ema_{w}'] = ema(out['Adj Close'], w)
        out[f'wma_{w}'] = wma(out['Adj Close'], w)

    out['macd'], out['macd_signal'], out['macd_hist'] = macd(out['Adj Close'])
    out['rsi_14'] = rsi(out['Adj Close'], 14)
    out['stoch_k_14'], out['stoch_d_3'] = stochastic_osc(out['High'], out['Low'], out['Close'], 14, 3)
    out['williams_r_14'] = williams_r(out['High'], out['Low'], out['Close'], 14)
    out['bb_upper_20'], out['bb_mid_20'], out['bb_lower_20'], out['bbp_20'] = bollinger_bands(out['Adj Close'], 20, 2)
    out['atr_14'] = atr(out['High'], out['Low'], out['Close'], 14)
    out['hv_20'] = hist_vol(out['ret_log'], 20)
    out['obv'] = obv(out['Adj Close'], out['Volume'])
    out['cmf_20'] = chaikin_money_flow(out['High'], out['Low'], out['Close'], out['Volume'], 20)
    out['vwap_20'] = rolling_vwap(out['High'], out['Low'], out['Close'], out['Volume'], 20)

    out.replace([np.inf, -np.inf], np.nan, inplace=True)
    return out

# ============================= SPLIT FACTOR (robust) =============================

def future_split_factor(index: pd.DatetimeIndex, tkr: yf.Ticker) -> pd.Series:
    """
    For each date d in `index`, return product of all split ratios for split dates strictly > d.
    Uses actions['Stock Splits'] if available; falls back to splits.
    """
    sp = None
    try:
        acts = tkr.actions
        if acts is not None and not acts.empty and "Stock Splits" in acts.columns:
            sp = acts["Stock Splits"].dropna()
    except Exception:
        sp = None
    if sp is None or sp.empty:
        sp = tkr.splits

    if sp is None or sp.empty:
        return pd.Series(1.0, index=index)

    sp = sp.copy()
    sp.index = _normalize_daily_index(sp.index)
    sp = pd.to_numeric(sp, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    sp = sp[sp > 0]  # keep only valid ratios
    # keep only split dates that fall inside the overall index range (or later)
    sp = sp[sp.index >= index.min()]
    if sp.empty:
        return pd.Series(1.0, index=index)
    # collapse duplicates on the same day (product; usually only one anyway)
    sp = sp.groupby(sp.index).prod().sort_index()

    factor = pd.Series(1.0, index=index)
    # multiply r into all dates strictly BEFORE the split date
    for d, r in sp.items():
        factor.loc[index < d] *= float(r)
    return factor

# ============================= MAIN BUILDER =============================

def build_yf_daily_table(ticker: str, years: int = 10) -> pd.DataFrame:
    t = yf.Ticker(ticker)

    # Prices (tz-naive, normalized to midnight)
    end = pd.Timestamp.today().normalize()
    start = end - pd.Timedelta(days=years * 365 + 10)
    px = t.history(start=start.date().isoformat(), end=end.date().isoformat(),
                   interval="1d", auto_adjust=False)
    if px is None or px.empty:
        raise RuntimeError(f"No price history for {ticker}")
    if isinstance(px.index, pd.DatetimeIndex) and px.index.tz is not None:
        try:
            px.index = px.index.tz_convert(None)
        except Exception:
            px.index = px.index.tz_localize(None)
    px.index = px.index.normalize()
    px.index.name = "date"

    feats = build_price_features(px)

    # Shares outstanding (ffill)
    try:
        sh = t.get_shares_full(start=start.date().isoformat())
        if sh is not None and not sh.empty:
            sh = sh.to_frame("shares_out")
            sh.index = _normalize_daily_index(sh.index)
            feats = feats.join(sh["shares_out"], how="left")
            feats["shares_out"] = feats["shares_out"].ffill()
        else:
            feats["shares_out"] = np.nan
    except Exception:
        feats["shares_out"] = np.nan

    # Accurate market cap: Close * shares_out * product of future splits (strictly after the day)
    try:
        cum_future = future_split_factor(feats.index, t)
    except Exception:
        cum_future = pd.Series(1.0, index=feats.index)

    feats["mcap_est"] = feats["Close"] * feats["shares_out"] * cum_future

    # Tag ticker and return
    feats["ticker"] = ticker
    return feats.reset_index()  # 'date' column

# ============================= RUN & SAVE =============================

def main():
    tickers = ["AAPL"]   # e.g. ["AAPL","MSFT","UPS"]
    years = 10

    all_tables = []
    for tk in tickers:
        print(f"Building daily table for {tk}...")
        df = build_yf_daily_table(tk, years=years)
        df = strip_tz(df)  # ensure tz-naive cols
        all_tables.append(df)
        out_path = f"{tk}_daily_enriched_{years}y.xlsx"
        df.to_excel(out_path, index=False)
        print(f"  Saved: {out_path} (rows={len(df)})")

    if all_tables:
        with pd.ExcelWriter("tickers_daily_enriched.xlsx", engine="openpyxl") as xl:
            for df in all_tables:
                tk = df["ticker"].iloc[0]
                strip_tz(df).to_excel(xl, sheet_name=tk[:31], index=False)
            pd.concat(all_tables, ignore_index=True).pipe(strip_tz).to_excel(xl, sheet_name="ALL_TICKERS", index=False)
        print("  Saved combined workbook: tickers_daily_enriched.xlsx")

if __name__ == "__main__":
    main()
