import streamlit as st
import pandas as pd
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Retail Demand Forecasting Dashboard",
    layout="wide"
)

# =====================================================
# COMPANY STYLE THEME
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #0b1120;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    color: white;
}

.sub-title {
    color: #94a3b8;
    font-size: 18px;
    margin-bottom: 20px;
}

[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 15px;
    padding: 20px;
}

[data-testid="metric-container"] label {
    color: #94a3b8 !important;
}

h2,h3 {
    color: white !important;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FILE PATHS
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

forecast_path = os.path.join(
    BASE_DIR,
    "data",
    "forecast.csv"
)

train_path = os.path.join(
    BASE_DIR,
    "data",
    "train.csv"
)

# =====================================================
# LOAD DATA
# =====================================================

forecast = pd.read_csv(forecast_path)

forecast["ds"] = pd.to_datetime(
    forecast["ds"]
)

forecast["yhat"] = forecast["yhat"].clip(lower=0)
forecast["yhat_lower"] = forecast["yhat_lower"].clip(lower=0)

sales_df = pd.read_csv(train_path)

sales_df["Order Date"] = pd.to_datetime(
    sales_df["Order Date"],
    dayfirst=True
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("Dashboard Filters")

selected_region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(
        sales_df["Region"].unique().tolist()
    )
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(
        sales_df["Category"].unique().tolist()
    )
)

filtered_df = sales_df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="main-title">
📊 Retail Demand Forecasting Dashboard
</div>

<div class="sub-title">
Business Intelligence | Sales Forecasting | Inventory Planning
</div>
""", unsafe_allow_html=True)

# =====================================================
# FUTURE FORECAST
# =====================================================

future_forecast = forecast[
    forecast["is_forecast"] == True
]

monthly_forecast = (
    future_forecast
    .set_index("ds")
    .resample("ME")
    .mean(numeric_only=True)
)

# =====================================================
# FORECAST CHART
# =====================================================

st.subheader("Monthly Sales Forecast")

st.line_chart(
    monthly_forecast["yhat"]
)

# =====================================================
# KPI CARDS
# =====================================================

forecasted_revenue = future_forecast["yhat"].sum()

highest_day = future_forecast.loc[
    future_forecast["yhat"].idxmax()
]

lowest_day = future_forecast.loc[
    future_forecast["yhat"].idxmin()
]

average_sales = future_forecast["yhat"].mean()

st.subheader("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Forecasted Revenue",
    f"${forecasted_revenue:,.2f}"
)

col2.metric(
    "Highest Demand",
    f"${highest_day['yhat']:,.2f}"
)

col3.metric(
    "Lowest Demand",
    f"${lowest_day['yhat']:,.2f}"
)

col4.metric(
    "Average Daily Sales",
    f"${average_sales:,.2f}"
)

# =====================================================
# PEAK DEMAND
# =====================================================

st.subheader("Highest Demand Day")

st.success(
    f"""
📈 Peak Demand Date:
{highest_day['ds'].strftime('%d %B %Y')}

Predicted Sales:
${highest_day['yhat']:,.2f}
"""
)

# =====================================================
# CATEGORY ANALYSIS
# =====================================================

st.subheader("Sales by Category")

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_sales)

# =====================================================
# REGION ANALYSIS
# =====================================================

st.subheader("Sales by Region")

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(region_sales)

# =====================================================
# TOP PRODUCTS
# =====================================================

st.subheader("Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# =====================================================
# FORECAST TABLE
# =====================================================

st.subheader("90-Day Future Forecast")

display_forecast = future_forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
].copy()

display_forecast.columns = [
    "Date",
    "Predicted Sales",
    "Lower Bound",
    "Upper Bound"
]

st.dataframe(
    display_forecast,
    use_container_width=True
)

# =====================================================
# FORECAST INFO
# =====================================================

with st.expander(
    "What are Lower Bound and Upper Bound?"
):
    st.write("""
Predicted Sales:
Expected sales value.

Lower Bound:
Conservative estimate.

Upper Bound:
Optimistic estimate.

These values form the forecast confidence interval.
""")

# =====================================================
# DOWNLOAD CSV
# =====================================================

csv = display_forecast.to_csv(
    index=False
)

st.download_button(
    label="Download Forecast CSV",
    data=csv,
    file_name="sales_forecast.csv",
    mime="text/csv"
)
