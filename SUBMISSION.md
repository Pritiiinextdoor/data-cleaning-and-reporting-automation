# Submission Guide

This project is ready to submit as a GitHub repository for your data analytics assignment.

## What to include in the repository
- `app.py`
- `src/data_loader.py`
- `src/charts.py`
- `requirements.txt`
- `README.md`
- `.gitignore`
- `tests/test_data_loader.py`
- `data/` folder containing `sales_revenue_dataset.csv`

## How to submit
1. Create a new GitHub repository for your project.
2. Copy these files into the repository root.
3. Add the dataset file to the `data/` folder.
4. Commit and push the repository to GitHub.
5. Share the GitHub repository URL as your submission link.

## How to run the dashboard
```bash
pip install -r requirements.txt
streamlit run app.py
```

## What the dashboard shows
- Executive KPIs
- Revenue and profit trends
- Category and region analysis
- Salesperson performance
- B2B vs B2C split
- Discount impact on profit
- Payment method distribution
- Product revenue leaderboard
- Units sold heatmap
- Profit margin by category
- Cumulative YTD revenue growth
- Auto-generated insights panel
