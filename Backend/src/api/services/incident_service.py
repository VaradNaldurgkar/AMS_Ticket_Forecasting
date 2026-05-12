import pandas as pd
import os
from datetime import datetime

# ========================================================
# PATH SETUP
# ========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# api/services -> api -> src -> Backend
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(CURRENT_DIR)
    )
)

MASTER_CSV = os.path.join(
    BASE_DIR, "data", "processed", "AMS_Ticket_Master.csv"
)

# Threshold (in days) after which an unresolved ticket is "Pending"
PENDING_THRESHOLD_DAYS = 7


# ========================================================
# HELPERS
# ========================================================

def _row_status(row, today):
    """Derive per-ticket status from open/resolve timestamps."""

    resolve = row.get("Resolve Time (Timezone based)")

    if pd.notna(resolve) and str(resolve).strip() != "":
        return "Closed"

    open_time = row.get("Open Time (Timezone based)")

    if pd.isna(open_time):
        return "Open"

    age_days = (today - open_time).days

    if age_days > PENDING_THRESHOLD_DAYS:
        return "Pending"

    return "Open"


def _dominant_status(open_c, closed_c, pending_c):
    """Pick the largest status bucket as the headline status."""

    counts = {
        "Open": open_c,
        "Closed": closed_c,
        "Pending": pending_c,
    }

    return max(counts, key=counts.get)


def _compute_trend(month_series):
    """Compare latest vs previous month count: up / down / neutral."""

    monthly = (
        month_series.value_counts()
        .sort_index()
    )

    if len(monthly) < 2:
        return "neutral"

    last = monthly.iloc[-1]
    prev = monthly.iloc[-2]

    if last > prev:
        return "up"

    if last < prev:
        return "down"

    return "neutral"


# ========================================================
# MAIN LOADER
# ========================================================

def load_incident_status_trend():

    df = pd.read_csv(MASTER_CSV)

    # Keep only incidents
    df = df[df["Ticket_Type"].str.lower() == "incident"].copy()

    # Parse timestamps
    df["Open Time (Timezone based)"] = pd.to_datetime(
        df["Open Time (Timezone based)"], errors="coerce"
    )

    df["Resolve Time (Timezone based)"] = pd.to_datetime(
        df["Resolve Time (Timezone based)"], errors="coerce"
    )

    # Reference "today" = latest reported date in dataset
    today = df["Open Time (Timezone based)"].max()

    if pd.isna(today):
        today = pd.Timestamp(datetime.utcnow())

    # Per-ticket status
    df["__status"] = df.apply(lambda r: _row_status(r, today), axis=1)

    # Aggregate per Title
    rows = []

    grouped = df.groupby("Title", dropna=True)

    for title, g in grouped:

        total = int(len(g))

        open_c = int((g["__status"] == "Open").sum())
        closed_c = int((g["__status"] == "Closed").sum())
        pending_c = int((g["__status"] == "Pending").sum())

        status = _dominant_status(open_c, closed_c, pending_c)

        trend = _compute_trend(g["Month"])

        rows.append({
            "name": str(title),
            "count": total,
            "open": open_c,
            "closed": closed_c,
            "pending": pending_c,
            "status": status,
            "trend": trend,
        })

    # Sort by total tickets desc
    rows.sort(key=lambda x: x["count"], reverse=True)

    return {
        "total_types": len(rows),
        "incidents": rows,
    }
