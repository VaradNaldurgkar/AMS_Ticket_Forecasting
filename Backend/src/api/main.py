from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your functions
from pipeline.step6_monthly_ticket_forecast import get_future_forecast
from pipeline.Prediction_Jan_to_Mar import get_actual_vs_predicted

app = FastAPI()

# ✅ VERY IMPORTANT (for React connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# 1. Actual vs Predicted (Jan–Apr)
# -----------------------------------
@app.get("/api/prediction/actual-vs-predicted")
def actual_vs_predicted():
    return get_actual_vs_predicted()


# -----------------------------------
# 2. Future Forecast (May–Oct)
# -----------------------------------
@app.get("/api/prediction/future")
def future_forecast():
    return get_future_forecast()


# -----------------------------------
# 3. Health check
# -----------------------------------
@app.get("/")
def home():
    return {"status": "API running 🚀"}