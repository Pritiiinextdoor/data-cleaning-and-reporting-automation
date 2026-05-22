from pathlib import Path

import streamlit as st

from src.charts import (
    cumulative_revenue_degree,
    discount_profit_scatter,
    monthly_revenue_profit_trend,
    payment_method_distribution,
    profit_margin_by_category,
    region_sales_performance,
    revenue_by_category,
    revenue_cost_profit_monthly,
    revenue_forecast_trend,
    segment_revenue_split,
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

st.set_page_config(page_title='Sales & Revenue Executive Dashboard', layout='wide')

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

st.title('Sales & Revenue Executive Dashboard')
st.markdown('A polished analytics project dashboard for executive-level sales insights.')

DATA_DIR = Path(__file__).resolve().parent / 'data'
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / 'sales_revenue_dataset.csv'

if not DATA_FILE.exists():
    st.error('Dataset not found. Place `sales_revenue_dataset.csv` in the `data/` folder and reload.')
    st.stop()

sales = load_sales_data(DATA_FILE)

st.sidebar.header('Filter controls')
min_date = sales['Date'].min().date()
max_date = sales['Date'].max().date()

date_range = st.sidebar.date_input('Date range', [min_date, max_date], min_value=min_date, max_value=max_date)
category_filter = st.sidebar.multiselect('Product category', options=sorted(sales['Category'].unique()), default=sorted(sales['Category'].unique()))
region_filter = st.sidebar.multiselect('Region', options=sorted(sales['Region'].unique()), default=sorted(sales['Region'].unique()))
salesperson_filter = st.sidebar.multiselect('Salesperson', options=sorted(sales['Salesperson'].unique()), default=sorted(sales['Salesperson'].unique()))
segment_filter = st.sidebar.multiselect('Customer segment', options=sorted(sales['Customer_Segment'].unique()), default=sorted(sales['Customer_Segment'].unique()))
payment_filter = st.sidebar.multiselect('Payment method', options=sorted(sales['Payment_Method'].unique()), default=sorted(sales['Payment_Method'].unique()))
discount_min, discount_max = st.sidebar.slider('Discount % range', min_value=0, max_value=15, value=(0, 15), step=1)

if len(date_range) != 2:
    st.sidebar.error('Select a valid date range.')
    st.stop()

filtered = filter_sales_data(
    sales,
    date_range,
    category_filter,
    region_filter,
    salesperson_filter,
    segment_filter,
    payment_filter,
    (discount_min, discount_max),
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

kpi_cols = st.columns(8)
card_values = [
    ('Total Revenue', f'₹{kpis["total_revenue"]:,.0f}', '#4bb543'),
    ('Total Profit', f'₹{kpis["total_profit"]:,.0f}', '#4bb543' if kpis['total_profit'] >= 0 else '#d72638'),
    ('Total Cost', f'₹{kpis["total_cost"]:,.0f}', '#d72638'),
    ('Profit Margin', f'{kpis["profit_margin"]:.2f} %', '#f7c94d'),
    ('Total Orders', f'{kpis["total_orders"]:,}', '#f5f3eb'),
    ('Average Discount', f'{kpis["avg_discount"]:.2f} %', '#7ed957'),
    ('Top Region', kpis['top_region'], '#f7c94d'),
    ('Top Salesperson', kpis['top_salesperson'], '#f7c94d'),
]
for column, (label, value, color) in zip(kpi_cols, card_values):
    with column:
        st.markdown(
            f"<div class='kpi-card'><h4 style='margin:0;color:#f5f3eb'>{label}</h4><p style='font-size:26px;margin:0;color:{color}'>{value}</p></div>",
            unsafe_allow_html=True,
        )

st.markdown('---')
col1, col2 = st.columns(2)
col1.plotly_chart(monthly_revenue_profit_trend(aggregates['monthly']), use_container_width=True)
col2.plotly_chart(cumulative_revenue_degree(aggregates['monthly']), use_container_width=True)

st.markdown('---')
st.subheader('Revenue Forecast & Predictive Model')
st.markdown('Forecasting future revenue using historical monthly trends identifies the next six-month revenue outlook.')
forecast_a, forecast_b, forecast_c = st.columns(3)
forecast_a.metric('Next Month Forecast', f'₹{forecast_summary["last_forecast"]:,.0f}', forecast_summary['next_month'])
forecast_b.metric('6-Month Revenue Outlook', f'₹{forecast_summary["six_month_forecast_total"]:,.0f}', 'Projected total')
forecast_c.metric('Forecast MAPE', f'{forecast_metrics["mape"]:.2f} %', 'Model fit error')

st.plotly_chart(revenue_forecast_trend(forecast_df), use_container_width=True)

st.markdown('---')
col1, col2, col3 = st.columns(3)
col1.plotly_chart(revenue_by_category(aggregates['category_revenue']), use_container_width=True)
col2.plotly_chart(region_sales_performance(aggregates['region_revenue']), use_container_width=True)
col3.plotly_chart(segment_revenue_split(aggregates['segment_revenue']), use_container_width=True)

st.markdown('---')
col1, col2 = st.columns(2)
col1.plotly_chart(revenue_cost_profit_monthly(aggregates['monthly']), use_container_width=True)
col2.plotly_chart(payment_method_distribution(filtered), use_container_width=True)

st.markdown('---')
col1, col2 = st.columns(2)
col1.plotly_chart(discount_profit_scatter(filtered), use_container_width=True)
col2.plotly_chart(top_products_by_revenue(aggregates['product_revenue']), use_container_width=True)

st.markdown('---')
col1, col2 = st.columns(2)
col1.plotly_chart(units_heatmap(aggregates['heatmap_matrix']), use_container_width=True)
col2.plotly_chart(profit_margin_by_category(aggregates['category_margin']), use_container_width=True)

st.markdown('---')
st.subheader('Automated Insights')
insight_col1, insight_col2 = st.columns(2)
with insight_col1:
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Best performing month</h4><p style='font-size:20px;margin:0;'>{insights['best_month']}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Highest profit margin category</h4><p style='font-size:20px;margin:0;'>{insights['best_category']}</p></div>", unsafe_allow_html=True)
with insight_col2:
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Region needing attention</h4><p style='font-size:20px;margin:0;color:#ff5b5b;'>{insights['lowest_region']}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Heavy discounting hurts profit?</h4><p style='font-size:20px;margin:0;'>{'Yes' if insights['negative_discount_effect'] else 'No'}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight-card'><h4 class='section-title'>Top salesperson</h4><p style='font-size:20px;margin:0;'>{kpis['top_salesperson']}</p></div>", unsafe_allow_html=True)

st.markdown('---')
st.caption('Use the sidebar slicers to explore date range, category, region, salesperson, customer segment, payment method, discount range, and future revenue forecast across all visuals.')
