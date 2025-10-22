# csv_dates_normalizer.py
# pip install pandas

from pathlib import Path
import pandas as pd


#```
# Matches target TARGET_COLS to DATE_FORMAT in INPUT_PATH folder
#```

# ========= EDIT THESE =========
INPUT_PATH = Path(r"data")  # file OR folder
RECURSIVE = True           # search subfolders if INPUT_PATH is a folder
OVERWRITE = True            # save changes back to the same file
TARGET_COLS = ["date", "observation_date"]  # columns to normalize if present
DATE_FORMAT = "%Y-%m-%d"    # desired output format
# ==============================

def normalize_date_column(df: pd.DataFrame, col: str) -> int:
    """
    Convert df[col] to YYYY-MM-DD where possible.
    Returns the number of rows that changed.
    """
    if col not in df.columns:
        return 0

    original = df[col].astype(str)

    # Try robust parsing: handles '1971-01-01 00:00:00', timezone, Excel serials, etc.
    parsed = pd.to_datetime(
        df[col],
        errors="coerce",  # invalid -> NaT
        utc=False,
        infer_datetime_format=True
    )

    # Format parsed dates; keep NaT as empty strings
    formatted = parsed.dt.strftime(DATE_FORMAT)
    # Where parsing failed (NaT), fall back to original value
    formatted = formatted.where(~parsed.isna(), other=original)

    # Count how many changed (only where we successfully parsed)
    changed_mask = (parsed.notna()) & (formatted != original)
    changed_count = int(changed_mask.sum())

    # Assign back
    df[col] = formatted
    return changed_count

def process_csv(csv_path: Path):
    try:
        df = pd.read_csv(csv_path, dtype=str)  # read as strings to avoid dtype surprises
    except Exception as e:
        print(f"[ERR] Failed to read {csv_path}: {e}")
        return

    total_changes = 0
    for col in TARGET_COLS:
        total_changes += normalize_date_column(df, col)

    if total_changes == 0:
        print(f"[OK]  {csv_path} (no date fields changed)")
        return

    if OVERWRITE:
        try:
            df.to_csv(csv_path, index=False)
            print(f"[OK]  {csv_path} (normalized {total_changes} date cells)")
        except Exception as e:
            print(f"[ERR] Failed to write {csv_path}: {e}")
    else:
        out_path = csv_path.with_name(f"{csv_path.stem}__normalized.csv")
        try:
            df.to_csv(out_path, index=False)
            print(f"[OK]  {out_path} (normalized {total_changes} date cells)")
        except Exception as e:
            print(f"[ERR] Failed to write {out_path}: {e}")

def main():
    p = INPUT_PATH.expanduser().resolve()
    if p.is_file():
        if p.suffix.lower() == ".csv":
            process_csv(p)
        else:
            print(f"[SKIP] Not a .csv file: {p}")
    elif p.is_dir():
        pattern = "**/*.csv" if RECURSIVE else "*.csv"
        files = list(p.glob(pattern))
        if not files:
            print(f"[INFO] No .csv files found in {p}")
        for fp in files:
            process_csv(fp)
    else:
        print(f"[ERR] Path not found: {p}")

if __name__ == "__main__":
    main()
