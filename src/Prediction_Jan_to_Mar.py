import os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error

# --------------------------------------------------
# 1. Load data
# --------------------------------------------------
df = pd.read_csv("data/processed/AMS_Yearly_Aggregated.csv")

# --------------------------------------------------
# 2. Filter Pune
# --------------------------------------------------
df = df[df["Location"] == "Pune"].copy()

# --------------------------------------------------
# 3. Monthly aggregation
# --------------------------------------------------
monthly = (
    df.groupby("Month")["Total_Tickets"]
    .sum()
    .reset_index()
)

monthly["Month"] = pd.to_datetime(monthly["Month"] + "-01")
monthly = monthly.sort_values("Month").reset_index(drop=True)

monthly["Time_Index"] = np.arange(len(monthly))
monthly["Month_Num"] = monthly["Month"].dt.month

# --------------------------------------------------
# 4. Seasonality
# --------------------------------------------------
monthly["sin_month"] = np.sin(2 * np.pi * monthly["Month_Num"] / 12)
monthly["cos_month"] = np.cos(2 * np.pi * monthly["Month_Num"] / 12)

# --------------------------------------------------
# 5. Lag features
# --------------------------------------------------
monthly["Lag_1"] = monthly["Total_Tickets"].shift(1)
monthly["Lag_2"] = monthly["Total_Tickets"].shift(2)
monthly["Lag_3"] = monthly["Total_Tickets"].shift(3)

monthly = monthly.dropna().reset_index(drop=True)

# --------------------------------------------------
# 6. Train data
# --------------------------------------------------
train = monthly[monthly["Month"] < "2026-01-01"].copy()

features = [
    "Time_Index",
    "sin_month", "cos_month",
    "Lag_1", "Lag_2", "Lag_3"
]

# --------------------------------------------------
# 7. Model
# --------------------------------------------------
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

# --------------------------------------------------
# 🔥 8. CONTROLLED RECURSION (CORRECT)
# --------------------------------------------------
monthly["Predicted_Tickets"] = monthly["Total_Tickets"].astype(float)
history = monthly.copy()

for i in range(len(history)):

    if history.loc[i, "Month"] < pd.Timestamp("2026-01-01"):
        continue

    current_month = history.loc[i, "Month"]

    # Jan
    if current_month == pd.Timestamp("2026-01-01"):
        lag_1 = history.loc[i-1, "Total_Tickets"]
        lag_2 = history.loc[i-2, "Total_Tickets"]
        lag_3 = history.loc[i-3, "Total_Tickets"]

    # Feb
    elif current_month == pd.Timestamp("2026-02-01"):
        lag_1 = history.loc[i-1, "Predicted_Tickets"]  # Jan pred
        lag_2 = history.loc[i-2, "Total_Tickets"]
        lag_3 = history.loc[i-3, "Total_Tickets"]

    # Mar
    else:
        lag_1 = history.loc[i-1, "Predicted_Tickets"]  # Feb pred
        lag_2 = history.loc[i-2, "Predicted_Tickets"]  # Jan pred
        lag_3 = history.loc[i-3, "Total_Tickets"]

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

# --------------------------------------------------
# 9. Error
# --------------------------------------------------
monthly["Absolute_Error"] = abs(
    monthly["Total_Tickets"] - monthly["Predicted_Tickets"]
)

# --------------------------------------------------
# 10. Save
# --------------------------------------------------
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "Final_3Month_Forecast_FIXED.csv")

monthly["Predicted_Tickets"] = monthly["Predicted_Tickets"].round().astype(int)
monthly.to_csv(output_path, index=False)

print(f"\n✅ Forecast saved to: {output_path}")

# --------------------------------------------------
# 11. Display
# --------------------------------------------------
print("\nPrediction vs Actual (Jan 2025 – Mar 2026)")
print(
    monthly[
        (monthly["Month"] >= "2026-01-01") &
        (monthly["Month"] <= "2026-03-01")
    ][["Month", "Total_Tickets", "Predicted_Tickets", "Absolute_Error"]]
)

# --------------------------------------------------
# 12. MAPE
# --------------------------------------------------
eval_window = monthly[
    (monthly["Month"] >= "2026-01-01") &
    (monthly["Month"] <= "2026-03-01")
]

MAPE = mean_absolute_percentage_error(
    eval_window["Total_Tickets"],
    eval_window["Predicted_Tickets"]
) * 100

print(f"\n✅ MAPE (Jan–Mar 2026): {MAPE:.2f}%")
print(f"✅ Model Accuracy     : {100 - MAPE:.2f}%")