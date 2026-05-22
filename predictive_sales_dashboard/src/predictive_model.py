from __future__ import annotations

import numpy as np
import pandas as pd


def prepare_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    monthly = (
        df.groupby(pd.Grouper(key='Date', freq='ME'))['Revenue']
        .sum()
        .reset_index()
        .dropna(subset=['Date'])
    )
    monthly = monthly.sort_values('Date').reset_index(drop=True)
    monthly['Month_Label'] = monthly['Date'].dt.strftime('%b %Y')
    monthly['Month_Index'] = np.arange(1, len(monthly) + 1)
    return monthly[['Month_Label', 'Date', 'Month_Index', 'Revenue']]


def forecast_revenue(df: pd.DataFrame, forecast_periods: int = 6) -> pd.DataFrame:
    monthly = prepare_monthly_revenue(df)
    x = monthly['Month_Index'].to_numpy()
    y = monthly['Revenue'].to_numpy()

    if len(x) < 2:
        raise ValueError('At least two months of revenue data are required for forecasting.')

    slope, intercept = np.polyfit(x, y, deg=1)
    future_indexes = np.arange(x[-1] + 1, x[-1] + 1 + forecast_periods)
    future_dates = pd.date_range(start=monthly['Date'].iloc[-1] + pd.offsets.MonthBegin(1), periods=forecast_periods, freq='MS')
    future_labels = future_dates.strftime('%b %Y')
    future_forecast = intercept + slope * future_indexes

    forecast_future = pd.DataFrame({
        'Month_Label': future_labels,
        'Date': future_dates,
        'Month_Index': future_indexes,
        'Revenue': np.nan,
        'Forecast': future_forecast,
        'Type': 'Forecast',
    })

    monthly['Forecast'] = intercept + slope * monthly['Month_Index']
    monthly['Type'] = 'Actual'
    monthly = monthly.rename(columns={'Revenue': 'Actual_Revenue'})
    monthly['Forecast'] = monthly['Forecast'].round(2)
    forecast_future['Forecast'] = forecast_future['Forecast'].round(2)
    combined = pd.concat([monthly, forecast_future], ignore_index=True, sort=False)
    combined['Revenue'] = combined['Actual_Revenue'].fillna(combined['Forecast'])
    return combined[['Month_Label', 'Date', 'Month_Index', 'Actual_Revenue', 'Forecast', 'Revenue', 'Type']]


def evaluate_forecast(df: pd.DataFrame) -> dict:
    combined = forecast_revenue(df, forecast_periods=0)
    actual = combined.loc[combined['Type'] == 'Actual', 'Actual_Revenue'].to_numpy()
    predicted = combined.loc[combined['Type'] == 'Actual', 'Forecast'].to_numpy()
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100 if actual.size else 0
    slope = (predicted[-1] - predicted[0]) / (len(predicted) - 1) if len(predicted) > 1 else 0
    trend = 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
    return {
        'rmse': float(rmse),
        'mape': float(mape),
        'trend': trend,
        'slope': float(slope),
    }


def next_period_summary(df: pd.DataFrame, forecast_periods: int = 6) -> dict:
    combined = forecast_revenue(df, forecast_periods=forecast_periods)
    forecast_rows = combined.loc[combined['Type'] == 'Forecast']
    avg_forecast = float(forecast_rows['Forecast'].mean())
    next_month = forecast_rows.iloc[0]['Month_Label']
    last_forecast = int(forecast_rows.iloc[-1]['Forecast'])
    return {
        'next_month': next_month,
        'avg_forecast': avg_forecast,
        'six_month_forecast_total': float(forecast_rows['Forecast'].sum()),
        'last_forecast': last_forecast,
    }
