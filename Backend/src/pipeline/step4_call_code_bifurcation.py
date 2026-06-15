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

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

INPUT_PATH = os.path.join(
    PROCESSED_DIR,
    "AMS_Ticket_Master.csv"
)

OUTPUT_PATH = os.path.join(
    PROCESSED_DIR,
    "Call_Code_Breakdown.csv"
)

# ========================================================
# STEP 1: LOAD FILTERED MASTER DATA
# ========================================================

if not os.path.exists(INPUT_PATH):
    raise FileNotFoundError(
        f"AMS_Ticket_Master.csv not found: {INPUT_PATH}"
    )

df = pd.read_csv(INPUT_PATH)

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
# STEP 3: CLEAN CALL CODE
# ========================================================

if "Call Code" not in df.columns:
    raise ValueError(
        "Call Code column not found in AMS_Ticket_Master.csv"
    )

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
# STEP 4: REMOVE DUPLICATE TICKETS
# ========================================================

before_duplicates = len(df)

df = df.drop_duplicates(
    subset=["Ticket_ID"]
)

after_duplicates = len(df)

print(
    f"\nDuplicates Removed: "
    f"{before_duplicates - after_duplicates}"
)

# ========================================================
# STEP 5: VALIDATION
# ========================================================

print("\nTicket Type Distribution:")
print(
    df["Ticket_Type"]
    .value_counts()
)

print("\nResolve Group Distribution:")
print(
    df["Resolve Group"]
    .value_counts()
)

# ========================================================
# STEP 6: CALL CODE BREAKDOWN
# ========================================================

call_code_breakdown = (
    df.groupby("Call Code")["Ticket_ID"]
    .nunique()
    .reset_index(name="Ticket_Count")
    .sort_values(
        by="Ticket_Count",
        ascending=False
    )
)

# ========================================================
# STEP 7: ADD PERCENTAGE
# ========================================================

total_tickets = call_code_breakdown[
    "Ticket_Count"
].sum()

call_code_breakdown["Percentage"] = (
    call_code_breakdown["Ticket_Count"]
    / total_tickets
    * 100
).round(2)

call_code_breakdown = (
    call_code_breakdown
    .reset_index(drop=True)
)

# ========================================================
# STEP 8: SAVE OUTPUT
# ========================================================

os.makedirs(PROCESSED_DIR, exist_ok=True)

call_code_breakdown.to_csv(
    OUTPUT_PATH,
    index=False
)

# ========================================================
# STEP 9: FINAL OUTPUT
# ========================================================

print("\n==================================================")
print("CALL CODE BIFURCATION CREATED")
print("==================================================")

print(f"Saved To: {OUTPUT_PATH}")

print("\nTop 10 Call Codes:\n")
print(call_code_breakdown.head(10))