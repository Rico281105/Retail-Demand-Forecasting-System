import pickle
import pandas as pd
import sqlite3

with open(
    "models/prophet_model.pkl",
    "rb"
) as f:
    model = pickle.load(f)

future = model.make_future_dataframe(
    periods=90
)

forecast = model.predict(
    future
)

forecast["yhat"] = forecast["yhat"].clip(lower=0)
forecast["yhat_lower"] = forecast["yhat_lower"].clip(lower=0)

forecast_df = forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
]

# Mark forecast rows
forecast_df["is_forecast"] = False

forecast_df.loc[
    forecast_df.index >= len(forecast_df) - 90,
    "is_forecast"
] = True

forecast_df.to_csv(
    "data/forecast.csv",
    index=False
)

conn = sqlite3.connect(
    "retail_forecast.db"
)

forecast_df.to_sql(
    "sales_forecast",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Forecast generated successfully.")
