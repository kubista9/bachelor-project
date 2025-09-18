import numpy as np, pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# --- Load & find date column robustly ---
df = pd.read_excel("AAPL_daily_enriched_10y_clean.xlsx", sheet_name=0, engine="openpyxl")
df.columns = df.columns.map(lambda c: str(c).replace("\u00A0", " ").strip())
# try common date-like names; else fallback to first column if parseable
date_col = None
for c in df.columns:
    lc = c.lower()
    if lc in {"date","datetime","timestamp"} or any(k in lc for k in ["date","time","timestamp"]):
        date_col = c
        break
if date_col is None:
    cand = df.columns[0]
    if pd.to_datetime(df[cand], errors="coerce").notna().mean() > 0.8:
        date_col = cand
    else:
        raise ValueError(f"Couldn't find a date column. Columns: {list(df.columns)}")

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df[df[date_col].notna()].sort_values(date_col).reset_index(drop=True)

# --- Target: next-day log return (Adj Close) ---
if "Adj Close" not in df.columns:
    raise ValueError("Expected 'Adj Close' column not found.")
df["ret"] = np.log(df["Adj Close"]).diff()
df["y"]   = df["ret"].shift(-1)

# --- Feature engineering ---
# price-return lags
for lag in [1,2,3,5,10,20]:
    df[f"ret_lag{lag}"] = df["ret"].shift(lag)

# rolling stats
for w in [5,10,20]:
    df[f"ret_mean_{w}"] = df["ret"].rolling(w).mean()
    df[f"ret_std_{w}"]  = df["ret"].rolling(w).std()
    df[f"ma_{w}"]       = df["Adj Close"].rolling(w).mean()

# calendar features
dt = df[date_col]
df["dow"]   = dt.dt.weekday
df["month"] = dt.dt.month

# volume-derived features (optional but helpful)
if "Volume" in df.columns:
    df["log_vol"] = np.log(df["Volume"].replace(0, np.nan))
    for w in [5,20]:
        df[f"vol_mean_{w}"] = df["log_vol"].rolling(w).mean()
        df[f"vol_std_{w}"]  = df["log_vol"].rolling(w).std()
        df[f"vol_z_{w}"]    = (df["log_vol"] - df[f"vol_mean_{w}"]) / df[f"vol_std_{w}"]

# assemble X/y
drop_cols = {date_col, "Open","High","Low","Close","Adj Close","y"}  # keep Volume-derived features we created
feature_cols = [c for c in df.columns if c not in drop_cols]
X = df[feature_cols]
y = df["y"]

mask = y.notna() & X.notna().all(axis=1)
X, y = X[mask], y[mask]

# --- Model ---
rf = RandomForestRegressor(
    n_estimators=500,
    max_depth=6,
    min_samples_leaf=20,
    max_features="sqrt",
    random_state=42,
    n_jobs=-1
)

# --- Time-aware CV ---
tscv = TimeSeriesSplit(n_splits=5)
oof = np.zeros(len(y))
for tr, va in tscv.split(X, y):
    rf.fit(X.iloc[tr], y.iloc[tr])
    oof[va] = rf.predict(X.iloc[va])

print("OOF MAE:", mean_absolute_error(y, oof))
print("OOF R^2:", r2_score(y, oof))

# Baselines
mae_naive_zero = y.abs().mean()                               # always predict 0
mae_naive_yday = (y - df.loc[y.index, "ret"].values).abs().mean()  # predict yesterday's return
print("Naive(0) MAE:", mae_naive_zero)
print("Naive(yesterday) MAE:", mae_naive_yday)

# Directional accuracy (how often sign is correct)
dir_acc = (np.sign(oof) == np.sign(y)).mean()
print("Directional accuracy:", dir_acc)

# Fit final on all data
rf.fit(X, y)
