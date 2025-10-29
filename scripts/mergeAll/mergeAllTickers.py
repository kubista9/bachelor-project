from pathlib import Path
from typing import Iterable, Iterator
import pandas as pd
import re

# ```
# Stacks rows from many CSV files into one file.
# - Scans INPUT_PATH (file or folder) for CSV files.
# - Concatenates rows (union of columns), optionally adds source info, sorts/dedupes.
# - Writes a single CSV (or set OUTPUT_EXT=".xlsx" to write Excel).
# ```

# ========= EDIT THESE =========
INPUT_PATH = Path(r"data/indicators")        # file OR folder
RECURSIVE = True                  # search subfolders if INPUT_PATH is a folder
INCLUDE_PATTERNS = ["*.csv", "*.csv.gz"]  # which CSV extensions to include

ADD_SOURCE_COLUMNS = False         # add 'source_file' column
DROP_DUPLICATES = False           # drop fully-duplicate rows after merge
NATURAL_SORT_FILENAMES = True      #  e.g., file2 comes before file10

# Sort after merge (only if these columns exist). Leave [] to skip sorting.
SORT_BY = []
SORT_DATE_COLUMNS = ["date"]      # parsed as datetime for sorting
ASCENDING = True

# Output
OUTPUT_PATH = Path(r"data/indicators/merged.csv") # where to write the merged data
OUTPUT_EXT = ".csv"               # ".csv" or ".xlsx"
OUTPUT_SHEET_NAME = "merged"      # only used if OUTPUT_EXT == ".xlsx"
# ==============================


def iter_csv_files(base: Path, patterns: Iterable[str], recursive: bool) -> list[Path]:
    if base.is_file():
        return [base] if any(base.match(p) for p in patterns) else []
    if not base.exists():
        print(f"[ERR] Path not found: {base}")
        return []
    glob_base = "**/" if recursive else ""
    files: list[Path] = []
    for pat in patterns:
        files.extend(base.glob(f"{glob_base}{pat}"))
    files = [f for f in files if f.is_file()]
    if NATURAL_SORT_FILENAMES:
        def nkey(s: str):
            return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]
        files.sort(key=lambda p: nkey(str(p)))
    else:
        files.sort()
    return files


def read_csv(fp: Path) -> pd.DataFrame | None:
    """
    Read CSV with robust defaults, preserving row order.
    - dtype=str to avoid type drift across files
    - sep=None + engine='python' to auto-detect delimiter
    - on_bad_lines='skip' to skip malformed lines
    """
    try:
        df = pd.read_csv(fp, dtype=str, sep=None, engine="python", on_bad_lines="skip")
        if ADD_SOURCE_COLUMNS:
            df = df.copy()
            df.insert(len(df.columns), "source_file", fp.name)
        return df
    except Exception as e:
        print(f"[ERR] Failed to read: {fp} -> {e}")
        return None


def main():
    base = INPUT_PATH.expanduser().resolve()
    files = iter_csv_files(base, INCLUDE_PATTERNS, RECURSIVE)
    if not files:
        print(f"[INFO] No CSV files found in {base}")
        return

    chunks: list[pd.DataFrame] = []
    for fp in files:
        df = read_csv(fp)
        if df is None or df.empty:
            print(f"[WARN] Empty or unreadable CSV skipped: {fp.name}")
            continue
        chunks.append(df)
        print(f"[OK]  Loaded {len(df)} rows from {fp.name}")

    if not chunks:
        print("[INFO] Nothing to merge.")
        return

    merged = pd.concat(chunks, axis=0, ignore_index=True, sort=False)
    if DROP_DUPLICATES:
        before = len(merged)
        merged = merged.drop_duplicates(ignore_index=True)
        print(f"[INFO] Dropped duplicates: {before - len(merged)}")

    # Write output (extension decides format)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        if OUTPUT_PATH.suffix.lower() == ".xlsx":
            with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as w:
                merged.to_excel(w, index=False, sheet_name="merged")
        else:
            merged.to_csv(OUTPUT_PATH.with_suffix(".csv"), index=False)
        print(f"[DONE] Wrote {len(merged)} rows -> {OUTPUT_PATH}")
    except Exception as e:
        print(f"[ERR] Write fail: {OUTPUT_PATH} -> {e}")


if __name__ == "__main__":
    main()