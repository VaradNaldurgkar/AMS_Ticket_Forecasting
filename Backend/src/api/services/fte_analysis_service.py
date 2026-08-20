import os
import pandas as pd

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(CURRENT_DIR)
    )
)

FTE_ANALYSIS_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "fte_analysis"
)

COMBINED_FILE = os.path.join(
    FTE_ANALYSIS_DIR,
    "combined_distribution.csv"
)

AMS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "AMS_Yearly_Aggregated.csv"
)

HISTORICAL_START = pd.Timestamp(
    "2026-01-01"
)

print("\n========== FTE ANALYSIS DEBUG ==========")
print("CURRENT_DIR:", CURRENT_DIR)
print("PROJECT_ROOT:", PROJECT_ROOT)
print("FTE_ANALYSIS_DIR:", FTE_ANALYSIS_DIR)
print("COMBINED_FILE:", COMBINED_FILE)
print("COMBINED FILE EXISTS:", os.path.exists(COMBINED_FILE))
print("AMS_FILE:", AMS_FILE)
print("AMS FILE EXISTS:", os.path.exists(AMS_FILE))
print("HISTORICAL START:", HISTORICAL_START.strftime("%Y-%m"))
print("========================================\n")


def get_combined_analysis():

    if not os.path.exists(COMBINED_FILE):
        return {
            "success": False,
            "message": "Combined distribution file not found",
            "path_checked": COMBINED_FILE
        }

    df = pd.read_csv(COMBINED_FILE)

    data = df.to_dict(
        orient="records"
    )

    return {
        "success": True,
        "total_records": len(data),
        "data": data
    }


def get_priority_summary():

    combined_response = get_combined_analysis()

    if not combined_response["success"]:
        return combined_response

    combined_data = combined_response["data"]

    priority_summary = {}

    for item in combined_data:

        priority = str(
            item["priority"]
        )

        if priority not in priority_summary:

            priority_summary[priority] = {
                "ticket_count": 0,
                "total_effort": 0
            }

        priority_summary[priority][
            "ticket_count"
        ] += item["ticket_count"]

        priority_summary[priority][
            "total_effort"
        ] += item["total_effort_min"]

    return {
        "success": True,
        "data": priority_summary
    }


