# Submission Guide

This project is the final internship submission for data cleaning and reporting automation.

## What is included

- `app.py` — Streamlit dashboard
- `src/data_loader.py` — raw sales data cleaning and transformation
- `src/charts.py` — dashboard visualizations
- `src/predictive_model.py` — revenue forecasting
- `requirements.txt`
- `README.md`
- `SUBMISSION.md`
- `tests/`
- `data/raw_sales_data-1.csv`

## How to submit with GitHub

1. Create a GitHub repository for this project.
2. Push all project files and the dataset (`data/raw_sales_data-1.csv`) to GitHub.
3. Copy the repository URL.
4. Paste the URL into the submission form.

Example:

    https://github.com/<yourusername>/<repo-name>

## GitHub CI

This repository includes a GitHub Actions workflow that runs tests on every push. It helps reviewers verify the project automatically.

## How to submit a live demo URL

If the platform requests a working app, deploy the dashboard and submit the live URL instead.

- Use Streamlit Community Cloud, Heroku, or Railway
- Deploy `app.py`
- Submit the generated app address

Example:

    https://<your-app-name>.streamlit.app

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What reviewers will see

- Cleaned order-level sales data
- Revenue and order trends
- Category and region analytics
- Payment method and status reports
- Top product revenue leaderboard
- 6-month revenue forecast
- Automated insights summary

## Final note

- Use the GitHub repo URL for code submission.
- Use a deployed app URL if the platform asks for a live demo.
- Ensure `data/raw_sales_data-1.csv` is included before pushing.
