from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os

# --------------------------------------------------
# FIX: Add project root (Backend) to Python path
# --------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))      # .../Backend/src/api
SRC_DIR = os.path.dirname(CURRENT_DIR)                        # .../Backend/src
BASE_DIR = os.path.dirname(SRC_DIR)                           # .../Backend

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --------------------------------------------------
# Imports (now resolvable)
# --------------------------------------------------
from pipeline.step7_monthly_ticket_forecast import get_future_forecast
from pipeline.Prediction_Jan_to_Mar import get_actual_vs_predicted

from api.routes import call_code

app = FastAPI()

# --------------------------------------------------
# CORS (for React)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# 1. Actual vs Predicted (Jan–Apr)
# --------------------------------------------------
@app.get("/api/prediction/actual-vs-predicted")
def actual_vs_predicted():
    return get_actual_vs_predicted()

# --------------------------------------------------
# 2. Future Forecast (May–Oct)
# --------------------------------------------------
@app.get("/api/prediction/future")
def future_forecast():
    return get_future_forecast()

# --------------------------------------------------
# 3. Call Code APIs
# --------------------------------------------------
app.include_router(
    call_code.router,
    prefix="/api/call-code",
    tags=["Call Code"]
)

# --------------------------------------------------
# 4. Health check
# --------------------------------------------------
@app.get("/")
def home():
    return {"status": "API running 🚀"}