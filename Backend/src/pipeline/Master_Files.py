import pandas as pd

# ============================================================
# FILE PATHS
# ============================================================

INCIDENT_FILE = r"../../data/Master/master_incidents.xlsx"
REQUEST_FILE = r"../../data/Master/master_requests.xlsx"

# ============================================================
# LOAD FILES
# ============================================================

incidents = pd.read_excel(INCIDENT_FILE)
requests = pd.read_excel(REQUEST_FILE)

# ============================================================
# FIND REQUIRED COLUMNS
# ============================================================

incident_date_col = next(
    col for col in incidents.columns
    if "Open Time" in col
)

request_date_col = next(
    col for col in requests.columns
    if "Open Time" in col
)

incident_resolve_col = next(
    col for col in incidents.columns
    if "Resolve Group" in col
)

request_resolve_col = next(
    col for col in requests.columns
    if "Resolve Group" in col
)

print(f"Incident Date Column   : {incident_date_col}")
print(f"Request Date Column    : {request_date_col}")
print(f"Incident Resolve Group : {incident_resolve_col}")
print(f"Request Resolve Group  : {request_resolve_col}")

# ============================================================
# CONVERT DATE COLUMNS
# ============================================================

incidents[incident_date_col] = pd.to_datetime(
    incidents[incident_date_col],
    errors="coerce"
)

requests[request_date_col] = pd.to_datetime(
    requests[request_date_col],
    errors="coerce"
)

# ============================================================
# FILTER VALUES
# ============================================================

valid_groups = [
    "AV/VC Support VW Group IT Solution",
    "Asset Support VW Group IT Solution",
    "Service Desk VW Group IT Solution"
]

start_date = pd.Timestamp("2026-01-01")
end_date = pd.Timestamp("2026-02-01")  # exclusive

# ============================================================
# INCIDENT FILTER
# ============================================================

jan_incidents = incidents[
    (incidents[incident_date_col] >= start_date)
    & (incidents[incident_date_col] < end_date)
    & (incidents[incident_resolve_col].isin(valid_groups))
]

# ============================================================
# REQUEST FILTER
# ============================================================

jan_requests = requests[
    (requests[request_date_col] >= start_date)
    & (requests[request_date_col] < end_date)
    & (requests[request_resolve_col].isin(valid_groups))
]

# ============================================================
# COUNTS
# ============================================================

incident_count = len(jan_incidents)
request_count = len(jan_requests)
total_count = incident_count + request_count

# ============================================================
# OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("JANUARY 2026 FILTERED TICKET COUNT")
print("=" * 60)

print(f"Incidents     : {incident_count:,}")
print(f"Requests      : {request_count:,}")
print(f"Total Tickets : {total_count:,}")

print("=" * 60)

# Optional: show group-wise split

print("\nINCIDENT GROUP SPLIT")
print(
    jan_incidents[incident_resolve_col]
    .value_counts()
    .sort_index()
)

print("\nREQUEST GROUP SPLIT")
print(
    jan_requests[request_resolve_col]
    .value_counts()
    .sort_index()
)