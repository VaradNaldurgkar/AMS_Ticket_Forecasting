from fastapi import APIRouter

from api.services.fte_analysis_service import (
    calculate_fte_required,
    get_combined_analysis,
    get_priority_summary,
    get_historical_pune_data
)

router = APIRouter()

# ======================================================
# COMBINED ANALYSIS
# ======================================================

@router.get("/combined-analysis")
def combined_analysis():

    return get_combined_analysis()

# ======================================================
# PRIORITY SUMMARY
# ======================================================

@router.get("/priority-summary")
def priority_summary():

    return get_priority_summary()

# ======================================================
# FTE CALCULATION
# ======================================================

@router.get("/calculate-fte/{predicted_tickets}")
def calculate_fte(
    predicted_tickets: int
):

    return calculate_fte_required(
        predicted_tickets
    )

# ======================================================
# HISTORICAL PUNE DATA
# ======================================================

@router.get("/historical-pune")
def historical_pune():
    return get_historical_pune_data()