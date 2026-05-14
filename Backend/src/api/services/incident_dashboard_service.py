import pandas as pd
import os

# ========================================================
# PATH SETUP
# ========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "Incident_Resolution_Metrics.csv"
)

# ========================================================
# LOAD INCIDENT DASHBOARD DATA
# ========================================================

def load_incident_dashboard_data():

    df = pd.read_csv(CSV_PATH)

    # ====================================================
    # SUMMARY CARDS
    # ====================================================

    total_incidents = int(
        df["Incident_Count"].sum()
    )

    top_row = df.iloc[0]

    top_incident = top_row["Incident_Type"]

    top_incident_count = int(
        top_row["Incident_Count"]
    )

    total_categories = int(len(df))

    # ====================================================
    # CHART DATA (TOP 5)
    # ====================================================

    top_5 = df.head(5)

    chart_data = []

    for _, row in top_5.iterrows():

        chart_data.append({

            "name": row["Incident_Type"],

            "tickets": int(
                row["Incident_Count"]
            )
        })

    # ====================================================
    # TABLE DATA
    # ====================================================

    table_data = []

    for _, row in df.head(15).iterrows():

        table_data.append({

            "incident_type": row["Incident_Type"],

            "incident_count": int(
                row["Incident_Count"]
            ),

            "avg_resolution_hours": round(
                float(row["Avg_Resolution_Hours"]),
                2
            ),

            "median_resolution_hours": round(
                float(row["Median_Resolution_Hours"]),
                2
            )
        })

    # ====================================================
    # FINAL RESPONSE
    # ====================================================

    response = {

        "summary_cards": {

            "total_incidents": total_incidents,

            "top_incident": top_incident,

            "top_incident_count": top_incident_count,

            "total_categories": total_categories
        },

        "chart_data": chart_data,

        "table_data": table_data
    }

    return response