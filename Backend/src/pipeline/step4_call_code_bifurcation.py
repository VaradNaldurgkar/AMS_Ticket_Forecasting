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
# STEP 5: SELECT REQUIRED COLUMNS (IMPORTANT: INCLUDE CALL CODE)
# ========================================================

required_columns = [
    "Incident ID",
    "Call Code",  # ✅ KEY COLUMN
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
# STEP 7: OPEN TIME FILTER (SAME LOGIC)
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
# STEP 8: CLEAN CALL CODE
# ========================================================

df["Call Code"] = (
    df["Call Code"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

# ========================================================
# STEP 9: REMOVE DUPLICATES (VERY IMPORTANT)
# ========================================================

df = df.drop_duplicates(subset=["Incident ID"])

# ========================================================
# STEP 10: CALL CODE BREAKDOWN
# ========================================================

call_code_breakdown = (
    df.groupby("Call Code")["Incident ID"]
    .nunique()
    .reset_index(name="Ticket_Count")
    .sort_values("Ticket_Count", ascending=False)
)

# ========================================================
# STEP 11: SAVE OUTPUT (TO PROCESSED FOLDER)
# ========================================================

os.makedirs(PROCESSED_DIR, exist_ok=True)

output_path = os.path.join(PROCESSED_DIR, "Call_Code_Breakdown.csv")

call_code_breakdown.to_csv(output_path, index=False)

# ========================================================
# STEP 12: LOGS
# ========================================================

print("\n✅ Call Code bifurcation created successfully")
print("✅ Date range: 2024-01 to 2026-03")
print(f"✅ Saved to: {output_path}")

print("\nPreview:")
print(call_code_breakdown.head(10))