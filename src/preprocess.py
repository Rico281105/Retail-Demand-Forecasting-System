import pandas as pd

INPUT_FILE = "data/train.csv"
OUTPUT_FILE = "data/processed_sales.csv"

def preprocess():

    df = pd.read_csv(INPUT_FILE)

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True
    )

    df = df.dropna()

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Day"] = df["Order Date"].dt.day
    df["Weekday"] = df["Order Date"].dt.day_name()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Data preprocessing completed.")

if __name__ == "__main__":
    preprocess()
