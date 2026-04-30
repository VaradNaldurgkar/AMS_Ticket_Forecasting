import pandas as pd
import glob
import os

# ========================================================
# STEP 0: RESOLVE PROJECT ROOT & RAW DATA PATH
# ========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# Load all IM and RR files
im_files = glob.glob(os.path.join(RAW_DIR, "*IM*.xlsx"))
rr_files = glob.glob(os.path.join(RAW_DIR, "*RR*.xlsx"))

if not im_files or not rr_files:
    raise FileNotFoundError(f"IM or RR raw files not found in {RAW_DIR}")

df_im = pd.concat([pd.read_excel(f) for f in im_files], ignore_index=True)
df_rr = pd.concat([pd.read_excel(f) for f in rr_files], ignore_index=True)

# ========================================================
# STEP 1: CLEAN COLUMN NAMES
# ========================================================

for df in (df_im, df_rr):
    df.columns = (
        df.columns
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )

# ========================================================
# STEP 2: STANDARDIZE RR COLUMN NAMES
# ========================================================

df_rr = df_rr.rename(columns={
    "Request ID": "Incident ID",
    "Reported Time (Timezone based)": "Reported Date (Timezone based)",
    "Complexity": "Priority"
})

# ========================================================
# STEP 3: ADD TICKET TYPE
# ========================================================

df_im["Ticket_Type"] = "Incident"
df_rr["Ticket_Type"] = "Service Request"

# ========================================================
# STEP 4: SELECT REQUIRED COMMON COLUMNS
# ========================================================

required_columns = [
    "Incident ID",
    "Priority",
    "Reported Date (Timezone based)",
    "Open Time (Timezone based)",
    "CI Location",
    "CI Location.1",
    "Ticket_Type"
]

df_im = df_im[required_columns]
df_rr = df_rr[required_columns]

# ========================================================
# STEP 5: COMBINE IM + RR DATA
# ========================================================

df = pd.concat([df_im, df_rr], ignore_index=True)

# ========================================================
# STEP 6: DATE DERIVATION (ROBUST)
# ========================================================

df["Reported_Date"] = pd.to_datetime(
    df["Reported Date (Timezone based)"],
    errors="coerce"
)

df["Reported_Date"] = df["Reported_Date"].fillna(
    pd.to_datetime(df["Open Time (Timezone based)"], errors="coerce")
)

# ========================================================
# STEP 7: FILTER DATE RANGE (2024 → MAR 2026) ✅✅✅
# ========================================================

df = df[
    (df["Reported_Date"] >= "2024-01-01") &
    (df["Reported_Date"] <= "2026-03-31")
]

# ========================================================
# STEP 8: MONTH DERIVATION
# ========================================================

df["Month"] = df["Reported_Date"].dt.to_period("M").astype(str)

# ========================================================
# STEP 9: LOCATION DERIVATION
# ========================================================

df["Location"] = df["CI Location"]

df["Location"] = df["Location"].where(
    df["Location"].notna() & (df["Location"].str.strip() != ""),
    df["CI Location.1"]
)

df["Location"] = df["Location"].fillna("Unknown")

# ========================================================
# STEP 10: MONTHLY AGGREGATION
# ========================================================

monthly_df = df.groupby(["Month", "Location"], as_index=False).agg(
    Total_Tickets=("Incident ID", "count"),
    Incidents=("Ticket_Type", lambda x: (x == "Incident").sum()),
    Service_Requests=("Ticket_Type", lambda x: (x == "Service Request").sum())
)

monthly_df = monthly_df.sort_values(by=["Month", "Location"])

# ========================================================
# STEP 11: PRIORITY BREAKDOWN
# ========================================================

priority_df = df.pivot_table(
    index=["Month", "Location"],
    columns="Priority",
    values="Incident ID",
    aggfunc="count",
    fill_value=0
).reset_index()

priority_df.columns = [
    f"P{int(col)}" if isinstance(col, (int, float)) else col
    for col in priority_df.columns
]

monthly_df = monthly_df.merge(
    priority_df,
    on=["Month", "Location"],
    how="left"
)

# ========================================================
# STEP 12: SAVE OUTPUT
# ========================================================

os.makedirs(PROCESSED_DIR, exist_ok=True)
output_path = os.path.join(PROCESSED_DIR, "AMS_Yearly_Aggregated.csv")

monthly_df.to_csv(output_path, index=False)

print("\n✅ Aggregation completed successfully")
print("✅ Date range:", monthly_df["Month"].min(), "to", monthly_df["Month"].max())
print(f"✅ Saved to: {output_path}")
