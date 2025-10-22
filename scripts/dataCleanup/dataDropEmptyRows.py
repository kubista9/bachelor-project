# csv_drop_empty_rows.py
# pip install pandas

from pathlib import Path
import pandas as pd
import os
import sys

#```
# Drops empty rows
#```

# ========= EDIT THESE =========
INPUT_PATH = Path(r"data")     # file OR folder
RECURSIVE = True               # search subfolders if INPUT_PATH is a folder
OVERWRITE = True               # save back to same file; if False -> write *_clean.csv
OUTPUT_SUFFIX = "_clean"       # used only if OVERWRITE=False

# NEW: subfolders to ignore (names only, anywhere in the tree)
IGNORE_DIR_NAMES = {"indicators"}
IGNORE_CASE = True

# Treat these strings as empty/NA when deciding to drop rows (case-insensitive)
NA_LIKE_STRINGS = {"na", "n/a", "null", "none", "nan"}
STRIP_WHITESPACE = True        # strip leading/trailing whitespace in cells before checks
# ==============================


def normalize_na(df: pd.DataFrame) -> pd.DataFrame:
    """Make it easy to detect empty rows by turning blanks/NA-like strings into pd.NA."""
    # Keep empty strings as-is from the parser, then normalize:
    if STRIP_WHITESPACE:
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Empty strings -> NA
    df = df.replace({"": pd.NA})

    # NA-like tokens (case-insensitive) -> NA
    if NA_LIKE_STRINGS:
        pattern = r"(?i)^\s*(%s)\s*$" % "|".join(map(pd.re.escape, NA_LIKE_STRINGS))
        df = df.replace(pattern, pd.NA, regex=True)

    return df


def drop_empty_rows(csv_path: Path):
    try:
        # keep_default_na=False ensures empty fields arrive as "" (so we can control NA handling)
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    except Exception as e:
        print(f"[ERR] Read fail: {csv_path} -> {e}")
        return

    before_rows = len(df)
    if before_rows == 0:
        print(f"[OK]  {csv_path}: 0 rows (nothing to do)")
        return

    df = normalize_na(df)

    # Drop rows where *all* columns are NA/empty
    df = df.dropna(how="all")

    after_rows = len(df)
    removed = before_rows - after_rows

    # If we removed everything, still write a header-only CSV to avoid downstream surprises
    if OVERWRITE:
        df.to_csv(csv_path, index=False)
        print(f"[OK]  {csv_path}: kept {after_rows} rows (-{removed} empty)")
    else:
        out_path = csv_path.with_name(f"{csv_path.stem}{OUTPUT_SUFFIX}.csv")
        df.to_csv(out_path, index=False)
        print(f"[OK]  {out_path}: kept {after_rows} rows (-{removed} empty)")


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
                # prune ignored directories in-place so os.walk skips them
                dirs[:] = [d for d in dirs if not should_skip_dir(d)]
                for fname in files:
                    if fname.lower().endswith(".csv"):
                        drop_empty_rows(Path(root) / fname)
    else:
        print(f"[ERR] Path not found: {p}")


def main():
    # Allow optional path override: python csv_drop_empty_rows.py <path>
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
    else:
        target = INPUT_PATH
    process_path(target.expanduser().resolve())


if __name__ == "__main__":
    main()
