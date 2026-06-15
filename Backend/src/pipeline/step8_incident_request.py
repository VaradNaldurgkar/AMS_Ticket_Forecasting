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

MASTER_PATH = os.path.join(
    PROCESSED_DIR,
    "AMS_Ticket_Master.csv"
)

BREAKDOWN_OUTPUT = os.path.join(
    PROCESSED_DIR,
    "Incident_Type_Breakdown.csv"
)

MONTHLY_OUTPUT = os.path.join(
    PROCESSED_DIR,
    "Incident_Type_Monthly.csv"
)

# ========================================================
# STEP 1: LOAD MASTER DATASET
# ========================================================

if not os.path.exists(MASTER_PATH):
    raise FileNotFoundError(
        f"AMS_Ticket_Master.csv not found:\n{MASTER_PATH}"
    )

df = pd.read_csv(MASTER_PATH)

print("\n==================================================")
print("AMS MASTER DATA LOADED")
print("==================================================")

print(f"Total Records Loaded: {len(df)}")

# ========================================================
# STEP 2: DATE PROCESSING
# ========================================================

df["Reported_Date"] = pd.to_datetime(
    df["Reported_Date"],
    errors="coerce"
)

df = df[df["Reported_Date"].notna()]

print(
    "\nDate Range:",
    df["Reported_Date"].min(),
    "to",
    df["Reported_Date"].max()
)

# ========================================================
# STEP 3: FILTER TRAINING WINDOW
# ========================================================

TRAIN_START_DATE = "2024-01-01"

df = df[
    df["Reported_Date"] >= TRAIN_START_DATE
]

# ========================================================
# STEP 4: PUNE ONLY
# ========================================================

df = df[
    df["Location"] == "Pune"
].copy()

print(f"\nPune Records: {len(df)}")

# ========================================================
# STEP 5: KEEP ONLY INCIDENTS
# ========================================================

df = df[
    df["Ticket_Type"] == "Incident"
].copy()

print(f"Incident Records: {len(df)}")

# ========================================================
# STEP 6: REMOVE DUPLICATES
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
# STEP 7: VALIDATION
# ========================================================

print("\nResolve Group Distribution:\n")

print(
    df["Resolve Group"]
    .value_counts()
)

# ========================================================
# STEP 8: MONTH COLUMN
# ========================================================

df["Month"] = (
    df["Reported_Date"]
    .dt.to_period("M")
    .astype(str)
)

# ========================================================
# STEP 9: CLEAN TITLES
# ========================================================

df["Title"] = (
    df["Title"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.lower()
)

df = df[
    df["Title"] != ""
]

# ========================================================
# STEP 10: INCIDENT TYPE BREAKDOWN
# ========================================================

incident_breakdown = (
    df.groupby("Title")["Ticket_ID"]
      .nunique()
      .reset_index(name="Incident_Count")
      .sort_values(
          "Incident_Count",
          ascending=False
      )
)

# ========================================================
# STEP 11: PERCENTAGE
# ========================================================

total_incidents = (
    incident_breakdown["Incident_Count"]
    .sum()
)

incident_breakdown["Percentage"] = (
    incident_breakdown["Incident_Count"]
    / total_incidents
    * 100
).round(2)

incident_breakdown = (
    incident_breakdown
    .reset_index(drop=True)
)

# ========================================================
# STEP 12: MONTHLY INCIDENT BREAKDOWN
# ========================================================

monthly_breakdown = (
    df.groupby(
        ["Month", "Title"]
    )
    .size()
    .reset_index(name="Incident_Count")
    .sort_values(
        ["Month", "Incident_Count"],
        ascending=[True, False]
    )
)

# ========================================================
# STEP 13: SAVE FILES
# ========================================================

os.makedirs(
    PROCESSED_DIR,
    exist_ok=True
)

incident_breakdown.to_csv(
    BREAKDOWN_OUTPUT,
    index=False
)

monthly_breakdown.to_csv(
    MONTHLY_OUTPUT,
    index=False
)

# ========================================================
# STEP 14: FINAL OUTPUT
# ========================================================

print("\n==================================================")
print("INCIDENT TYPE BREAKDOWN CREATED")
print("==================================================")

print(f"\nBreakdown File:")
print(BREAKDOWN_OUTPUT)

print(f"\nMonthly Breakdown File:")
print(MONTHLY_OUTPUT)

print("\nTop 20 Incident Titles:\n")

print(
    incident_breakdown.head(20)
)

print(
    f"\nTotal Unique Incident Titles: "
    f"{len(incident_breakdown)}"
)

print(
    f"\nTotal Incident Records: "
    f"{total_incidents}"
)

print(
    f"\nLatest Month In Dataset: "
    f"{df['Month'].max()}"
)