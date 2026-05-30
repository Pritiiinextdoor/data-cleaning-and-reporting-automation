# Sales Data Automation Dashboard

A complete Python solution for cleaning raw sales data, generating automated reports, and forecasting revenue.

## What this project includes

- Raw sales ingestion and cleaning with `pandas`
- Missing value handling, duplicate removal, and inconsistent field normalization
- Automated reporting in dashboard and Excel output
- Visual summaries for revenue, region performance, payment mix, order status, top products, and forecasted revenue
- Predictive revenue forecast for the next 6 months using historical sales trends

## Key outcomes

- Understand data preprocessing for a raw transactional dataset
- Automate cleaning and report generation workflows using Python and Excel
- Improve reporting efficiency with a Streamlit dashboard and exportable summary files

## Outputs produced by automation

- `output/cleaned_sales_data.csv`
- `output/sales_report.xlsx`
- `output/summary_report.txt`

## Key files

- `app.py` — Streamlit dashboard for interactive reporting
- `automation.py` — automation script for cleaning and Excel report generation
- `src/data_loader.py` — raw file loading, cleaning, and aggregation
- `src/charts.py` — visual summary functions for the dashboard
- `src/predictive_model.py` — forecast model and evaluation utilities
- `tests/` — automated tests for data loading and forecasting

## Notes for submission

- The repository now supports both interactive dashboard exploration and batch automation exports
- The cleaning pipeline handles missing values, duplicate order IDs, inconsistent text fields, and numeric parsing
- The Excel report captures cleaned data plus summary tabs for KPIs and revenue breakdowns