def get_historical_pune_data():

    if not os.path.exists(AMS_FILE):
        return {
            "success": False,
            "message": "AMS file not found",
            "path_checked": AMS_FILE
        }

    df = pd.read_csv(
        AMS_FILE
    )

    required_columns = [
        "Month",
        "Location",
        "Total_Tickets"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        return {
            "success": False,
            "message": (
                "Required columns missing: "
                +
                ", ".join(missing_columns)
            )
        }

    df["Location"] = (
        df["Location"]
        .astype(str)
        .str.strip()
    )

    df = df[
        df["Location"].str.casefold()
        ==
        "pune".casefold()
    ].copy()

    if df.empty:
        return {
            "success": True,
            "data": []
        }

    df["Month"] = pd.to_datetime(
        df["Month"].astype(str) + "-01",
        errors="coerce"
    )

    df["Total_Tickets"] = pd.to_numeric(
        df["Total_Tickets"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "Month",
            "Total_Tickets"
        ]
    )

    df = df[
        df["Month"] >= HISTORICAL_START
    ].copy()

    df = (
        df
        .sort_values("Month")
        .drop_duplicates(
            subset=["Month"],
            keep="last"
        )
        .reset_index(drop=True)
    )

    if df.empty:
        return {
            "success": True,
            "data": []
        }

    historical_data = []

    for _, row in df.iterrows():

        historical_data.append(
            {
                "month": row["Month"].strftime(
                    "%b %Y"
                ),
                "tickets": int(
                    round(
                        row["Total_Tickets"]
                    )
                )
            }
        )

    return {
        "success": True,
        "data": historical_data
    }


def calculate_fte_required(
    predicted_tickets,
    productive_minutes=7400
):

    combined_response = get_combined_analysis()

    if not combined_response["success"]:
        return combined_response

    combined_data = combined_response["data"]

    workload_breakdown = []

    total_effort = 0

    AVAILABLE_ENGINEERS = 22

    monthly_productivity = [
        77,
        115,
        97,
        117,
        85
    ]

    AVG_PRODUCTIVITY = round(
        sum(monthly_productivity)
        /
        len(monthly_productivity),
        1
    )

    monthly_capacity = round(
        AVAILABLE_ENGINEERS
        *
        AVG_PRODUCTIVITY,
        1
    )

    for item in combined_data:

        distribution_percentage = float(
            item["distribution_percentage"]
        )

        avg_resolution_time = float(
            item["avg_resolution_time"]
        )

        category = item["category"]

        priority = item["priority"]

        estimated_tickets = round(
            (
                distribution_percentage
                /
                100
            )
            *
            predicted_tickets
        )

        effort = (
            estimated_tickets
            *
            avg_resolution_time
        )

        total_effort += effort

        workload_breakdown.append(
            {
                "category": category,
                "priority": priority,
                "distribution_percentage":
                    distribution_percentage,
                "estimated_tickets":
                    estimated_tickets,
                "avg_resolution_time":
                    round(
                        avg_resolution_time,
                        2
                    ),
                "total_effort":
                    round(
                        effort,
                        2
                    )
            }
        )

    fte_required = (
        total_effort
        /
        productive_minutes
    )

    engineers_required = int(
        round(
            fte_required + 0.5
        )
    )

    capacity_available = (
        engineers_required
        *
        productive_minutes
    )

    if capacity_available > 0:

        utilization = (
            total_effort
            /
            capacity_available
        ) * 100

    else:

        utilization = 0

    required_tickets_per_engineer = round(
        predicted_tickets
        /
        AVAILABLE_ENGINEERS,
        1
    )

    productivity_gap = round(
        required_tickets_per_engineer
        -
        AVG_PRODUCTIVITY,
        1
    )

    ticket_gap = round(
        monthly_capacity
        -
        predicted_tickets,
        1
    )

    productivity_increase_needed = round(
        (
            productivity_gap
            /
            AVG_PRODUCTIVITY
        )
        *
        100,
        1
    )

    if productivity_increase_needed <= 5:

        status = "Healthy"

    elif productivity_increase_needed <= 15:

        status = "Moderate Risk"

    else:

        status = "High Risk"

    priority_summary = {}

    for item in workload_breakdown:

        priority = str(
            item["priority"]
        )

        if priority not in priority_summary:

            priority_summary[priority] = {
                "tickets": 0,
                "effort": 0
            }

        priority_summary[priority][
            "tickets"
        ] += item[
            "estimated_tickets"
        ]

        priority_summary[priority][
            "effort"
        ] += item[
            "total_effort"
        ]

    return {
        "success": True,
        "predicted_tickets":
            predicted_tickets,
        "productive_minutes":
            productive_minutes,
        "total_effort":
            round(
                total_effort,
                2
            ),
        "fte_required":
            round(
                fte_required,
                2
            ),
        "engineers_required":
            engineers_required,
        "capacity_available":
            capacity_available,
        "utilization":
            round(
                utilization,
                1
            ),
        "available_engineers":
            AVAILABLE_ENGINEERS,
        "monthly_productivity":
            monthly_productivity,
        "avg_productivity":
            AVG_PRODUCTIVITY,
        "monthly_capacity":
            monthly_capacity,
        "required_tickets_per_engineer":
            required_tickets_per_engineer,
        "productivity_gap":
            productivity_gap,
        "ticket_gap":
            ticket_gap,
        "productivity_increase_needed":
            productivity_increase_needed,
        "status":
            status,
        "priority_summary":
            priority_summary,
        "workload_breakdown":
            workload_breakdown
    }