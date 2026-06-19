import pandas as pd
from prophet import Prophet
import pickle

df = pd.read_csv(
    "data/processed_sales.csv"
)

df["Order Date"] = pd.to_datetime(
    df["Order Date"]
)

sales_data = (
    df.groupby("Order Date")["Sales"]
    .sum()
    .reset_index()
)

sales_data.columns = [
    "ds",
    "y"
]

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

model.fit(sales_data)

with open(
    "models/prophet_model.pkl",
    "wb"
) as f:
    pickle.dump(model, f)

print("Model trained successfully.")
