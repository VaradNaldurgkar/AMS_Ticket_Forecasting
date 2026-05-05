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

INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "AMS_Ticket_Master.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "Service_Call_Code_Breakdown.csv")

# ========================================================
# LOAD DATA
# ========================================================

df = pd.read_csv(INPUT_PATH)

# ========================================================
# FILTER ONLY SERVICE REQUESTS
# ========================================================

df = df[df["Ticket_Type"] == "Service Request"].copy()

# ========================================================
# CLEAN DATA
# ========================================================

df["Call Code"] = df["Call Code"].fillna("Unknown")
df["Title"] = df["Title"].fillna("").str.lower()

# ========================================================
# CATEGORY NORMALIZATION (same as incident)
# ========================================================

def normalize_category(title):
    if "citrix" in title:
        return "Citrix Issue"
    elif "laptop" in title:
        return "Laptop Issue"
    elif "vpn" in title:
        return "VPN Issue"
    elif "headset" in title:
        return "Headset Issue"
    elif "teams" in title:
        return "MS Teams Issue"
    elif "internet" in title:
        return "Internet Issue"
    elif "access" in title:
        return "Access Issue"
    else:
        return "Other"

df["Category"] = df["Title"].apply(normalize_category)

# ========================================================
# COUNT BY CALL CODE + CATEGORY
# ========================================================

counts = (
    df.groupby(["Call Code", "Category"])
    .size()
    .reset_index(name="Count")
)

# ========================================================
# CATEGORY TOTALS (for %)
# ========================================================

category_totals = (
    counts.groupby("Category")["Count"]
    .sum()
    .reset_index(name="Category_Total")
)

# ========================================================
# MERGE + CALCULATE %
# ========================================================

final_df = counts.merge(category_totals, on="Category")

final_df["Percentage"] = (
    final_df["Count"] / final_df["Category_Total"] * 100
).round(2)

# ========================================================
# FINAL FORMAT
# ========================================================

final_df = final_df[
    ["Call Code", "Category", "Count", "Percentage"]
].sort_values(
    ["Category", "Count"],
    ascending=[True, False]
)

# ========================================================
# SAVE OUTPUT
# ========================================================

final_df.to_csv(OUTPUT_PATH, index=False)

print("\n✅ Service Call Code bifurcation created successfully")
print(f"✅ Saved to: {OUTPUT_PATH}")
print("\nPreview:")
print(final_df.head(10))