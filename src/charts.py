import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def monthly_revenue_trend(monthly: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly['Month_Label'], y=monthly['Revenue'], name='Revenue', marker_color='#1f77b4', hovertemplate='Month: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=monthly['Month_Label'], y=monthly['Units_Sold'], mode='lines+markers', name='Units Sold', line=dict(color='#2ca02c', width=3), hovertemplate='Month: %{x}<br>Units Sold: %{y}<extra></extra>'))
    fig.update_layout(title='Monthly Revenue and Units Sold Trend', xaxis_title='Month', yaxis_title='Amount / Units', template='plotly_white', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return fig


def cumulative_revenue_trend(monthly: pd.DataFrame) -> go.Figure:
    fig = px.line(monthly, x='Month_Label', y='Cumulative_Revenue', markers=True, title='Cumulative Revenue Growth', labels={'Cumulative_Revenue': 'Cumulative Revenue (₹)', 'Month_Label': 'Month'})
    fig.update_traces(line=dict(color='#1f77b4', width=3), hovertemplate='Month: %{x}<br>YTD Revenue: ₹%{y:,.0f}<extra></extra>')
    fig.update_layout(template='plotly_white', xaxis_title='Month', yaxis_title='Cumulative Revenue (₹)')
    return fig


def revenue_forecast_trend(forecast_df: pd.DataFrame) -> go.Figure:
    actual = forecast_df[forecast_df['Type'] == 'Actual']
    forecast = forecast_df[forecast_df['Type'] == 'Forecast']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=actual['Month_Label'], y=actual['Actual_Revenue'], mode='lines+markers', name='Actual Revenue', line=dict(color='#1f77b4', width=3), hovertemplate='Month: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=forecast['Month_Label'], y=forecast['Forecast'], mode='lines+markers', name='Forecast Revenue', line=dict(color='#ff7f0e', width=3, dash='dash'), marker=dict(symbol='diamond', size=10), hovertemplate='Month: %{x}<br>Forecast: ₹%{y:,.0f}<extra></extra>'))
    fig.update_layout(title='Actual Revenue vs 6-Month Forecast', xaxis_title='Month', yaxis_title='Revenue (₹)', template='plotly_white', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return fig


def revenue_by_category(category_revenue: pd.DataFrame) -> go.Figure:
    fig = px.pie(category_revenue, values='Revenue', names='Product_Category', hole=0.45, title='Revenue by Product Category', color_discrete_sequence=['#1f77b4', '#f7c94d', '#2ca02c', '#d62728'])
    fig.update_traces(textinfo='percent+label', hovertemplate='%{label}: ₹%{value:,.0f}<extra></extra>')
    fig.update_layout(showlegend=True, legend_title_text='Category', template='plotly_white')
    return fig


def region_sales_performance(region_revenue: pd.DataFrame) -> go.Figure:
    fig = px.bar(region_revenue, x='Revenue', y='Region', orientation='h', title='Region-wise Revenue', labels={'Revenue': 'Revenue (₹)', 'Region': 'Region'}, color='Revenue', color_continuous_scale='Blues')
    fig.update_traces(hovertemplate='Region: %{y}<br>Revenue: ₹%{x:,.0f}<extra></extra>')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False)
    return fig


def payment_method_distribution(payment_revenue: pd.DataFrame) -> go.Figure:
    fig = px.bar(payment_revenue.sort_values('Revenue', ascending=True), x='Revenue', y='Payment_Method', orientation='h', title='Revenue by Payment Method', labels={'Revenue': 'Revenue (₹)', 'Payment_Method': 'Payment Method'}, color='Revenue', color_continuous_scale='Blues')
    fig.update_traces(hovertemplate='Payment: %{y}<br>Revenue: ₹%{x:,.0f}<extra></extra>')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False)
    return fig


def status_breakdown_chart(status_breakdown: pd.DataFrame) -> go.Figure:
    fig = px.bar(status_breakdown.sort_values('Count', ascending=True), x='Count', y='Status', orientation='h', title='Order Status Breakdown', labels={'Count': 'Order Count', 'Status': 'Order Status'}, color='Count', color_continuous_scale='Blues')
    fig.update_traces(hovertemplate='Status: %{y}<br>Orders: %{x}<extra></extra>')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False)
    return fig


def top_products_by_revenue(product_revenue: pd.DataFrame) -> go.Figure:
    fig = px.bar(product_revenue.sort_values('Revenue', ascending=True), x='Revenue', y='Product_Name', orientation='h', title='Top Products by Revenue', labels={'Revenue': 'Revenue (₹)', 'Product_Name': 'Product'}, color='Revenue', color_continuous_scale='Blues')
    fig.update_traces(hovertemplate='Product: %{y}<br>Revenue: ₹%{x:,.0f}<extra></extra>')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False)
    return fig


def units_heatmap(heatmap_matrix: pd.DataFrame) -> go.Figure:
    fig = go.Figure(data=go.Heatmap(z=heatmap_matrix.values, x=heatmap_matrix.columns, y=heatmap_matrix.index, colorscale='Blues', hovertemplate='Category: %{y}<br>Region: %{x}<br>Units Sold: %{z}<extra></extra>'))
    fig.update_layout(title='Units Sold by Category & Region', xaxis_title='Region', yaxis_title='Product Category', template='plotly_white')
    return fig
