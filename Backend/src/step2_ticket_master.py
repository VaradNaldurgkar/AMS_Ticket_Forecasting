import pandas as pd
import os

# =========================================================
# STEP 0: FILE PATHS
# =========================================================

im_path = "data/raw/IM Raw Data Report April 25 to till  April 26.xlsx"
rr_path = "data/raw/RR RF Raw Data Report April 25 to till April 26.xlsx"

output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)

output_path = f"{output_dir}/AMS_Ticket_Master.csv"

# =========================================================
# STEP 1: LOAD RAW FILES
# =========================================================

df_im = pd.read_excel(im_path)
df_rr = pd.read_excel(rr_path)

# =========================================================
# STEP 2: CLEAN COLUMN NAMES
# =========================================================

for df in (df_im, df_rr):
    df.columns = df.columns.str.replace("\n", " ", regex=False).str.strip()

# =========================================================
# STEP 3: STANDARDIZE COLUMN NAMES
# =========================================================

df_im = df_im.rename(columns={
    "Incident ID": "Ticket_ID",
    "Reported Date (Timezone based)": "Reported_Date"
})

df_rr = df_rr.rename(columns={
    "Request ID": "Ticket_ID",
    "Reported Time (Timezone based)": "Reported_Date",
    "Complexity": "Priority"
})

# =========================================================
# STEP 4: ADD TICKET TYPE
# =========================================================

df_im["Ticket_Type"] = "Incident"
df_rr["Ticket_Type"] = "Service Request"

# =========================================================
# STEP 5: SELECT REQUIRED DASHBOARD COLUMNS
# =========================================================

columns_needed = [
    "Ticket_ID",
    "Ticket_Type",
    "Title",
    "Reported_Date",
    "Priority",
    "Call Code",
    "CI Location",
    "Open Time (Timezone based)",
    "Resolve Time (Timezone based)"
]

df_im = df_im[[c for c in columns_needed if c in df_im.columns]]
df_rr = df_rr[[c for c in columns_needed if c in df_rr.columns]]

# =========================================================
# STEP 6: COMBINE IM + RR (NO AGGREGATION)
# =========================================================

df = pd.concat([df_im, df_rr], ignore_index=True)

# =========================================================
# STEP 7: DATE ENRICHMENT & SAFE CLEANUP
# =========================================================

df["Reported_Date"] = pd.to_datetime(df["Reported_Date"], errors="coerce")
df["Month"] = df["Reported_Date"].dt.to_period("M").astype(str)

for col in ["Priority", "Call Code", "CI Location"]:
    if col not in df.columns:
        df[col] = "Unknown"
    else:
        df[col] = df[col].fillna("Unknown")

# =========================================================
# STEP 8: SAVE TICKET MASTER
# =========================================================

df.to_csv(output_path, index=False)

print(" AMS_Ticket_Master.csv created successfully")
print(" Path:", output_path)
print(" Total tickets:", len(df))
