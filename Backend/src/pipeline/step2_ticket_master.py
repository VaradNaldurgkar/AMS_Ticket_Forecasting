import pandas as pd
import os

# =========================================================
# STEP 0 : PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MASTER_DIR = os.path.join(
    BASE_DIR,
    "data",
    "Master"
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

os.makedirs(
    PROCESSED_DIR,
    exist_ok=True
)

OUTPUT_FILE = os.path.join(
    PROCESSED_DIR,
    "AMS_Ticket_Master.csv"
)

INCIDENT_MASTER = os.path.join(
    MASTER_DIR,
    "master_incidents.csv"
)

REQUEST_MASTER = os.path.join(
    MASTER_DIR,
    "master_requests.csv"
)

print("\n========== STEP 2 ==========")

print("Incident Master :", INCIDENT_MASTER)
print("Request Master  :", REQUEST_MASTER)

if not os.path.exists(INCIDENT_MASTER):
    raise FileNotFoundError(
        "master_incidents.csv not found"
    )

if not os.path.exists(REQUEST_MASTER):
    raise FileNotFoundError(
        "master_requests.csv not found"
    )

# =========================================================
# LOAD CSV MASTERS
# =========================================================

df_im = pd.read_csv(
    INCIDENT_MASTER,
    low_memory=False,
    dtype=str
)

df_rr = pd.read_csv(
    REQUEST_MASTER,
    low_memory=False,
    dtype=str
)

print("\nLoaded Incident :", len(df_im))
print("Loaded Request  :", len(df_rr))

# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

for df in [df_im, df_rr]:

    df.columns = (

        df.columns
        .str.replace("\n", " ", regex=False)
        .str.strip()

    )

# =========================================================
# STANDARDIZE COLUMN NAMES
# =========================================================

df_im.rename(

    columns={

        "Incident ID": "Ticket_ID",

        "Reported Date (Timezone based)": "Reported_Date"

    },

    inplace=True

)

df_rr.rename(

    columns={

        "Request ID": "Ticket_ID",

        "Reported Time (Timezone based)": "Reported_Date",

        "Complexity": "Priority"

    },

    inplace=True

)

# =========================================================
# ADD TICKET TYPE
# =========================================================

df_im["Ticket_Type"] = "Incident"

df_rr["Ticket_Type"] = "Service Request"

print("\nIncident Columns")
print(df_im.columns.tolist())

print("\nRequest Columns")
print(df_rr.columns.tolist())

# =========================================================
# SELECT REQUIRED COLUMNS
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
    "Close Group"

]

df_im = df_im[
    [c for c in columns_needed if c in df_im.columns]
]

df_rr = df_rr[
    [c for c in columns_needed if c in df_rr.columns]
]

# =========================================================
# COMBINE
# =========================================================

df = pd.concat(
    [
        df_im,
        df_rr
    ],
    ignore_index=True
)

print("\nCombined Tickets :", len(df))

# =========================================================
# LOCATION
# =========================================================

if "CI Location" not in df.columns:
    df["CI Location"] = ""

if "CI Location.1" not in df.columns:
    df["CI Location.1"] = ""

df["Location"] = df["CI Location"]

df["Location"] = df["Location"].where(

    df["Location"].notna()
    &
    (
        df["Location"]
        .astype(str)
        .str.strip()
        != ""
    ),

    df["CI Location.1"]

)

df["Location"] = (
    df["Location"]
    .fillna("Unknown")
)

print("\n========== LOCATION ==========")

print(
    df["Location"]
    .value_counts()
    .head(20)
)

# =========================================================
# DATE
# =========================================================

df["Reported_Date"] = pd.to_datetime(

    df["Reported_Date"],

    errors="coerce"

)

df["Reported_Date"] = df["Reported_Date"].fillna(

    pd.to_datetime(

        df["Open Time (Timezone based)"],

        errors="coerce"

    )

)

print("\nEarliest :", df["Reported_Date"].min())
print("Latest   :", df["Reported_Date"].max())

# =========================================================
# KEEP DATA FROM JAN 2024
# =========================================================

TRAIN_START = pd.Timestamp("2024-01-01")

df = df[
    df["Reported_Date"] >= TRAIN_START
]

df["Month"] = (

    df["Reported_Date"]
    .dt.to_period("M")
    .astype(str)

)

print("\n========== MONTH SUMMARY ==========")

print(
    df["Month"]
    .value_counts()
    .sort_index()
)

# =========================================================
# NULL HANDLING
# =========================================================

for col in [

    "Priority",

    "Call Code",

    "CI Location",

    "CI Location.1",

    "Location",

    "Close Group"

]:

    if col not in df.columns:

        df[col] = "Unknown"

    else:

        df[col] = (

            df[col]
            .fillna("Unknown")

        )

# =========================================================
# SORT DATA
# =========================================================

df = df.sort_values(
    "Reported_Date"
)

# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n========== FINAL SUMMARY ==========")

print("Total Tickets :", len(df))

print(
    "\nIncident :",
    len(
        df[
            df["Ticket_Type"] == "Incident"
        ]
    )
)

print(
    "Service Request :",
    len(
        df[
            df["Ticket_Type"] == "Service Request"
        ]
    )
)

print("\nClose Groups")

print(
    df["Close Group"]
    .value_counts()
)

print("\nLocation")

print(
    df["Location"]
    .value_counts()
    .head(20)
)

print("\nDate Range")

print(
    df["Month"].min(),
    "->",
    df["Month"].max()
)

# =========================================================
# SAVE
# =========================================================

df.to_csv(

    OUTPUT_FILE,

    index=False

)

print("\n========================================")
print("AMS_Ticket_Master.csv Created")
print("Rows :", len(df))
print("Path :", OUTPUT_FILE)
print("========================================")