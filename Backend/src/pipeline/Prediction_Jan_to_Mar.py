import os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error

# ========================================================
# PATH SETUP
# ========================================================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# ========================================================
# HELPER
# ========================================================
def safe_lag(history, idx):
    val = history.loc[idx, "Total_Tickets"]
    if not pd.isna(val):
        return val
    return history.loc[idx, "Predicted_Tickets"]

# ========================================================
# MAIN FUNCTION
# ========================================================
def get_actual_vs_predicted():

    input_path = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "AMS_Yearly_Aggregated.csv"
    )

    df = pd.read_csv(input_path)

    # ----------------------------------------------------
    # Filter Pune
    # ----------------------------------------------------
    df = df[df["Location"] == "Pune"].copy()

    # ----------------------------------------------------
    # Monthly aggregation
    # ----------------------------------------------------
    monthly = (
        df.groupby("Month")["Total_Tickets"]
        .sum()
        .reset_index()
    )

    monthly["Month"] = pd.to_datetime(monthly["Month"] + "-01")
    monthly = monthly.sort_values("Month").reset_index(drop=True)

    # ----------------------------------------------------
    # Time + seasonality
    # ----------------------------------------------------
    monthly["Time_Index"] = np.arange(len(monthly))
    monthly["Month_Num"] = monthly["Month"].dt.month

    monthly["sin_month"] = np.sin(2 * np.pi * monthly["Month_Num"] / 12)
    monthly["cos_month"] = np.cos(2 * np.pi * monthly["Month_Num"] / 12)

    # ----------------------------------------------------
    # Extend till April 2026
    # ----------------------------------------------------
    last_date = monthly["Month"].max()

    while last_date < pd.Timestamp("2026-04-01"):
        next_month = last_date + pd.DateOffset(months=1)

        new_row = {
            "Month": next_month,
            "Total_Tickets": np.nan,
            "Time_Index": monthly["Time_Index"].max() + 1,
            "Month_Num": next_month.month
        }

        monthly = pd.concat([monthly, pd.DataFrame([new_row])], ignore_index=True)
        last_date = next_month

    # recompute seasonality
    monthly["sin_month"] = np.sin(2 * np.pi * monthly["Month_Num"] / 12)
    monthly["cos_month"] = np.cos(2 * np.pi * monthly["Month_Num"] / 12)

    # ----------------------------------------------------
    # ✅ FINAL FEATURES
    # ----------------------------------------------------
    monthly["Lag_1"] = monthly["Total_Tickets"].shift(1)
    monthly["Lag_2"] = monthly["Total_Tickets"].shift(2)
    monthly["Lag_3"] = monthly["Total_Tickets"].shift(3)
    monthly["Lag_6"] = monthly["Total_Tickets"].shift(6)

    # ----------------------------------------------------
    # TRAIN DATA
    # ----------------------------------------------------
    train = monthly[monthly["Month"] < "2026-01-01"].dropna()

    features = [
        "Time_Index",
        "sin_month",
        "cos_month",
        "Lag_1",
        "Lag_2",
        "Lag_3",
        "Lag_6"
    ]

    # ----------------------------------------------------
    # ✅ FINAL MODEL
    # ----------------------------------------------------
    model = XGBRegressor(
        n_estimators=180,
        max_depth=2,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=1.5,
        reg_lambda=2.5,
        random_state=42
    )

    weights = np.linspace(1.0, 3.0, len(train))

    model.fit(train[features], train["Total_Tickets"], sample_weight=weights)

    # ----------------------------------------------------
    # WALK-FORWARD
    # ----------------------------------------------------
    monthly["Predicted_Tickets"] = monthly["Total_Tickets"].astype(float)
    history = monthly.copy()

    forecast_start = pd.Timestamp("2026-01-01")

    for i in range(len(history)):

        if history.loc[i, "Month"] < forecast_start:
            continue

        lag1 = safe_lag(history, i-1)
        lag2 = safe_lag(history, i-2)
        lag3 = safe_lag(history, i-3)
        lag6 = safe_lag(history, i-6)

        row = pd.DataFrame({
            "Time_Index": [history.loc[i, "Time_Index"]],
            "sin_month": [history.loc[i, "sin_month"]],
            "cos_month": [history.loc[i, "cos_month"]],
            "Lag_1": [lag1],
            "Lag_2": [lag2],
            "Lag_3": [lag3],
            "Lag_6": [lag6]
        })

        pred = model.predict(row)[0]

        # 🔥 CRITICAL FIX: SMOOTHING
        pred = 0.7 * pred + 0.3 * lag1

        history.loc[i, "Predicted_Tickets"] = pred

    monthly["Predicted_Tickets"] = history["Predicted_Tickets"]

    # ----------------------------------------------------
    # OUTPUT
    # ----------------------------------------------------
    result_df = monthly[
        (monthly["Month"] >= "2026-01-01") &
        (monthly["Month"] <= "2026-04-01")
    ]

    data = []
    for _, row in result_df.iterrows():
        data.append({
            "month": row["Month"].strftime("%b %Y"),
            "actual": int(row["Total_Tickets"]) if not pd.isna(row["Total_Tickets"]) else None,
            "predicted": int(row["Predicted_Tickets"]),
            "error": (
                float(abs(row["Total_Tickets"] - row["Predicted_Tickets"]))
                if not pd.isna(row["Total_Tickets"])
                else None
            )
        })

    eval_window = result_df.iloc[:3].dropna()

    mape = mean_absolute_percentage_error(
        eval_window["Total_Tickets"],
        eval_window["Predicted_Tickets"]
    ) * 100

    accuracy = 100 - mape

    return {
        "data": data,
        "kpis": {
            "accuracy": round(accuracy, 2),
            "mape": round(mape, 2)
        }
    }


# ========================================================
# RUN
# ========================================================
if __name__ == "__main__":
    result = get_actual_vs_predicted()

    print("\nPrediction vs Actual (Jan–Apr 2026):\n")
    for row in result["data"]:
        print(row)

    print("\nKPIs:")
    print(f"Accuracy: {result['kpis']['accuracy']}%")
    print(f"MAPE    : {result['kpis']['mape']}%")