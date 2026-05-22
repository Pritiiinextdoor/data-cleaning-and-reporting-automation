# Sales Revenue Analysis & Forecasting Dashboard

This project delivers a complete analytics deliverable for your internship task using the `sales_revenue_dataset.csv` dataset.

## What this project includes

- Data cleaning and preprocessing with `pandas`
- Executive KPI metrics for revenue, profit, cost, margin, orders, discounts, top region, and top salesperson
- Visual analytics for monthly revenue and profit trends, revenue by category, region performance, customer segment split, product performance, discount impact, and heatmap analysis
- Predictive revenue forecasting for the next 6 months using historical monthly sales trends
- Forecast evaluation metrics and future outlook

## Forecast summary

- Next month revenue forecast: **₹4,774,003** (January 2025)
- 6-month revenue outlook: **₹27,489,821.07**
- Forecast model accuracy (MAPE): **24.69%**

## How to run

1. Make sure the dataset file is placed in `data/sales_revenue_dataset.csv`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

## Key files

- `app.py` — main Streamlit dashboard
- `src/data_loader.py` — data ingestion, cleaning, filtering, and KPI aggregation
- `src/charts.py` — dashboard visualization functions
- `src/predictive_model.py` — monthly revenue forecasting logic and evaluation
- `tests/` — automated tests for data loading and forecasting logic

## Notes for submission

- The dashboard is ready to run immediately after placing the CSV file in `data/`
- It includes both descriptive analytics and predictive modeling components
- The forecast is based on monthly revenue trends from the dataset and provides a business-ready outlook for the next six months
