from pathlib import Path

import pandas as pd

from src.data_loader import compute_aggregates, compute_kpis, load_sales_data
from src.predictive_model import evaluate_forecast, forecast_revenue, next_period_summary

OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)
RAW_DATA_PATH = Path('data') / 'raw_sales_data-1.csv'


def save_excel_report(df: pd.DataFrame, output_path: Path) -> None:
    aggregates = compute_aggregates(df)
    kpis = compute_kpis(df)
    forecast_df = forecast_revenue(df, forecast_periods=6)
    metrics = evaluate_forecast(df)
    summary = next_period_summary(df, forecast_periods=6)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Cleaned_Data', index=False)
        pd.DataFrame([kpis]).to_excel(writer, sheet_name='KPI_Summary', index=False)
        aggregates['monthly'].to_excel(writer, sheet_name='Monthly_Revenue', index=False)
        aggregates['category_revenue'].to_excel(writer, sheet_name='Category_Revenue', index=False)
        aggregates['region_revenue'].to_excel(writer, sheet_name='Region_Revenue', index=False)
        aggregates['payment_revenue'].to_excel(writer, sheet_name='Payment_Methods', index=False)
        aggregates['status_breakdown'].to_excel(writer, sheet_name='Order_Status', index=False)
        aggregates['product_revenue'].to_excel(writer, sheet_name='Top_Products', index=False)
        forecast_df.to_excel(writer, sheet_name='Revenue_Forecast', index=False)
        pd.DataFrame([
            {
                'Next month forecast': summary['next_month'],
                '6-month forecast total': summary['six_month_forecast_total'],
                'Forecast MAPE': metrics['mape'],
                'Forecast trend': metrics['trend'],
            }
        ]).to_excel(writer, sheet_name='Forecast_Summary', index=False)


def save_summary_text(df: pd.DataFrame, output_path: Path) -> None:
    kpis = compute_kpis(df)
    summary = next_period_summary(df, forecast_periods=6)
    metrics = evaluate_forecast(df)
    lines = [
        'Sales Data Automation Summary',
        '=============================',
        f'Total cleaned records: {len(df)}',
        f'Total revenue: ₹{kpis["total_revenue"]:,.0f}',
        f'Total orders: {kpis["total_orders"]:,}',
        f'Average order value: ₹{kpis["avg_order_value"]:,.0f}',
        f'Average rating: {kpis["avg_rating"]:.2f}',
        f'Top category: {kpis["top_category"]}',
        f'Top region: {kpis["top_region"]}',
        f'Forecast next month: {summary["next_month"]}',
        f'Six-month outlook: ₹{summary["six_month_forecast_total"]:,.0f}',
        f'Forecast MAPE: {metrics["mape"]:.2f}% ({metrics["trend"]})',
    ]
    output_path.write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f'Missing raw sales file: {RAW_DATA_PATH.resolve()}')

    cleaned = load_sales_data(RAW_DATA_PATH)
    cleaned_file = OUTPUT_DIR / 'cleaned_sales_data.csv'
    cleaned.to_csv(cleaned_file, index=False)

    report_file = OUTPUT_DIR / 'sales_report.xlsx'
    save_excel_report(cleaned, report_file)

    summary_file = OUTPUT_DIR / 'summary_report.txt'
    save_summary_text(cleaned, summary_file)

    print('Automation complete.')
    print(f'Cleaned data: {cleaned_file}')
    print(f'Excel report: {report_file}')
    print(f'Summary text: {summary_file}')


if __name__ == '__main__':
    main()
