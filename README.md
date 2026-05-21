# Sales & Revenue Executive Dashboard

This is a complete data analytics project built as an executive-ready sales dashboard for 2024.
The dashboard is designed to satisfy the assignment instructions with a polished analytics experience.

## What the project includes
- 8 KPI cards for Total Revenue, Total Profit, Total Cost, Profit Margin, Total Orders, Average Discount, Top Region, and Top Salesperson
- 12 interactive charts including trend analysis, category split, region performance, segment split, discount impact, payment distribution, product leaderboard, heatmap, and cumulative revenue
- Global sidebar filters for date range, category, region, salesperson, customer segment, payment method, and discount range
- Automated insights cards for best month, best category, weakest region, discount impact, and top salesperson
- A modular codebase with reusable data and chart functions

## Project structure
- `app.py` — Streamlit application entrypoint
- `src/data_loader.py` — data ingestion, cleaning, filtering, and KPI aggregation
- `src/charts.py` — reusable chart builders for all dashboard visuals
- `data/` — dataset folder for `sales_revenue_dataset.csv`
- `requirements.txt` — Python dependencies
- `.gitignore` — recommended ignore rules
- `tests/test_data_loader.py` — basic validation for data ingestion and profit margin calculations

## Compliance checklist
- [x] Monthly revenue and profit trend chart
- [x] Revenue by category chart
- [x] Region-wise sales performance chart
- [x] Salesperson leaderboard chart
- [x] Revenue vs cost vs profit monthly chart
- [x] B2B vs B2C revenue split chart
- [x] Discount vs profit scatter plot
- [x] Payment method distribution chart
- [x] Top 10 products by revenue chart
- [x] Units sold heatmap by category and region
- [x] Profit margin by category chart
- [x] Cumulative YTD revenue growth line
- [x] Date range, category, region, salesperson, segment, payment, and discount filters
- [x] Automated insights panel

## Dataset
Place the dataset file here:

```bash
./data/sales_revenue_dataset.csv
```

The dashboard expects the dataset with the same columns as described in the assignment.

## Run locally
1. Create and activate a Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the dashboard:
   ```bash
   streamlit run app.py
   ```

## Submission instructions
- Upload this folder to your GitHub repository.
- Include this `README.md` in the root of the repo.
- Share the GitHub repository link as your submission.

## Notes
- If your dataset file is outside the repository, copy it into `data/sales_revenue_dataset.csv`.
- The app is ready to run after dependency installation and placing the dataset in the `data/` folder.
