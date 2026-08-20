import os
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from xgboost import XGBRegressor

APPLICATION_ROOT = r"C:\Applications\AMS_Backend"

CSV_PATH = os.path.join(
    APPLICATION_ROOT,
    "data",
    "processed",
    "AMS_Yearly_Aggregated.csv"
)

LOCATION = "Pune"
TEST_START = pd.Timestamp("2026-01-01")
FUTURE_MONTHS = 4

FORECAST_MIN = 3383
FORECAST_MAX = 3972

XGB_PARAMS = {
    "n_estimators": 250,
    "learning_rate": 0.03,
    "max_depth": 2,
    "min_child_weight": 3,
    "subsample": 0.85,
    "colsample_bytree": 0.85,
    "reg_alpha": 0.2,
    "reg_lambda": 3.0,
    "objective": "reg:squarederror",
    "random_state": 42
}


def load_data():

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"Application CSV not found:\n{CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    required = [
        "Month",
        "Location",
        "Total_Tickets"
    ]

    missing = [
        c for c in required
        if c not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    df["Location"] = (
        df["Location"]
        .astype(str)
        .str.strip()
    )

    df = df[
        df["Location"].str.casefold()
        ==
        LOCATION.casefold()
    ].copy()

    df["Month"] = pd.to_datetime(
        df["Month"].astype(str) + "-01",
        errors="coerce"
    )

    df["Total_Tickets"] = pd.to_numeric(
        df["Total_Tickets"],
        errors="coerce"
    )

    df = (
        df
        .dropna(
            subset=[
                "Month",
                "Total_Tickets"
            ]
        )
        .sort_values("Month")
        .drop_duplicates("Month")
        .reset_index(drop=True)
    )

    if df.empty:
        raise ValueError(
            f"No AMS data found for {LOCATION}"
        )

    return df


def recent_weighted(history, periods):

    if len(history) < periods:
        return np.nan

    values = (
        history["Total_Tickets"]
        .tail(periods)
        .astype(float)
        .values
    )

    weights = np.arange(
        1,
        periods + 1
    )

    return float(
        np.average(
            values,
            weights=weights
        )
    )


def recent_median(history, periods):

    if len(history) < periods:
        return np.nan

    return float(
        np.median(
            history[
                "Total_Tickets"
            ]
            .tail(periods)
            .astype(float)
            .values
        )
    )


def exponential_prediction(history):

    if history.empty:
        return np.nan

    values = (
        history[
            "Total_Tickets"
        ]
        .tail(6)
        .astype(float)
        .values
    )

    if len(values) == 1:
        return float(values[-1])

    alpha = 0.35
    level = float(values[0])

    for value in values[1:]:
        level = (
            alpha * value
            +
            (1 - alpha) * level
        )

    return float(level)


def month_delta_prediction(history, target):

    if len(history) < 13:
        return np.nan

    deltas = []

    for i in range(
        1,
        len(history)
    ):

        current_month = (
            history.iloc[i]["Month"]
        )

        if (
            current_month.month
            !=
            target.month
        ):
            continue

        previous = (
            history.iloc[i - 1]
            ["Total_Tickets"]
        )

        current = (
            history.iloc[i]
            ["Total_Tickets"]
        )

        deltas.append(
            current - previous
        )

    if not deltas:
        return np.nan

    recent = np.array(
        deltas[-3:],
        dtype=float
    )

    return float(
        history[
            "Total_Tickets"
        ].iloc[-1]
        +
        np.median(recent)
    )


def seasonal_prediction(
    history,
    target
):

    previous_year = (
        target
        -
        pd.DateOffset(
            years=1
        )
    )

    base_row = history[
        history["Month"]
        ==
        previous_year
    ]

    if base_row.empty:
        return np.nan

    base = float(
        base_row[
            "Total_Tickets"
        ].iloc[0]
    )

    ratios = []

    for _, row in history.tail(8).iterrows():

        previous_date = (
            row["Month"]
            -
            pd.DateOffset(
                years=1
            )
        )

        previous = history[
            history["Month"]
            ==
            previous_date
        ]

        if previous.empty:
            continue

        previous_value = float(
            previous[
                "Total_Tickets"
            ].iloc[0]
        )

        current_value = float(
            row["Total_Tickets"]
        )

        if previous_value <= 0:
            continue

        ratios.append(
            current_value
            /
            previous_value
        )

    if not ratios:
        return base

    growth = float(
        np.median(
            ratios[-4:]
        )
    )

    growth = np.clip(
        growth,
        0.90,
        1.35
    )

    damped_growth = (
        1.0
        +
        0.45
        *
        (growth - 1.0)
    )

    return float(
        base
        *
        damped_growth
    )


def level_adjusted_seasonal(
    history,
    target
):

    previous_year = (
        target
        -
        pd.DateOffset(
            years=1
        )
    )

    base_row = history[
        history["Month"]
        ==
        previous_year
    ]

    if base_row.empty:
        return np.nan

    base = float(
        base_row[
            "Total_Tickets"
        ].iloc[0]
    )

    current_recent = (
        history[
            "Total_Tickets"
        ]
        .tail(3)
        .mean()
    )

    previous_year_months = []

    for _, row in history.tail(3).iterrows():

        previous_date = (
            row["Month"]
            -
            pd.DateOffset(
                years=1
            )
        )

        previous = history[
            history["Month"]
            ==
            previous_date
        ]

        if previous.empty:
            continue

        previous_year_months.append(
            float(
                previous[
                    "Total_Tickets"
                ].iloc[0]
            )
        )

    if not previous_year_months:
        return np.nan

    previous_level = np.mean(
        previous_year_months
    )

    if previous_level <= 0:
        return np.nan

    level_ratio = (
        current_recent
        /
        previous_level
    )

    level_ratio = np.clip(
        level_ratio,
        1.00,
        1.30
    )

    damped_ratio = (
        1.0
        +
        0.45
        *
        (level_ratio - 1.0)
    )

    return float(
        base
        *
        damped_ratio
    )


def trend_prediction(history):

    if len(history) < 4:
        return np.nan

    values = (
        history[
            "Total_Tickets"
        ]
        .tail(6)
        .astype(float)
        .values
    )

    x = np.arange(
        len(values)
    )

    coefficient = np.polyfit(
        x,
        values,
        1
    )

    prediction = np.polyval(
        coefficient,
        len(values)
    )

    recent_mean = (
        np.mean(values)
    )

    prediction = (
        0.55 * prediction
        +
        0.45 * recent_mean
    )

    return float(
        prediction
    )


def xgb_prediction(
    history,
    target
):

    if len(history) < 18:
        return np.nan

    d = history.copy()

    d["month"] = (
        d["Month"].dt.month
    )

    d["sin_month"] = np.sin(
        2
        * np.pi
        * d["month"]
        / 12
    )

    d["cos_month"] = np.cos(
        2
        * np.pi
        * d["month"]
        / 12
    )

    d["time_index"] = np.arange(
        len(d)
    )

    for lag in [
        1,
        2,
        3,
        6,
        12
    ]:

        d[f"lag_{lag}"] = (
            d["Total_Tickets"]
            .shift(lag)
        )

    previous = (
        d["Total_Tickets"]
        .shift(1)
    )

    d["rolling_3"] = (
        previous
        .rolling(3)
        .mean()
    )

    d["rolling_6"] = (
        previous
        .rolling(6)
        .mean()
    )

    d["rolling_12"] = (
        previous
        .rolling(12)
        .mean()
    )

    d["mom_growth"] = (
        (
            d["lag_1"]
            -
            d["lag_2"]
        )
        /
        d["lag_2"].replace(
            0,
            np.nan
        )
    ).clip(
        -0.25,
        0.25
    )

    d["yoy_growth"] = (
        (
            d["lag_1"]
            -
            d["lag_12"]
        )
        /
        d["lag_12"].replace(
            0,
            np.nan
        )
    ).clip(
        -0.20,
        0.50
    )

    features = [
        "month",
        "sin_month",
        "cos_month",
        "time_index",
        "lag_1",
        "lag_2",
        "lag_3",
        "lag_6",
        "lag_12",
        "rolling_3",
        "rolling_6",
        "rolling_12",
        "mom_growth",
        "yoy_growth"
    ]

    train = d.dropna(
        subset=features
    )

    if len(train) < 8:
        return np.nan

    model = XGBRegressor(
        **XGB_PARAMS
    )

    model.fit(
        train[features],
        np.log1p(
            train["Total_Tickets"]
        )
    )

    extended = pd.concat(
        [
            history,
            pd.DataFrame(
                {
                    "Month": [target],
                    "Total_Tickets": [np.nan]
                }
            )
        ],
        ignore_index=True
    )

    extended["month"] = (
        extended["Month"].dt.month
    )

    extended["sin_month"] = np.sin(
        2
        * np.pi
        * extended["month"]
        / 12
    )

    extended["cos_month"] = np.cos(
        2
        * np.pi
        * extended["month"]
        / 12
    )

    extended["time_index"] = np.arange(
        len(extended)
    )

    for lag in [
        1,
        2,
        3,
        6,
        12
    ]:

        extended[f"lag_{lag}"] = (
            extended[
                "Total_Tickets"
            ]
            .shift(lag)
        )

    previous = (
        extended[
            "Total_Tickets"
        ]
        .shift(1)
    )

    extended["rolling_3"] = (
        previous
        .rolling(3)
        .mean()
    )

    extended["rolling_6"] = (
        previous
        .rolling(6)
        .mean()
    )

    extended["rolling_12"] = (
        previous
        .rolling(12)
        .mean()
    )

    extended["mom_growth"] = (
        (
            extended["lag_1"]
            -
            extended["lag_2"]
        )
        /
        extended["lag_2"].replace(
            0,
            np.nan
        )
    ).clip(
        -0.25,
        0.25
    )

    extended["yoy_growth"] = (
        (
            extended["lag_1"]
            -
            extended["lag_12"]
        )
        /
        extended["lag_12"].replace(
            0,
            np.nan
        )
    ).clip(
        -0.20,
        0.50
    )

    target_row = extended[
        extended["Month"]
        ==
        target
    ]

    if target_row.empty:
        return np.nan

    if target_row[
        features
    ].isna().any().any():
        return np.nan

    prediction = model.predict(
        target_row[
            features
        ]
    )[0]

    return float(
        np.expm1(
            prediction
        )
    )


def component_predictions(
    history,
    target
):

    return {
        "recent3":
            recent_weighted(
                history,
                3
            ),

        "recent6":
            recent_weighted(
                history,
                6
            ),

        "median3":
            recent_median(
                history,
                3
            ),

        "exponential":
            exponential_prediction(
                history
            ),

        "seasonal":
            seasonal_prediction(
                history,
                target
            ),

        "level_seasonal":
            level_adjusted_seasonal(
                history,
                target
            ),

        "trend":
            trend_prediction(
                history
            ),

        "month_delta":
            month_delta_prediction(
                history,
                target
            ),

        "xgb":
            xgb_prediction(
                history,
                target
            )
    }


def normalize_prediction(
    value
):

    if not np.isfinite(value):
        return np.nan

    return float(
        np.clip(
            value,
            FORECAST_MIN,
            FORECAST_MAX
        )
    )


def historical_validation_scores(
    history
):

    validation_months = (
        history["Month"]
        .sort_values()
        .unique()
    )

    if len(validation_months) < 6:
        return {}

    start_index = max(
        0,
        len(validation_months) - 12
    )

    validation_months = (
        validation_months[
            start_index:
        ]
    )

    errors = {}

    for target in validation_months:

        target = pd.Timestamp(
            target
        )

        train_history = history[
            history["Month"]
            <
            target
        ].copy()

        if len(train_history) < 6:
            continue

        components = component_predictions(
            train_history,
            target
        )

        actual_row = history[
            history["Month"]
            ==
            target
        ]

        if actual_row.empty:
            continue

        actual = float(
            actual_row[
                "Total_Tickets"
            ].iloc[0]
        )

        for name, prediction in components.items():

            if not np.isfinite(
                prediction
            ):
                continue

            if name not in errors:
                errors[name] = []

            errors[name].append(
                abs(
                    prediction
                    -
                    actual
                )
            )

    scores = {}

    for name, values in errors.items():

        if not values:
            continue

        scores[name] = (
            np.mean(values)
        )

    return scores


def adaptive_prediction(
    history,
    target
):

    components = component_predictions(
        history,
        target
    )

    valid = {
        name: value
        for name, value
        in components.items()
        if np.isfinite(value)
    }

    if not valid:

        return float(
            history[
                "Total_Tickets"
            ].iloc[-1]
        )

    scores = historical_validation_scores(
        history
    )

    if not scores:

        weights = {
            "recent3": 0.30,
            "recent6": 0.15,
            "median3": 0.10,
            "exponential": 0.15,
            "seasonal": 0.10,
            "level_seasonal": 0.10,
            "trend": 0.05,
            "month_delta": 0.05,
            "xgb": 0.00
        }

    else:

        inverse_scores = {}

        for name in valid:

            score = scores.get(
                name,
                np.nan
            )

            if (
                np.isfinite(score)
                and
                score > 0
            ):

                inverse_scores[name] = (
                    1.0
                    /
                    score
                )

        if not inverse_scores:

            return float(
                recent_weighted(
                    history,
                    min(3, len(history))
                )
            )

        total_inverse = sum(
            inverse_scores.values()
        )

        weights = {
            name:
                value
                /
                total_inverse
            for name, value
            in inverse_scores.items()
        }

    weighted_values = []

    for name, value in valid.items():

        weight = weights.get(
            name,
            0.0
        )

        if weight <= 0:
            continue

        weighted_values.append(
            (
                name,
                value,
                weight
            )
        )

    if not weighted_values:

        return float(
            recent_weighted(
                history,
                min(3, len(history))
            )
        )

    total = sum(
        value * weight
        for _, value, weight
        in weighted_values
    )

    weight_total = sum(
        weight
        for _, _, weight
        in weighted_values
    )

    prediction = (
        total
        /
        weight_total
    )

    recent_level = (
        recent_weighted(
            history,
            min(3, len(history))
        )
    )

    if np.isfinite(recent_level):

        prediction = (
            0.70 * prediction
            +
            0.30 * recent_level
        )

    return float(
        prediction
    )


def bounded_future_forecast(
    prediction
):

    if not np.isfinite(
        prediction
    ):

        return float(
            FORECAST_MIN
        )

    prediction = float(
        prediction
    )

    return float(
        np.clip(
            prediction,
            FORECAST_MIN,
            FORECAST_MAX
        )
    )


def get_actual_vs_predicted():

    df = load_data()

    test = df[
        df["Month"]
        >=
        TEST_START
    ].copy()

    if test.empty:
        raise ValueError(
            "No 2026 test data available."
        )

    results = []

    print(
        "\n=============================================="
    )
    print(
        "AMS FORECASTING - APPLICATION DATA"
    )
    print(
        "=============================================="
    )
    print(
        "CSV:",
        CSV_PATH
    )
    print(
        "Location:",
        LOCATION
    )
    print(
        "Rows:",
        len(df)
    )
    print(
        "First month:",
        df["Month"].min().strftime(
            "%Y-%m"
        )
    )
    print(
        "Last month:",
        df["Month"].max().strftime(
            "%Y-%m"
        )
    )

    print(
        "\n2026 source values:"
    )

    print(
        test[
            [
                "Month",
                "Total_Tickets"
            ]
        ].to_string(
            index=False
        )
    )

    print(
        "=============================================="
    )

    print(
        "\nWALK-FORWARD EVALUATION"
    )
    print(
        "----------------------------------------------"
    )

    for _, row in test.iterrows():

        target = row["Month"]

        history = df[
            df["Month"]
            <
            target
        ].copy()

        prediction = adaptive_prediction(
            history,
            target
        )

        if not np.isfinite(
            prediction
        ):

            prediction = (
                history[
                    "Total_Tickets"
                ].iloc[-1]
            )

        predicted = int(
            round(
                prediction
            )
        )

        actual = int(
            row[
                "Total_Tickets"
            ]
        )

        error = abs(
            actual
            -
            predicted
        )

        pct_error = (
            error
            /
            actual
            *
            100
        )

        results.append(
            {
                "month":
                    target.strftime(
                        "%b %Y"
                    ),

                "actual":
                    actual,

                "predicted":
                    predicted,

                "error":
                    error,

                "pct_error":
                    round(
                        pct_error,
                        2
                    ),

                "is_anomaly":
                    False
            }
        )

        print(
            f"{target.strftime('%b %Y'):>9} "
            f"actual={actual:>5} "
            f"predicted={predicted:>5} "
            f"error={error:>4} "
            f"({pct_error:>5.1f}%)"
        )

    actuals = np.array(
        [
            row["actual"]
            for row in results
        ],
        dtype=float
    )

    predictions = np.array(
        [
            row["predicted"]
            for row in results
        ],
        dtype=float
    )

    mape = (
        mean_absolute_percentage_error(
            actuals,
            predictions
        )
        *
        100
    )

    total_actual = (
        actuals.sum()
    )

    total_predicted = (
        predictions.sum()
    )

    aggregate_error = (
        abs(
            total_actual
            -
            total_predicted
        )
        /
        total_actual
        *
        100
    )

    aggregate_accuracy = (
        100
        -
        aggregate_error
    )

    future = []

    history = df.copy()

    print(
        "\nFUTURE FORECAST"
    )
    print(
        "----------------------------------------------"
    )

    for _ in range(
        FUTURE_MONTHS
    ):

        target = (
            history[
                "Month"
            ].iloc[-1]
            +
            pd.DateOffset(
                months=1
            )
        )

        raw_prediction = adaptive_prediction(
            history,
            target
        )

        prediction = bounded_future_forecast(
            raw_prediction
        )

        predicted = int(
            round(
                prediction
            )
        )

        future.append(
            {
                "month":
                    target.strftime(
                        "%b %Y"
                    ),

                "predicted":
                    predicted,

                "min_range":
                    FORECAST_MIN,

                "max_range":
                    FORECAST_MAX
            }
        )

        print(
            f"{target.strftime('%b %Y'):>9} "
            f"predicted={predicted:>5} "
            f"range="
            f"{FORECAST_MIN}-"
            f"{FORECAST_MAX}"
        )

        history = pd.concat(
            [
                history,
                pd.DataFrame(
                    {
                        "Month": [
                            target
                        ],

                        "Total_Tickets": [
                            predicted
                        ]
                    }
                )
            ],
            ignore_index=True
        )

    return {
        "data": results,

        "kpis": {
            "accuracy_walk_forward":
                round(
                    100 - mape,
                    2
                ),

            "mape_walk_forward":
                round(
                    mape,
                    2
                ),

            "accuracy_all_months":
                round(
                    100 - mape,
                    2
                ),

            "mape_all_months":
                round(
                    mape,
                    2
                ),

            "aggregate_accuracy":
                round(
                    aggregate_accuracy,
                    2
                ),

            "aggregate_total_actual":
                int(
                    total_actual
                ),

            "aggregate_total_predicted":
                int(
                    total_predicted
                ),

            "anomaly_months": []
        },

        "future_forecast":
            future,

        "forecast_range": {
            "min":
                FORECAST_MIN,

            "max":
                FORECAST_MAX
        }
    }


if __name__ == "__main__":

    result = (
        get_actual_vs_predicted()
    )

    print(
        "\n=============================================="
    )

    print(
        "FINAL KPIs"
    )

    print(
        "=============================================="
    )

    print(
        "Accuracy:",
        result["kpis"][
            "accuracy_walk_forward"
        ],
        "%"
    )

    print(
        "MAPE:",
        result["kpis"][
            "mape_walk_forward"
        ],
        "%"
    )

    print(
        "Aggregate Accuracy:",
        result["kpis"][
            "aggregate_accuracy"
        ],
        "%"
    )

    print(
        "Total Actual:",
        result["kpis"][
            "aggregate_total_actual"
        ]
    )

    print(
        "Total Predicted:",
        result["kpis"][
            "aggregate_total_predicted"
        ]
    )

    print(
        "\nApplication CSV used:"
    )

    print(
        CSV_PATH
    )

    print(
        "\n=============================================="
    )