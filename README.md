# Retail Demand Forecasting System

## Overview

Retail Demand Forecasting System is a machine learning and business analytics project that predicts future retail sales using historical Superstore sales data. The project leverages time-series forecasting techniques to help businesses optimize inventory planning, reduce stock shortages, and improve decision-making through data-driven insights.

## Features

* Data Cleaning and Preprocessing
* Exploratory Data Analysis (EDA)
* Time-Series Sales Forecasting using Prophet
* Interactive Streamlit Dashboard
* Sales Trend Analysis
* Category-wise Sales Analysis
* Region-wise Sales Analysis
* Top Products Analysis
* Forecast Export to CSV
* SQL-based Forecast Storage

## Technologies Used

* Python
* Pandas
* NumPy
* Prophet
* Streamlit
* SQL (SQLite)
* Matplotlib
* Seaborn

## Project Structure

```text
Retail-Demand-Forecasting/
│
├── data/
│   └── train.csv
│
├── dashboard/
│   └── app.py
│
├── src/
│   ├── preprocess.py
│   ├── train.py
│   └── forecast.py
│
├── models/
│   └── .gitkeep
│
├── requirements.txt
├── README.md
└── .gitignore
```
## Dashboard Insights

* Forecasted Revenue
* Highest Demand Day
* Lowest Demand Day
* Average Daily Sales
* Monthly Sales Forecast
* Sales by Category
* Sales by Region
* Top 10 Products by Sales

## Installation

1. Clone the repository

git clone <repository-url>

2. Install dependencies

pip install -r requirements.txt

## Run the Project

python src/preprocess.py

python src/train.py

python src/forecast.py

streamlit run dashboard/app.py

## Future Enhancements

* LSTM-based forecasting model
* Product-level demand forecasting
* Inventory optimization recommendations
* Power BI integration
* Cloud deployment

## Author

Rico281105
