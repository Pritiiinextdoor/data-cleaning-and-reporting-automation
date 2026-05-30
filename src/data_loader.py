from pathlib import Path
import numpy as np
import pandas as pd

MONTH_ORDER = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def _normalize_text(series: pd.Series) -> pd.Series:
    normalized = series.astype(str).str.strip()
    normalized = normalized.replace({'nan': pd.NA, 'NaN': pd.NA, '': pd.NA})
    return normalized.where(normalized.notna(), pd.NA)


def _title_text(series: pd.Series) -> pd.Series:
    return _normalize_text(series).str.title().fillna('Unknown')


def load_sales_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    if 'Order_ID' in df.columns:
        df['Order_ID'] = df['Order_ID'].astype(str).str.strip()

    if 'Order_Date' in df.columns:
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%Y-%m-%d', errors='coerce')

    numeric_columns = ['Quantity', 'Unit_Price', 'Total_Price', 'Age', 'Rating']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.drop_duplicates(subset=['Order_ID']) if 'Order_ID' in df.columns else df.drop_duplicates()
    df = df.dropna(subset=['Order_ID', 'Order_Date', 'Total_Price'])

    if 'Age' in df.columns:
        age_fill = df['Age'].median(skipna=True)
        age_fill = 0 if np.isnan(age_fill) else age_fill
        df['Age'] = df['Age'].fillna(age_fill).astype(int)

    if 'Rating' in df.columns:
        rating_fill = df['Rating'].median(skipna=True)
        rating_fill = 0.0 if np.isnan(rating_fill) else rating_fill
        df['Rating'] = df['Rating'].fillna(rating_fill)

    df['Customer_Name'] = _title_text(df['Customer_Name']) if 'Customer_Name' in df.columns else pd.Series('Unknown')
    df['Region'] = _title_text(df['Region']) if 'Region' in df.columns else pd.Series('Unknown')
    df['Product_Category'] = _title_text(df['Product_Category']) if 'Product_Category' in df.columns else pd.Series('Unknown')
    df['Product_Name'] = _title_text(df['Product_Name']) if 'Product_Name' in df.columns else pd.Series('Unknown')
    df['Payment_Method'] = _title_text(df['Payment_Method']) if 'Payment_Method' in df.columns else pd.Series('Unknown')
    df['Status'] = _title_text(df['Status']) if 'Status' in df.columns else pd.Series('Unknown')

    if 'Email' in df.columns:
        df['Email'] = _normalize_text(df['Email']).str.lower().fillna('unknown@example.com')

    if 'Phone' in df.columns:
        df['Phone'] = _normalize_text(df['Phone']).fillna('Unknown')

    df['Quantity'] = df['Quantity'].fillna(0).astype(int) if 'Quantity' in df.columns else 0
    df['Revenue'] = df['Total_Price']
    df['Average_Order_Value'] = np.where(df['Quantity'] > 0, df['Revenue'] / df['Quantity'], df['Revenue'])
    df['Date'] = df['Order_Date']
    df['Month'] = df['Date'].dt.strftime('%b')
    df['Month_Num'] = df['Date'].dt.month
    df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')
    df['Month_Label'] = df['Date'].dt.strftime('%b %Y')
    df['Month_Order'] = pd.Categorical(df['Month'], categories=MONTH_ORDER, ordered=True)

    df = df.sort_values('Date').reset_index(drop=True)
    return df


def filter_sales_data(
    df: pd.DataFrame,
    date_range: tuple,
    categories: list,
    regions: list,
    payments: list,
    statuses: list,
    rating_range: tuple,
) -> pd.DataFrame:
    start_date, end_date = date_range
    filtered = df[
        (df['Date'] >= pd.to_datetime(start_date)) &
        (df['Date'] <= pd.to_datetime(end_date)) &
        (df['Product_Category'].isin(categories)) &
        (df['Region'].isin(regions)) &
        (df['Payment_Method'].isin(payments)) &
        (df['Status'].isin(statuses)) &
        (df['Rating'] >= rating_range[0]) &
        (df['Rating'] <= rating_range[1])
    ]
    return filtered


def compute_kpis(df: pd.DataFrame) -> dict:
    revenue_total = df['Revenue'].sum()
    total_orders = df['Order_ID'].nunique()
    avg_order_value = df.groupby('Order_ID')['Revenue'].sum().mean() if not df.empty else 0
    top_category = df.groupby('Product_Category')['Revenue'].sum().idxmax() if not df.empty else None
    top_region = df.groupby('Region')['Revenue'].sum().idxmax() if not df.empty else None
    top_product = df.groupby('Product_Name')['Revenue'].sum().idxmax() if not df.empty else None
    top_payment = df.groupby('Payment_Method')['Revenue'].sum().idxmax() if not df.empty else None
    avg_rating = float(df['Rating'].mean()) if 'Rating' in df.columns and not df['Rating'].dropna().empty else 0
    returned_count = int(df[df['Status'] == 'Returned']['Order_ID'].nunique()) if 'Status' in df.columns else 0
    pending_count = int(df[df['Status'] == 'Pending']['Order_ID'].nunique()) if 'Status' in df.columns else 0
    return {
        'total_revenue': revenue_total,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'top_category': top_category,
        'top_region': top_region,
        'top_product': top_product,
        'top_payment': top_payment,
        'avg_rating': avg_rating,
        'returned_orders': returned_count,
        'pending_orders': pending_count,
    }


def compute_aggregates(df: pd.DataFrame) -> dict:
    monthly = (
        df.groupby(['Year_Month', 'Month_Order', 'Month', 'Month_Label'], sort=False)
        .agg(Revenue=('Revenue', 'sum'), Orders=('Order_ID', 'nunique'), Units_Sold=('Quantity', 'sum'))
        .reset_index()
        .sort_values(['Year_Month'])
    )
    monthly['Cumulative_Revenue'] = monthly['Revenue'].cumsum()

    return {
        'monthly': monthly,
        'category_revenue': df.groupby('Product_Category', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=False),
        'region_revenue': df.groupby('Region', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=True),
        'payment_revenue': df.groupby('Payment_Method', as_index=False)['Revenue'].sum(),
        'status_breakdown': df['Status'].value_counts().reset_index(name='Count').rename(columns={'index': 'Status'}),
        'product_revenue': df.groupby('Product_Name', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=False).head(10),
        'heatmap_matrix': df.pivot_table(index='Product_Category', columns='Region', values='Quantity', aggfunc='sum').fillna(0),
        'category_rating': df.groupby('Product_Category', as_index=False)['Rating'].mean().sort_values('Rating', ascending=False),
    }


def evaluate_insights(df: pd.DataFrame, aggregates: dict) -> dict:
    monthly = aggregates['monthly']
    best_month = monthly.loc[monthly['Revenue'].idxmax(), 'Month_Label'] if not monthly.empty else None
    best_category = aggregates['category_rating'].loc[aggregates['category_rating']['Rating'].idxmax(), 'Product_Category'] if not aggregates['category_rating'].empty else None
    lowest_region = aggregates['region_revenue'].loc[aggregates['region_revenue']['Revenue'].idxmin(), 'Region'] if not aggregates['region_revenue'].empty else None
    top_payment = aggregates['payment_revenue'].loc[aggregates['payment_revenue']['Revenue'].idxmax(), 'Payment_Method'] if not aggregates['payment_revenue'].empty else None
    return {
        'best_month': best_month,
        'best_category': best_category,
        'lowest_region': lowest_region,
        'top_payment': top_payment,
    }
