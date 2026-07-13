from pathlib import Path
import pandas as pd

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

MASTER_FOLDER = BASE_DIR / "data" / "Master"

MASTER_FOLDER.mkdir(parents=True, exist_ok=True)

INCIDENT_MASTER = MASTER_FOLDER / "master_incidents.csv"
REQUEST_MASTER = MASTER_FOLDER / "master_requests.csv"

print("\n================ PATH DEBUG ================")
print("BASE_DIR          :", BASE_DIR)
print("MASTER_FOLDER     :", MASTER_FOLDER)
print("INCIDENT_MASTER   :", INCIDENT_MASTER)
print("REQUEST_MASTER    :", REQUEST_MASTER)
print("============================================\n")

# ============================================================
# FILTERS
# ============================================================

VALID_GROUPS = [
    "AV/VC Support VW Group IT Solution",
    "Asset Support VW Group IT Solution",
    "Service Desk VW Group IT Solution"
]

LOCATION = "pune"

# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

def clean_columns(df):

    df.columns = [
        str(col).replace("\n", " ").strip()
        for col in df.columns
    ]

    return df


# ============================================================
# NORMALIZE STRINGS
# ============================================================

def normalize_strings(df):

    for col in df.columns:

        if df[col].dtype == object:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

    return df



# ============================================================
# AUTO HEADER DETECTION
# ============================================================

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
                print(f"✓ Using header={header}")
                return df

        except Exception:
            pass

    raise Exception(
        f"Could not find '{required_column}' in {file_path.name}"
    )


# ============================================================
# DETECT REPORT TYPE
# ============================================================
def get_report_type(file_path: Path):

    xls = pd.ExcelFile(file_path)

    if "Incident Records" in xls.sheet_names:
        return "incident"

    if "Request Records" in xls.sheet_names:
        return "request"

    if "Sheet1" in xls.sheet_names:

        df = pd.read_excel(
            file_path,
            sheet_name="Sheet1",
            nrows=5
        )

        df.columns = [
            str(c).replace("\n", " ").strip()
            for c in df.columns
        ]

        if "Incident ID" in df.columns:
            return "incident"

        if "Request ID" in df.columns:
            return "request"

    return "unknown"


# ============================================================
# READ INCIDENT REPORT
# Supports:
#   1. Incident Records sheet
#   2. Sheet1 format
# ============================================================

def read_incident_report(file_path: Path):

    print(f"\nReading Incident Report : {file_path.name}")

    xls = pd.ExcelFile(file_path)

    if "Incident Records" in xls.sheet_names:
        sheet = "Incident Records"

    elif "Sheet1" in xls.sheet_names:
        sheet = "Sheet1"

    else:
        raise Exception(
            f"Unknown Incident format : {file_path.name}"
        )

    df = read_excel_auto(
        file_path,
        sheet,
        "Incident ID"
    )

    if "Incident ID April" in df.columns:
        df.rename(
            columns={
                "Incident ID April": "Incident ID"
            },
            inplace=True
        )

    df = normalize_strings(df)

    print("\n========== INCIDENT COLUMNS ==========")
    print(df.columns.tolist())

    return df


# ============================================================
# READ REQUEST REPORT
# Supports:
#   1. Request Records
#   2. Sheet1
# ============================================================

def read_request_report(file_path: Path):

    print(f"\nReading Request Report : {file_path.name}")

    xls = pd.ExcelFile(file_path)

    # -------------------------------------------------------
    # Detect Sheet
    # -------------------------------------------------------

    if "Request Records" in xls.sheet_names:

        sheet = "Request Records"

    elif "Sheet1" in xls.sheet_names:

        sheet = "Sheet1"

    else:

        raise Exception(
            f"Unknown Request format : {file_path.name}"
        )

    # -------------------------------------------------------
    # Automatically detect correct header
    # -------------------------------------------------------

    df = read_excel_auto(
        file_path=file_path,
        sheet_name=sheet,
        required_column="Request ID"
    )

    # -------------------------------------------------------
    # Handle older April format
    # -------------------------------------------------------

    if "Request ID April" in df.columns:

        df.rename(
            columns={
                "Request ID April": "Request ID"
            },
            inplace=True
        )

    # -------------------------------------------------------
    # Clean Data
    # -------------------------------------------------------

    df = clean_columns(df)
    df = normalize_strings(df)

    print("\n========== REQUEST COLUMNS ==========")
    print(df.columns.tolist())

    return df


# ============================================================
# FILTER DATAFRAME
# ============================================================

