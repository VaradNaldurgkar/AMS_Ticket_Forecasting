from fastapi import APIRouter

from api.services.forecast_evaluation_service import (
    get_forecast_evaluation
)

router = APIRouter()

@router.get("/")
def forecast_evaluation():

    return get_forecast_evaluation()