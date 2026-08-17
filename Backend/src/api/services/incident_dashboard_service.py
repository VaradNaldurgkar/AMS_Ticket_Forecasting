import pandas as pd
import os


# ========================================================
# PATH SETUP
# ========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)


# ========================================================
# MASTER INCIDENT FILE
# ========================================================

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Master",
    "master_incidents.csv"
)


# ========================================================
# CONSTANTS
# ========================================================

INCIDENT_TYPE_COLUMN = "Title"

OPEN_TIME_COLUMN = "Open Time (Timezone based)"

RESOLVE_TIME_COLUMN = "Resolve Time (Timezone based)"

UNCATEGORIZED_TYPE = "General / Uncategorized"


# ========================================================
# LOAD MASTER INCIDENT DATA
# ========================================================

def load_master_incident_data():

    if not os.path.exists(CSV_PATH):

        raise FileNotFoundError(
            f"Incident master file not found: {CSV_PATH}"
        )

    df = pd.read_csv(
        CSV_PATH,
        dtype=str,
        low_memory=False
    )

    # ----------------------------------------------------
    # Clean column names
    # ----------------------------------------------------

    df.columns = [
        str(col)
        .replace("\n", " ")
        .strip()
        for col in df.columns
    ]

    return df


# ========================================================
# VALIDATE REQUIRED COLUMNS
# ========================================================

