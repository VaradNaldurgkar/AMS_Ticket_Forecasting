from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os

# --------------------------------------------------
# ADD SRC DIRECTORY TO PYTHON PATH
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.dirname(CURRENT_DIR)

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# --------------------------------------------------
# IMPORT ROUTES
# --------------------------------------------------

from api.routes.service import (
    router as service_router
)

from api.routes import call_code

from api.routes import incident

from api.routes import incident_dashboard

from api.routes import forecast_evaluation

# ✅ NEW IMPORT
from api.routes.fte_analysis_route import (
    router as fte_router
)

# --------------------------------------------------
# IMPORT PIPELINES
# --------------------------------------------------

from pipeline.step7_monthly_ticket_forecast import (
    get_future_forecast
)

from pipeline.Prediction_Jan_to_Mar import (
    get_actual_vs_predicted
)

# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI()

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# PREDICTION APIs
# --------------------------------------------------

@app.get("/api/prediction/actual-vs-predicted")
def actual_vs_predicted():

    return get_actual_vs_predicted()

@app.get("/api/prediction/future")
def future_forecast():

    return get_future_forecast()

# --------------------------------------------------
# FORECAST EVALUATION APIs
# --------------------------------------------------

app.include_router(
    forecast_evaluation.router,
    prefix="/api/prediction/evaluation",
    tags=["Forecast Evaluation"]
)

# --------------------------------------------------
# CALL CODE APIs
# --------------------------------------------------

app.include_router(
    call_code.router,
    prefix="/api/call-code",
    tags=["Call Code"]
)

# --------------------------------------------------
# SERVICE APIs
# --------------------------------------------------

app.include_router(
    service_router,
    prefix="/api/service",
    tags=["Service"]
)

# --------------------------------------------------
# INCIDENT APIs
# --------------------------------------------------

app.include_router(
    incident.router,
    prefix="/api/incident",
    tags=["Incident"]
)

# --------------------------------------------------
# INCIDENT DASHBOARD APIs
# --------------------------------------------------

app.include_router(
    incident_dashboard.router,
    prefix="/api/incident-dashboard",
    tags=["Incident Dashboard"]
)

# --------------------------------------------------
# ✅ FTE ANALYSIS APIs
# --------------------------------------------------

app.include_router(
    fte_router,
    prefix="/api/fte",
    tags=["FTE Analysis"]
)

# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "status": "API running 🚀"
    }