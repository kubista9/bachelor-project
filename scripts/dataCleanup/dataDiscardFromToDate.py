# csv_date_range_filter.py
# pip install pandas

from pathlib import Path
import pandas as pd

#```
# Discards rows that are outside of START_DATE_STR to END_DATE_STR in fields TARGET_COLS, checks all csv files in INPUT_PATH
#```


# ========= EDIT THESE =========
INPUT_PATH = Path(r"data")     # file OR folder
RECURSIVE = True              # search subfolders if INPUT_PATH is a folder
OVERWRITE = True               # save back to same file; if False -> write *_filtered.csv
TARGET_COLS = ["date", "observation_date"]  # priority order
DROP_UNPARSABLE = True         # rows with invalid dates -> drop (treated as outside interval)

# Date window (inclusive)
START_DATE_STR = "2000-01-01"
END_DATE_STR   = "2025-08-30"  # "end at 2025 September"
# ==============================

START_DATE = pd.Timestamp(START_DATE_STR)
END_DATE   = pd.Timestamp(END_DATE_STR)

def find_date_col(df: pd.DataFrame) -> str | None:
    for c in TARGET_COLS:
        if c in df.columns:
            return c
    return None

def filter_by_date(csv_path: Path):
    try:
        df = pd.read_csv(csv_path, dtype=str)  # read everything as string to avoid surprises
    except Exception as e:
        print(f"[ERR] Read fail: {csv_path} -> {e}")
        return

    col = find_date_col(df)
    if not col:
        print(f"[SKIP] No date column ({TARGET_COLS}) in {csv_path.name}")
        return

    # Parse dates robustly
    parsed = pd.to_datetime(df[col], errors="coerce", utc=False, infer_datetime_format=True)

    # Build mask: inside [START_DATE, END_DATE]
    in_range = (parsed >= START_DATE) & (parsed <= END_DATE)

    if DROP_UNPARSABLE:
        keep_mask = in_range & parsed.notna()
    else:
        # Keep unparseable rows (treat as unknown), but still exclude definitively out-of-range
        keep_mask = in_range | parsed.isna()

    before = len(df)
    df_filtered = df[keep_mask].copy()
    after = len(df_filtered)

    if OVERWRITE:
        try:
            df_filtered.to_csv(csv_path, index=False)
            print(f"[OK]  {csv_path.name}: kept {after}/{before} rows "
                  f"({START_DATE_STR}..{END_DATE_STR})")
        except Exception as e:
            print(f"[ERR] Write fail: {csv_path} -> {e}")
    else:
        out_path = csv_path.with_name(f"{csv_path.stem}__filtered.csv")
        try:
            df_filtered.to_csv(out_path, index=False)
            print(f"[OK]  {out_path.name}: kept {after}/{before} rows "
                  f"({START_DATE_STR}..{END_DATE_STR})")
        except Exception as e:
            print(f"[ERR] Write fail: {out_path} -> {e}")

def main():
    p = INPUT_PATH.expanduser().resolve()
    if p.is_file():
        if p.suffix.lower() == ".csv":
            filter_by_date(p)
        else:
            print(f"[SKIP] Not a .csv file: {p}")
    elif p.is_dir():
        pattern = "**/*.csv" if RECURSIVE else "*.csv"
        files = list(p.glob(pattern))
        if not files:
            print(f"[INFO] No .csv files found in {p}")
        for fp in files:
            filter_by_date(fp)
    else:
        print(f"[ERR] Path not found: {p}")

if __name__ == "__main__":
    main()
