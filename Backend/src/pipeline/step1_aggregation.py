import pandas as pd
import os

# ========================================================
# STEP 0: RESOLVE PROJECT PATHS
# ========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

MASTER_PATH = os.path.join(
    PROCESSED_DIR,
    "AMS_Ticket_Master.csv"
)

OUTPUT_PATH = os.path.join(
    PROCESSED_DIR,
    "AMS_Yearly_Aggregated.csv"
)

# ========================================================
# STEP 1: LOAD FILTERED MASTER DATA
# ========================================================

if not os.path.exists(MASTER_PATH):
    raise FileNotFoundError(
        f"AMS_Ticket_Master.csv not found:\n{MASTER_PATH}"
    )

df = pd.read_csv(MASTER_PATH)

print("\n✅ Loaded AMS_Ticket_Master.csv")
print("✅ Records:", len(df))

# ========================================================
# STEP 2: DATE PROCESSING
# ========================================================

df["Reported_Date"] = pd.to_datetime(
    df["Reported_Date"],
    errors="coerce"
)

df = df[df["Reported_Date"].notna()]

print(
    "\nLatest date before filtering:",
    df["Reported_Date"].max()
)

# ========================================================
# STEP 3: FILTER DATE RANGE
# ========================================================

df = df[
    (df["Reported_Date"] >= "2024-01-01") &
    (df["Reported_Date"] <= "2026-04-30")
]

print(
    "Latest date after filtering:",
    df["Reported_Date"].max()
)

# ========================================================
# STEP 4: MONTH DERIVATION
# ========================================================

df["Month"] = (
    df["Reported_Date"]
    .dt.to_period("M")
    .astype(str)
)

# ========================================================
# STEP 5: USE LOCATION FROM MASTER FILE
# ========================================================

if "Location" not in df.columns:
    raise ValueError(
        "Location column not found in AMS_Ticket_Master.csv. "
        "Please regenerate AMS_Ticket_Master.csv using step2_ticket_master.py"
    )

df["Location"] = (
    df["Location"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

df["Location"] = df["Location"].replace(
    "",
    "Unknown"
)

print("\nLocation Distribution:")
print(df["Location"].value_counts().head(20))

print("\nTicket Type vs Location:")
print(
    pd.crosstab(
        df["Ticket_Type"],
        df["Location"]
    )
)

# ========================================================
# STEP 6: PRIORITY CLEANUP
# ========================================================

if "Priority" not in df.columns:
    df["Priority"] = "Unknown"

df["Priority"] = df["Priority"].fillna("Unknown")

# ========================================================
# STEP 7: MONTHLY AGGREGATION
# ========================================================

monthly_df = df.groupby(
    ["Month", "Location"],
    as_index=False
).agg(
    Total_Tickets=("Ticket_ID", "nunique"),

    Incidents=(
        "Ticket_Type",
        lambda x: (x == "Incident").sum()
    ),

    Service_Requests=(
        "Ticket_Type",
        lambda x: (x == "Service Request").sum()
    )
)

# ========================================================
# STEP 8: PRIORITY BREAKDOWN
# ========================================================

priority_df = df.pivot_table(
    index=["Month", "Location"],
    columns="Priority",
    values="Ticket_ID",
    aggfunc="nunique",
    fill_value=0
).reset_index()

priority_df.columns = [
    f"P{int(col)}"
    if isinstance(col, (int, float))
    else str(col)
    for col in priority_df.columns
]

monthly_df = monthly_df.merge(
    priority_df,
    on=["Month", "Location"],
    how="left"
)

# ========================================================
# STEP 9: SAVE OUTPUT
# ========================================================

os.makedirs(PROCESSED_DIR, exist_ok=True)

monthly_df.to_csv(
    OUTPUT_PATH,
    index=False
)

# ========================================================
# STEP 10: VALIDATION
# ========================================================

print("\n========== AGGREGATION SUMMARY ==========")

print(
    "Date range:",
    monthly_df["Month"].min(),
    "to",
    monthly_df["Month"].max()
)

print(
    "Locations:",
    monthly_df["Location"].nunique()
)

print(
    "Rows:",
    len(monthly_df)
)

print(
    "\nSample:"
)

print(monthly_df.head())

print("\n✅ Aggregation completed successfully")
print(f"✅ Saved to: {OUTPUT_PATH}")