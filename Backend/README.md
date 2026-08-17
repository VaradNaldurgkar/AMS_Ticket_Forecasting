# AMS Backend Deployment Guide

## Technology Stack

- Python 3.14
- FastAPI
- Uvicorn
- Pandas
- XGBoost

## Deployment Steps

1. Extract the deployment package.

2. Open Command Prompt as Administrator.

3. Run:

```
install_dependencies.bat
```

4. Start the application:

```
start_server.bat
```

5. Configure IIS Reverse Proxy to:

```
http://127.0.0.1:8000
```

## Required IIS Components

- IIS
- URL Rewrite Module
- Application Request Routing (ARR)

## Application Entry Point

```
src.api.main:app
```

## Health Check

```
http://127.0.0.1:8000/
```

## Notes

- Keep the `data` folder intact.
- Do not delete the Master or Processed folders.
- The application requires the CSV master files during startup.