from fastapi import APIRouter
from api.services.call_code_service import (
    get_incident_call_code_data,
    get_service_call_code_data,
    get_call_code_summary,
    get_full_call_code_analysis
)

router = APIRouter()

# -----------------------------------
# 1. INCIDENT
# -----------------------------------
@router.get("/incident")
def incident_call_code():
    return get_incident_call_code_data()


# -----------------------------------
# 2. SERVICE
# -----------------------------------
@router.get("/service")
def service_call_code():
    return get_service_call_code_data()


# -----------------------------------
# 3. SUMMARY
# -----------------------------------
@router.get("/summary")
def call_code_summary():
    return get_call_code_summary()


# -----------------------------------
# 4. FULL ANALYSIS (FOR BAR CHART)
# -----------------------------------
@router.get("/full-analysis")
def full_analysis():
    return get_full_call_code_analysis()