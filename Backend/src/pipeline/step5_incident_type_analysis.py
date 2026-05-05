import pandas as pd
import glob
import os

# ========================================================
# STEP 0: PATH SETUP (SAME AS AGGREGATION)
# ========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# ========================================================
# STEP 1: LOAD ALL FILES (2024 + 2025 + 2026)
# ========================================================

im_files = glob.glob(os.path.join(RAW_DIR, "*IM*.xlsx"))
rr_files = glob.glob(os.path.join(RAW_DIR, "*RR*.xlsx"))

if not im_files or not rr_files:
    raise FileNotFoundError(f"IM or RR files not found in {RAW_DIR}")

df_im = pd.concat([pd.read_excel(f) for f in im_files], ignore_index=True)
df_rr = pd.concat([pd.read_excel(f) for f in rr_files], ignore_index=True)

# ========================================================
# STEP 2: CLEAN COLUMN NAMES
# ========================================================

for df in (df_im, df_rr):
    df.columns = df.columns.str.replace("\n", " ", regex=False).str.strip()

# ========================================================
# STEP 3: STANDARDIZE RR COLUMNS
# ========================================================

df_rr = df_rr.rename(columns={
    "Request ID": "Incident ID",
    "Reported Time (Timezone based)": "Reported Date (Timezone based)",
    "Complexity": "Priority"
})

# ========================================================
# STEP 4: ADD TYPE
# ========================================================

df_im["Ticket_Type"] = "Incident"
df_rr["Ticket_Type"] = "Service Request"

# ========================================================
# STEP 5: SELECT REQUIRED COLUMNS
# ========================================================

required_columns = [
    "Incident ID",
    "Call Code",
    "Title",
    "Open Time (Timezone based)",
    "Ticket_Type"
]

df_im = df_im[required_columns]
df_rr = df_rr[required_columns]

# ========================================================
# STEP 6: COMBINE DATA
# ========================================================

df = pd.concat([df_im, df_rr], ignore_index=True)

# ========================================================
# STEP 7: OPEN TIME FILTER (IMPORTANT)
# ========================================================

df["Open_Date"] = pd.to_datetime(
    df["Open Time (Timezone based)"],
    errors="coerce"
)

df = df[df["Open_Date"].notna()]

df = df[
    (df["Open_Date"] >= "2024-01-01") &
    (df["Open_Date"] <= "2026-03-31")
]

# ========================================================
# STEP 8: KEEP ONLY INCIDENTS
# ========================================================

df = df[df["Ticket_Type"] == "Incident"].copy()

# ========================================================
# STEP 9: CLEAN TITLE + CATEGORY
# ========================================================

df["Title"] = df["Title"].fillna("").astype(str).str.lower()

def normalize_incident(title):
    if "citrix" in title:
        return "Citrix Issue"
    elif "laptop" in title:
        return "Laptop Issue"
    elif "vpn" in title:
        return "VPN Issue"
    elif "headset" in title:
        return "Headset Issue"
    elif "teams" in title:
        return "MS Teams Issue"
    elif "internet" in title:
        return "Internet Issue"
    elif "access" in title:
        return "Access Issue"
    else:
        return "Other"

df["Category"] = df["Title"].apply(normalize_incident)

# ========================================================
# STEP 10: CLEAN CALL CODE
# ========================================================

df["Call Code"] = (
    df["Call Code"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

# ========================================================
# STEP 11: REMOVE DUPLICATES (CRITICAL)
# ========================================================

df = df.drop_duplicates(subset=["Incident ID"])

# ========================================================
# STEP 12: COUNT INCIDENTS
# ========================================================

counts = (
    df.groupby(["Call Code", "Category"])["Incident ID"]
    .nunique()
    .reset_index(name="Count")
)

# ========================================================
# STEP 13: PERCENTAGE (WITHIN CATEGORY)
# ========================================================

category_totals = (
    counts.groupby("Category")["Count"]
    .sum()
    .reset_index(name="Category_Total")
)

final_df = counts.merge(category_totals, on="Category")

final_df["Percentage"] = (
    final_df["Count"] / final_df["Category_Total"] * 100
).round(2)

final_df = final_df[
    ["Call Code", "Category", "Count", "Percentage"]
].sort_values(
    ["Category", "Count"],
    ascending=[True, False]
)

# ========================================================
# STEP 14: SAVE OUTPUT
# ========================================================

os.makedirs(PROCESSED_DIR, exist_ok=True)

output_path = os.path.join(PROCESSED_DIR, "Incident_Call_Code_Breakdown.csv")

final_df.to_csv(output_path, index=False)

# ========================================================
# STEP 15: LOGS
# ========================================================

print("\n✅ Incident Call Code bifurcation created successfully")
print("✅ Date range: 2024-01 to 2026-03")
print(f"✅ Saved to: {output_path}")

print("\nPreview:")
print(final_df.head(10))