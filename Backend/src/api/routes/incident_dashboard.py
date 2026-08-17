from fastapi import APIRouter, Query

from api.services.incident_dashboard_service import (
    load_incident_dashboard_data
)

router = APIRouter()


# ========================================================
# INCIDENT DASHBOARD API
# ========================================================

@router.get("/")
def get_incident_dashboard(
    year: int | None = Query(
        default=None,
        description="Filter incidents by year, e.g. 2026"
    ),
    month: int | None = Query(
        default=None,
        ge=1,
        le=12,
        description="Filter incidents by month, 1-12"
    ),
    start_date: str | None = Query(
        default=None,
        description="Filter incidents from this date, format YYYY-MM-DD"
    ),
    end_date: str | None = Query(
        default=None,
        description="Filter incidents until this date, format YYYY-MM-DD"
    )
):
    """
    Return Incident Dashboard data.

    Supported filters:
        ?year=2026
        ?year=2026&month=7
        ?start_date=2026-01-01&end_date=2026-07-31
        ?year=2026&month=7&start_date=2026-07-01&end_date=2026-07-31
    """

    data = load_incident_dashboard_data(
        year=year,
        month=month,
        start_date=start_date,
        end_date=end_date
    )

    return data