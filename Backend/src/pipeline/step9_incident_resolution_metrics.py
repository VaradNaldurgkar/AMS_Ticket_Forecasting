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

df = df[
    df["Ticket_Type"] == "Incident"
].copy()

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

df["Title_Lower"] = (
    df["Title"]
    .str.lower()
)

# ========================================================
# INCIDENT CLASSIFICATION
# ========================================================

def normalize_incident(title):

    title = str(title).lower()

    # ====================================================
    # TEST / DUMMY TICKETS
    # ====================================================

    if any(word in title for word in [

        "test ticket",
        "test issue",
        "dummy"

    ]):
        return "Test Ticket"

    # ====================================================
    # ACCESS / LOGIN ISSUES
    # ====================================================

    elif any(word in title for word in [

        "password",
        "login",
        "log in",
        "signin",
        "sign in",
        "authentication",
        "access denied",
        "access issue",
        "account locked",
        "unlock",
        "credential",
        "mfa",
        "otp",
        "2fa",
        "token",
        "account access",
        "ad account",
        "active directory",
        "permissions",
        "window account",
        "signature pin blocked"

    ]):
        return "Access Issue"

    # ====================================================
    # EMAIL / OUTLOOK / OFFICE
    # ====================================================

    elif any(word in title for word in [

        "outlook",
        "mail",
        "mailbox",
        "email",
        "exchange",
        "distribution list",
        "shared mailbox",
        "ms office",
        "office 365"

    ]):
        return "Email Issue"

    # ====================================================
    # LAPTOP / HARDWARE / MACBOOK
    # ====================================================

    elif any(word in title for word in [

        "laptop",
        "keyboard",
        "mouse",
        "dock",
        "battery",
        "charger",
        "screen",
        "display",
        "monitor",
        "hardware",
        "usb",
        "camera",
        "webcam",
        "touchpad",
        "desktop",
        "pc issue",
        "device issue",
        "macbook",
        "ram upgradation",
        "system slowness"

    ]):
        return "Laptop"

    # ====================================================
    # VPN / RDP
    # ====================================================

    elif any(word in title for word in [

        "vpn",
        "global protect",
        "pulse secure",
        "remote access",
        "rdp"

    ]):
        return "VPN"

    # ====================================================
    # CITRIX
    # ====================================================

    elif any(word in title for word in [

        "citrix",
        "vdi",
        "virtual desktop",
        "workspace app"

    ]):
        return "Citrix"

    # ====================================================
    # MS TEAMS
    # ====================================================

    elif any(word in title for word in [

        "teams",
        "meeting",
        "audio issue",
        "video issue",
        "call issue",
        "conference",
        "voice issue"

    ]):
        return "MS Teams"

    # ====================================================
    # NETWORK / INTERNET
    # ====================================================

    elif any(word in title for word in [

        "network",
        "internet",
        "wifi",
        "wi-fi",
        "lan",
        "connection",
        "connectivity",
        "dns",
        "proxy"

    ]):
        return "Network"

    # ====================================================
    # PRINTER
    # ====================================================

    elif any(word in title for word in [

        "printer",
        "printing",
        "scanner",
        "print queue",
        "print issue",
        "not able to print"

    ]):
        return "Printer"

    # ====================================================
    # SAP
    # ====================================================

    elif any(word in title for word in [

        "sap",
        "sap gui",
        "hana"

    ]):
        return "SAP"

    # ====================================================
    # PKI / SMART CARD
    # ====================================================

    elif any(word in title for word in [

        "pki",
        "smart card",
        "certificate",
        "token certificate"

    ]):
        return "PKI Certificates"

    # ====================================================
    # BITLOCKER
    # ====================================================

    elif any(word in title for word in [

        "bitlocker",
        "recovery key",
        "encryption"

    ]):
        return "BitLocker"

    # ====================================================
    # BROWSER
    # ====================================================

    elif any(word in title for word in [

        "browser",
        "chrome",
        "edge",
        "firefox",
        "internet explorer",
        "browser crash"

    ]):
        return "Browser Issue"

    # ====================================================
    # APPLICATIONS / SOFTWARE
    # ====================================================

    elif any(word in title for word in [

        "application",
        "software",
        "tool not working",
        "app issue",
        "software install",
        "installation issue",
        "client tool",
        "terraform",
        "composer",
        "aws cli",
        "manage engine"

    ]):
        return "Application"

    # ====================================================
    # HEADSET / AUDIO
    # ====================================================

    elif any(word in title for word in [

        "headset",
        "headphone",
        "microphone",
        "mic",
        "speaker",
        "speaker issue"

    ]):
        return "Headset"

    # ====================================================
    # FILE SHARING / STORAGE / SERVER
    # ====================================================

    elif any(word in title for word in [

        "onedrive",
        "sharepoint",
        "share drive",
        "shared folder",
        "c drive",
        "server",
        "disk space",
        "storage",
        "opening file at server"

    ]):
        return "File Sharing"

    # ====================================================
    # WINDOWS / OS
    # ====================================================

    elif any(word in title for word in [

        "windows",
        "blue screen",
        "bsod",
        "os issue",
        "operating system"

    ]):
        return "Operating System"

    # ====================================================
    # MOBILE DEVICES
    # ====================================================

    elif any(word in title for word in [

        "mobile",
        "iphone",
        "android",
        "phone issue",
        "intune"

    ]):
        return "Mobile Device"

    # ====================================================
    # HR / ATTENDANCE
    # ====================================================

    elif any(word in title for word in [

        "attendance",
        "attendance regularization",
        "regularization",
        "doj correction",
        "mandatory training",
        "training completion",
        "performance management"

    ]):
        return "HR Request"

    # ====================================================
    # SECURITY / COMPLIANCE
    # ====================================================

    elif any(word in title for word in [

        "fireeye",
        "malware",
        "vulnerability",
        "compliance",
        "security awareness",
        "suspicious pattern"

    ]):
        return "Security Alert"
    
    elif any(word in title for word in [

    "success factor",
    "successfactor",
    "leave",
    "attendance",
    "regularization",
    "training assignment",
    "anti-corruption training"

    ]):
        return "HR Request"
    
    elif any(word in title for word in [

    "security logs",
    "event log",
    "antivirus",
    "av not updated",
    "trellix",
    "checkpoint",
    "zscalar",
    "zscaler"

    ]):
        return "Security Alert"
    

    elif any(word in title for word in [

    "jira",
    "azure cli",
    "vsc",
    "udemy",
    "aisha",
    "oneconnect",
    "one connect",
    "kira"

    ]):
        return "Application"
    


    elif any(word in title for word in [

    "hdmi",
    "desk phone",
    "z-book"

   ]):
        return "Laptop"
    


    elif any(word in title for word in [

    "profile activation",
    "account reset",
    "resource access"

    ]):
        return "Access Issue"

    # ====================================================
    # REMAINING
    # ====================================================

    else:
        return "General / Uncategorized"

# ========================================================
# APPLY CLASSIFICATION
# ========================================================

df["Incident_Type"] = (
    df["Title_Lower"]
    .apply(normalize_incident)
)

# ========================================================
# ANALYZE OTHER CATEGORY
# ========================================================

other_df = df[
    df["Incident_Type"] == "Other"
]

print("\n==============================")
print("TOP UNKNOWN INCIDENT TITLES")
print("==============================\n")

print(
    other_df["Title"]
    .value_counts()
    .head(50)
)

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

final_df.to_csv(
    OUTPUT_PATH,
    index=False
)

# ========================================================
# LOGS
# ========================================================

print(
    "\n✅ Incident Resolution Metrics created successfully"
)

print(
    f"✅ Saved to: {OUTPUT_PATH}"
)

print("\nPreview:\n")

print(final_df.head(20))