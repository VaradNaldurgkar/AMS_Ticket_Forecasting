from fastapi import APIRouter

from api.services.requisition_service import (
    get_asset_breakdown,
    get_software_breakdown,
    get_asset_dashboard,
    get_software_dashboard
)

router = APIRouter()

# ======================================================
# ASSET BREAKDOWN
# ======================================================

@router.get(
    "/asset-breakdown"
)
def asset_breakdown():

    return get_asset_breakdown()

# ======================================================
# SOFTWARE BREAKDOWN
# ======================================================

@router.get(
    "/software-breakdown"
)
def software_breakdown():

    return get_software_breakdown()

# ======================================================
# ASSET DASHBOARD
# ======================================================

@router.get(
    "/asset-dashboard"
)
def asset_dashboard():

    return get_asset_dashboard()

# ======================================================
# SOFTWARE DASHBOARD
# ======================================================

@router.get(
    "/software-dashboard"
)
def software_dashboard():

    return get_software_dashboard()