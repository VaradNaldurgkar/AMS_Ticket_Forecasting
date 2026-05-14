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
    "Incident_Resolution_Metrics.csv"
)

# ========================================================
# LOAD DATA
# ========================================================

df = pd.read_csv(INPUT_PATH)

# ========================================================
# KEEP ONLY INCIDENTS
# ========================================================

df = df[df["Ticket_Type"] == "Incident"].copy()

# ========================================================
# CLEAN IMPORTANT COLUMNS
# ========================================================

df["Title"] = (
    df["Title"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# ========================================================
# CONVERT DATES
# ========================================================

df["Open Time (Timezone based)"] = pd.to_datetime(
    df["Open Time (Timezone based)"],
    errors="coerce"
)

df["Resolve Time (Timezone based)"] = pd.to_datetime(
    df["Resolve Time (Timezone based)"],
    errors="coerce"
)

# ========================================================
# REMOVE INVALID DATES
# ========================================================

df = df[
    df["Open Time (Timezone based)"].notna() &
    df["Resolve Time (Timezone based)"].notna()
]

# ========================================================
# CALCULATE RESOLUTION TIME
# ========================================================

df["Resolution_Hours"] = (
    (
        df["Resolve Time (Timezone based)"] -
        df["Open Time (Timezone based)"]
    ).dt.total_seconds() / 3600
)

# ========================================================
# REMOVE INVALID / EXTREME VALUES
# ========================================================

df = df[
    (df["Resolution_Hours"] >= 0) &
    (df["Resolution_Hours"] <= 168)
]

# ========================================================
# NORMALIZE INCIDENT CATEGORY
# ========================================================

df["Title_Lower"] = df["Title"].str.lower()

def normalize_incident(title):

    title = str(title).lower()

    if "laptop" in title:
        return "Laptop"

    elif "vpn" in title:
        return "VPN"

    elif "citrix" in title:
        return "Citrix"

    elif "headset" in title:
        return "Headset"

    elif "teams" in title:
        return "MS Teams"

    elif "internet" in title:
        return "Internet"

    elif "access" in title:
        return "Access Issue"

    elif "outlook" in title:
        return "Outlook"

    elif "wifi" in title or "wi-fi" in title:
        return "Wi-Fi"

    elif "mouse" in title:
        return "Mouse"

    elif "bitlocker" in title:
        return "BitLocker"

    elif "authentication" in title:
        return "Authentication"

    elif "pki" in title:
        return "PKI Certificates"

    elif "smart card" in title:
        return "Smart Card"

    elif "password" in title:
        return "Password Reset"

    elif "mailbox" in title:
        return "Mailbox"

    elif "printer" in title:
        return "Printer"

    elif "sap" in title:
        return "SAP"

    elif "application" in title:
        return "Application"

    elif "network" in title:
        return "Network"

    elif "account" in title:
        return "Account Issue"

    elif "login" in title:
        return "Login Issue"

    elif "email" in title:
        return "Email Issue"

    elif "browser" in title:
        return "Browser Issue"

    else:
        return "Other"

df["Incident_Type"] = df["Title_Lower"].apply(normalize_incident)

# ========================================================
# GROUP + AGGREGATE
# ========================================================

final_df = (
    df.groupby("Incident_Type")
    .agg(
        Incident_Count=(
            "Incident_Type",
            "count"
        ),

        Avg_Resolution_Hours=(
            "Resolution_Hours",
            "mean"
        ),

        Median_Resolution_Hours=(
            "Resolution_Hours",
            "median"
        )
    )
    .reset_index()
)

# ========================================================
# ROUND VALUES
# ========================================================

numeric_columns = [
    "Avg_Resolution_Hours",
    "Median_Resolution_Hours"
]

final_df[numeric_columns] = (
    final_df[numeric_columns]
    .round(2)
)

# ========================================================
# SORT BY INCIDENT COUNT
# ========================================================

final_df = final_df.sort_values(
    "Incident_Count",
    ascending=False
)

# ========================================================
# SAVE CSV
# ========================================================

final_df.to_csv(OUTPUT_PATH, index=False)

# ========================================================
# LOGS
# ========================================================

print("\n✅ Incident Resolution Metrics created successfully")

print(f"✅ Saved to: {OUTPUT_PATH}")

print("\nPreview:\n")

print(final_df.head(20))