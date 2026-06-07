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
    df["year"] = df["Month"].dt.year

    # Short-term memory
    df["lag_1"] = df["Total_Tickets"].shift(1)
    df["lag_2"] = df["Total_Tickets"].shift(2)
    df["lag_3"] = df["Total_Tickets"].shift(3)
    df["lag_6"] = df["Total_Tickets"].shift(6)

    # Same month previous year
    df["lag_12"] = df["Total_Tickets"].shift(12)

    # Rolling averages
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

    # Month-over-month growth
    df["mom_growth"] = (
        (df["lag_1"] - df["lag_2"])
        / df["lag_2"]
    )

    # Year-over-year growth
    df["yoy_growth"] = (
        (df["lag_1"] - df["lag_12"])
        / df["lag_12"]
    )

    df["trend_1"] = (
    df["lag_1"] - df["lag_2"]
)

    df["trend_2"] = (
    df["lag_2"] - df["lag_3"]
)

    df["trend_change"] = (
    df["trend_1"] - df["trend_2"]
)

    # Volatility
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

    # ----------------------------------------------------
    # Pune only
    # ----------------------------------------------------
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

    # ====================================================
    # FEATURES
    # ====================================================
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

    "trend_1",
    "trend_2",
    "trend_change",

    "rolling_mean_3",

    "mom_growth",
    "yoy_growth",

    "rolling_std_3"
]

    # ====================================================
    # TRAIN DATA
    # ====================================================
    train = monthly[
        monthly["Month"] < "2026-01-01"
    ]

    # ====================================================
    # TEST DATA
    # Automatically includes all available
    # months from Jan 2026 onward
    # ====================================================
    test = monthly[
        monthly["Month"] >= "2026-01-01"
    ]

    X_train = train[feature_cols]
    y_train = train["Total_Tickets"]

    X_test = test[feature_cols]
    y_test = test["Total_Tickets"]

    # ====================================================
    # XGBOOST MODEL
    # ====================================================
    model = XGBRegressor(

    n_estimators=1000,
    learning_rate=0.01,

    max_depth=2,
    min_child_weight=5,

    subsample=0.8,
    colsample_bytree=0.8,

    reg_alpha=0.5,
    reg_lambda=2,

    objective="reg:squarederror",

    random_state=42
)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nFeature Importance:\n")

    for name, score in zip(
    feature_cols,
    model.feature_importances_
    ):
        
       print(
        f"{name:<20} {score:.4f}"
    )

    # ====================================================
    # RESULT DATAFRAME
    # ====================================================
    result_df = pd.DataFrame({
        "Month": test["Month"].values,
        "Actual_Tickets": y_test.values,
        "Predicted_Tickets": predictions
    })

    # ====================================================
    # RESPONSE DATA
    # ====================================================
    data = []

    for _, row in result_df.iterrows():

        actual = int(row["Actual_Tickets"])
        predicted = int(round(row["Predicted_Tickets"]))

        data.append({
            "month": row["Month"].strftime("%b %Y"),
            "actual": actual,
            "predicted": predicted,
            "error": abs(actual - predicted)
        })

    # ====================================================
    # KPI
    # ====================================================
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
            "mape": round(mape, 2)
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
    print(
        f"Accuracy: {result['kpis']['accuracy']}%"
    )
    print(
        f"MAPE    : {result['kpis']['mape']}%"
    )