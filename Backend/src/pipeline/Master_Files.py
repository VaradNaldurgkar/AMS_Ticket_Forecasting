from pathlib import Path
import pandas as pd

# ==========================================================
# FILE PATHS
# ==========================================================

DESKTOP = Path.home() / "Desktop"

INCIDENT_FILE = DESKTOP / "1_100_IM Raw Data Report_July.xlsx"
REQUEST_FILE = DESKTOP / "1_100_RF Raw Data Report_July.xlsx"

# ==========================================================
# FILTERS (Same as Application)
# ==========================================================

VALID_GROUPS = [
    "Asset Support VW Group IT Solution",
    "AUAP O365 AMS Users Support VW Group",
    "AV/VC Support VW Group IT Solution",
    "AZUF Network L3 Advanced Support VW Group",
    "BI AMS Service Desk VW Group",
    "Devstack Support VW Group",
    "DIPON VWITS Support SKODA",
    "DWP User Profile Support VW Group",
    "Exchange Support SKODA Auto VW India",
    "Group Client SD Advanced Support VW Group",
    "ISERVE Services Support VW Group",
    "IT4IT Support VW Group IT Solution",
    "ITAM Support VW Group",
    "KAM Support SKODA Auto VW India",
    "M365 Basis Infra Advanced Support VW Group",
    "MAC Support VW",
    "Mailing Services MX - Vulnerabilities and Compliance Support VW Group",
    "Network Support SKODA Auto VW India Pune",
    "Power BI Support VW Group",
    "PRESS II AMS ITSP Support VW Group",
    "SC3 Support VW Group",
    "Server Support SKODA Auto VW India Pune",
    "Service Desk VW Group IT Solution",
    "SF Support VW Group IT Solution",
    "UAM Support VW Group IT Solution",
    "User Connectivity Dispatcher Internet Access Remote Access Support VW Group",
    "User Connectivity Group Device Advanced Support VW Group"
]

LOCATION = "pune"

# ==========================================================
# CLEAN COLUMNS
# ==========================================================

def clean_columns(df):

    df.columns = [
        str(col).replace("\n", " ").strip()
        for col in df.columns
    ]

    return df


# ==========================================================
# NORMALIZE STRINGS
# ==========================================================

def normalize_strings(df):

    for col in df.columns:

        if df[col].dtype == object:

            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    return df


# ==========================================================
# AUTO HEADER DETECTION
# ==========================================================

def read_excel_auto(file_path, sheet_name, required_column):

    for header in range(8):

        try:

            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                header=header,
                dtype=str
            )

            df = clean_columns(df)

            if required_column in df.columns:

                print(f"✓ {file_path.name} using header={header}")
                return df

        except Exception:
            pass

    raise Exception(
        f"{required_column} not found in {file_path.name}"
    )


# ==========================================================
# LOAD REPORT
# ==========================================================

def load_report(file_path, report_type):

    with pd.ExcelFile(file_path) as xls:

        if report_type == "incident":

            sheet = (
                "Incident Records"
                if "Incident Records" in xls.sheet_names
                else "Sheet1"
            )

            df = read_excel_auto(
                file_path,
                sheet,
                "Incident ID"
            )

        else:

            sheet = (
                "Request Records"
                if "Request Records" in xls.sheet_names
                else "Sheet1"
            )

            df = read_excel_auto(
                file_path,
                sheet,
                "Request ID"
            )

    df = clean_columns(df)
    df = normalize_strings(df)

    return df

# ==========================================================
# FILTER
# ==========================================================

