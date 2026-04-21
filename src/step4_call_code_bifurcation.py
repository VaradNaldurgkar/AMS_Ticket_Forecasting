import pandas as pd

# ========================================================
# FILE PATHS
# ========================================================

input_path = "data/processed/AMS_Ticket_Master.csv"

desktop_output_path = (
    r"C:\Users\S08OFJF\Desktop\Call_Code_Breakdown.csv"
)

# ========================================================
# LOAD DATA
# ========================================================

df = pd.read_csv(input_path)

# ========================================================
# SAFE CLEANUP
# ========================================================

df["Call Code"] = df["Call Code"].fillna("Unknown")

# ========================================================
# CALL CODE BIFURCATION
# ========================================================

call_code_breakdown = (
    df.groupby("Call Code")
    .size()
    .reset_index(name="Ticket_Count")
    .sort_values("Ticket_Count", ascending=False)
)

# ========================================================
# SAVE OUTPUT TO DESKTOP ✅
# ========================================================

call_code_breakdown.to_csv(desktop_output_path, index=False)

print("\n✅ Call Code bifurcation created successfully")
print(f"✅ File saved to: {desktop_output_path}")

print("\nPreview:")
print(call_code_breakdown.head(10))