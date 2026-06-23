import pandas as pd
import os
import re

# -----------------------------
# Dynamic Paths
# -----------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))

software_file = os.path.join(
    base_dir, "..", "..", "data", "Master",
    "master_software.xlsx"
)

output_file = os.path.join(
    base_dir, "..", "..", "data", "processed",
    "Software_Category_Count.csv"
)

software_file = os.path.normpath(software_file)
output_file = os.path.normpath(output_file)

# Debug
print("Software file:", software_file)
print("Exists?", os.path.exists(software_file))

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_excel(software_file, engine="openpyxl")

print("\n========== DATE DEBUG ==========")
print("Raw Created head:")
print(df["Created"].head(10))

print("\nRaw Created tail:")
print(df["Created"].tail(10))

# -----------------------------
# Date Parsing
# -----------------------------
df["Created"] = pd.to_datetime(
    df["Created"],
    errors="coerce",
    dayfirst=True
)

print("\n========== PARSED DATE DEBUG ==========")
print("Invalid dates:", df["Created"].isna().sum())

print("\nYear distribution after parsing:")
print(df["Created"].dt.year.value_counts(dropna=False))

df["Year"] = df["Created"].dt.year

# Remove rows with invalid year
df = df[df["Year"].notna()]
df["Year"] = df["Year"].astype(int)

# -----------------------------
# Clean + Extract software names
# -----------------------------
def extract_software(text):
    if pd.isna(text):
        return []

    matches = re.findall(r"Software Name:\s*([^,]+)", str(text))

    cleaned = []

    for m in matches:
        name = m.strip()

        # Remove unwanted parts
        name = re.split(r"Version:", name)[0].strip()
        name = re.split(r"Rejected By", name)[0].strip()

        name_lower = name.lower()

        # Standardization rules
        if "sap" in name_lower:
            name = "SAP"
        elif "citrix" in name_lower:
            name = "Citrix"
        elif "docker" in name_lower:
            name = "Docker Desktop"
        elif "copilot" in name_lower:
            name = "GitHub Copilot"
        elif "python" in name_lower:
            name = "Python"
        elif "node" in name_lower:
            name = "Node.js"
        elif "git" in name_lower and "github" not in name_lower:
            name = "Git"
        elif "visual studio code" in name_lower or "vs code" in name_lower:
            name = "VS Code"
        elif "intellij" in name_lower:
            name = "IntelliJ IDEA"
        elif "postman" in name_lower:
            name = "Postman"
        elif "sql" in name_lower:
            name = "SQL Tool"
        elif "java" in name_lower or "jdk" in name_lower:
            name = "JDK"
        elif "workspace" in name_lower or "web client" in name_lower:
            name = "Citrix"
        else:
            name = name.title().strip()

        cleaned.append(name)

    return cleaned


# -----------------------------
# Approved Software Processing
# -----------------------------
approved_records = []

for _, row in df.iterrows():
    year = row["Year"]
    softwares = extract_software(row["Approved software List"])

    for software in softwares:
        approved_records.append({
            "Year": year,
            "Software": software
        })

approved_df = pd.DataFrame(approved_records)

approved_count = (
    approved_df
    .groupby(["Year", "Software"])
    .size()
    .reset_index(name="Approved Count")
)

# -----------------------------
# Rejected Software Processing
# -----------------------------
rejected_records = []

for _, row in df.iterrows():
    year = row["Year"]
    softwares = extract_software(row["Rejected Software List"])

    for software in softwares:
        rejected_records.append({
            "Year": year,
            "Software": software
        })

rejected_df = pd.DataFrame(rejected_records)

if len(rejected_df) > 0:
    rejected_count = (
        rejected_df
        .groupby(["Year", "Software"])
        .size()
        .reset_index(name="Rejected Count")
    )
else:
    rejected_count = pd.DataFrame(
        columns=["Year", "Software", "Rejected Count"]
    )

# -----------------------------
# Merge Approved + Rejected
# -----------------------------
final_df = pd.merge(
    approved_count,
    rejected_count,
    on=["Year", "Software"],
    how="outer"
).fillna(0)

# Sort
final_df = final_df.sort_values(
    by=["Year", "Approved Count"],
    ascending=[True, False]
)

# Convert counts to int
final_df["Approved Count"] = final_df["Approved Count"].astype(int)
final_df["Rejected Count"] = final_df["Rejected Count"].astype(int)

# -----------------------------
# Save Output
# -----------------------------
os.makedirs(os.path.dirname(output_file), exist_ok=True)
final_df.to_csv(output_file, index=False)

print("\n✅ File created:", output_file)
print(final_df.head(20))