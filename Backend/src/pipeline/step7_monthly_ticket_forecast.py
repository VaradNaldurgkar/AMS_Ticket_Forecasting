import os
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

# ========================================================
# PATH
# ========================================================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# ========================================================
# MAIN FUNCTION
# ========================================================
def get_future_forecast():

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
    # SARIMA MODEL
    # ----------------------------------------------------
    model = SARIMAX(
        monthly["Total_Tickets"],
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    model_fit = model.fit(disp=False)

    # ----------------------------------------------------
    # FORECAST (🔴 CHANGED TO 3)
    # ----------------------------------------------------
    N_FUTURE_MONTHS = 3
    forecast = model_fit.forecast(steps=N_FUTURE_MONTHS)

    # ----------------------------------------------------
    # SEASON-AWARE STABILIZATION
    # ----------------------------------------------------
    history = list(monthly["Total_Tickets"].values)
    final_forecast = []

    for i in range(N_FUTURE_MONTHS):

        pred_model = forecast.iloc[i]
        lag1 = history[-1]

        # seasonal anchor
        if len(history) >= 12:
            seasonal_anchor = history[-12]
        else:
            seasonal_anchor = lag1

        # blend
        pred = (
            0.6 * pred_model +
            0.25 * lag1 +
            0.15 * seasonal_anchor
        )

        # caps
        upper_cap = seasonal_anchor * 1.08
        lower_cap = seasonal_anchor * 0.92

        pred = max(min(pred, upper_cap), lower_cap)

        history.append(pred)
        final_forecast.append(int(pred))

    # ----------------------------------------------------
    # FUTURE DATES
    # ----------------------------------------------------
    future_months = pd.date_range(
        start=monthly["Month"].max() + pd.offsets.MonthBegin(1),
        periods=N_FUTURE_MONTHS,
        freq="MS"
    )

    result = []

    for m, p in zip(future_months, final_forecast):
        result.append({
            "month": m.strftime("%b %Y"),
            "predicted": int(p)
        })

    return result


# ========================================================
# RUN SCRIPT
# ========================================================
if __name__ == "__main__":

    print("\nRunning 3-Month Forecast...\n")

    forecast = get_future_forecast()

    print("Next 3 Months Prediction:\n")

    for row in forecast:
        print(row)