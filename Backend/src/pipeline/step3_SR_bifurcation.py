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

INPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "AMS_Ticket_Master.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "SR_Breakdown.csv"
)

# ========================================================
# LOAD DATA
# ========================================================

df = pd.read_csv(INPUT_PATH)

print("\n==================================================")
print("AMS MASTER DATA LOADED")
print("==================================================")

print(f"Total Records Loaded: {len(df)}")

# ========================================================
# CLEAN DATA
# ========================================================

df.columns = df.columns.str.strip()

df["Ticket_Type"] = (
    df["Ticket_Type"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["Title"] = (
    df["Title"]
    .fillna("Unknown Request")
    .astype(str)
    .str.strip()
)

# ========================================================
# REMOVE DUPLICATES
# ========================================================

before_duplicates = len(df)

df = df.drop_duplicates()

after_duplicates = len(df)

print(f"\nDuplicates Removed: {before_duplicates - after_duplicates}")

# ========================================================
# FILTER ONLY SERVICE REQUESTS
# ========================================================

df_sr = df[
    df["Ticket_Type"]
    .str.lower() == "service request"
].copy()

print(f"\nTotal Service Requests: {len(df_sr)}")

# ========================================================
# GROUP + COUNT
# ========================================================

sr_breakdown = (
    df_sr.groupby("Title")
    .size()
    .reset_index(name="Service_Request_Count")
)

# ========================================================
# SORT DESCENDING
# ========================================================

sr_breakdown = sr_breakdown.sort_values(
    by="Service_Request_Count",
    ascending=False
)

# ========================================================
# ADD PERCENTAGE
# ========================================================

total_sr = sr_breakdown["Service_Request_Count"].sum()

sr_breakdown["Percentage"] = (
    sr_breakdown["Service_Request_Count"]
    / total_sr
    * 100
).round(2)

# ========================================================
# RESET INDEX
# ========================================================

sr_breakdown = sr_breakdown.reset_index(drop=True)

# ========================================================
# SAVE OUTPUT
# ========================================================

sr_breakdown.to_csv(
    OUTPUT_PATH,
    index=False
)

# ========================================================
# FINAL OUTPUT
# ========================================================

print("\n==================================================")
print("SERVICE REQUEST BIFURCATION CREATED")
print("==================================================")

print(f"Saved To: {OUTPUT_PATH}")

print("\nTop 10 Service Requests:\n")

print(sr_breakdown.head(10))