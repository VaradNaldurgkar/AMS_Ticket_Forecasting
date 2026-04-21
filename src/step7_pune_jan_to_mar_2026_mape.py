import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error

# --------------------------------------------------
# 1. Load aggregated data
# --------------------------------------------------
df = pd.read_csv("data/processed/AMS_Yearly_Aggregated.csv")

# --------------------------------------------------
# 2. Filter Pune only
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

# Create time index
monthly["Time_Index"] = np.arange(len(monthly))

# --------------------------------------------------
# 4. Train / Test split
#    Train : Jan 2025 – Dec 2025
#    Test  : Jan 2026 – Mar 2026
# --------------------------------------------------
train = monthly[monthly["Month"] < "2026-01-01"]
test = monthly[
    (monthly["Month"] >= "2026-01-01") &
    (monthly["Month"] <= "2026-03-01")
].copy()

X_train = train[["Time_Index"]]
y_train = train["Total_Tickets"]

X_test = test[["Time_Index"]]
y_test = test["Total_Tickets"]

# --------------------------------------------------
# 5. Train Linear Regression model
# --------------------------------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# --------------------------------------------------
# 6. Predict 2026 months
# --------------------------------------------------
test["Predicted_Tickets"] = (
    model.predict(X_test).round().astype(int)
)

test["Absolute_Error"] = abs(
    test["Total_Tickets"] - test["Predicted_Tickets"]
)

# --------------------------------------------------
# 7. Save forecast to Desktop as CSV ✅
# --------------------------------------------------
desktop_output_path = (
    r"C:\Users\S08OFJF\Desktop\Pune_Monthly_Ticket_Forecast.csv"
)

test.to_csv(desktop_output_path, index=False)

print(f"\n✅ Forecast saved to: {desktop_output_path}")

# --------------------------------------------------
# 8. Display prediction vs actual
# --------------------------------------------------
print("\nPrediction vs Actual (Jan–Mar 2026)")
print(
    test[
        ["Month", "Total_Tickets", "Predicted_Tickets", "Absolute_Error"]
    ]
)

# --------------------------------------------------
# 9. MAPE calculation (FULL MONTHS ONLY)
# --------------------------------------------------
MAPE = mean_absolute_percentage_error(
    test["Total_Tickets"],
    test["Predicted_Tickets"]
) * 100

Accuracy = 100 - MAPE

print(f"\nMAPE (Jan–Mar 2026): {MAPE:.2f}%")
print(f"Model Accuracy     : {Accuracy:.2f}%")