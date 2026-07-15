import pandas as pd
import os

# =====================================================
# PATHS
# =====================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.abspath(
    os.path.join(
        CURRENT_DIR,
        "..",
        "..",
        "data"
    )
)

MASTER_FILE = os.path.join(
    BASE_DIR,
    "Master",
    "master_assets.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "processed",
    "Asset_Category_Count.csv"
)

print("\n========================================")
print("ASSET CATEGORY PIPELINE")
print("========================================")
print("Master File :", MASTER_FILE)
print("Output File :", OUTPUT_FILE)
print("========================================\n")

# =====================================================
# LOAD MASTER CSV
# =====================================================

if not os.path.exists(MASTER_FILE):
    raise FileNotFoundError(
        f"Master Asset CSV not found:\n{MASTER_FILE}"
    )

df_assets = pd.read_csv(
    MASTER_FILE,
    dtype=str,
    low_memory=False
)

print("Rows Loaded :", len(df_assets))

# =====================================================
# DATE
# =====================================================

df_assets["Created"] = pd.to_datetime(
    df_assets["Created"],
    errors="coerce"
)

df_assets = df_assets[
    df_assets["Created"].notna()
]

df_assets["Year"] = df_assets["Created"].dt.year

print("\n========== YEAR DISTRIBUTION ==========")
print(df_assets["Year"].value_counts().sort_index())

# =====================================================
# ASSET LIST CLEANING
# =====================================================

ASSET_COLUMN = "Asset List"

df_assets = df_assets[
    df_assets[ASSET_COLUMN].notna()
].copy()

df_assets[ASSET_COLUMN] = (
    df_assets[ASSET_COLUMN]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.replace(r",+", ",", regex=True)
    .str.strip()
)

# =====================================================
# SPLIT MULTIPLE ASSETS
# =====================================================

df_assets["Category"] = (
    df_assets[ASSET_COLUMN]
    .str.split(",")
)

df_assets = df_assets.explode("Category")

df_assets["Category"] = (
    df_assets["Category"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df_assets = df_assets[
    df_assets["Category"] != ""
]

# =====================================================
# STANDARDIZE NAMES
# =====================================================

df_assets["Category"] = (
    df_assets["Category"]
    .str.title()
)

df_assets["Category"] = df_assets["Category"].replace({

    "Accesories": "Accessories",

    "Key Board": "Keyboard",

    "Dongel": "Dongle"

})

# =====================================================
# COUNT
# =====================================================

category_count = (

    df_assets

    .groupby(
        ["Year", "Category"]
    )

    .size()

    .reset_index(name="Count")

)

category_count.rename(

    columns={

        "Category": "Asset Category"

    },

    inplace=True

)

category_count = category_count.sort_values(

    by=["Year", "Count"],

    ascending=[True, False]

)

# =====================================================
# SAVE
# =====================================================

os.makedirs(

    os.path.join(BASE_DIR, "processed"),

    exist_ok=True

)

category_count.to_csv(

    OUTPUT_FILE,

    index=False

)

print("\n========================================")
print("ASSET CATEGORY SUMMARY")
print("========================================")
print("Total Records :", len(category_count))
print(category_count.head(20))
print("\nSaved :", OUTPUT_FILE)
print("========================================")