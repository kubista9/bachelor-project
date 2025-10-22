# csv_drop_empty_rows.py
# pip install pandas

from pathlib import Path
import pandas as pd
import os
import sys
import re   # <-- NEW

#```
# Drops empty rows
#```

# ========= EDIT THESE =========
INPUT_PATH = Path(r"data")     # file OR folder
RECURSIVE = True               # search subfolders if INPUT_PATH is a folder
OVERWRITE = True               # save back to same file; if False -> write *_clean.csv
OUTPUT_SUFFIX = "_clean"       # used only if OVERWRITE=False

# NEW: subfolders to ignore (names only, anywhere in the tree)
IGNORE_DIR_NAMES = {"indicators","ticker data","tickers",}
IGNORE_CASE = True

# Treat these strings as empty/NA when deciding to drop rows (case-insensitive)
NA_LIKE_STRINGS = {"na", "n/a", "null", "none", "nan"}
STRIP_WHITESPACE = True        # strip leading/trailing whitespace in cells before checks

# Drop policy
# If None -> check ALL columns. Or set e.g. {"date", "value"} to check specific columns.
COLUMNS_TO_CHECK: set[str] | None = None
# ==============================


def normalize_na(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize blanks/NA-like tokens to pd.NA so we can drop rows reliably."""
    if STRIP_WHITESPACE:
        obj = df.select_dtypes(include="object")
        if not obj.empty:
            df[obj.columns] = obj.apply(lambda s: s.str.strip())

    # Empty strings -> NA
    df = df.replace({"": pd.NA})

    # NA-like tokens (case-insensitive) -> NA
    if NA_LIKE_STRINGS:
        escaped = [re.escape(s) for s in NA_LIKE_STRINGS]
        regex = re.compile(rf"^\s*(?:{'|'.join(escaped)})\s*$", re.IGNORECASE)
        df = df.replace(regex, pd.NA)

    return df


def drop_empty_rows(csv_path: Path):
    try:
        # keep_default_na=False keeps blanks as "" so we control NA handling ourselves
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    except Exception as e:
        print(f"[ERR] Read fail: {csv_path} -> {e}")
        return

    before_rows = len(df)
    if before_rows == 0:
        print(f"[OK]  {csv_path}: 0 rows (nothing to do)")
        return

    df = normalize_na(df)

    # -------- NEW BEHAVIOR: drop if ANY checked column is empty --------
    if COLUMNS_TO_CHECK:
        missing_cols = [c for c in COLUMNS_TO_CHECK if c not in df.columns]
        if missing_cols:
            print(f"[WARN] {csv_path}: columns not found and ignored: {missing_cols}")
        cols = [c for c in COLUMNS_TO_CHECK if c in df.columns]
        if cols:
            mask_any_empty = df[cols].isna().any(axis=1)
        else:
            mask_any_empty = pd.Series(False, index=df.index)
    else:
        # Check all columns
        mask_any_empty = df.isna().any(axis=1)

    df = df.loc[~mask_any_empty].copy()
    # -------------------------------------------------------------------

    after_rows = len(df)
    removed = before_rows - after_rows

    if OVERWRITE:
        df.to_csv(csv_path, index=False)
        print(f"[OK]  {csv_path}: kept {after_rows} rows (-{removed} with empties)")
    else:
        out_path = csv_path.with_name(f"{csv_path.stem}{OUTPUT_SUFFIX}.csv")
        df.to_csv(out_path, index=False)
        print(f"[OK]  {out_path}: kept {after_rows} rows (-{removed} with empties)")


def should_skip_dir(name: str) -> bool:
    if not IGNORE_DIR_NAMES:
        return False
    if IGNORE_CASE:
        return name.lower() in {d.lower() for d in IGNORE_DIR_NAMES}
    return name in IGNORE_DIR_NAMES


def process_path(p: Path):
    if p.is_file():
        if p.suffix.lower() == ".csv":
            drop_empty_rows(p)
        else:
            print(f"[SKIP] Not a .csv file: {p}")
    elif p.is_dir():
        if not RECURSIVE:
            for fp in p.glob("*.csv"):
                drop_empty_rows(fp)
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if not should_skip_dir(d)]
                for fname in files:
                    if fname.lower().endswith(".csv"):
                        drop_empty_rows(Path(root) / fname)
    else:
        print(f"[ERR] Path not found: {p}")


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_PATH
    process_path(target.expanduser().resolve())


if __name__ == "__main__":
    main()