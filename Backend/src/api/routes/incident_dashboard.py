from fastapi import APIRouter

from api.services.incident_dashboard_service import (
    load_incident_dashboard_data
)

router = APIRouter()

# ========================================================
# INCIDENT DASHBOARD API
# ========================================================

@router.get("/")

def get_incident_dashboard():

    data = load_incident_dashboard_data()

    return data