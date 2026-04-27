import pandas as pd
import os

input_path = "data/processed/AMS_Ticket_Master.csv"
output_path = "data/processed/SR_Breakdown.csv"

df = pd.read_csv(input_path)

# Filter Service Requests
df_sr = df[df["Ticket_Type"] == "Service Request"]

# Bifurcation by Priority
sr_breakdown = (
    df_sr.groupby("Title")
    .size()
    .reset_index(name="Service_Request_Count")
    .sort_values("Service_Request_Count", ascending=False)
)

sr_breakdown.to_csv(output_path, index=False)

print("Service Request bifurcation created")
print("Path:", output_path)
print(sr_breakdown.head())