def filter_ams_dataframe(df):

    print("\n========== REQUEST FILTER DEBUG ==========")

    # ---------------------------------------------------
    # Resolve Group Check
    # ---------------------------------------------------

    if "Resolve Group" not in df.columns:
        print("Resolve Group column not found.")
        return df

    df["Resolve Group"] = (
        df["Resolve Group"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    print("\nResolve Group Distribution:")
    print(df["Resolve Group"].value_counts(dropna=False).head(20))

    # ---------------------------------------------------
    # Location Check
    # ---------------------------------------------------

    if "CI Location" not in df.columns:
        df["CI Location"] = ""

    if "CI Location.1" not in df.columns:
        df["CI Location.1"] = ""

    df["CI Location"] = (
        df["CI Location"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["CI Location.1"] = (
        df["CI Location.1"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    print("\nCI Location Distribution:")
    print(df["CI Location"].value_counts(dropna=False).head(20))

    print("\nCI Location.1 Distribution:")
    print(df["CI Location.1"].value_counts(dropna=False).head(20))

    # ---------------------------------------------------
    # Resolve Group Filter
    # ---------------------------------------------------

    df = df[
        df["Resolve Group"].isin(VALID_GROUPS)
    ]

    print("\nRows after Resolve Group filter :", len(df))

    # ---------------------------------------------------
    # Final Location
    # ---------------------------------------------------

    df["FINAL_LOCATION"] = df["CI Location"]

    df["FINAL_LOCATION"] = df["FINAL_LOCATION"].where(
        df["FINAL_LOCATION"] != "",
        df["CI Location.1"]
    )

    df["FINAL_LOCATION"] = (
        df["FINAL_LOCATION"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    print("\nFINAL_LOCATION Distribution:")
    print(df["FINAL_LOCATION"].value_counts(dropna=False).head(20))

    # ---------------------------------------------------
    # Pune Filter
    # ---------------------------------------------------

    df = df[
        df["FINAL_LOCATION"].str.contains(
            LOCATION,
            case=False,
            na=False
        )
    ]

    print("Rows after Location filter :", len(df))

    df = df.drop(columns=["FINAL_LOCATION"])

    df = df.reset_index(drop=True)

    print("\n========== FINAL FILTER RESULT ==========")
    print("Rows After Filter :", len(df))

    return df


# ============================================================
# LOAD MASTER CSV
# ============================================================

def load_master(master_path: Path):

    print("\n========== LOADING MASTER ==========")

    print(master_path)

    if not master_path.exists():

        print("Master does not exist.")
        return pd.DataFrame()

    master = pd.read_csv(
        master_path,
        dtype=str,
        low_memory=False
    )

    master = clean_columns(master)
    master = normalize_strings(master)

    print("Rows Loaded :", len(master))

    return master


# ============================================================
# SAVE MASTER CSV
# ============================================================

def save_master(df, master_path: Path):

    df.to_csv(
        master_path,
        index=False,
        encoding="utf-8"
    )

    print("\nMaster Saved")
    print(master_path)
    print("Rows :", len(df))


# ============================================================
# APPEND RECORDS
# ============================================================

def append_records(
        master_df,
        upload_df,
        unique_column
):

    print("\n========== append_records ==========")
    print("Unique Column :", unique_column)
    print("Master Empty  :", master_df.empty)
    print("Master Columns:", master_df.columns.tolist())
    print("Upload Columns:", upload_df.columns.tolist())

    upload_df = upload_df.copy()

    upload_df[unique_column] = (
        upload_df[unique_column]
        .astype(str)
        .str.strip()
    )

    # First upload

    if master_df.empty:

        print("Creating first master...")

        upload_df = upload_df.drop_duplicates(
            subset=[unique_column]
        )

        return (
            upload_df,
            len(upload_df),
            0
        )

    master_df[unique_column] = (
        master_df[unique_column]
        .astype(str)
        .str.strip()
    )

    master_ids = set(

    master_df[unique_column]
    .dropna()
    .astype(str)
    .str.strip()

)

    new_rows = upload_df[
        ~upload_df[unique_column].isin(master_ids)
    ]

    duplicate_rows = upload_df[
        upload_df[unique_column].isin(master_ids)
    ]

    updated_master = pd.concat(
        [
            master_df,
            new_rows
        ],
        ignore_index=True
    )

    updated_master = updated_master.drop_duplicates(
        subset=[unique_column],
        keep="first"
    )

    return (
        updated_master,
        len(new_rows),
        len(duplicate_rows)
    )


    # ============================================================
# INCIDENT MASTER
# ============================================================

def append_incident_master(upload_file):

    print("\n" + "=" * 80)
    print("PROCESSING INCIDENT FILE")
    print("=" * 80)

    upload_df = read_incident_report(upload_file)

    print("Rows Read :", len(upload_df))

    upload_df = filter_ams_dataframe(upload_df)

    print("Rows After Filter :", len(upload_df))

    master_df = load_master(INCIDENT_MASTER)

    updated_master, new_count, duplicate_count = append_records(
        master_df,
        upload_df,
        "Incident ID"
    )

    save_master(
        updated_master,
        INCIDENT_MASTER
    )

    print("\n========== INCIDENT SUMMARY ==========")
    print(f"Existing Master : {len(master_df)}")
    print(f"Uploaded Rows   : {len(upload_df)}")
    print(f"New Rows        : {new_count}")
    print(f"Duplicates      : {duplicate_count}")
    print(f"Final Master    : {len(updated_master)}")

    return {
        "type": "incident",
        "uploaded": len(upload_df),
        "new": new_count,
        "duplicates": duplicate_count,
        "total": len(updated_master)
    }


# ============================================================
# REQUEST MASTER
# ============================================================

def append_request_master(upload_file):

    print("\n" + "=" * 80)
    print("PROCESSING REQUEST FILE")
    print("=" * 80)

    upload_df = read_request_report(upload_file)
    print("\n========== REQUEST COLUMNS ==========")
    print(upload_df.columns.tolist())

    print("Rows Read :", len(upload_df))

    upload_df = filter_ams_dataframe(upload_df)

    print("Rows After Filter :", len(upload_df))

    master_df = load_master(REQUEST_MASTER)

    updated_master, new_count, duplicate_count = append_records(
        master_df,
        upload_df,
        "Request ID"
    )

    save_master(
        updated_master,
        REQUEST_MASTER
    )

    print("\n========== REQUEST SUMMARY ==========")
    print(f"Existing Master : {len(master_df)}")
    print(f"Uploaded Rows   : {len(upload_df)}")
    print(f"New Rows        : {new_count}")
    print(f"Duplicates      : {duplicate_count}")
    print(f"Final Master    : {len(updated_master)}")

    return {
        "type": "request",
        "uploaded": len(upload_df),
        "new": new_count,
        "duplicates": duplicate_count,
        "total": len(updated_master)
    }