import pandas as pd
import os

# ========================================================
# PATHS
# ========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "Forecast_Evaluation.csv"
)

# ========================================================
# MANUAL MONTHLY EVALUATION DATA
# ========================================================

data = [
    {
        "Month": "Jan 2026",
        "Actual": 2774,
        "Predicted": 2838
    },
    {
        "Month": "Feb 2026",
        "Actual": 2947,
        "Predicted": 2863
    },
    {
        "Month": "Mar 2026",
        "Actual": 2672,
        "Predicted": 2871
    },
    {
        "Month": "Apr 2026",
        "Actual": 2960,
        "Predicted": 2941
    }
]

# ========================================================
# DATAFRAME
# ========================================================

df = pd.DataFrame(data)

# ========================================================
# ERROR CALCULATION
# ========================================================

df["Error"] = abs(
    df["Actual"] - df["Predicted"]
)

df["Error_Percentage"] = (
    df["Error"] / df["Actual"] * 100
).round(2)

# ========================================================
# SAVE CSV
# ========================================================

df.to_csv(OUTPUT_PATH, index=False)

# ========================================================
# LOGS
# ========================================================

print("\n✅ Forecast Evaluation CSV Created")

print(f"\nSaved to:\n{OUTPUT_PATH}")

print("\nPreview:\n")

print(df)