import os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_actual_vs_predicted():

    input_path = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "AMS_Yearly_Aggregated.csv"
    )

    df = pd.read_csv(input_path)

    df = df[df["Location"] == "Pune"].copy()

    monthly = (
        df.groupby("Month")["Total_Tickets"]
        .sum()
        .reset_index()
    )

    monthly["Month"] = pd.to_datetime(monthly["Month"] + "-01")
    monthly = monthly.sort_values("Month").reset_index(drop=True)

    monthly["Time_Index"] = np.arange(len(monthly))
    monthly["Month_Num"] = monthly["Month"].dt.month

    monthly["sin_month"] = np.sin(2 * np.pi * monthly["Month_Num"] / 12)
    monthly["cos_month"] = np.cos(2 * np.pi * monthly["Month_Num"] / 12)

    # Ensure Apr exists
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

    # Lag features
    monthly["Lag_1"] = monthly["Total_Tickets"].shift(1)
    monthly["Lag_2"] = monthly["Total_Tickets"].shift(2)
    monthly["Lag_3"] = monthly["Total_Tickets"].shift(3)

    train = monthly[monthly["Month"] < "2026-01-01"].dropna()

    features = [
        "Time_Index",
        "sin_month", "cos_month",
        "Lag_1", "Lag_2", "Lag_3"
    ]

    model = XGBRegressor(
        n_estimators=400,
        max_depth=4,
        learning_rate=0.07,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.5,
        reg_lambda=1.0,
        random_state=42
    )

    weights = np.linspace(1, 2.5, len(train))
    model.fit(train[features], train["Total_Tickets"], sample_weight=weights)

    # Prediction loop
    monthly["Predicted_Tickets"] = monthly["Total_Tickets"].astype(float)
    history = monthly.copy()

    forecast_start = pd.Timestamp("2026-01-01")

    for i in range(len(history)):

        if history.loc[i, "Month"] < forecast_start:
            continue

        lag_1 = history.loc[i-1, "Predicted_Tickets"]
        lag_2 = history.loc[i-2, "Predicted_Tickets"]
        lag_3 = history.loc[i-3, "Predicted_Tickets"]

        row = pd.DataFrame({
            "Time_Index": [history.loc[i, "Time_Index"]],
            "sin_month": [history.loc[i, "sin_month"]],
            "cos_month": [history.loc[i, "cos_month"]],
            "Lag_1": [lag_1],
            "Lag_2": [lag_2],
            "Lag_3": [lag_3]
        })

        pred = model.predict(row)[0]
        history.loc[i, "Predicted_Tickets"] = pred

    monthly["Predicted_Tickets"] = history["Predicted_Tickets"]

    # Extract Jan–Apr
    result_df = monthly[
        (monthly["Month"] >= "2026-01-01") &
        (monthly["Month"] <= "2026-04-01")
    ]

    # Convert to JSON
    data = []
    for _, row in result_df.iterrows():
        data.append({
            "month": row["Month"].strftime("%b %Y"),
            "actual": int(row["Total_Tickets"]) if not pd.isna(row["Total_Tickets"]) else None,
            "predicted": int(row["Predicted_Tickets"]),
            "error": float(abs(row["Total_Tickets"] - row["Predicted_Tickets"]))
        })

    # KPIs
    eval_window = result_df.iloc[:3]

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