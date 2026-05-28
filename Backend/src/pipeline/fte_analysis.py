import os
import pandas as pd

# -----------------------------
# DYNAMIC BASE PATH (NO PATH ERRORS)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "VWITS SLA Data_Feb-26 EUS.xlsx")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "fte_analysis")

# Create output folder if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"📥 Reading file from: {RAW_PATH}")
print(f"📤 Output will be saved to: {OUTPUT_DIR}")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel(RAW_PATH, sheet_name="Resolution Data", engine="openpyxl")

# Clean columns
df.columns = df.columns.str.strip()

# Rename for convenience
df.rename(columns={
    "Proportional Solution Time [min]": "resolution_time",
    "Current Priority": "priority",
    "Title": "title"
}, inplace=True)

# Drop null resolution times
df = df.dropna(subset=["resolution_time"])

# -----------------------------
# CREATE CATEGORY FROM TITLE
# -----------------------------
def categorize_issue(title):
    title = str(title).lower()

    if any(x in title for x in ["password", "login", "access", "authentication"]):
        return "Access / Login / Password"
    elif any(x in title for x in ["vpn", "zscaler", "network", "internet"]):
        return "Network / VPN"
    elif any(x in title for x in ["laptop", "mouse", "headset", "charger", "hardware"]):
        return "Hardware Issues"
    elif "citrix" in title or "vdi" in title:
        return "Citrix / VDI"
    elif any(x in title for x in ["teams", "outlook", "mail"]):
        return "Collaboration Tools"
    elif any(x in title for x in ["install", "software", "request"]):
        return "Software / Installation"
    elif "wifi" in title:
        return "WiFi Issues"
    elif any(x in title for x in ["pki", "certificate"]):
        return "PKI / Certificate"
    elif any(x in title for x in ["slow", "performance"]):
        return "Performance Issues"
    elif "successfactor" in title:
        return "HR Systems"
    else:
        return "Others"

df["category"] = df["title"].apply(categorize_issue)

# -----------------------------
# 1. CATEGORY-WISE ANALYSIS
# -----------------------------
category_analysis = df.groupby("category").agg(
    avg_resolution_time=("resolution_time", "mean"),
    ticket_count=("resolution_time", "count")
).reset_index()

category_analysis["avg_resolution_time"] = category_analysis["avg_resolution_time"].round(2)

# Sort by ticket volume
category_analysis = category_analysis.sort_values(by="ticket_count", ascending=False)

category_path = os.path.join(OUTPUT_DIR, "category_resolution_time.csv")
category_analysis.to_csv(category_path, index=False)

# -----------------------------
# 2. PRIORITY-BASED FTE ANALYSIS
# -----------------------------
priority_analysis = df.groupby("priority").agg(
    avg_resolution_time=("resolution_time", "mean"),
    ticket_count=("resolution_time", "count")
).reset_index()

priority_analysis["avg_resolution_time"] = priority_analysis["avg_resolution_time"].round(2)

# -----------------------------
# FTE CALCULATION
# -----------------------------
MINUTES_PER_DAY = 420   # 7 productive hours
WORKING_DAYS = 20
FTE_CAPACITY = MINUTES_PER_DAY * WORKING_DAYS  # monthly capacity

priority_analysis["total_effort_min"] = (
    priority_analysis["avg_resolution_time"] * priority_analysis["ticket_count"]
)

priority_analysis["fte_required"] = (
    priority_analysis["total_effort_min"] / FTE_CAPACITY
).round(2)

priority_path = os.path.join(OUTPUT_DIR, "priority_fte_analysis.csv")
priority_analysis.to_csv(priority_path, index=False)

# -----------------------------
# FINAL OUTPUT
# -----------------------------
print("\n✅ Analysis Complete!")
print(f"✅ Category file: {category_path}")
print(f"✅ Priority FTE file: {priority_path}")
