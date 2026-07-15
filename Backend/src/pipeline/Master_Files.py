import os
import pandas as pd

# ==========================================================
# PATH
# ==========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(CURRENT_DIR)
)

FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw",
    "u_it_asset_report.xlsx"
)

print("=" * 100)
print("FILE PATH")
print(FILE)
print("Exists :", os.path.exists(FILE))
print("=" * 100)

# ==========================================================
# LOAD WORKBOOK
# ==========================================================

xls = pd.ExcelFile(FILE)

print("\nSHEETS FOUND")
print("-" * 100)

for sheet in xls.sheet_names:
    print(sheet)

# ==========================================================
# INSPECT EVERY HEADER
# ==========================================================

for sheet in xls.sheet_names:

    print("\n")
    print("=" * 100)
    print("SHEET :", sheet)
    print("=" * 100)

    for header in range(8):

        print("\n")
        print("-" * 60)
        print(f"HEADER = {header}")
        print("-" * 60)

        try:

            df = pd.read_excel(
                FILE,
                sheet_name=sheet,
                header=header,
                dtype=str
            )

            print("Rows :", len(df))
            print("Columns :", len(df.columns))

            print("\nCOLUMN NAMES\n")

            for i, col in enumerate(df.columns, start=1):
                print(f"{i:02d}. {col}")

            print("\nFIRST 5 ROWS\n")
            print(df.head())

            print("\nDATA TYPES\n")
            print(df.dtypes)

            print("\nNULL COUNT\n")
            print(df.isnull().sum())

        except Exception as e:

            print(e)

# ==========================================================
# SEARCH IMPORTANT COLUMNS
# ==========================================================

print("\n")
print("=" * 100)
print("SEARCHING FOR IMPORTANT COLUMNS")
print("=" * 100)

keywords = [
    "RITM",
    "Asset",
    "Asset List",
    "Requested",
    "Requester",
    "Created",
    "User",
    "Category",
    "Approval"
]

for sheet in xls.sheet_names:

    df = pd.read_excel(
        FILE,
        sheet_name=sheet,
        header=0,
        dtype=str
    )

    for col in df.columns:

        for key in keywords:

            if key.lower() in str(col).lower():
                print(col)

print("\n")
print("=" * 100)
print("END")
print("=" * 100)