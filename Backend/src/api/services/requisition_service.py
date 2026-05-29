import os
import pandas as pd

# ======================================================
# PATHS
# ======================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(CURRENT_DIR)
    )
)

PROCESSED_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed"
)

ASSET_FILE = os.path.join(
    PROCESSED_DIR,
    "Asset_Category_Count.csv"
)

SOFTWARE_FILE = os.path.join(
    PROCESSED_DIR,
    "Software_Category_Count.csv"
)

# ======================================================
# ASSET BREAKDOWN
# ======================================================

def get_asset_breakdown():

    if not os.path.exists(ASSET_FILE):

        return []

    df = pd.read_csv(
        ASSET_FILE
    )

    df = df.head(10)

    return [

        {
            "name": row["Asset Category"],
            "count": int(row["Count"])
        }

        for _, row in df.iterrows()

    ]

# ======================================================
# SOFTWARE BREAKDOWN
# ======================================================

def get_software_breakdown():

    if not os.path.exists(SOFTWARE_FILE):

        return []

    df = pd.read_csv(
        SOFTWARE_FILE
    )

    df = df.head(10)

    return [

        {
            "name": row["Software"],
            "count": int(
                row["Approved Count"]
            )
        }

        for _, row in df.iterrows()

    ]

# ======================================================
# ASSET DASHBOARD
# ======================================================

def get_asset_dashboard():

    if not os.path.exists(ASSET_FILE):

        return {}

    df = pd.read_csv(
        ASSET_FILE
    )

    total_requests = int(
        df["Count"].sum()
    )

    top_row = df.iloc[0]

    return {

        "total_requests":
            total_requests,

        "top_item":
            top_row["Asset Category"],

        "top_count":
            int(top_row["Count"]),

        "total_categories":
            len(df),

        "pie_chart_data": [

            {
                "name":
                    row["Asset Category"],

                "tickets":
                    int(row["Count"])
            }

            for _, row in df.head(10).iterrows()

        ]
    }

# ======================================================
# SOFTWARE DASHBOARD
# ======================================================

def get_software_dashboard():

    if not os.path.exists(SOFTWARE_FILE):

        return {}

    df = pd.read_csv(
        SOFTWARE_FILE
    )

    total_requests = int(
        df["Approved Count"].sum()
    )

    top_row = df.iloc[0]

    return {

        "total_requests":
            total_requests,

        "top_item":
            top_row["Software"],

        "top_count":
            int(
                top_row["Approved Count"]
            ),

        "total_categories":
            len(df),

        "pie_chart_data": [

            {
                "name":
                    row["Software"],

                "tickets":
                    int(
                        row["Approved Count"]
                    )
            }

            for _, row in df.head(10).iterrows()

        ]
    }