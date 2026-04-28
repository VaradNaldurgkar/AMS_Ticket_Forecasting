import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_future_forecast():

    input_path = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "AMS_Yearly_Aggregated.csv"
    )

    df = pd.read_csv(input_path)

    # Filter Pune
    df = df[df["Location"] == "Pune"].copy()

    # Monthly aggregation
    monthly = (
        df.groupby("Month")["Total_Tickets"]
        .sum()
        .reset_index()
    )

    monthly["Month"] = pd.to_datetime(monthly["Month"] + "-01")
    monthly = monthly.sort_values("Month").reset_index(drop=True)
    monthly["Time_Index"] = np.arange(len(monthly))

    # Train model
    X = monthly[["Time_Index"]]
    y = monthly["Total_Tickets"]

    model = LinearRegression()
    model.fit(X, y)

    # Forecast
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

    # Convert to JSON-friendly format
    result = []

    for m, p in zip(future_months, future_predictions):
        result.append({
            "month": m.strftime("%b %Y"),
            "predicted": int(p)
        })

    return result