def filter_dataframe(df, report_type):

    original_rows = len(df)

    # ------------------------------------------------------
    # CLOSE GROUP FILTER
    # ------------------------------------------------------

    if "Close Group" not in df.columns:
        raise Exception("'Close Group' column not found.")

    df["Close Group"] = (
        df["Close Group"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df = df[
        df["Close Group"].isin(VALID_GROUPS)
    ]

    print(f"\nRows after Close Group filter : {len(df)} / {original_rows}")

    # ------------------------------------------------------
    # LOCATION COLUMNS
    # ------------------------------------------------------

    if "CI Location" not in df.columns:
        df["CI Location"] = ""

    if "CI Location.1" not in df.columns:
        df["CI Location.1"] = ""

    df["CI Location"] = (
        df["CI Location"]
        .replace("nan", "")
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["CI Location.1"] = (
        df["CI Location.1"]
        .replace("nan", "")
        .fillna("")
        .astype(str)
        .str.strip()
    )

    print("\nCI Location Distribution:")
    print(
        df["CI Location"]
        .value_counts(dropna=False)
        .head(20)
    )

    print("\nCI Location.1 Distribution:")
    print(
        df["CI Location.1"]
        .value_counts(dropna=False)
        .head(20)
    )

    # ------------------------------------------------------
    # FINAL LOCATION
    # ------------------------------------------------------

    df["FINAL_LOCATION"] = df["CI Location"]

    mask = df["FINAL_LOCATION"] == ""

    df.loc[
        mask,
        "FINAL_LOCATION"
    ] = df.loc[
        mask,
        "CI Location.1"
    ]

    df["FINAL_LOCATION"] = (
        df["FINAL_LOCATION"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    print("\nFINAL_LOCATION Distribution:")
    print(
        df["FINAL_LOCATION"]
        .value_counts(dropna=False)
        .head(20)
    )

    # ------------------------------------------------------
    # PUNE FILTER
    # ------------------------------------------------------

    before_location = len(df)

    df = df[
        df["FINAL_LOCATION"].str.contains(
            LOCATION,
            case=False,
            na=False
        )
    ]

    print(f"\nRows after Pune filter : {len(df)} / {before_location}")

    df = df.drop(columns=["FINAL_LOCATION"])

    return df.reset_index(drop=True)


# ==========================================================
# COUNT JULY 2026
# ==========================================================

def count_month(df, report_type):

    if report_type == "incident":
        date_column = "Open Time (Timezone based)"
    else:
        date_column = "Open Time (Timezone based)"

    if date_column not in df.columns:

        print("\nAvailable Columns:")
        print(df.columns.tolist())

        raise Exception(
            f"{date_column} not found."
        )

    print(f"\nUsing date column : {date_column}")

    df = df.copy()

    df[date_column] = pd.to_datetime(
        df[date_column],
        errors="coerce"
    )

    print("\nMonth Distribution:")
    print(
        df[date_column]
        .dt.to_period("M")
        .value_counts()
        .sort_index()
    )

    july = df[
        (df[date_column].dt.year == 2026) &
        (df[date_column].dt.month == 7)
    ]

    print(f"\nJuly 2026 Count : {len(july)}")

    return july

# ==========================================================
# MAIN
# ==========================================================

print("\n" + "=" * 60)
print("INCIDENT REPORT")
print("=" * 60)

incident = load_report(
    INCIDENT_FILE,
    "incident"
)

incident = filter_dataframe(
    incident,
    "incident"
)

incident_july = count_month(
    incident,
    "incident"
)

print("\nIncident Tickets (July 2026)")
print("-" * 40)
print(len(incident_july))


print("\n" + "=" * 60)
print("REQUEST REPORT")
print("=" * 60)

request = load_report(
    REQUEST_FILE,
    "request"
)

request = filter_dataframe(
    request,
    "request"
)

request_july = count_month(
    request,
    "request"
)

print("\nRequest Tickets (July 2026)")
print("-" * 40)
print(len(request_july))


# ==========================================================
# FINAL SUMMARY
# ==========================================================

total_tickets = len(incident_july) + len(request_july)

print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

print(f"Incident Tickets : {len(incident_july)}")
print(f"Request Tickets  : {len(request_july)}")
print("-" * 60)
print(f"Total Tickets    : {total_tickets}")
print("=" * 60)