from pathlib import Path
import pandas as pd

file = Path(
    r"C:\Users\S08OFJF\Desktop\AMS_Ticket_Forecasting\Backend\data\Raw\1_100_IM Raw Data Report_June.xlsx"
)

for i in range(8):
    print("\n====================")
    print("HEADER =", i)
    print("====================")

    df = pd.read_excel(
        file,
        header=i,
        nrows=3
    )

    print(df.columns.tolist())