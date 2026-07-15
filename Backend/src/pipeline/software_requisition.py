import pandas as pd
import os
import re

# =====================================================
# PATHS
# =====================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.abspath(
    os.path.join(
        CURRENT_DIR,
        "..",
        "..",
        "data"
    )
)

MASTER_FILE = os.path.join(
    BASE_DIR,
    "Master",
    "master_software.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "processed",
    "Software_Category_Count.csv"
)

print("\n========================================")
print("SOFTWARE REQUISITION PIPELINE")
print("========================================")
print("Master File :", MASTER_FILE)
print("Output File :", OUTPUT_FILE)
print("========================================")

# =====================================================
# LOAD MASTER CSV
# =====================================================

if not os.path.exists(MASTER_FILE):
    raise FileNotFoundError(
        f"Master Software CSV not found:\n{MASTER_FILE}"
    )

df = pd.read_csv(
    MASTER_FILE,
    dtype=str,
    low_memory=False
)

print("\nRows Loaded :", len(df))

# =====================================================
# DATE PARSING
# =====================================================

df["Created"] = pd.to_datetime(
    df["Created"],
    errors="coerce"
)

df = df[df["Created"].notna()].copy()

df["Year"] = df["Created"].dt.year.astype(int)

print("\n========== YEAR DISTRIBUTION ==========")
print(df["Year"].value_counts().sort_index())

# =====================================================
# SOFTWARE EXTRACTION
# =====================================================

def extract_software(text):

    if pd.isna(text):
        return []

    matches = re.findall(
        r"Software Name:\s*([^,]+)",
        str(text)
    )

    cleaned = []

    for m in matches:

        name = m.strip()

        name = re.split(
            r"Version:",
            name
        )[0].strip()

        name = re.split(
            r"Rejected By",
            name
        )[0].strip()

        lower = name.lower()

        if "sap" in lower:
            name = "SAP"

        elif "citrix" in lower:
            name = "Citrix"

        elif "docker" in lower:
            name = "Docker Desktop"

        elif "copilot" in lower:
            name = "GitHub Copilot"

        elif "python" in lower:
            name = "Python"

        elif "node" in lower:
            name = "Node.js"

        elif "git" in lower and "github" not in lower:
            name = "Git"

        elif "visual studio code" in lower or "vs code" in lower:
            name = "VS Code"

        elif "intellij" in lower:
            name = "IntelliJ IDEA"

        elif "postman" in lower:
            name = "Postman"

        elif "sql" in lower:
            name = "SQL Tool"

        elif "java" in lower or "jdk" in lower:
            name = "JDK"

        elif "workspace" in lower or "web client" in lower:
            name = "Citrix"

        else:
            name = name.title().strip()

        cleaned.append(name)

    return cleaned

# =====================================================
# APPROVED SOFTWARE
# =====================================================

approved_records = []

for _, row in df.iterrows():

    softwares = extract_software(
        row.get("Approved software List", "")
    )

    for software in softwares:

        approved_records.append({

            "Year": row["Year"],

            "Software": software

        })

approved_df = pd.DataFrame(
    approved_records
)

if len(approved_df):

    approved_count = (

        approved_df

        .groupby(
            ["Year", "Software"]
        )

        .size()

        .reset_index(name="Approved Count")

    )

else:

    approved_count = pd.DataFrame(
        columns=[
            "Year",
            "Software",
            "Approved Count"
        ]
    )

# =====================================================
# REJECTED SOFTWARE
# =====================================================

rejected_records = []

for _, row in df.iterrows():

    softwares = extract_software(
        row.get("Rejected Software List", "")
    )

    for software in softwares:

        rejected_records.append({

            "Year": row["Year"],

            "Software": software

        })

rejected_df = pd.DataFrame(
    rejected_records
)

if len(rejected_df):

    rejected_count = (

        rejected_df

        .groupby(
            ["Year", "Software"]
        )

        .size()

        .reset_index(name="Rejected Count")

    )

else:

    rejected_count = pd.DataFrame(
        columns=[
            "Year",
            "Software",
            "Rejected Count"
        ]
    )

# =====================================================
# MERGE
# =====================================================

final_df = pd.merge(

    approved_count,

    rejected_count,

    on=[
        "Year",
        "Software"
    ],

    how="outer"

).fillna(0)

final_df["Approved Count"] = final_df["Approved Count"].astype(int)
final_df["Rejected Count"] = final_df["Rejected Count"].astype(int)

final_df = final_df.sort_values(

    by=[
        "Year",
        "Approved Count"
    ],

    ascending=[
        True,
        False
    ]

)

# =====================================================
# SAVE
# =====================================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

final_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n========================================")
print("SOFTWARE SUMMARY")
print("========================================")
print(final_df.head(20))
print("\nSaved :", OUTPUT_FILE)
print("========================================")