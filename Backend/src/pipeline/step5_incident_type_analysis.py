import pandas as pd

# ========================================================
# LOAD DATA
# ========================================================

df = pd.read_csv("data/processed/AMS_Ticket_Master.csv")

# -------------------------------
# FILTER ONLY INCIDENTS
# -------------------------------
df = df[df["Ticket_Type"] == "Incident"].copy()

# -------------------------------
# NORMALIZE INCIDENT CATEGORY
# -------------------------------
df["Title"] = df["Title"].fillna("").str.lower()

def normalize_incident(title):
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

df["Category"] = df["Title"].apply(normalize_incident)

# -------------------------------
# CALL CODE CLEANUP
# -------------------------------
df["Call Code"] = df["Call Code"].fillna("Unknown")

# -------------------------------
# COUNT INCIDENTS
# -------------------------------
counts = (
    df.groupby(["Call Code", "Category"])
    .size()
    .reset_index(name="Count")
)

# -------------------------------
# CALCULATE PERCENTAGE
# (within each Category)
# -------------------------------
category_totals = (
    counts.groupby("Category")["Count"]
    .sum()
    .reset_index(name="Category_Total")
)

final_df = counts.merge(category_totals, on="Category")

final_df["Percentage"] = (
    final_df["Count"] / final_df["Category_Total"] * 100
).round(2)

final_df = final_df[
    ["Call Code", "Category", "Count", "Percentage"]
].sort_values(
    ["Category", "Count"],
    ascending=[True, False]
)

# ========================================================
# SAVE OUTPUT TO DESKTOP ✅
# ========================================================

desktop_output_path = (
    r"C:\Users\S08OFJF\Desktop\Incident_Call_Code_Breakdown.csv"
)

final_df.to_csv(desktop_output_path, index=False)

print("\n✅ Incident Call Code bifurcation created successfully")
print(f"✅ File saved to: {desktop_output_path}")

print("\nPreview:")
print(final_df.head(10))