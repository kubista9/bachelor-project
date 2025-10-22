# csv_last_value_fill_daily_ignore_dirs.py
# pip install pandas

from pathlib import Path
import pandas as pd
import os

#```
# Fills up missing days with last known data from last date
#```

# ========= EDIT THESE =========
INPUT_PATH = Path(r"data")     # file OR folder
RECURSIVE = True               # search subfolders if INPUT_PATH is a folder
OVERWRITE = True               # save back to same file; if False -> write *_filled.csv
DATE_CANDIDATES = ["date", "observation_date"]  # columns to try for the date
OUTPUT_SUFFIX = "_filled"      # used only if OVERWRITE=False
FREQUENCY = "D"                # "D" for daily; e.g., "MS" for monthly expansion
NORMALIZE_TO_DATE = True       # drop time-of-day; keep only YYYY-MM-DD

# Optional bounds (leave as None to use min/max from file)
START_DATE_STR = None          # e.g., "2000-01-01"
END_DATE_STR   = None          # e.g., "2025-09-30"

# NEW: subfolders to ignore (names only, anywhere in the tree)
IGNORE_DIR_NAMES = {"indicators"}
IGNORE_CASE = True
# ==============================

START_DATE = pd.to_datetime(START_DATE_STR) if START_DATE_STR else None
END_DATE   = pd.to_datetime(END_DATE_STR)   if END_DATE_STR else None

def find_date_col(df: pd.DataFrame) -> str | None:
    for c in DATE_CANDIDATES:
        if c in df.columns:
            return c
    return None

def to_dateonly(s: pd.Series) -> pd.Series:
    """Parse a series to datetime and optionally normalize to date (drop time)."""
    dt = pd.to_datetime(s, errors="coerce", utc=False, infer_datetime_format=True)
    if NORMALIZE_TO_DATE:
        dt = dt.dt.normalize()
    return dt

def expand_and_ffill(csv_path: Path):
    try:
        df = pd.read_csv(csv_path, dtype=str)
    except Exception as e:
        print(f"[ERR] Read fail: {csv_path} -> {e}")
        return

    date_col = find_date_col(df)
    if not date_col:
        print(f"[SKIP] No date column ({DATE_CANDIDATES}) in {csv_path.name}")
        return

    dt = to_dateonly(df[date_col])
    good = dt.notna()
    if not good.any():
        print(f"[SKIP] All dates unparsable in {csv_path.name}")
        return

    df = df.loc[good].copy()
    dt = dt.loc[good]

    df.index = dt
    df.drop(columns=[date_col], inplace=True)

    if START_DATE is not None:
        df = df[df.index >= START_DATE]
    if END_DATE is not None:
        df = df[df.index <= END_DATE]
    if df.empty:
        print(f"[SKIP] No rows within bounds in {csv_path.name}")
        return

    df = df[~df.index.duplicated(keep="last")].sort_index()

    start = df.index.min() if START_DATE is None else max(df.index.min(), START_DATE)
    end   = df.index.max() if END_DATE   is None else min(df.index.max(), END_DATE)
    full_idx = pd.date_range(start=start, end=end, freq=FREQUENCY)

    before = len(df)
    df = df.reindex(full_idx)
    df = df.ffill()  # carry last known value forward

    out = df.copy()
    out.insert(0, date_col, out.index.strftime("%Y-%m-%d"))
    out.reset_index(drop=True, inplace=True)

    added = len(out) - before

    if OVERWRITE:
        out.to_csv(csv_path, index=False)
        print(f"[OK]  {csv_path}: expanded to {len(out)} rows (+{added}), daily ffill")
    else:
        out_path = csv_path.with_name(f"{csv_path.stem}{OUTPUT_SUFFIX}.csv")
        out.to_csv(out_path, index=False)
        print(f"[OK]  {out_path}: expanded to {len(out)} rows (+{added}), daily ffill")

def should_skip_dir(name: str) -> bool:
    if not IGNORE_DIR_NAMES:
        return False
    if IGNORE_CASE:
        return name.lower() in {d.lower() for d in IGNORE_DIR_NAMES}
    return name in IGNORE_DIR_NAMES

def process_path(p: Path):
    if p.is_file():
        if p.suffix.lower() == ".csv":
            expand_and_ffill(p)
        else:
            print(f"[SKIP] Not a .csv file: {p}")
    elif p.is_dir():
        if not RECURSIVE:
            # top-level only
            for fp in p.glob("*.csv"):
                expand_and_ffill(fp)
        else:
            # walk and prune ignored directories
            for root, dirs, files in os.walk(p):
                # prune dirs in-place so os.walk skips them
                dirs[:] = [d for d in dirs if not should_skip_dir(d)]
                for fname in files:
                    if fname.lower().endswith(".csv"):
                        expand_and_ffill(Path(root) / fname)
    else:
        print(f"[ERR] Path not found: {p}")

def main():
    process_path(INPUT_PATH.expanduser().resolve())

if __name__ == "__main__":
    main()
