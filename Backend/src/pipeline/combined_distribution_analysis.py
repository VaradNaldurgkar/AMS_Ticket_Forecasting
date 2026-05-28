import os
import pandas as pd

# ======================================================
# DYNAMIC BASE PATH
# ======================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

RAW_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "VWITS SLA Data_Feb-26 EUS.xlsx"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "fte_analysis"
)

# Create output folder if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📥 Reading file from:")
print(RAW_PATH)

print(f"\n📤 Saving output to:")
print(OUTPUT_DIR)

# ======================================================
# LOAD EXCEL
# ======================================================

df = pd.read_excel(
    RAW_PATH,
    sheet_name="Resolution Data",
    engine="openpyxl"
)

# ======================================================
# CLEAN COLUMNS
# ======================================================

df.columns = df.columns.str.strip()

df.rename(columns={

    "Proportional Solution Time [min]":
        "resolution_time",

    "Current Priority":
        "priority",

    "Title":
        "title"

}, inplace=True)

# Remove null values
df = df.dropna(
    subset=["resolution_time"]
)

# ======================================================
# CATEGORY CLASSIFICATION
# ======================================================

def categorize_issue(title):

    title = str(title).lower()

    if any(
        x in title
        for x in [
            "password",
            "login",
            "access",
            "authentication"
        ]
    ):
        return "Access / Login / Password"

    elif any(
        x in title
        for x in [
            "vpn",
            "zscaler",
            "network",
            "internet"
        ]
    ):
        return "Network / VPN"

    elif any(
        x in title
        for x in [
            "laptop",
            "mouse",
            "headset",
            "charger",
            "hardware"
        ]
    ):
        return "Hardware Issues"

    elif (
        "citrix" in title or
        "vdi" in title
    ):
        return "Citrix / VDI"

    elif any(
        x in title
        for x in [
            "teams",
            "outlook",
            "mail"
        ]
    ):
        return "Collaboration Tools"

    elif any(
        x in title
        for x in [
            "install",
            "software",
            "request"
        ]
    ):
        return "Software / Installation"

    elif "wifi" in title:
        return "WiFi Issues"

    elif any(
        x in title
        for x in [
            "pki",
            "certificate"
        ]
    ):
        return "PKI / Certificate"

    elif any(
        x in title
        for x in [
            "slow",
            "performance"
        ]
    ):
        return "Performance Issues"

    elif "successfactor" in title:
        return "HR Systems"

    else:
        return "Others"

# Apply category mapping
df["category"] = df["title"].apply(
    categorize_issue
)

# ======================================================
# PRIORITY CLEANING
# ======================================================

df["priority"] = (
    df["priority"]
    .astype(str)
    .str.strip()
)

# ======================================================
# COMBINED CATEGORY + PRIORITY ANALYSIS
# ======================================================

combined_analysis = df.groupby(
    ["category", "priority"]
).agg(

    avg_resolution_time=(
        "resolution_time",
        "mean"
    ),

    ticket_count=(
        "resolution_time",
        "count"
    )

).reset_index()

# Round values
combined_analysis[
    "avg_resolution_time"
] = combined_analysis[
    "avg_resolution_time"
].round(2)

# ======================================================
# TOTAL EFFORT
# ======================================================

combined_analysis[
    "total_effort_min"
] = (

    combined_analysis[
        "avg_resolution_time"
    ] *

    combined_analysis[
        "ticket_count"
    ]

).round(2)

# ======================================================
# DISTRIBUTION PERCENTAGE
# ======================================================

total_tickets = combined_analysis[
    "ticket_count"
].sum()

combined_analysis[
    "distribution_percentage"
] = (

    combined_analysis[
        "ticket_count"
    ] /

    total_tickets

    * 100

).round(2)

# ======================================================
# SORTING
# ======================================================

combined_analysis = combined_analysis.sort_values(

    by="ticket_count",

    ascending=False

)

# ======================================================
# SAVE CSV
# ======================================================

output_path = os.path.join(

    OUTPUT_DIR,

    "combined_distribution.csv"

)

combined_analysis.to_csv(

    output_path,

    index=False

)

# ======================================================
# FINAL OUTPUT
# ======================================================

print("\n✅ Combined Distribution Created Successfully!")

print(f"\n📄 File saved at:")
print(output_path)

print("\n📊 Sample Data:\n")

print(combined_analysis.head())