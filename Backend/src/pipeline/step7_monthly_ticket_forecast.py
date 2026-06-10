import os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor

# ========================================================
# PATH
# ========================================================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# ========================================================
# FEATURE ENGINEERING
# ========================================================
def create_features(df):

    df = df.copy()

    df["month_num"] = df["Month"].dt.month

    df["month_sin"] = np.sin(
        2 * np.pi * df["month_num"] / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * df["month_num"] / 12
    )

    df["quarter"] = df["Month"].dt.quarter

    # --------------------------------------------------
    # Lags
    # --------------------------------------------------
    df["lag_1"]  = df["Total_Tickets"].shift(1)
    df["lag_2"]  = df["Total_Tickets"].shift(2)
    df["lag_3"]  = df["Total_Tickets"].shift(3)
    df["lag_6"]  = df["Total_Tickets"].shift(6)
    df["lag_12"] = df["Total_Tickets"].shift(12)

    # --------------------------------------------------
    # Trends
    # --------------------------------------------------
    df["trend_1"]      = df["lag_1"] - df["lag_2"]
    df["trend_2"]      = df["lag_2"] - df["lag_3"]
    df["trend_change"] = df["trend_1"] - df["trend_2"]

    # --------------------------------------------------
    # Rolling averages
    # --------------------------------------------------
    df["rolling_mean_3"] = (
        df["Total_Tickets"]
        .shift(1)
        .rolling(3)
        .mean()
    )

    df["rolling_mean_6"] = (
        df["Total_Tickets"]
        .shift(1)
        .rolling(6)
        .mean()
    )

    df["rolling_mean_12"] = (
        df["Total_Tickets"]
        .shift(1)
        .rolling(12)
        .mean()
    )

    # --------------------------------------------------
    # Growth rates — FIX: guard against div/0 and inf
    # --------------------------------------------------
    df["mom_growth"] = (
        (df["lag_1"] - df["lag_2"])
        / df["lag_2"].replace(0, np.nan)
    ).clip(-2, 2)

    df["yoy_growth"] = (
        (df["lag_1"] - df["lag_12"])
        / df["lag_12"].replace(0, np.nan)
    ).clip(-2, 2)

    # --------------------------------------------------
    # Volatility
    # --------------------------------------------------
    df["rolling_std_3"] = (
        df["Total_Tickets"]
        .shift(1)
        .rolling(3)
        .std()
    )

    df["rolling_std_6"] = (
        df["Total_Tickets"]
        .shift(1)
        .rolling(6)
        .std()
    )

    # --------------------------------------------------
    # Ratio features — seasonal context
    # --------------------------------------------------
    df["lag1_vs_mean6"] = (
        df["lag_1"]
        / df["rolling_mean_6"].replace(0, np.nan)
    )

    df["lag1_vs_lag12"] = (
        df["lag_1"]
        / df["lag_12"].replace(0, np.nan)
    )

    return df


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

    # --------------------------------------------------
    # Pune only
    # --------------------------------------------------
    df = df[df["Location"] == "Pune"].copy()

    # --------------------------------------------------
    # Monthly aggregation
    # --------------------------------------------------
    monthly = (
        df.groupby("Month")["Total_Tickets"]
        .sum()
        .reset_index()
    )

    monthly["Month"] = pd.to_datetime(
        monthly["Month"] + "-01"
    )

    monthly = monthly.sort_values(
        "Month"
    ).reset_index(drop=True)

    print("\nHistorical Monthly Data:\n")
    print(monthly.tail(12))

    # --------------------------------------------------
    # FEATURE DATASET
    # --------------------------------------------------
    feature_df = create_features(monthly)

    feature_df = feature_df.dropna().reset_index(drop=True)

    feature_cols = [
        "month_num",
        "month_sin",
        "month_cos",
        "quarter",

        "lag_1",
        "lag_2",
        "lag_3",
        "lag_6",
        "lag_12",

        "trend_1",
        "trend_2",
        "trend_change",

        "rolling_mean_3",
        "rolling_mean_6",   # added
        "rolling_mean_12",  # added

        "mom_growth",
        "yoy_growth",

        "rolling_std_3",
        "rolling_std_6",    # added

        "lag1_vs_mean6",    # new ratio
        "lag1_vs_lag12",    # new ratio
    ]

    X_train = feature_df[feature_cols]
    y_train = feature_df["Total_Tickets"]

    # --------------------------------------------------
    # MODEL
    # --------------------------------------------------
    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.03,

        max_depth=3,           # was 3 — kept
        min_child_weight=3,    # was 5 — relaxed

        subsample=0.8,
        colsample_bytree=0.8,

        reg_alpha=0.3,         # relaxed
        reg_lambda=1.5,        # relaxed

        objective="reg:squarederror",
        random_state=42
    )

    model.fit(X_train, y_train)

    print("\nFeature Importance:\n")

    for name, score in zip(
        feature_cols,
        model.feature_importances_
    ):
        print(f"{name:<20} {score:.4f}")

    # --------------------------------------------------
    # FORECAST NEXT 3 MONTHS
    # --------------------------------------------------
    N_FUTURE_MONTHS = 3

    history = monthly.copy()

    predictions = []

    for _ in range(N_FUTURE_MONTHS):

        next_month = (
            history["Month"].max()
            + pd.offsets.MonthBegin(1)
        )

        lag_1  = history["Total_Tickets"].iloc[-1]
        lag_2  = history["Total_Tickets"].iloc[-2]
        lag_3  = history["Total_Tickets"].iloc[-3]
        lag_6  = history["Total_Tickets"].iloc[-6]
        lag_12 = history["Total_Tickets"].iloc[-12]

        trend_1      = lag_1 - lag_2
        trend_2      = lag_2 - lag_3
        trend_change = trend_1 - trend_2

        rolling_mean_3 = (
            history["Total_Tickets"].iloc[-3:].mean()
        )

        rolling_mean_6 = (
            history["Total_Tickets"].iloc[-6:].mean()
        )

        rolling_mean_12 = (
            history["Total_Tickets"].iloc[-12:].mean()
        )

        rolling_std_3 = (
            history["Total_Tickets"].iloc[-3:].std()
        )

        rolling_std_6 = (
            history["Total_Tickets"].iloc[-6:].std()
        )

        # FIX: guard against div/0 and inf
        mom_growth = (
            np.clip((lag_1 - lag_2) / lag_2, -2, 2)
            if lag_2 != 0 else 0.0
        )

        yoy_growth = (
            np.clip((lag_1 - lag_12) / lag_12, -2, 2)
            if lag_12 != 0 else 0.0
        )

        lag1_vs_mean6 = (
            lag_1 / rolling_mean_6
            if rolling_mean_6 != 0 else 1.0
        )

        lag1_vs_lag12 = (
            lag_1 / lag_12
            if lag_12 != 0 else 1.0
        )

        month_sin = np.sin(
            2 * np.pi * next_month.month / 12
        )

        month_cos = np.cos(
            2 * np.pi * next_month.month / 12
        )

        X_future = pd.DataFrame([{
            "month_num":      next_month.month,
            "month_sin":      month_sin,
            "month_cos":      month_cos,
            "quarter":        next_month.quarter,

            "lag_1":          lag_1,
            "lag_2":          lag_2,
            "lag_3":          lag_3,
            "lag_6":          lag_6,
            "lag_12":         lag_12,

            "trend_1":        trend_1,
            "trend_2":        trend_2,
            "trend_change":   trend_change,

            "rolling_mean_3":  rolling_mean_3,
            "rolling_mean_6":  rolling_mean_6,
            "rolling_mean_12": rolling_mean_12,

            "mom_growth":     mom_growth,
            "yoy_growth":     yoy_growth,

            "rolling_std_3":  rolling_std_3,
            "rolling_std_6":  rolling_std_6,

            "lag1_vs_mean6":  lag1_vs_mean6,
            "lag1_vs_lag12":  lag1_vs_lag12,
        }])

        pred = model.predict(X_future)[0]

        # ------------------------------------------
        # Trend adjustment
        # ------------------------------------------
        trend = lag_1 - lag_2

        pred = (
            0.90 * pred
            + 0.10 * (lag_1 + trend)
        )

        # ------------------------------------------
        # Safety bounds
        # ------------------------------------------
        upper_limit = lag_1 * 1.15
        lower_limit = lag_1 * 0.85

        pred = max(
            lower_limit,
            min(pred, upper_limit)
        )

        predictions.append(int(round(pred)))

        history.loc[len(history)] = [
            next_month,
            pred
        ]

    # --------------------------------------------------
    # BUILD RESULT
    # --------------------------------------------------
    future_months = pd.date_range(
        start=monthly["Month"].max()
        + pd.offsets.MonthBegin(1),
        periods=N_FUTURE_MONTHS,
        freq="MS"
    )

    result = []

    for m, p in zip(future_months, predictions):
        result.append({
            "month":     m.strftime("%b %Y"),
            "predicted": int(p)
        })

    return result


# ========================================================
# RUN
# ========================================================
if __name__ == "__main__":

    print("\nRunning XGBoost Forecast...\n")

    forecast = get_future_forecast()

    print("\nNext 3 Months Prediction:\n")

    for row in forecast:
        print(row)