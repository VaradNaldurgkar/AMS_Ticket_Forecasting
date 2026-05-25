import pandas as pd
import os

# ========================================================
# PATH
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
    "Forecast_Evaluation.csv"
)

# ========================================================
# MAIN
# ========================================================

def get_forecast_evaluation():

    df = pd.read_csv(CSV_PATH)

    data = []

    for _, row in df.iterrows():

        data.append({
            "month": row["Month"],
            "actual": int(row["Actual"]),
            "predicted": int(row["Predicted"]),
            "error": int(row["Error"]),
            "error_percentage": float(row["Error_Percentage"])
        })

    return {
        "data": data
    }