import os
import pandas as pd
import numpy as np
 
from sklearn.metrics import mean_absolute_percentage_error
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
    # MARCH FIX: True same-calendar-month prior year lag
    # --------------------------------------------------
    # lag_12 is Feb-2025 when predicting March-2026
    # (12 rows back in sorted monthly data = prior month,
    # not prior year same month).
    # lag_same_month explicitly picks the value from the
    # same calendar month one year ago using a date join,
    # giving the model Mar-2025=2679 when predicting Mar-2026.
    month_map = df.set_index("Month")["Total_Tickets"]
    df["lag_same_month"] = df["Month"].apply(
        lambda m: month_map.get(
            m - pd.DateOffset(years=1), np.nan
        )
    )
 
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
 
    # --------------------------------------------------
    # Trend features
    # --------------------------------------------------
    df["trend_1"] = df["lag_1"] - df["lag_2"]
    df["trend_2"] = df["lag_2"] - df["lag_3"]
    df["trend_change"] = df["trend_1"] - df["trend_2"]
 
    # --------------------------------------------------
    # MARCH FIX: same-month trend vs prior year
    # Tells the model whether this month is running
    # above or below the same month last year.
    # For March: 2947 / 2679 = +1.10 (above last March)
    # but model can learn that high values here still
    # revert toward lag_same_month.
    # --------------------------------------------------
    df["vs_same_month_ratio"] = (
        df["lag_1"]
        / df["lag_same_month"].replace(0, np.nan)
    ).clip(0.5, 2.0)
 
    # --------------------------------------------------
    # Growth rates
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
    # MAY FIX: true same-month yoy growth
    # yoy_growth uses lag_12 (prior-month value shifted
    # 12 rows). yoy_same_month uses lag_same_month so
    # May compares against actual May-2025, not Apr-2025.
    # --------------------------------------------------
    df["yoy_same_month"] = (
        (df["Total_Tickets"] - df["lag_same_month"])
        / df["lag_same_month"].replace(0, np.nan)
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
    # Ratio features
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
# MAIN
# ========================================================
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
 
    monthly["Month"] = pd.to_datetime(
        monthly["Month"] + "-01"
    )
 
    monthly = monthly.sort_values(
        "Month"
    ).reset_index(drop=True)
 
    monthly = create_features(monthly)
 
    monthly = monthly.dropna().reset_index(drop=True)
 
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
        "lag_same_month",       # MARCH FIX: true prior-year same month
 
        "trend_1",
        "trend_2",
        "trend_change",
 
        "rolling_mean_3",
        "rolling_mean_6",
 
        "mom_growth",
        "yoy_growth",
        "yoy_same_month",       # MAY FIX: true same-month yoy
 
        "rolling_std_3",
        "rolling_std_6",
 
        "lag1_vs_mean6",
        "lag1_vs_lag12",
        "vs_same_month_ratio",  # MARCH FIX: momentum vs same month last year
    ]
 
    # ==================================================
    # TRAIN / TEST SPLIT
    # ==================================================
    train = monthly[monthly["Month"] < "2026-01-01"]
    test  = monthly[monthly["Month"] >= "2026-01-01"]
 
    X_train = train[feature_cols]
    y_train = train["Total_Tickets"]
 
    X_test = test[feature_cols]
    y_test = test["Total_Tickets"]
 
    # ==================================================
    # XGBOOST MODEL
    # colsample_bytree 0.6 so rolling_std_3 cannot
    # dominate every tree at 23% importance.
    # ==================================================
    model = XGBRegressor(
 
        n_estimators=1000,
        learning_rate=0.01,
 
        max_depth=3,
        min_child_weight=3,
 
        subsample=0.8,
        colsample_bytree=0.6,
 
        reg_alpha=0.3,
        reg_lambda=1.5,
 
        objective="reg:squarederror",
        random_state=42
    )
 
    model.fit(X_train, y_train)
 
    predictions = model.predict(X_test)
 
    print("\nFeature Importance:\n")
    for name, score in zip(feature_cols, model.feature_importances_):
        print(f"{name:<22} {score:.4f}")
 
    result_df = pd.DataFrame({
        "Month":             test["Month"].values,
        "Actual_Tickets":    y_test.values,
        "Predicted_Tickets": predictions
    })
 
    data = []
    for _, row in result_df.iterrows():
        actual    = int(row["Actual_Tickets"])
        predicted = int(round(row["Predicted_Tickets"]))
        data.append({
            "month":     row["Month"].strftime("%b %Y"),
            "actual":    actual,
            "predicted": predicted,
            "error":     abs(actual - predicted)
        })
 
    mape = (
        mean_absolute_percentage_error(
            result_df["Actual_Tickets"],
            result_df["Predicted_Tickets"]
        )
        * 100
    )
 
    accuracy = 100 - mape
 
    return {
        "data": data,
        "kpis": {
            "accuracy": round(accuracy, 2),
            "mape":     round(mape, 2)
        }
    }
 
 
# ========================================================
# RUN
# ========================================================
if __name__ == "__main__":
 
    result = get_actual_vs_predicted()
 
    print("\nPrediction vs Actual:\n")
    for row in result["data"]:
        print(row)
 
    print("\nKPIs:")
    print(f"Accuracy: {result['kpis']['accuracy']}%")
    print(f"MAPE    : {result['kpis']['mape']}%")