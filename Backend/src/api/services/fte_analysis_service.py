import os
import pandas as pd

# ======================================================
# DEBUGGING PATHS
# ======================================================

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

# ======================================================
# FILE PATHS
# ======================================================

COMBINED_FILE = os.path.join(
    FTE_ANALYSIS_DIR,
    "combined_distribution.csv"
)

# ======================================================
# DEBUG PRINTS
# ======================================================

print("\n========== FTE ANALYSIS DEBUG ==========")

print("CURRENT_DIR:")
print(CURRENT_DIR)

print("\nPROJECT_ROOT:")
print(PROJECT_ROOT)

print("\nFTE_ANALYSIS_DIR:")
print(FTE_ANALYSIS_DIR)

print("\nCOMBINED_FILE:")
print(COMBINED_FILE)

print("\nCOMBINED FILE EXISTS:")
print(os.path.exists(COMBINED_FILE))

print("\n========================================\n")

# ======================================================
# GET COMBINED ANALYSIS
# ======================================================

def get_combined_analysis():

    if not os.path.exists(COMBINED_FILE):

        return {

            "success": False,

            "message":
                "Combined distribution file not found",

            "path_checked":
                COMBINED_FILE

        }

    df = pd.read_csv(COMBINED_FILE)

    data = df.to_dict(
        orient="records"
    )

    return {

        "success": True,

        "total_records":
            len(data),

        "data":
            data

    }

# ======================================================
# GET PRIORITY SUMMARY
# ======================================================

def get_priority_summary():

    combined_response = (
        get_combined_analysis()
    )

    if not combined_response["success"]:

        return combined_response

    combined_data = (
        combined_response["data"]
    )

    priority_summary = {}

    for item in combined_data:

        priority = str(
            item["priority"]
        )

        if priority not in priority_summary:

            priority_summary[
                priority
            ] = {

                "ticket_count": 0,

                "total_effort": 0

            }

        priority_summary[
            priority
        ]["ticket_count"] += (
            item["ticket_count"]
        )

        priority_summary[
            priority
        ]["total_effort"] += (
            item["total_effort_min"]
        )

    return {

        "success": True,

        "data":
            priority_summary

    }

# ======================================================
# CALCULATE FTE REQUIRED
# ======================================================

def calculate_fte_required(
    predicted_tickets,
    productive_minutes=7400
):

    combined_response = (
        get_combined_analysis()
    )

    if not combined_response["success"]:

        return combined_response

    combined_data = (
        combined_response["data"]
    )

    workload_breakdown = []

    total_effort = 0

    # ==================================================
    # CATEGORY + PRIORITY WORKLOAD
    # ==================================================

    for item in combined_data:

        distribution_percentage = float(
            item[
                "distribution_percentage"
            ]
        )

        avg_resolution_time = float(
            item[
                "avg_resolution_time"
            ]
        )

        category = item["category"]

        priority = item["priority"]

        # ----------------------------------------------
        # ESTIMATED FUTURE TICKETS
        # ----------------------------------------------

        estimated_tickets = round(

            (
                distribution_percentage / 100
            ) *

            predicted_tickets

        )

        # ----------------------------------------------
        # TOTAL EFFORT
        # ----------------------------------------------

        effort = (

            estimated_tickets *

            avg_resolution_time

        )

        total_effort += effort

        workload_breakdown.append({

            "category":
                category,

            "priority":
                priority,

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

        })

    # ==================================================
    # FINAL FTE
    # ==================================================

    fte_required = (

        total_effort /

        productive_minutes

    )

    engineers_required = int(
        round(fte_required + 0.5)
    )

    capacity_available = (
        engineers_required *
        productive_minutes
    )

    utilization = (

        (
            total_effort /
            capacity_available
        ) * 100

    )

    # ==================================================
    # PRIORITY SUMMARY
    # ==================================================

    priority_summary = {}

    for item in workload_breakdown:

        priority = str(
            item["priority"]
        )

        if priority not in priority_summary:

            priority_summary[
                priority
            ] = {

                "tickets": 0,

                "effort": 0

            }

        priority_summary[
            priority
        ]["tickets"] += (
            item[
                "estimated_tickets"
            ]
        )

        priority_summary[
            priority
        ]["effort"] += (
            item[
                "total_effort"
            ]
        )

    # ==================================================
    # FINAL RESPONSE
    # ==================================================

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

        "priority_summary":
            priority_summary,

        "workload_breakdown":
            workload_breakdown

    }