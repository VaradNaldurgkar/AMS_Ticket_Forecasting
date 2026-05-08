import pandas as pd
import os

# ========================================================
# PATH SETUP
# ========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# api/services -> api -> src -> Backend
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(CURRENT_DIR)
    )
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "SR_Breakdown.csv"
)

# ========================================================
# LOAD CSV
# ========================================================

def load_service_breakdown():

    df = pd.read_csv(CSV_PATH)

    # ====================================================
    # KPI DATA
    # ====================================================

    total_tickets = int(
        df["Service_Request_Count"].sum()
    )

    top_ticket = (
        df.iloc[0]["Title"]
        if not df.empty else "N/A"
    )

    top_ticket_count = int(
        df.iloc[0]["Service_Request_Count"]
        if not df.empty else 0
    )

    total_categories = int(len(df))

    # ====================================================
    # PIE CHART DATA
    # ====================================================

    pie_chart_data = []

    top_5 = df.head(5)

    for _, row in top_5.iterrows():

        pie_chart_data.append({
            "name": row["Title"][:25],
            "tickets": int(row["Service_Request_Count"])
        })

    # ====================================================
    # BAR CHART DATA
    # ====================================================

    bar_chart_data = []

    for _, row in top_5.iterrows():

        bar_chart_data.append({
            "name": row["Title"][:20],
            "tickets": int(row["Service_Request_Count"])
        })

    # ====================================================
    # FINAL RESPONSE
    # ====================================================

    response = {

        "summary_cards": {

            "total_tickets": total_tickets,

            "top_ticket": top_ticket,

            "top_ticket_count": top_ticket_count,

            "total_categories": total_categories
        },

        "pie_chart_data": pie_chart_data,

        "bar_chart_data": bar_chart_data
    }

    return response