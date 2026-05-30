from pathlib import Path

import streamlit as st

from src.charts import (
    cumulative_revenue_trend,
    monthly_revenue_trend,
    payment_method_distribution,
    revenue_by_category,
    region_sales_performance,
    revenue_forecast_trend,
    status_breakdown_chart,
    top_products_by_revenue,
    units_heatmap,
)
from src.data_loader import (
    compute_aggregates,
    compute_kpis,
    evaluate_insights,
    filter_sales_data,
    load_sales_data,
)
from src.predictive_model import (
    evaluate_forecast,
    forecast_revenue,
    next_period_summary,
)

st.set_page_config(page_title='Sales Automation Dashboard', layout='wide')

st.markdown(
    """
    <style>
        .reportview-container { background-color: #0b1724; color: #f5f3eb; }
        .stButton>button { background-color: #c79214; color: #0b1724; }
        .stMetricLabel { color: #f5f3eb; }
        .stMetricDelta { color: #a8ff60; }
        .kpi-card { background: #112338; border-radius: 18px; padding: 18px; margin-bottom: 12px; }
        .insight-card { background: #112338; border-radius: 18px; padding: 18px; margin-bottom: 16px; }
        .section-title { color: #f7c94d; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title('Automated Sales Cleaning & Reporting Dashboard')
st.markdown('This dashboard cleans raw sales data, handles duplicates and missing values, and generates reporting automation insights.')

DATA_DIR = Path(__file__).resolve().parent / 'data'
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / 'raw_sales_data-1.csv'

if not DATA_FILE.exists():
    st.error('Dataset not found. Place `raw_sales_data-1.csv` in the `data/` folder and reload.')
    st.stop()

sales = load_sales_data(DATA_FILE)

st.sidebar.header('Filter controls')
min_date = sales['Date'].min().date()
max_date = sales['Date'].max().date()

date_range = st.sidebar.date_input('Date range', [min_date, max_date], min_value=min_date, max_value=max_date)
category_filter = st.sidebar.multiselect('Product category', options=sorted(sales['Product_Category'].unique()), default=sorted(sales['Product_Category'].unique()))
region_filter = st.sidebar.multiselect('Region', options=sorted(sales['Region'].unique()), default=sorted(sales['Region'].unique()))
payment_filter = st.sidebar.multiselect('Payment method', options=sorted(sales['Payment_Method'].unique()), default=sorted(sales['Payment_Method'].unique()))
status_filter = st.sidebar.multiselect('Order status', options=sorted(sales['Status'].unique()), default=sorted(sales['Status'].unique()))
rating_min, rating_max = st.sidebar.slider('Rating range', min_value=float(sales['Rating'].min()), max_value=float(sales['Rating'].max()), value=(float(sales['Rating'].min()), float(sales['Rating'].max())), step=0.1)

if len(date_range) != 2:
    st.sidebar.error('Select a valid date range.')
    st.stop()

filtered = filter_sales_data(
    sales,
    date_range,
    category_filter,
    region_filter,
    payment_filter,
    status_filter,
    (rating_min, rating_max),
)

if filtered.empty:
    st.warning('No data matches the selected filters. Please adjust the controls.')
    st.stop()

kpis = compute_kpis(filtered)
aggregates = compute_aggregates(filtered)
forecast_df = forecast_revenue(filtered, forecast_periods=6)
forecast_metrics = evaluate_forecast(filtered)
forecast_summary = next_period_summary(filtered, forecast_periods=6)
insights = evaluate_insights(filtered, aggregates)

kpi_cols = st.columns(6)
card_values = [
    ('Total Revenue', f'₹{kpis["total_revenue"]:,.0f}', '#4bb543'),
    ('Total Orders', f'{kpis["total_orders"]:,}', '#f5f3eb'),
    ('Avg Order Value', f'₹{kpis["avg_order_value"]:,.0f}', '#f7c94d'),
    ('Average Rating', f'{kpis["avg_rating"]:.1f}', '#7ed957'),
    ('Top Category', kpis['top_category'], '#f7c94d'),
    ('Top Region', kpis['top_region'], '#f7c94d'),
]
for column, (label, value, color) in zip(kpi_cols, card_values):
    with column:
        st.markdown(
            f"<div class='kpi-card'><h4 style='margin:0;color:#f5f3eb'>{label}</h4><p style='font-size:22px;margin:0;color:{color}'>{value}</p></div>",
            unsafe_allow_html=True,
        )

st.markdown('---')
col1, col2 = st.columns(2)
col1.plotly_chart(monthly_revenue_trend(aggregates['monthly']), use_container_width=True)
col2.plotly_chart(cumulative_revenue_trend(aggregates['monthly']), use_container_width=True)

st.markdown('---')
col1, col2, col3 = st.columns(3)
col1.plotly_chart(revenue_by_category(aggregates['category_revenue']), use_container_width=True)
col2.plotly_chart(region_sales_performance(aggregates['region_revenue']), use_container_width=True)
col3.plotly_chart(payment_method_distribution(aggregates['payment_revenue']), use_container_width=True)

st.markdown('---')
col1, col2 = st.columns(2)
col1.plotly_chart(status_breakdown_chart(aggregates['status_breakdown']), use_container_width=True)
col2.plotly_chart(top_products_by_revenue(aggregates['product_revenue']), use_container_width=True)

st.markdown('---')
col1, col2 = st.columns(2)
col1.plotly_chart(units_heatmap(aggregates['heatmap_matrix']), use_container_width=True)
col2.plotly_chart(revenue_forecast_trend(forecast_df), use_container_width=True)

st.markdown('---')
st.subheader('Automated Insights')
insight_col1, insight_col2 = st.columns(2)
with insight_col1:
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Best performing month</h4><p style='font-size:20px;margin:0;'>{insights['best_month']}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Highest rated category</h4><p style='font-size:20px;margin:0;'>{insights['best_category']}</p></div>", unsafe_allow_html=True)
with insight_col2:
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Lowest revenue region</h4><p style='font-size:20px;margin:0;color:#ff5b5b;'>{insights['lowest_region']}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Best payment method</h4><p style='font-size:20px;margin:0;'>{insights['top_payment']}</p></div>", unsafe_allow_html=True)

st.markdown('---')
st.caption('Use the sidebar filters to explore data cleaning results, reporting automation, and forecast insights by category, region, payment method, status, and rating.')
