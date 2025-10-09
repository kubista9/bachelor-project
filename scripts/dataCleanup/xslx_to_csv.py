# xlsx_same_name_to_csv_in_code.py
# pip install pandas openpyxl

from pathlib import Path
import pandas as pd

# ========= EDIT THESE =========
INPUT_PATH = Path(r"data")  # file OR folder
FIRST_SHEET_ONLY = True   # True: only the first sheet -> <name>.csv
OVERWRITE = True          # False: skip if CSV already exists
INDEX = False             # include DataFrame index in CSV?
RECURSIVE = False         # if INPUT_PATH is a folder: search subfolders too
# ==============================

def sanitize(s: str) -> str:
    return "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in s).strip().replace(" ", "_")

def convert_one_file(xlsx_path: Path):
    if not xlsx_path.exists() or xlsx_path.suffix.lower() != ".xlsx":
        print(f"[SKIP] Not an .xlsx: {xlsx_path}")
        return

    if FIRST_SHEET_ONLY:
        out_csv = xlsx_path.with_suffix(".csv")  # same folder, same base name
        if out_csv.exists() and not OVERWRITE:
            print(f"[SKIP] Exists: {out_csv}")
            return
        df = pd.read_excel(xlsx_path, sheet_name=0, engine="openpyxl")
        df.to_csv(out_csv, index=INDEX)
        print(f"[OK]  {out_csv}")
    else:
        xl = pd.ExcelFile(xlsx_path, engine="openpyxl")
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            safe_sheet = sanitize(sheet)
            out_csv = xlsx_path.with_name(f"{xlsx_path.stem}__{safe_sheet}.csv")
            if out_csv.exists() and not OVERWRITE:
                print(f"[SKIP] Exists: {out_csv}")
                continue
            df.to_csv(out_csv, index=INDEX)
            print(f"[OK]  {out_csv}")

def main():
    p = INPUT_PATH.expanduser().resolve()
    if p.is_file():
        convert_one_file(p)
    elif p.is_dir():
        pattern = "**/*.xlsx" if RECURSIVE else "*.xlsx"
        files = list(p.glob(pattern))
        if not files:
            print(f"[INFO] No .xlsx files found in {p}")
        for fp in files:
            convert_one_file(fp)
    else:
        print(f"[ERR] Path not found: {p}")

if __name__ == "__main__":
    main()
