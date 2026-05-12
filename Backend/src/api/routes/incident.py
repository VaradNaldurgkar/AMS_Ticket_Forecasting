from fastapi import APIRouter

from api.services.incident_service import (
    load_incident_status_trend
)

router = APIRouter()

# ========================================================
# INCIDENT STATUS + TREND API
# ========================================================

@router.get("/status-trend")
def get_status_trend():

    return load_incident_status_trend()
