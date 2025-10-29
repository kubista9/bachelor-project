# csv_merge_into_base_by_date_autofolder.py
# pip install pandas

from pathlib import Path
from typing import Optional, Iterable
import pandas as pd
import os
import re

# ========= EDIT THESE =========
# Base file to merge into
BASE_CSV = Path(r"data/indicators/merged.csv")

# Folder containing CSVs to add
INPUT_DIR = Path(r"data/fred")
RECURSIVE = False
INCLUDE_PATTERNS: list[str] = ["*.csv", "*.csv.gz"]  # add "*.txt" if needed
EXCLUDE_NAMES: set[str] = set()  # e.g. {"readme.csv"}

# Join keys
DATE_COL = "date"                        # canonical date column
TICKER_COL: Optional[str] = None         # set to "ticker" to merge on (date, ticker)

# Join behavior
JOIN_HOW = "left"                        # "left" or "inner"

# Column handling
ADD_PREFIX = True                        # prefix columns from each file
FILE_ALIASES: dict[str, str] = {}        # optional overrides: {"BAA10Y_Spread.csv": "baa10y"}
DROP_DUPLICATE_COLUMNS = True

# CSV read options
READ_KW = dict(dtype=str, sep=None, engine="python", on_bad_lines="skip")

# Output
OUTPUT_PATH = Path(r"data/merged_withIndicators.csv")
# ==============================

# Common date column aliases (case-insensitive)
DATE_ALIASES = {"date", "DATE", "observation_date", "time", "timestamp"}

def read_csv_robust(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path, **READ_KW)
    except Exception as e:
        raise RuntimeError(f"Failed to read {path}: {e}")

def normalize_date_series(s: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(s, errors="coerce", utc=False)
    return parsed.dt.strftime("%Y-%m-%d")

def alias_for(path: Path) -> str:
    name = path.name
    if name in FILE_ALIASES:
        return FILE_ALIASES[name]
    return path.stem

def coerce_date_column(df: pd.DataFrame, where: str) -> pd.DataFrame:
    if DATE_COL in df.columns:
        return df
    lower_map = {c.lower(): c for c in df.columns}
    for a in DATE_ALIASES:
        if a.lower() in lower_map:
            real = lower_map[a.lower()]
            if real != DATE_COL:
                df = df.rename(columns={real: DATE_COL})
            return df
    raise ValueError(
        f"Missing date column in {where}. Looked for {DATE_COL} or aliases {sorted(DATE_ALIASES)}. "
        f"Available: {list(df.columns)}"
    )

def drop_identical_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    seen = {}
    to_drop = []
    for col in df.columns:
        sig = (tuple(pd.isna(df[col])), tuple(df[col].fillna("__NA__")))
        if sig in seen:
            to_drop.append(col)
        else:
            seen[sig] = col
    if to_drop:
        df = df.drop(columns=to_drop)
        print(f"[INFO] Dropped {len(to_drop)} duplicate column(s): {to_drop}")
    return df

def merge_one(base: pd.DataFrame, add_df: pd.DataFrame, merge_on: list[str], alias: str) -> pd.DataFrame:
    right_cols = [c for c in add_df.columns if c not in merge_on]
    if ADD_PREFIX:
        add_df = add_df.rename(columns={c: f"{alias}__{c}" for c in right_cols})
        right_cols = [f"{alias}__{c}" for c in right_cols]
    add_view = add_df[merge_on + right_cols]
    return base.merge(add_view, on=merge_on, how=JOIN_HOW, copy=False)

def natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

def list_input_csvs(folder: Path, patterns: Iterable[str], recursive: bool) -> list[Path]:
    if not folder.exists():
        print(f"[ERR] Input folder not found: {folder}")
        return []
    files: list[Path] = []
    for pat in patterns:
        files += list(folder.rglob(pat) if recursive else folder.glob(pat))
    # keep files only, unique, sorted naturally
    uniq = sorted({p.resolve() for p in files if p.is_file()}, key=lambda p: natural_key(str(p)))
    return uniq

def main():
    print("[INFO] CWD =", os.getcwd())

    # Load and normalize base
    base = read_csv_robust(BASE_CSV)
    base = coerce_date_column(base, f"BASE_CSV ({BASE_CSV})").copy()
    base[DATE_COL] = normalize_date_series(base[DATE_COL])

    base_has_ticker = TICKER_COL is not None and TICKER_COL in base.columns
    if base_has_ticker:
        base[TICKER_COL] = base[TICKER_COL].astype(str)

    print(f"[OK]  Loaded base: {BASE_CSV} with {len(base)} rows and {base.shape[1]} cols")

    # Build file list from folder
    candidates = list_input_csvs(INPUT_DIR, INCLUDE_PATTERNS, RECURSIVE)

    # Skip base/output files and any excluded names
    skip_set = {
        BASE_CSV.resolve(),
        OUTPUT_PATH.resolve(),
        OUTPUT_PATH.with_suffix(".csv").resolve(),
        OUTPUT_PATH.with_suffix(".csv.gz").resolve(),
    }
    files = []
    for p in candidates:
        if p in skip_set:
            continue
        if p.name in EXCLUDE_NAMES:
            continue
        files.append(p)

    if not files:
        print(f"[INFO] No CSV files found to merge in {INPUT_DIR}")
        return

    print("[INFO] Files to merge:")
    for p in files:
        print("  -", p)

    # Merge each file
    for path in files:
        add_df = read_csv_robust(path)
        add_df = coerce_date_column(add_df, f"{path}").copy()
        add_df[DATE_COL] = normalize_date_series(add_df[DATE_COL])

        # decide merge keys for this file
        add_has_ticker = base_has_ticker and (TICKER_COL in add_df.columns)
        if add_has_ticker:
            add_df[TICKER_COL] = add_df[TICKER_COL].astype(str)
            merge_on = [DATE_COL, TICKER_COL]
        else:
            merge_on = [DATE_COL]
            if base_has_ticker and TICKER_COL not in add_df.columns:
                print(f"[INFO] '{path.name}' has no '{TICKER_COL}'. Merging on date only.")

        add_df = add_df.drop_duplicates()
        before_cols = base.shape[1]
        al = alias_for(path)
        base = merge_one(base, add_df, merge_on, al)
        print(f"[OK]  Merged {path.name} as '{al}' (+{base.shape[1] - before_cols} cols) on {merge_on}")

    if DROP_DUPLICATE_COLUMNS:
        base = drop_identical_duplicate_columns(base)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    base.to_csv(OUTPUT_PATH, index=False)
    print(f"[DONE] Wrote: {OUTPUT_PATH} with {len(base)} rows, {base.shape[1]} cols")

if __name__ == "__main__":
    main()
