import os
import re
import pandas as pd

# ======================================================
# PATHS
# ======================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(CURRENT_DIR)
    )
)

MASTER_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "Master"
)

ASSET_FILE = os.path.join(
    MASTER_DIR,
    "master_assets.csv"
)

SOFTWARE_FILE = os.path.join(
    MASTER_DIR,
    "master_software.csv"
)

# ======================================================
# GLOBAL DATA CACHE
# ======================================================

ASSET_DF = None
SOFTWARE_DF = None


def load_master_data():
    global ASSET_DF, SOFTWARE_DF

    print("Loading master files into memory...")

    if os.path.exists(ASSET_FILE):
        ASSET_DF = pd.read_csv(
    ASSET_FILE,
    low_memory=False
)
        print("Asset data loaded:", len(ASSET_DF))

    if os.path.exists(SOFTWARE_FILE):
        SOFTWARE_DF = pd.read_csv(
    SOFTWARE_FILE,
    low_memory=False
)
        print("Software data loaded:", len(SOFTWARE_DF))


load_master_data()


# ======================================================
# REFRESH MASTER DATA
# ======================================================

def refresh_master_data():

    global ASSET_DF, SOFTWARE_DF

    if os.path.exists(ASSET_FILE):

        ASSET_DF = pd.read_csv(
            ASSET_FILE,
            low_memory=False
        )

    if os.path.exists(SOFTWARE_FILE):

        SOFTWARE_DF = pd.read_csv(
            SOFTWARE_FILE,
            low_memory=False
        )


# ======================================================
# COMMON FILTER
# ======================================================

def apply_date_filters(df, year="all", start_date=None, end_date=None):

    df = df.copy()

    df["Created"] = pd.to_datetime(
        df["Created"],
        errors="coerce"
    )

    df = df[df["Created"].notna()]

    if year != "all":
        df = df[df["Created"].dt.year == int(year)]

    if start_date:
        df = df[df["Created"] >= pd.to_datetime(start_date)]

    if end_date:
        df = df[df["Created"] <= pd.to_datetime(end_date)]

    return df


# ======================================================
# ASSET HELPERS
# ======================================================

def extract_assets(asset_text):

    if pd.isna(asset_text):
        return []

    assets = str(asset_text).split(",")
    cleaned = []

    for asset in assets:
        asset = asset.strip()

        if asset:
            cleaned.append(asset.title())

    return cleaned


# ======================================================
# SOFTWARE HELPERS
# ======================================================

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
        name = re.split(r"Version:", name)[0].strip()
        name_lower = name.lower()

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
        elif "sql" in name_lower:
            name = "SQL Tool"
        else:
            name = name.title().strip()

        cleaned.append(name)

    return cleaned


# ======================================================
# ASSET BREAKDOWN
# ======================================================

def get_asset_breakdown(year="all", start_date=None, end_date=None):

    refresh_master_data()

    global ASSET_DF

    if ASSET_DF is None:
        return []

    df = apply_date_filters(
        ASSET_DF,
        year,
        start_date,
        end_date
    )

    records = []

    for _, row in df.iterrows():
        records.extend(extract_assets(row["Asset List"]))

    if not records:
        return []

    asset_df = pd.DataFrame(records, columns=["Asset Category"])

    result = (
        asset_df.groupby("Asset Category")
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
        .head(10)
    )

    return [
        {
            "name": row["Asset Category"],
            "count": int(row["Count"])
        }
        for _, row in result.iterrows()
    ]


# ======================================================
# SOFTWARE BREAKDOWN
# ======================================================

def get_software_breakdown(year="all", start_date=None, end_date=None):

    refresh_master_data()

    global SOFTWARE_DF

    if SOFTWARE_DF is None:
        return []

    df = apply_date_filters(
        SOFTWARE_DF,
        year,
        start_date,
        end_date
    )

    records = []

    for _, row in df.iterrows():
        records.extend(
            extract_software(row["Approved software List"])
        )

    if not records:
        return []

    software_df = pd.DataFrame(records, columns=["Software"])

    result = (
        software_df.groupby("Software")
        .size()
        .reset_index(name="Approved Count")
        .sort_values(by="Approved Count", ascending=False)
        .head(10)
    )

    return [
        {
            "name": row["Software"],
            "count": int(row["Approved Count"])
        }
        for _, row in result.iterrows()
    ]


# ======================================================
# ASSET DASHBOARD
# ======================================================

def get_asset_dashboard(year="all", start_date=None, end_date=None):

    refresh_master_data()

    global ASSET_DF

    if ASSET_DF is None:
        return {}

    df = apply_date_filters(ASSET_DF, year, start_date, end_date)

    records = []

    for _, row in df.iterrows():
        records.extend(extract_assets(row["Asset List"]))

    if not records:
        return {}

    asset_df = pd.DataFrame(records, columns=["Asset Category"])

    full_result = (
        asset_df.groupby("Asset Category")
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
    )

    top_10 = full_result.head(10)
    top_item = full_result.iloc[0]

    return {
        "total_requests": int(full_result["Count"].sum()),
        "top_item": top_item["Asset Category"],
        "top_count": int(top_item["Count"]),
        "total_categories": len(full_result),
        "pie_chart_data": [
            {
                "name": row["Asset Category"],
                "tickets": int(row["Count"])
            }
            for _, row in top_10.iterrows()
        ]
    }


# ======================================================
# SOFTWARE DASHBOARD
# ======================================================

def get_software_dashboard(year="all", start_date=None, end_date=None):

    refresh_master_data()

    global SOFTWARE_DF

    if SOFTWARE_DF is None:
        return {}

    df = apply_date_filters(SOFTWARE_DF, year, start_date, end_date)

    records = []

    for _, row in df.iterrows():
        records.extend(
            extract_software(row["Approved software List"])
        )

    if not records:
        return {}

    software_df = pd.DataFrame(records, columns=["Software"])

    full_result = (
        software_df.groupby("Software")
        .size()
        .reset_index(name="Approved Count")
        .sort_values(by="Approved Count", ascending=False)
    )

    top_10 = full_result.head(10)
    top_item = full_result.iloc[0]

    return {
        "total_requests": int(full_result["Approved Count"].sum()),
        "top_item": top_item["Software"],
        "top_count": int(top_item["Approved Count"]),
        "total_categories": len(full_result),
        "pie_chart_data": [
            {
                "name": row["Software"],
                "tickets": int(row["Approved Count"])
            }
            for _, row in top_10.iterrows()
        ]
    }