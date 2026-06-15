import pandas as pd
import os

# ========================================================
# PATH SETUP
# ========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

INPUT_PATH = os.path.join(
    PROCESSED_DIR,
    "AMS_Ticket_Master.csv"
)

OUTPUT_PATH = os.path.join(
    PROCESSED_DIR,
    "Service_Call_Code_Breakdown.csv"
)

# ========================================================
# LOAD DATA
# ========================================================

if not os.path.exists(INPUT_PATH):
    raise FileNotFoundError(
        f"AMS_Ticket_Master.csv not found:\n{INPUT_PATH}"
    )

df = pd.read_csv(INPUT_PATH)

print("\n==================================================")
print("AMS MASTER DATA LOADED")
print("==================================================")

print(f"Total Records Loaded: {len(df)}")

# ========================================================
# DATE FILTER
# ========================================================

df["Reported_Date"] = pd.to_datetime(
    df["Reported_Date"],
    errors="coerce"
)

df = df[df["Reported_Date"].notna()]

df = df[
    (df["Reported_Date"] >= "2024-01-01") &
    (df["Reported_Date"] <= "2026-04-30")
]

print(
    "\nDate Range:",
    df["Reported_Date"].min(),
    "to",
    df["Reported_Date"].max()
)

# ========================================================
# KEEP ONLY SERVICE REQUESTS
# ========================================================

df = df[
    df["Ticket_Type"] == "Service Request"
].copy()

print(
    "Service Request Records:",
    len(df)
)

# ========================================================
# CLEAN TITLE
# ========================================================

df["Title"] = (
    df["Title"]
    .fillna("")
    .astype(str)
    .str.lower()
    .str.strip()
)

# ========================================================
# CATEGORY NORMALIZATION
# ========================================================

def normalize_category(title):

    if "citrix" in title:
        return "Citrix"

    elif "laptop" in title:
        return "Laptop"

    elif "vpn" in title:
        return "VPN"

    elif "headset" in title:
        return "Headset"

    elif "teams" in title:
        return "MS Teams"

    elif "internet" in title or "wifi" in title:
        return "Internet/WiFi"

    elif "access" in title:
        return "Access"
    
    elif "application" in title:
        return "Application"

    elif "outlook" in title:
        return "Outlook"

    elif "security" in title:
        return "Security"

    else:
        return "Other"


# CREATE CATEGORY COLUMN
df["Category"] = df["Title"].apply(
    normalize_category
)
    
    

# ========================================================
# CLEAN CALL CODE
# ========================================================

df["Call Code"] = (
    df["Call Code"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

df["Call Code"] = df["Call Code"].replace(
    "",
    "Unknown"
)

# ========================================================
# REMOVE DUPLICATES
# ========================================================

before_duplicates = len(df)

df = df.drop_duplicates(
    subset=["Ticket_ID"]
)

after_duplicates = len(df)

print(
    f"Duplicates Removed: "
    f"{before_duplicates - after_duplicates}"
)

# ========================================================
# VALIDATION
# ========================================================

print("\nResolve Group Distribution:")

print(
    df["Resolve Group"]
    .value_counts()
)

# ========================================================
# COUNT BY CALL CODE + CATEGORY
# ========================================================

counts = (
    df.groupby(
        ["Call Code", "Category"]
    )["Ticket_ID"]
    .nunique()
    .reset_index(name="Count")
)

# ========================================================
# CATEGORY TOTALS
# ========================================================

category_totals = (
    counts.groupby("Category")["Count"]
    .sum()
    .reset_index(name="Category_Total")
)

# ========================================================
# PERCENTAGE CALCULATION
# ========================================================

final_df = counts.merge(
    category_totals,
    on="Category"
)

final_df["Percentage"] = (
    final_df["Count"]
    / final_df["Category_Total"]
    * 100
).round(2)

# ========================================================
# FINAL FORMAT
# ========================================================

final_df = final_df[
    [
        "Call Code",
        "Category",
        "Count",
        "Percentage"
    ]
].sort_values(
    ["Category", "Count"],
    ascending=[True, False]
)

# ========================================================
# SAVE OUTPUT
# ========================================================

final_df.to_csv(
    OUTPUT_PATH,
    index=False
)

# ========================================================
# LOGS
# ========================================================

print("\n==================================================")
print("SERVICE CALL CODE BIFURCATION CREATED")
print("==================================================")

print(f"Saved To: {OUTPUT_PATH}")

print("\nPreview:\n")
print(final_df.head(20))