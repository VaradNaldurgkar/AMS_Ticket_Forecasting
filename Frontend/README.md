# AMS Ticket Forecasting & Resource Planning Dashboard

## Project Overview

AMS Ticket Forecasting & Resource Planning Dashboard is an intelligent analytics platform built to analyze ticket inflow, predict future ticket volumes, and estimate engineer requirements for efficient ticket resolution.

This project helps AMS teams and management:

* Forecast monthly ticket inflow
* Analyze incidents and service requests
* Monitor resolution metrics
* Understand service bifurcation
* Track IT asset and software requisitions
* Estimate required engineer capacity for future workload

The platform integrates Machine Learning models with a dashboard to provide insights for better workforce planning and operational efficiency.

---

# Key Features

## Ticket Forecasting

* Monthly ticket volume prediction
* Historical trend analysis
* Actual vs predicted comparison
* Forecast evaluation metrics

## Incident Analysis

* Incident category breakdown
* Incident type analysis
* Resolution metrics
* Service-based bifurcation

## Service Request Analysis

* Call code bifurcation
* Service request classification
* Top service requests

## IT Requisition Dashboard

### IT Asset Requisition

* Asset category breakdown
* Year-wise filtering (2025 / 2026)
* Top requested assets

### Software Requisition

* Software request breakdown
* Approval/Rejection analysis
* Year-wise filtering (2025 / 2026)

## Upload Module

* Upload AMS ticket data
* Upload IT asset requisition files
* Upload software requisition files
* Automatic master file updates
* Duplicate removal using unique identifiers

---

# Tech Stack

## Frontend

* React.js
* Vite
* CSS
* Recharts

## Backend

* FastAPI
* Python

## Data Processing

* Pandas
* NumPy
* OpenPyXL

## Machine Learning

* XGBoost
* Scikit-learn

---

# Project Structure

```bash
AMS_Ticket_Forecasting/
│
├── Backend/
│   ├── data/
│   │   ├── raw/
│   │   ├── Master/
│   │   └── processed/
│   │
│   └── src/
│       ├── api/
│       │   ├── routes/
│       │   └── services/
│       │
│       └── pipeline/
│
└── Frontend/
    └── src/
```

---

# Data Flow

```text
Raw Excel Files
      ↓
Upload via Frontend
      ↓
Backend Upload API
      ↓
Master Excel Files Updated
      ↓
Pipeline Processing
      ↓
Processed CSV Files
      ↓
Dashboard APIs
      ↓
Frontend Dashboard
```

---

# Machine Learning Pipeline

## Data Aggregation

* Incident data processing
* Request data processing

## Feature Engineering

Features used:

* Lag features
* Rolling mean
* Rolling std
* Seasonal patterns

## Model Training

Algorithm used:

* XGBoost Regressor

## Forecast Output

* Predicted ticket volume
* Required engineer estimation

---

# Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

Windows:

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Backend

```bash
cd Backend/src
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# Frontend Setup

## Install Dependencies

```bash
npm install
```

## Run Frontend

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# Main API Endpoints

## Prediction APIs

* `/api/prediction/actual-vs-predicted`
* `/api/prediction/future`

## Incident APIs

* `/api/incident`

## Service APIs

* `/api/service`

## Requisition APIs

* `/api/requisition/asset-dashboard`
* `/api/requisition/software-dashboard`
* `/api/requisition/asset-breakdown`
* `/api/requisition/software-breakdown`

## Upload APIs

* `/api/upload-excel`
* `/api/uploads`

---

# Upload Types Supported

## AMS Upload

Requires:

* Incident file
* Request file

## Asset Upload

Requires:

* IT Asset requisition file

## Software Upload

Requires:

* Software requisition file

---

# Important Pipeline Files

* `step1_aggregation.py`
* `step2_ticket_master.py`
* `Asset_count.py`
* `software_requisition.py`
* `Prediction_Jan_to_Mar.py`
* `step7_monthly_ticket_forecast.py`

---

# Dashboard Modules

* Forecast Dashboard
* Incident Dashboard
* Service Dashboard
* FTE Analysis Dashboard
* Requisition Dashboard

---

# Future Enhancements

* Real-time dashboard updates from Excel
* Database integration
* Automated retraining
* Cloud deployment
* Role-based access control
* Notification system

---

# Author

**Varad Naldurgkar**
BTech Computer Science
AMS Ticket Forecasting Project
