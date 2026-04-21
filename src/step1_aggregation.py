import pandas as pd

# ========================================================
# STEP 0: FILE PATHS
# ========================================================

im_path = "data/raw/IM Raw Data Report April 25 to till  April 26.xlsx"
rr_path = "data/raw/RR RF Raw Data Report April 25 to till April 26.xlsx"

# ========================================================
# STEP 1: LOAD FILES
# ========================================================

df_im = pd.read_excel(im_path)
df_rr = pd.read_excel(rr_path)

# ========================================================
# STEP 2: CLEAN COLUMN NAMES
# ========================================================

for df in [df_im, df_rr]:
    df.columns = (
        df.columns
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )

# ========================================================
# STEP 3: STANDARDIZE RR COLUMN NAMES
# ========================================================

df_rr = df_rr.rename(columns={
    "Request ID": "Incident ID",
    "Reported Time (Timezone based)": "Reported Date (Timezone based)",
    "Complexity": "Priority"
})

# ========================================================
# STEP 4: ADD TICKET TYPE
# ========================================================

df_im["Ticket_Type"] = "Incident"
df_rr["Ticket_Type"] = "Service Request"

# ========================================================
# STEP 5: SELECT REQUIRED COMMON COLUMNS
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
# STEP 6: COMBINE IM + RR DATA
# ========================================================

df = pd.concat([df_im, df_rr], ignore_index=True)

# ========================================================
# STEP 7: DATE DERIVATION
# ========================================================

df["Reported_Date"] = pd.to_datetime(
    df["Reported Date (Timezone based)"],
    errors="coerce"
)

df["Reported_Date"] = df["Reported_Date"].fillna(
    pd.to_datetime(df["Open Time (Timezone based)"], errors="coerce")
)

# ========================================================
# STEP 8: MONTH DERIVATION
# ========================================================

df["Month"] = df["Reported_Date"].dt.to_period("M").astype(str)

# ========================================================
# STEP 9: LOCATION DERIVATION
# ========================================================

df["Location"] = "Unknown"

if "CI Location" in df.columns:
    df["Location"] = df["CI Location"]

if "CI Location.1" in df.columns:
    df["Location"] = df["Location"].where(
        df["Location"].notna() & (df["Location"].str.strip() != ""),
        df["CI Location.1"]
    )

df["Location"] = df["Location"].fillna("Unknown")

# ========================================================
# STEP 10: MONTHLY AGGREGATION
# ========================================================

monthly_df = df.groupby(["Month", "Location"]).agg(
    Total_Tickets=("Incident ID", "count"),
    Incidents=("Ticket_Type", lambda x: (x == "Incident").sum()),
    Service_Requests=("Ticket_Type", lambda x: (x == "Service Request").sum())
).reset_index()

monthly_df = monthly_df.sort_values(by=["Month", "Location"])

# ========================================================
# STEP 11: PRIORITY / COMPLEXITY BREAKDOWN
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
# STEP 12: SAVE FINAL OUTPUT TO DESKTOP ✅
# ========================================================

desktop_output_path = (
    r"C:\Users\S08OFJF\Desktop\AMS_Yearly_Aggregated.csv"
)

monthly_df.to_csv(desktop_output_path, index=False)

print("\n✅ Final Dataset with Priority/Complexity Breakdown:")
print(monthly_df.head(10))

print(f"\n✅ Aggregated dataset saved to: {desktop_output_path}")