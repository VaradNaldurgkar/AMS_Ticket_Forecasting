import pandas as pd
import glob
import os

# ========================================================
# STEP 0: PATH SETUP
# ========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# ========================================================
# STEP 1: LOAD ALL IM FILES
# ========================================================

im_files = glob.glob(
    os.path.join(RAW_DIR, "*IM*.xlsx")
)

if not im_files:
    raise FileNotFoundError(
        f"No IM files found in: {RAW_DIR}"
    )

df_im = pd.concat(
    [pd.read_excel(file) for file in im_files],
    ignore_index=True
)

# ========================================================
# STEP 2: CLEAN COLUMN NAMES
# ========================================================

df_im.columns = (
    df_im.columns
    .str.replace("\n", " ", regex=False)
    .str.strip()
)

# ========================================================
# STEP 3: ADD TICKET TYPE
# ========================================================

df_im["Ticket_Type"] = "Incident"

# ========================================================
# STEP 4: SELECT REQUIRED COLUMNS
# ========================================================

required_columns = [
    "Incident ID",
    "Title",
    "Open Time (Timezone based)",
    "Ticket_Type"
]

df_im = df_im[required_columns]

# ========================================================
# STEP 5: CONVERT DATE
# ========================================================

df_im["Open_Date"] = pd.to_datetime(
    df_im["Open Time (Timezone based)"],
    errors="coerce"
)

df_im = df_im[
    df_im["Open_Date"].notna()
]

# ========================================================
# STEP 6: FILTER DATE RANGE
# ========================================================

df_im = df_im[
    (df_im["Open_Date"] >= "2024-01-01") &
    (df_im["Open_Date"] <= "2026-03-31")
]

# ========================================================
# STEP 7: KEEP ONLY INCIDENTS
# ========================================================

df_im = df_im[
    df_im["Ticket_Type"] == "Incident"
].copy()

# ========================================================
# STEP 8: CLEAN TITLES
# ========================================================

df_im["Title"] = (
    df_im["Title"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

# ========================================================
# STEP 9: REMOVE DUPLICATES
# ========================================================

df_im = df_im.drop_duplicates(
    subset=["Incident ID"]
)

# ========================================================
# STEP 10: COUNT INCIDENT TYPES
# ========================================================

incident_breakdown = (
    df_im.groupby("Title")["Incident ID"]
    .nunique()
    .reset_index(name="Incident_Count")
    .sort_values(
        "Incident_Count",
        ascending=False
    )
)

# ========================================================
# STEP 11: SAVE OUTPUT
# ========================================================

os.makedirs(PROCESSED_DIR, exist_ok=True)

output_path = os.path.join(
    PROCESSED_DIR,
    "Incident_Type_Breakdown.csv"
)

incident_breakdown.to_csv(
    output_path,
    index=False
)

# ========================================================
# STEP 12: LOGS
# ========================================================

print("\n✅ Incident Type Breakdown created successfully")

print(f"✅ Saved to: {output_path}")

print("\nPreview:")

print(incident_breakdown.head(20))