from api.utils.csv_loader import load_csv

# -----------------------------------
# HELPER: CLEAN DATA TYPES
# -----------------------------------
def clean_dataframe(df):
    df["Call Code"] = df["Call Code"].astype(str)
    df["Category"] = df["Category"].astype(str)

    # Ensure numeric
    df["Count"] = df["Count"].astype(float).astype(int)
    df["Percentage"] = df["Percentage"].astype(float)

    return df


# -----------------------------------
# 1. INCIDENT DATA
# -----------------------------------
def get_incident_call_code_data():
    df = load_csv("Incident_Call_Code_Breakdown.csv")
    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# -----------------------------------
# 2. SERVICE DATA
# -----------------------------------
def get_service_call_code_data():
    df = load_csv("Service_Call_Code_Breakdown.csv")
    df = clean_dataframe(df)

    return df.to_dict(orient="records")


# -----------------------------------
# 3. INCIDENT SUMMARY (KPI CARDS)
# -----------------------------------
def get_call_code_summary():
    df = load_csv("Incident_Call_Code_Breakdown.csv")
    df = clean_dataframe(df)

    total_tickets = int(df["Count"].sum())

    grouped = (
        df.groupby("Call Code")["Count"]
        .sum()
        .reset_index()
        .sort_values("Count", ascending=False)
    )

    top = grouped.iloc[0]

    return {
        "total_tickets": total_tickets,
        "dominant_channel": top["Call Code"],
        "percentage": round((top["Count"] / total_tickets) * 100, 2),
        "breakdown": grouped.to_dict(orient="records")
    }


# -----------------------------------
# 4. FULL ANALYSIS (FOR BAR CHART)
# -----------------------------------
def get_full_call_code_analysis():
    df_inc = clean_dataframe(load_csv("Incident_Call_Code_Breakdown.csv"))
    df_sr = clean_dataframe(load_csv("Service_Call_Code_Breakdown.csv"))

    # Aggregate Incident
    incident_grouped = (
        df_inc.groupby("Call Code")["Count"]
        .sum()
        .reset_index()
    )

    # Aggregate Service
    service_grouped = (
        df_sr.groupby("Call Code")["Count"]
        .sum()
        .reset_index()
    )

    # Merge both
    merged = incident_grouped.merge(
        service_grouped,
        on="Call Code",
        how="outer",
        suffixes=("_incident", "_service")
    ).fillna(0)

    # Final clean structure for frontend
    result = [
        {
            "callCode": row["Call Code"],
            "incident": int(row["Count_incident"]),
            "service": int(row["Count_service"])
        }
        for _, row in merged.iterrows()
    ]

    return result