import pandas as pd
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def load_csv(filename):
    path = os.path.join(PROCESSED_DIR, filename)
    return pd.read_csv(path)