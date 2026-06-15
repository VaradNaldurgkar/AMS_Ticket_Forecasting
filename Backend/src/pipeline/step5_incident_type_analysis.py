import pandas as pd
import os

# ========================================================
# STEP 0: PATH SETUP
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
    "Incident_Call_Code_Breakdown.csv"
)

# ========================================================
# STEP 1: LOAD FILTERED MASTER DATA
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
# STEP 2: DATE FILTER
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
# STEP 3: KEEP ONLY INCIDENTS
# ========================================================

df = df[
    df["Ticket_Type"] == "Incident"
].copy()

print(
    "Incident Records:",
    len(df)
)

# ========================================================
# STEP 4: CLEAN TITLE
# ========================================================

df["Title"] = (
    df["Title"]
    .fillna("")
    .astype(str)
    .str.lower()
    .str.strip()
)

# ========================================================
# STEP 5: INCIDENT CATEGORIZATION
# ========================================================
def normalize_incident(title):
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
    elif "internet" in title or "wifi" in title or "wi-fi" in title:
        return "Internet/WiFi"
    elif "access" in title:
        return "Access"
    elif "outlook" in title:
        return "Outlook"
    elif (
        "application" in title
        or "software" in title
        or "install" in title
        or "uninstall" in title
    ):
        return "Application"
    elif (
        "authentication" in title
        or "certificate" in title
        or "pki" in title
    ):
        return "Security"
    else:
        return "Other"
    
df["Category"] = df["Title"].apply(normalize_incident)

# ========================================================
# STEP 6: CLEAN CALL CODE
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
# STEP 7: REMOVE DUPLICATES
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
# STEP 8: VALIDATION
# ========================================================

print("\nResolve Group Distribution:")

print(
    df["Resolve Group"]
    .value_counts()
)

# ========================================================
# STEP 9: INCIDENT BREAKDOWN
# ========================================================

counts = (
    df.groupby(
        ["Call Code", "Category"]
    )["Ticket_ID"]
    .nunique()
    .reset_index(name="Count")
)

# ========================================================
# STEP 10: CATEGORY PERCENTAGE
# ========================================================

category_totals = (
    counts.groupby("Category")["Count"]
    .sum()
    .reset_index(name="Category_Total")
)

final_df = counts.merge(
    category_totals,
    on="Category"
)

final_df["Percentage"] = (
    final_df["Count"]
    / final_df["Category_Total"]
    * 100
).round(2)

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
# STEP 11: SAVE OUTPUT
# ========================================================

os.makedirs(
    PROCESSED_DIR,
    exist_ok=True
)

final_df.to_csv(
    OUTPUT_PATH,
    index=False
)

# ========================================================
# STEP 12: LOGS
# ========================================================

print("\n==================================================")
print("INCIDENT CALL CODE BIFURCATION CREATED")
print("==================================================")

print(f"Saved To: {OUTPUT_PATH}")

print("\nPreview:\n")
print(final_df.head(20))