import pandas as pd

from src.predictive_model import evaluate_forecast, forecast_revenue, next_period_summary


def test_forecast_revenue_basic():
    sample = pd.DataFrame(
        {
            'Date': ['01-01-2024', '01-02-2024', '01-03-2024', '01-04-2024'],
            'Revenue': [1000.0, 1200.0, 1400.0, 1600.0],
        }
    )
    result = forecast_revenue(sample, forecast_periods=2)
    assert result.shape[0] == 6
    assert 'Forecast' in result.columns
    assert result.loc[result['Type'] == 'Forecast', 'Forecast'].iloc[0] > 0
    assert result.loc[result['Type'] == 'Actual', 'Actual_Revenue'].iloc[0] == 1000.0


def test_evaluate_forecast_returns_metrics():
    sample = pd.DataFrame(
        {
            'Date': ['01-01-2024', '01-02-2024', '01-03-2024', '01-04-2024'],
            'Revenue': [1000.0, 1100.0, 1200.0, 1300.0],
        }
    )
    metrics = evaluate_forecast(sample)
    assert metrics['rmse'] >= 0
    assert metrics['mape'] >= 0
    assert metrics['trend'] in ('increasing', 'decreasing', 'stable')


def test_next_period_summary_values():
    sample = pd.DataFrame(
        {
            'Date': ['01-01-2024', '01-02-2024', '01-03-2024', '01-04-2024'],
            'Revenue': [1000.0, 1100.0, 1200.0, 1300.0],
        }
    )
    summary = next_period_summary(sample, forecast_periods=3)
    assert summary['avg_forecast'] > 0
    assert 'next_month' in summary
    assert summary['six_month_forecast_total'] > 0
