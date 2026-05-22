from pathlib import Path
import numpy as np
import pandas as pd

MONTH_ORDER = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def load_sales_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
    df['Discount_%'] = pd.to_numeric(df['Discount_%'], errors='coerce')
    df['Units_Sold'] = pd.to_numeric(df['Units_Sold'], errors='coerce')
    df = df.dropna(subset=['Date', 'Revenue', 'Cost', 'Profit'])
    df['Profit_Margin_%'] = np.where(df['Revenue'] != 0, df['Profit'] / df['Revenue'] * 100, 0)
    df['Month'] = df['Date'].dt.strftime('%b')
    df['Month_Num'] = df['Date'].dt.month
    df['Month_Order'] = pd.Categorical(df['Month'], categories=MONTH_ORDER, ordered=True)
    return df


def filter_sales_data(
    df: pd.DataFrame,
    date_range: tuple,
    categories: list,
    regions: list,
    salespeople: list,
    segments: list,
    payments: list,
    discount_range: tuple,
) -> pd.DataFrame:
    start_date, end_date = date_range
    filtered = df[
        (df['Date'] >= pd.to_datetime(start_date)) &
        (df['Date'] <= pd.to_datetime(end_date)) &
        (df['Category'].isin(categories)) &
        (df['Region'].isin(regions)) &
        (df['Salesperson'].isin(salespeople)) &
        (df['Customer_Segment'].isin(segments)) &
        (df['Payment_Method'].isin(payments)) &
        (df['Discount_%'] >= discount_range[0]) &
        (df['Discount_%'] <= discount_range[1])
    ]
    return filtered


def compute_kpis(df: pd.DataFrame) -> dict:
    revenue_total = df['Revenue'].sum()
    profit_total = df['Profit'].sum()
    cost_total = df['Cost'].sum()
    profit_margin = (profit_total / revenue_total * 100) if revenue_total else 0
    order_count = df['Order_ID'].nunique()
    avg_discount = df['Discount_%'].mean()
    top_region = df.groupby('Region')['Revenue'].sum().idxmax() if not df.empty else None
    top_salesperson = df.groupby('Salesperson')['Revenue'].sum().idxmax() if not df.empty else None
    return {
        'total_revenue': revenue_total,
        'total_profit': profit_total,
        'total_cost': cost_total,
        'profit_margin': profit_margin,
        'total_orders': order_count,
        'avg_discount': avg_discount,
        'top_region': top_region,
        'top_salesperson': top_salesperson,
    }


def compute_aggregates(df: pd.DataFrame) -> dict:
    monthly = (
        df.groupby(['Month_Order', 'Month'], sort=False)[['Revenue', 'Profit', 'Cost']]
        .sum()
        .reset_index()
        .sort_values('Month_Order')
    )
    monthly['Cumulative_Revenue'] = monthly['Revenue'].cumsum()
    return {
        'monthly': monthly,
        'category_revenue': df.groupby('Category', as_index=False)['Revenue'].sum(),
        'region_revenue': df.groupby('Region', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=True),
        'salesperson_revenue': df.groupby('Salesperson', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=True),
        'segment_revenue': df.groupby('Customer_Segment', as_index=False)['Revenue'].sum(),
        'product_revenue': df.groupby('Product_Name', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=False).head(10),
        'heatmap_matrix': df.pivot_table(index='Category', columns='Region', values='Units_Sold', aggfunc='sum').fillna(0),
        'category_margin': df.groupby('Category', as_index=False)['Profit_Margin_%'].mean().sort_values('Profit_Margin_%', ascending=False),
    }


def evaluate_insights(df: pd.DataFrame, aggregates: dict) -> dict:
    monthly = aggregates['monthly']
    best_month = monthly.loc[monthly['Revenue'].idxmax(), 'Month'] if not monthly.empty else None
    best_category = aggregates['category_margin'].loc[aggregates['category_margin']['Profit_Margin_%'].idxmax(), 'Category'] if not aggregates['category_margin'].empty else None
    lowest_region = aggregates['region_revenue'].loc[aggregates['region_revenue']['Revenue'].idxmin(), 'Region'] if not aggregates['region_revenue'].empty else None
    heavy_discount = df[df['Discount_%'] > 10]
    negative_discount_effect = False
    if not heavy_discount.empty:
        negative_discount_effect = heavy_discount['Profit'].mean() < df['Profit'].mean()
    return {
        'best_month': best_month,
        'best_category': best_category,
        'lowest_region': lowest_region,
        'negative_discount_effect': negative_discount_effect,
    }
