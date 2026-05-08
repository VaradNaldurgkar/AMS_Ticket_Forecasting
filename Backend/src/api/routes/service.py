from fastapi import APIRouter

from api.services.service_service import (
    load_service_breakdown
)
router = APIRouter()

# ========================================================
# SERVICE BREAKDOWN API
# ========================================================

@router.get("/service-breakdown")
def get_service_breakdown():

    data = load_service_breakdown()

    return data