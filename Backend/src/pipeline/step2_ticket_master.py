import pandas as pd
import glob
import os

# =========================================================
# STEP 0: RESOLVE PROJECT PATHS ✅
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

output_path = os.path.join(PROCESSED_DIR, "AMS_Ticket_Master.csv")

# =========================================================
# STEP 1: LOAD ALL RAW FILES (2024 + 2025) ✅
# =========================================================

im_files = glob.glob(os.path.join(RAW_DIR, "*IM*.xlsx"))
rr_files = glob.glob(os.path.join(RAW_DIR, "*RR*.xlsx"))

if not im_files or not rr_files:
    raise FileNotFoundError("IM or RR raw files not found")

df_im = pd.concat([pd.read_excel(f) for f in im_files], ignore_index=True)
df_rr = pd.concat([pd.read_excel(f) for f in rr_files], ignore_index=True)

# =========================================================
# STEP 2: CLEAN COLUMN NAMES
# =========================================================

for df in [df_im, df_rr]:
    df.columns = df.columns.str.replace("\n", " ", regex=False).str.strip()

# =========================================================
# STEP 3: STANDARDIZE COLUMN NAMES ✅
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
# STEP 5: SELECT SAFE COMMON COLUMNS ✅
# =========================================================

columns_needed = [
    "Ticket_ID",
    "Ticket_Type",
    "Title",
    "Reported_Date",
    "Open Time (Timezone based)",
    "Resolve Time (Timezone based)",
    "Priority",
    "Call Code",
    "CI Location"
]

df_im = df_im[[c for c in columns_needed if c in df_im.columns]]
df_rr = df_rr[[c for c in columns_needed if c in df_rr.columns]]

# =========================================================
# STEP 6: COMBINE IM + RR
# =========================================================

df = pd.concat([df_im, df_rr], ignore_index=True)

# =========================================================
# STEP 7: ROBUST DATE DERIVATION ✅✅✅
# =========================================================

df["Reported_Date"] = pd.to_datetime(df["Reported_Date"], errors="coerce")

# ✅ fallback to Open Time (CRITICAL FIX)
df["Reported_Date"] = df["Reported_Date"].fillna(
    pd.to_datetime(df["Open Time (Timezone based)"], errors="coerce")
)

# ✅ filter training window
df = df[
    (df["Reported_Date"] >= "2024-01-01") &
    (df["Reported_Date"] <= "2025-12-31")
]

df["Month"] = df["Reported_Date"].dt.to_period("M").astype(str)

# =========================================================
# STEP 8: SAFE NULL HANDLING
# =========================================================

for col in ["Priority", "Call Code", "CI Location"]:
    if col not in df.columns:
        df[col] = "Unknown"
    else:
        df[col] = df[col].fillna("Unknown")

# =========================================================
# STEP 9: SAVE TICKET MASTER ✅
# =========================================================

df.to_csv(output_path, index=False)

print("\n✅ AMS_Ticket_Master.csv created successfully")
print("✅ Path:", output_path)
print("✅ Date range:", df["Month"].min(), "to", df["Month"].max())
print("✅ Total tickets:", len(df))