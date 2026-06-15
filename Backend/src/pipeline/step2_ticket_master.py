import pandas as pd
import glob
import os

# =========================================================
# STEP 0: RESOLVE PROJECT PATHS
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
# STEP 1: LOAD ALL RAW FILES (2024 + 2025)
# =========================================================

im_files = glob.glob(os.path.join(RAW_DIR, "*IM*.xlsx"))
rr_files = glob.glob(os.path.join(RAW_DIR, "*RR*.xlsx"))

if not im_files:
    raise FileNotFoundError("No IM files found")

if not rr_files:
    raise FileNotFoundError("No RR files found")

df_im = pd.concat(
    [pd.read_excel(file) for file in im_files],
    ignore_index=True
)

df_rr = pd.concat(
    [pd.read_excel(file) for file in rr_files],
    ignore_index=True
)

# =========================================================
# STEP 2: CLEAN COLUMN NAMES
# =========================================================

for df in [df_im, df_rr]:
    df.columns = (
        df.columns
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )

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
# STEP 5: FILTER TARGET RESOLVE GROUPS
# =========================================================

incident_groups = [
    "AV/VC Support VW Group IT Solution",
    "Antivirus Support VW Group IT Solution",
    "Asset Support VW Group IT Solution",
    "Service Desk VW Group IT Solution"
]

service_request_groups = [
    "Service Desk VW Group IT Solution",
    "Asset Support VW Group IT Solution",
    "Antivirus Support VW Group IT Solution"
]

if "Resolve Group" not in df_im.columns:
    raise ValueError("Resolve Group column missing in Incident file")

if "Resolve Group" not in df_rr.columns:
    raise ValueError("Resolve Group column missing in Service Request file")

df_im["Resolve Group"] = (
    df_im["Resolve Group"]
    .astype(str)
    .str.strip()
)

df_rr["Resolve Group"] = (
    df_rr["Resolve Group"]
    .astype(str)
    .str.strip()
)

df_im = df_im[
    df_im["Resolve Group"].isin(incident_groups)
]

df_rr = df_rr[
    df_rr["Resolve Group"].isin(service_request_groups)
]

print("\n========== FILTER RESULTS ==========")
print("Incident Tickets:", len(df_im))
print("Service Request Tickets:", len(df_rr))

print("\nIncident Group Distribution:")
print(df_im["Resolve Group"].value_counts())

print("\nService Request Group Distribution:")
print(df_rr["Resolve Group"].value_counts())

# =========================================================
# STEP 6: SELECT REQUIRED COLUMNS
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
    "CI Location",
    "CI Location.1",
    "Resolve Group"
]

df_im = df_im[[c for c in columns_needed if c in df_im.columns]]
df_rr = df_rr[[c for c in columns_needed if c in df_rr.columns]]

# =========================================================
# STEP 7: COMBINE INCIDENT + SERVICE REQUEST
# =========================================================

df = pd.concat([df_im, df_rr], ignore_index=True)

# =========================================================
# STEP 7.5: LOCATION DERIVATION
# =========================================================

if "CI Location" not in df.columns:
    df["CI Location"] = None

if "CI Location.1" not in df.columns:
    df["CI Location.1"] = None

# Primary location
df["Location"] = df["CI Location"]

# Fallback to CI Location.1 when CI Location is blank
df["Location"] = df["Location"].where(
    df["Location"].notna() &
    (df["Location"].astype(str).str.strip() != ""),
    df["CI Location.1"]
)

df["Location"] = df["Location"].fillna("Unknown")

print("\n========== LOCATION CHECK ==========")

print("\nLocation count by Ticket Type:")
print(
    df.groupby("Ticket_Type")["Location"]
      .apply(lambda x: x.notna().sum())
)

print("\nTop 20 Locations:")
print(
    df["Location"]
      .value_counts()
      .head(20)
)

# =========================================================
# STEP 8: DATE PROCESSING
# =========================================================

df["Reported_Date"] = pd.to_datetime(
    df["Reported_Date"],
    errors="coerce"
)

# Fallback to Open Time if Reported_Date is missing
df["Reported_Date"] = df["Reported_Date"].fillna(
    pd.to_datetime(
        df["Open Time (Timezone based)"],
        errors="coerce"
    )
)

print(
    "\nLatest date before filtering:",
    df["Reported_Date"].max()
)

# =========================================================
# TRAINING WINDOW: JAN 2024 TO APR 2026
# =========================================================

TRAIN_START_DATE = "2024-01-01"
TRAIN_END_DATE = "2026-04-30"

df = df[
    (df["Reported_Date"] >= TRAIN_START_DATE) &
    (df["Reported_Date"] <= TRAIN_END_DATE)
]

df["Month"] = (
    df["Reported_Date"]
    .dt.to_period("M")
    .astype(str)
)

print(
    "\nLatest date after filtering:",
    df["Reported_Date"].max()
)

# =========================================================
# STEP 9: NULL HANDLING
# =========================================================

for col in [
    "Priority",
    "Call Code",
    "CI Location",
    "CI Location.1",
    "Location",
    "Resolve Group"
]:
    if col not in df.columns:
        df[col] = "Unknown"
    else:
        df[col] = df[col].fillna("Unknown")

# =========================================================
# STEP 10: FINAL VALIDATION
# =========================================================

print("\n========== FINAL DATASET ==========")

print(
    "\nFinal Incident Group Counts:"
)

print(
    df[df["Ticket_Type"] == "Incident"]
    ["Resolve Group"]
    .value_counts()
)

print(
    "\nFinal Service Request Group Counts:"
)

print(
    df[df["Ticket_Type"] == "Service Request"]
    ["Resolve Group"]
    .value_counts()
)


print("\n========== LOCATION VALIDATION ==========")

print(
    df.groupby(["Ticket_Type", "Location"])
      .size()
      .sort_values(ascending=False)
      .head(20)
)

# =========================================================
# STEP 11: SAVE
# =========================================================

df.to_csv(output_path, index=False)

print("\n✅ AMS_Ticket_Master.csv created successfully")
print("✅ Path:", output_path)
print("✅ Date range:", df["Month"].min(), "to", df["Month"].max())
print("✅ Total tickets:", len(df))
print("✅ Incident tickets:", len(df[df["Ticket_Type"] == "Incident"]))
print("✅ Service Request tickets:", len(df[df["Ticket_Type"] == "Service Request"]))