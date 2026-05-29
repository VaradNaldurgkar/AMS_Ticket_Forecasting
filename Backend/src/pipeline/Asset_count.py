import pandas as pd
import os

# -----------------------------
# Get project root dynamically
# -----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up 2 levels → Backend/
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "data"))

# Debug print (VERY important)
print("📁 Base Dir:", BASE_DIR)

asset_file = os.path.join(BASE_DIR, "raw", "u_it_asset_report.xlsx")
output_file = os.path.join(BASE_DIR, "processed", "Asset_Category_Count.csv")

print("📄 Asset File Path:", asset_file)

# -----------------------------
# Load Excel
# -----------------------------
df_assets = pd.read_excel(asset_file, engine="openpyxl")

asset_column = "Asset List"

# -----------------------------
# Cleaning
# -----------------------------
df_assets = df_assets[df_assets[asset_column].notna()]
df_assets[asset_column] = df_assets[asset_column].astype(str)

df_assets[asset_column] = df_assets[asset_column].str.replace(r'\s+', ' ', regex=True)
df_assets[asset_column] = df_assets[asset_column].str.replace(',+', ',', regex=True)

# -----------------------------
# Split
# -----------------------------
df_exploded = df_assets.assign(
    Category=df_assets[asset_column].str.split(",")
).explode("Category")

df_exploded["Category"] = df_exploded["Category"].str.strip()

df_exploded = df_exploded[
    (df_exploded["Category"] != "") &
    (df_exploded["Category"].notna())
]

df_exploded["Category"] = df_exploded["Category"].str.title()

df_exploded["Category"] = df_exploded["Category"].replace({
    "Accesories": "Accessories",
    "Key Board": "Keyboard",
    "Dongel": "Dongle"
})

# -----------------------------
# Count
# -----------------------------
category_count = (
    df_exploded["Category"]
    .value_counts()
    .reset_index()
)

category_count.columns = ["Asset Category", "Count"]

# -----------------------------
# Save
# -----------------------------
os.makedirs(os.path.join(BASE_DIR, "processed"), exist_ok=True)
category_count.to_csv(output_file, index=False)

print("\n✅ Output saved at:", output_file)
print(category_count.head(10))
