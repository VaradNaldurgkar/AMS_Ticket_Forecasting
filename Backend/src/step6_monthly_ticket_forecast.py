import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ------------------------------------------------
# 1. Load aggregated monthly data
# ------------------------------------------------
input_path = "data/processed/AMS_Yearly_Aggregated.csv"
df = pd.read_csv(input_path)

# ------------------------------------------------
# 2. Filter ONLY Pune
# ------------------------------------------------
df = df[df["Location"] == "Pune"].copy()

# ------------------------------------------------
# 3. Prepare monthly totals (Pune only)
# ------------------------------------------------
monthly = (
    df.groupby("Month")["Total_Tickets"]
    .sum()
    .reset_index()
)

# Convert Month to datetime
monthly["Month"] = pd.to_datetime(monthly["Month"] + "-01")

# Sort and create time index
monthly = monthly.sort_values("Month").reset_index(drop=True)
monthly["Time_Index"] = np.arange(len(monthly))

# ------------------------------------------------
# 4. Train Linear Regression model
# ------------------------------------------------
X = monthly[["Time_Index"]]
y = monthly["Total_Tickets"]

model = LinearRegression()
model.fit(X, y)

# ------------------------------------------------
# 5. Forecast next 6 months
# ------------------------------------------------
N_FUTURE_MONTHS = 6

future_index = np.arange(
    monthly["Time_Index"].max() + 1,
    monthly["Time_Index"].max() + 1 + N_FUTURE_MONTHS
)

future_months = pd.date_range(
    start=monthly["Month"].max() + pd.offsets.MonthBegin(1),
    periods=N_FUTURE_MONTHS,
    freq="MS"
)

future_predictions = model.predict(
    future_index.reshape(-1, 1)
).round().astype(int)

# ------------------------------------------------
# 6. Create forecast DataFrame
# ------------------------------------------------
forecast_df = pd.DataFrame({
    "Month": future_months,
    "Predicted_Pune_Tickets": future_predictions
})

# ------------------------------------------------
# 7. Save forecast to PROJECT folder
# ------------------------------------------------
project_output_path = "data/processed/Pune_Monthly_Ticket_Forecast.csv"
forecast_df.to_csv(project_output_path, index=False)

# ------------------------------------------------
# 8. Save forecast directly to DESKTOP
# ------------------------------------------------
desktop_output_path = r"C:\Users\S08OFJF\Desktop\Pune_Monthly_Ticket_Forecast.csv"
forecast_df.to_csv(desktop_output_path, index=False)

# ------------------------------------------------
# 9. Output confirmation
# ------------------------------------------------
print("Pune-only monthly ticket forecast created")
print("Saved to project folder:", project_output_path)
print("Saved to Desktop:", desktop_output_path)
print("\nForecast Output:")
print(forecast_df)