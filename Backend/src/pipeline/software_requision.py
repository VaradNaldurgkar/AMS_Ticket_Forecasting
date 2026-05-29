import pandas as pd
import os
import re

# -----------------------------
# Dynamic Paths (FIXED)
# -----------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))

software_file = os.path.join(base_dir, "..", "..", "data", "raw", "u_vwits_u_software_requisition_report.xlsx")
output_file = os.path.join(base_dir, "..", "..", "data", "processed", "Software_Category_Count.csv")

software_file = os.path.normpath(software_file)
output_file = os.path.normpath(output_file)

# Debug
print("Software file:", software_file)
print("Exists?", os.path.exists(software_file))

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_excel(software_file, engine="openpyxl")

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

        # Normalize
        name_lower = name.lower()

        # ---- Standardization rules ----
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
approved_list = []

for val in df["Approved software List"]:
    approved_list.extend(extract_software(val))

approved_count = pd.Series(approved_list).value_counts().reset_index()
approved_count.columns = ["Software", "Approved Count"]

# -----------------------------
# Rejected Software Processing
# -----------------------------
rejected_list = []

for val in df.get("Rejected Software List", []):
    rejected_list.extend(extract_software(val))

rejected_count = pd.Series(rejected_list).value_counts().reset_index()
rejected_count.columns = ["Software", "Rejected Count"]

# -----------------------------
# Merge both into one clean table
# -----------------------------
final_df = pd.merge(
    approved_count,
    rejected_count,
    on="Software",
    how="outer"
).fillna(0)

# Sort by highest approvals
final_df = final_df.sort_values(by="Approved Count", ascending=False)

# Convert counts to int
final_df["Approved Count"] = final_df["Approved Count"].astype(int)
final_df["Rejected Count"] = final_df["Rejected Count"].astype(int)

# -----------------------------
# Save Output
# -----------------------------
os.makedirs(os.path.dirname(output_file), exist_ok=True)
final_df.to_csv(output_file, index=False)

print("✅ File created:", output_file)
