import os
import numpy as np
import pandas as pd
from xgboost import XGBRegressor


APPLICATION_ROOT = r"C:\Applications\AMS_Backend"

CSV_PATH = os.path.join(
    APPLICATION_ROOT,
    "data",
    "processed",
    "AMS_Yearly_Aggregated.csv"
)

LOCATION = "Pune"

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


FEATURES = [
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
        column
        for column in required
        if column not in df.columns
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


def create_features(df):

    d = df.copy()

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

    d["lag_1"] = (
        d["Total_Tickets"]
        .shift(1)
    )

    d["lag_2"] = (
        d["Total_Tickets"]
        .shift(2)
    )

    d["lag_3"] = (
        d["Total_Tickets"]
        .shift(3)
    )

    d["lag_6"] = (
        d["Total_Tickets"]
        .shift(6)
    )

    d["lag_12"] = (
        d["Total_Tickets"]
        .shift(12)
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

    return d


def xgb_prediction(
    history,
    target
):

    if len(history) < 18:
        return np.nan

    train = create_features(
        history
    )

    train = train.dropna(
        subset=FEATURES
    )

    if len(train) < 8:
        return np.nan

    model = XGBRegressor(
        **XGB_PARAMS
    )

    model.fit(
        train[FEATURES],
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

    extended = create_features(
        extended
    )

    target_row = extended[
        extended["Month"] == target
    ]

    if target_row.empty:
        return np.nan

    if target_row[
        FEATURES
    ].isna().any().any():
        return np.nan

    prediction = model.predict(
        target_row[FEATURES]
    )[0]

    return float(
        np.expm1(
            prediction
        )
    )


def recent_weighted(
    history,
    periods
):

    if len(history) < periods:
        return np.nan

    values = (
        history[
            "Total_Tickets"
        ]
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


def recent_median(
    history,
    periods
):

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


def exponential_prediction(
    history
):

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

    level = float(
        values[0]
    )

    for value in values[1:]:

        level = (
            alpha * value
            +
            (1 - alpha) * level
        )

    return float(level)


def trend_prediction(
    history
):

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

    trend_value = np.polyval(
        coefficient,
        len(values)
    )

    recent_mean = (
        np.mean(values)
    )

    return float(
        0.55 * trend_value
        +
        0.45 * recent_mean
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

    growth_values = []

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
            row[
                "Total_Tickets"
            ]
        )

        if previous_value <= 0:
            continue

        growth_values.append(
            current_value
            /
            previous_value
        )

    if not growth_values:
        return base

    growth = float(
        np.median(
            growth_values[-4:]
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

    recent_values = (
        history[
            "Total_Tickets"
        ]
        .tail(3)
        .astype(float)
        .values
    )

    recent_level = (
        np.mean(
            recent_values
        )
    )

    previous_values = []

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

        previous_values.append(
            float(
                previous[
                    "Total_Tickets"
                ].iloc[0]
            )
        )

    if not previous_values:
        return np.nan

    previous_level = np.mean(
        previous_values
    )

    if previous_level <= 0:
        return np.nan

    level_ratio = (
        recent_level
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


def month_delta_prediction(
    history,
    target
):

    if len(history) < 13:
        return np.nan

    deltas = []

    for i in range(
        1,
        len(history)
    ):

        current = history.iloc[i]

        if (
            current["Month"].month
            !=
            target.month
        ):
            continue

        previous = history.iloc[
            i - 1
        ]

        delta = (
            current["Total_Tickets"]
            -
            previous["Total_Tickets"]
        )

        deltas.append(
            delta
        )

    if not deltas:
        return np.nan

    recent_delta = np.median(
        deltas[-3:]
    )

    latest = float(
        history[
            "Total_Tickets"
        ].iloc[-1]
    )

    return float(
        latest
        +
        recent_delta
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


def validation_scores(
    history
):

    months = (
        history["Month"]
        .sort_values()
        .unique()
    )

    if len(months) < 10:
        return {}

    months = months[
        -12:
    ]

    scores = {}

    for target in months:

        target = pd.Timestamp(
            target
        )

        train_history = history[
            history["Month"]
            <
            target
        ].copy()

        if len(train_history) < 8:
            continue

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

        predictions = component_predictions(
            train_history,
            target
        )

        for name, prediction in predictions.items():

            if not np.isfinite(
                prediction
            ):
                continue

            if name not in scores:
                scores[name] = []

            scores[name].append(
                abs(
                    prediction
                    -
                    actual
                )
            )

    final_scores = {}

    for name, values in scores.items():

        if values:
            final_scores[name] = (
                np.mean(values)
            )

    return final_scores


def adaptive_prediction(
    history,
    target
):

    predictions = component_predictions(
        history,
        target
    )

    valid = {
        name: value
        for name, value
        in predictions.items()
        if np.isfinite(value)
    }

    if not valid:

        return float(
            history[
                "Total_Tickets"
            ].iloc[-1]
        )

    scores = validation_scores(
        history
    )

    if scores:

        inverse = {}

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

                inverse[name] = (
                    1.0 / score
                )

        if inverse:

            total = sum(
                inverse.values()
            )

            weights = {
                name:
                    value / total
                for name, value
                in inverse.items()
            }

        else:

            weights = {}

    else:

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

    if not weights:

        return float(
            recent_weighted(
                history,
                min(3, len(history))
            )
        )

    total_prediction = 0.0
    total_weight = 0.0

    for name, value in valid.items():

        weight = weights.get(
            name,
            0.0
        )

        if weight <= 0:
            continue

        total_prediction += (
            value
            *
            weight
        )

        total_weight += weight

    if total_weight <= 0:

        return float(
            recent_weighted(
                history,
                min(3, len(history))
            )
        )

    prediction = (
        total_prediction
        /
        total_weight
    )

    recent_level = (
        recent_weighted(
            history,
            min(3, len(history))
        )
    )

    if np.isfinite(
        recent_level
    ):

        prediction = (
            0.70 * prediction
            +
            0.30 * recent_level
        )

    return float(
        prediction
    )


def bounded_forecast(
    prediction
):

    if not np.isfinite(
        prediction
    ):
        return float(
            FORECAST_MIN
        )

    return float(
        np.clip(
            prediction,
            FORECAST_MIN,
            FORECAST_MAX
        )
    )


def get_future_forecast():

    df = load_data()

    if len(df) < 12:
        raise ValueError(
            "At least 12 months of data are required."
        )

    history = df.copy()

    predictions = []

    print(
        "\n=============================================="
    )

    print(
        "AMS FUTURE TICKET FORECAST"
    )

    print(
        "=============================================="
    )

    print(
        "Application CSV:",
        CSV_PATH
    )

    print(
        "Location:",
        LOCATION
    )

    print(
        "Historical rows:",
        len(df)
    )

    print(
        "Last actual month:",
        df["Month"].iloc[-1].strftime(
            "%Y-%m"
        )
    )

    print(
        "Last actual tickets:",
        int(
            df[
                "Total_Tickets"
            ].iloc[-1]
        )
    )

    print(
        "Forecast range:",
        f"{FORECAST_MIN}-{FORECAST_MAX}"
    )

    print(
        "\nFUTURE FORECAST"
    )

    print(
        "----------------------------------------------"
    )

    for step in range(
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

        prediction = bounded_forecast(
            raw_prediction
        )

        predicted = int(
            round(
                prediction
            )
        )

        predictions.append(
            {
                "month":
                    target.strftime(
                        "%b %Y"
                    ),

                "predicted":
                    predicted
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

    print(
        "\n=============================================="
    )

    return predictions


if __name__ == "__main__":

    forecast = get_future_forecast()

    print(
        "\nNEXT MONTHS FORECAST"
    )

    print(
        "=============================================="
    )

    for row in forecast:

        print(
            f"{row['month']:>10} "
            f"-> "
            f"{row['predicted']:,} tickets"
        )