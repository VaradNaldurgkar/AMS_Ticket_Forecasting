from fastapi import APIRouter, Query

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

@router.get("/asset-breakdown")
def asset_breakdown(
    year: str = Query("all"),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    return get_asset_breakdown(
        year,
        start_date,
        end_date
    )


# ======================================================
# SOFTWARE BREAKDOWN
# ======================================================

@router.get("/software-breakdown")
def software_breakdown(
    year: str = Query("all"),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    return get_software_breakdown(
        year,
        start_date,
        end_date
    )


# ======================================================
# ASSET DASHBOARD
# ======================================================

@router.get("/asset-dashboard")
def asset_dashboard(
    year: str = Query("all"),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    return get_asset_dashboard(
        year,
        start_date,
        end_date
    )


# ======================================================
# SOFTWARE DASHBOARD
# ======================================================

@router.get("/software-dashboard")
def software_dashboard(
    year: str = Query("all"),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    return get_software_dashboard(
        year,
        start_date,
        end_date
    )