def validate_columns(df):

    required_columns = [
        INCIDENT_TYPE_COLUMN,
        OPEN_TIME_COLUMN,
        RESOLVE_TIME_COLUMN
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise Exception(
            "Required columns missing from "
            "master_incidents.csv: "
            + ", ".join(missing_columns)
        )


# ========================================================
# GET AVAILABLE FILTER OPTIONS
#
# IMPORTANT:
# These values are generated directly from the current
# master_incidents.csv.
#
# Nothing is hardcoded.
# ========================================================

def get_available_filters(df):

    filter_df = df.copy()

    # ----------------------------------------------------
    # Convert Open Time
    # ----------------------------------------------------

    filter_df[OPEN_TIME_COLUMN] = pd.to_datetime(
        filter_df[OPEN_TIME_COLUMN],
        errors="coerce"
    )

    # ----------------------------------------------------
    # Remove invalid dates
    # ----------------------------------------------------

    filter_df = filter_df[
        filter_df[OPEN_TIME_COLUMN].notna()
    ].copy()

    # ----------------------------------------------------
    # Empty master
    # ----------------------------------------------------

    if filter_df.empty:

        return {
            "years": [],
            "months": [],
            "min_date": "",
            "max_date": ""
        }

    # ----------------------------------------------------
    # AVAILABLE YEARS
    # ----------------------------------------------------

    years = sorted(
        filter_df[OPEN_TIME_COLUMN]
        .dt.year
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    # ----------------------------------------------------
    # AVAILABLE MONTHS
    #
    # Only months that actually exist in the master
    # are returned.
    #
    # Example:
    #
    # Master has Jan-Jun
    # -> January ... June
    #
    # July upload happens
    # -> July automatically appears.
    # ----------------------------------------------------

    month_numbers = sorted(
        filter_df[OPEN_TIME_COLUMN]
        .dt.month
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    month_labels = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    months = [
        {
            "value": month,
            "label": month_labels[month]
        }
        for month in month_numbers
    ]

    # ----------------------------------------------------
    # MINIMUM DATE
    # ----------------------------------------------------

    min_date = (
        filter_df[OPEN_TIME_COLUMN]
        .min()
        .strftime("%Y-%m-%d")
    )

    # ----------------------------------------------------
    # MAXIMUM DATE
    # ----------------------------------------------------

    max_date = (
        filter_df[OPEN_TIME_COLUMN]
        .max()
        .strftime("%Y-%m-%d")
    )

    # ----------------------------------------------------
    # FINAL FILTER INFORMATION
    # ----------------------------------------------------

    return {
        "years": years,
        "months": months,
        "min_date": min_date,
        "max_date": max_date
    }


# ========================================================
# APPLY DATE FILTERS
# ========================================================

def apply_date_filters(
    df,
    year=None,
    month=None,
    start_date=None,
    end_date=None
):

    filtered_df = df.copy()

    # ----------------------------------------------------
    # Convert Open Time
    #
    # Ticket month/year is determined using
    # Open Time (Timezone based).
    # ----------------------------------------------------

    filtered_df[OPEN_TIME_COLUMN] = pd.to_datetime(
        filtered_df[OPEN_TIME_COLUMN],
        errors="coerce"
    )

    # ----------------------------------------------------
    # Remove rows where Open Time is invalid
    # ----------------------------------------------------

    filtered_df = filtered_df[
        filtered_df[OPEN_TIME_COLUMN].notna()
    ].copy()

    # ----------------------------------------------------
    # YEAR FILTER
    # ----------------------------------------------------

    if year is not None:

        try:

            year = int(year)

        except (TypeError, ValueError):

            raise ValueError(
                f"Invalid year: {year}"
            )

        filtered_df = filtered_df[
            filtered_df[OPEN_TIME_COLUMN].dt.year == year
        ]

    # ----------------------------------------------------
    # MONTH FILTER
    # ----------------------------------------------------

    if month is not None:

        try:

            month = int(month)

        except (TypeError, ValueError):

            raise ValueError(
                f"Invalid month: {month}"
            )

        if month < 1 or month > 12:

            raise ValueError(
                "Month must be between 1 and 12."
            )

        filtered_df = filtered_df[
            filtered_df[OPEN_TIME_COLUMN].dt.month == month
        ]

    # ----------------------------------------------------
    # START DATE FILTER
    # ----------------------------------------------------

    if start_date:

        start = pd.to_datetime(
            start_date,
            errors="coerce"
        )

        if pd.isna(start):

            raise ValueError(
                f"Invalid start_date: {start_date}"
            )

        # Include complete start date.
        #
        # Example:
        # 2026-07-01
        #
        # includes everything from
        # 2026-07-01 00:00:00 onward.

        start = start.normalize()

        filtered_df = filtered_df[
            filtered_df[OPEN_TIME_COLUMN] >= start
        ]

    # ----------------------------------------------------
    # END DATE FILTER
    # ----------------------------------------------------

    if end_date:

        end = pd.to_datetime(
            end_date,
            errors="coerce"
        )

        if pd.isna(end):

            raise ValueError(
                f"Invalid end_date: {end_date}"
            )

        # Include the COMPLETE end date.
        #
        # Example:
        #
        # end_date = 2026-07-31
        #
        # becomes:
        #
        # 2026-08-01 00:00:00
        #
        # Therefore every ticket on July 31
        # is included.

        end = (
            end.normalize()
            + pd.Timedelta(days=1)
        )

        filtered_df = filtered_df[
            filtered_df[OPEN_TIME_COLUMN] < end
        ]

    return filtered_df.reset_index(drop=True)


# ========================================================
# CALCULATE RESOLUTION TIME
# ========================================================

def calculate_resolution_hours(df):

    df = df.copy()

    # ----------------------------------------------------
    # Convert Resolve Time
    # ----------------------------------------------------

    df[RESOLVE_TIME_COLUMN] = pd.to_datetime(
        df[RESOLVE_TIME_COLUMN],
        errors="coerce"
    )

    # ----------------------------------------------------
    # Resolution time in hours
    # ----------------------------------------------------

    df["__resolution_hours"] = (
        (
            df[RESOLVE_TIME_COLUMN]
            - df[OPEN_TIME_COLUMN]
        )
        .dt.total_seconds()
        / 3600
    )

    # ----------------------------------------------------
    # Remove invalid negative values
    # ----------------------------------------------------

    df.loc[
        df["__resolution_hours"] < 0,
        "__resolution_hours"
    ] = pd.NA

    return df


# ========================================================
# LOAD INCIDENT DASHBOARD DATA
# ========================================================

def load_incident_dashboard_data(
    year=None,
    month=None,
    start_date=None,
    end_date=None
):

    # ====================================================
    # LOAD MASTER
    # ====================================================

    df = load_master_incident_data()

    print("\n============================================")
    print("INCIDENT DASHBOARD")
    print("============================================")

    print("Master File:")
    print(CSV_PATH)

    print(
        "Rows before filters :",
        len(df)
    )

    # ====================================================
    # VALIDATE
    # ====================================================

    validate_columns(df)

    # ====================================================
    # AVAILABLE FILTERS
    #
    # IMPORTANT:
    # This is calculated BEFORE applying the selected
    # filters so the frontend always knows the complete
    # date range currently available in the master.
    # ====================================================

    available_filters = get_available_filters(df)

    print("\nAvailable Filters")
    print("--------------------------------------------")

    print(
        "Years      :",
        available_filters["years"]
    )

    print(
        "Months     :",
        available_filters["months"]
    )

    print(
        "Minimum Date:",
        available_filters["min_date"]
    )

    print(
        "Maximum Date:",
        available_filters["max_date"]
    )

    # ====================================================
    # APPLY DATE FILTERS
    # ====================================================

    df = apply_date_filters(
        df,
        year=year,
        month=month,
        start_date=start_date,
        end_date=end_date
    )

    print(
        "\nRows after date filters :",
        len(df)
    )

    # ====================================================
    # CALCULATE RESOLUTION
    # ====================================================

    df = calculate_resolution_hours(df)

    # ====================================================
    # CLEAN INCIDENT TYPE
    # ====================================================

    df[INCIDENT_TYPE_COLUMN] = (
        df[INCIDENT_TYPE_COLUMN]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # ----------------------------------------------------
    # Empty titles become General / Uncategorized
    # ----------------------------------------------------

    df.loc[
        df[INCIDENT_TYPE_COLUMN] == "",
        INCIDENT_TYPE_COLUMN
    ] = UNCATEGORIZED_TYPE

    # ====================================================
    # SUMMARY TOTAL
    #
    # Includes ALL incidents after selected filters.
    # ====================================================

    total_incidents = int(
        len(df)
    )

    # ====================================================
    # AGGREGATE INCIDENT TYPES
    # ====================================================

    grouped = (
        df.groupby(
            INCIDENT_TYPE_COLUMN,
            dropna=False
        )
        .agg(
            incident_count=(
                INCIDENT_TYPE_COLUMN,
                "size"
            ),
            avg_resolution_hours=(
                "__resolution_hours",
                "mean"
            ),
            median_resolution_hours=(
                "__resolution_hours",
                "median"
            )
        )
        .reset_index()
    )

    # ====================================================
    # SORT BY TICKET COUNT
    # ====================================================

    grouped = grouped.sort_values(
        "incident_count",
        ascending=False
    ).reset_index(drop=True)

    # ====================================================
    # REMOVE GENERAL / UNCATEGORIZED
    #
    # Used for:
    # - Top Incident Type
    # - Top 5 chart
    # - Total Categories
    #
    # General / Uncategorized remains in table.
    # ====================================================

    filtered_df = grouped[
        grouped[INCIDENT_TYPE_COLUMN]
        .str.lower()
        != UNCATEGORIZED_TYPE.lower()
    ].copy()

    # ====================================================
    # SUMMARY CARDS
    # ====================================================

    if not filtered_df.empty:

        top_row = filtered_df.iloc[0]

        top_incident = str(
            top_row[INCIDENT_TYPE_COLUMN]
        )

        top_incident_count = int(
            top_row["incident_count"]
        )

    else:

        top_incident = "N/A"

        top_incident_count = 0

    total_categories = int(
        len(filtered_df)
    )

    # ====================================================
    # CHART DATA
    #
    # TOP 5 INCIDENT TYPES
    # ====================================================

    top_5 = filtered_df.head(5)

    chart_data = []

    for _, row in top_5.iterrows():

        chart_data.append({

            "name": str(
                row[INCIDENT_TYPE_COLUMN]
            ),

            "tickets": int(
                row["incident_count"]
            )
        })

    # ====================================================
    # TABLE DATA
    #
    # Keep General / Uncategorized here.
    # ====================================================

    table_data = []

    for _, row in grouped.head(15).iterrows():

        avg_resolution = row[
            "avg_resolution_hours"
        ]

        median_resolution = row[
            "median_resolution_hours"
        ]

        # ------------------------------------------------
        # Handle missing resolution times
        # ------------------------------------------------

        if pd.isna(avg_resolution):

            avg_resolution_value = 0

        else:

            avg_resolution_value = round(
                float(avg_resolution),
                2
            )

        if pd.isna(median_resolution):

            median_resolution_value = 0

        else:

            median_resolution_value = round(
                float(median_resolution),
                2
            )

        table_data.append({

            "incident_type": str(
                row[INCIDENT_TYPE_COLUMN]
            ),

            "incident_count": int(
                row["incident_count"]
            ),

            "avg_resolution_hours":
                avg_resolution_value,

            "median_resolution_hours":
                median_resolution_value
        })

    # ====================================================
    # APPLIED FILTERS
    # ====================================================

    applied_filters = {

        "year": year,

        "month": month,

        "start_date": start_date,

        "end_date": end_date
    }

    # ====================================================
    # FINAL RESPONSE
    # ====================================================

    response = {

        # ------------------------------------------------
        # Dashboard data
        # ------------------------------------------------

        "summary_cards": {

            "total_incidents":
                total_incidents,

            "top_incident":
                top_incident,

            "top_incident_count":
                top_incident_count,

            "total_categories":
                total_categories
        },

        "chart_data":
            chart_data,

        "table_data":
            table_data,

        # ------------------------------------------------
        # Dynamic filter information
        #
        # Frontend uses this to populate:
        # - Year dropdown
        # - Month dropdown
        # - Date picker limits
        # ------------------------------------------------

        "available_filters":
            available_filters,

        # ------------------------------------------------
        # Currently applied filters
        # ------------------------------------------------

        "filters":
            applied_filters
    }

    # ====================================================
    # DEBUG
    # ====================================================

    print("\nDashboard Summary")
    print("--------------------------------------------")

    print(
        "Total Incidents   :",
        total_incidents
    )

    print(
        "Top Incident      :",
        top_incident
    )

    print(
        "Top Incident Count:",
        top_incident_count
    )

    print(
        "Total Categories  :",
        total_categories
    )

    print("\nApplied Filters")
    print("--------------------------------------------")

    print(
        "Year       :",
        year
    )

    print(
        "Month      :",
        month
    )

    print(
        "Start Date :",
        start_date
    )

    print(
        "End Date   :",
        end_date
    )

    print("\n============================================")

    return response