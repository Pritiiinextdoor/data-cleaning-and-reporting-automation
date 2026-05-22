import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def monthly_revenue_profit_trend(monthly: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Revenue'], mode='lines+markers', name='Revenue', line=dict(color='#1f77b4', width=3), hovertemplate='Month: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Profit'], mode='lines+markers', name='Profit', line=dict(color='#2ca02c', width=3), hovertemplate='Month: %{x}<br>Profit: ₹%{y:,.0f}<extra></extra>'))
    fig.update_layout(title='Monthly Revenue & Profit Trend', xaxis_title='Month', yaxis_title='Amount (₹)', template='plotly_white', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return fig


def cumulative_revenue_degree(monthly: pd.DataFrame) -> go.Figure:
    fig = px.line(monthly, x='Month', y='Cumulative_Revenue', markers=True, title='Cumulative Revenue Growth (YTD)', labels={'Cumulative_Revenue': 'Cumulative Revenue (₹)'} )
    fig.update_traces(line=dict(color='#1f77b4', width=3), hovertemplate='Month: %{x}<br>YTD Revenue: ₹%{y:,.0f}<extra></extra>')
    fig.update_layout(template='plotly_white', xaxis_title='Month', yaxis_title='Cumulative Revenue (₹)')
    return fig


def revenue_forecast_trend(forecast_df: pd.DataFrame) -> go.Figure:
    actual = forecast_df[forecast_df['Type'] == 'Actual']
    forecast = forecast_df[forecast_df['Type'] == 'Forecast']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=actual['Month_Label'],
        y=actual['Actual_Revenue'],
        mode='lines+markers',
        name='Actual Revenue',
        line=dict(color='#1f77b4', width=3),
        hovertemplate='Month: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>',
    ))
    fig.add_trace(go.Scatter(
        x=forecast['Month_Label'],
        y=forecast['Forecast'],
        mode='lines+markers',
        name='Forecast Revenue',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        marker=dict(symbol='diamond', size=10),
        hovertemplate='Month: %{x}<br>Forecast: ₹%{y:,.0f}<extra></extra>',
    ))
    fig.update_layout(
        title='Actual Revenue and 6-Month Forecast',
        xaxis_title='Month',
        yaxis_title='Revenue (₹)',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    )
    return fig


def revenue_by_category(category_revenue: pd.DataFrame) -> go.Figure:
    fig = px.pie(category_revenue, values='Revenue', names='Category', hole=0.45, title='Revenue by Category', color_discrete_sequence=['#1f77b4', '#f7c94d', '#2ca02c'])
    fig.update_traces(textinfo='percent+label', hovertemplate='%{label}: ₹%{value:,.0f}<extra></extra>')
    fig.update_layout(showlegend=True, legend_title_text='Category', template='plotly_white')
    return fig


def region_sales_performance(region_revenue: pd.DataFrame) -> go.Figure:
    fig = px.bar(region_revenue, x='Revenue', y='Region', orientation='h', title='Region-wise Sales Performance', labels={'Revenue': 'Revenue (₹)', 'Region': 'Region'}, color='Revenue', color_continuous_scale='Blues')
    fig.update_traces(hovertemplate='Region: %{y}<br>Revenue: ₹%{x:,.0f}<extra></extra>')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False)
    return fig


def segment_revenue_split(segment_revenue: pd.DataFrame) -> go.Figure:
    fig = px.pie(segment_revenue, values='Revenue', names='Customer_Segment', hole=0.45, title='B2B vs B2C Revenue Split', color_discrete_sequence=['#1f77b4', '#2ca02c'])
    fig.update_traces(textinfo='percent+label', hovertemplate='%{label}: ₹%{value:,.0f} <extra></extra>')
    fig.update_layout(showlegend=True, legend_title_text='Segment', template='plotly_white')
    return fig


def revenue_cost_profit_monthly(monthly: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Revenue', x=monthly['Month'], y=monthly['Revenue'], marker_color='#1f77b4', hovertemplate='Month: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Bar(name='Cost', x=monthly['Month'], y=monthly['Cost'], marker_color='#d62728', hovertemplate='Month: %{x}<br>Cost: ₹%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Bar(name='Profit', x=monthly['Month'], y=monthly['Profit'], marker_color='#2ca02c', hovertemplate='Month: %{x}<br>Profit: ₹%{y:,.0f}<extra></extra>'))
    fig.update_layout(barmode='group', title='Revenue vs Cost vs Profit by Month', xaxis_title='Month', yaxis_title='Amount (₹)', template='plotly_white')
    return fig


def discount_profit_scatter(filtered: pd.DataFrame) -> go.Figure:
    fig = px.scatter(filtered, x='Discount_%', y='Profit', color='Category', size='Revenue', title='Discount Impact on Profit', labels={'Discount_%': 'Discount %', 'Profit': 'Profit (₹)'}, color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(hovertemplate='Discount: %{x}%<br>Profit: ₹%{y:,.0f}<br>Revenue: ₹%{marker.size:,.0f}<extra></extra>')
    fig.update_layout(template='plotly_white', xaxis=dict(ticksuffix='%'), yaxis_title='Profit (₹)')
    return fig


def payment_method_distribution(filtered: pd.DataFrame) -> go.Figure:
    payment_counts = filtered['Payment_Method'].value_counts().reset_index()
    payment_counts.columns = ['Payment_Method', 'Count']
    fig = px.bar(payment_counts, x='Count', y='Payment_Method', orientation='h', title='Payment Method Distribution', labels={'Payment_Method': 'Payment Method', 'Count': 'Number of Orders'}, color='Count', color_continuous_scale='Blues')
    fig.update_traces(hovertemplate='Method: %{y}<br>Orders: %{x}<extra></extra>')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False)
    return fig


def top_products_by_revenue(product_revenue: pd.DataFrame) -> go.Figure:
    fig = px.bar(product_revenue.sort_values('Revenue', ascending=True), x='Revenue', y='Product_Name', orientation='h', title='Top 10 Products by Revenue', labels={'Revenue': 'Revenue (₹)', 'Product_Name': 'Product'}, color='Revenue', color_continuous_scale='Blues')
    fig.update_traces(hovertemplate='Product: %{y}<br>Revenue: ₹%{x:,.0f}<extra></extra>')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False)
    return fig


def units_heatmap(heatmap_matrix: pd.DataFrame) -> go.Figure:
    fig = go.Figure(data=go.Heatmap(z=heatmap_matrix.values, x=heatmap_matrix.columns, y=heatmap_matrix.index, colorscale='Blues', hovertemplate='Category: %{y}<br>Region: %{x}<br>Units Sold: %{z}<extra></extra>'))
    fig.update_layout(title='Units Sold by Category & Region', xaxis_title='Region', yaxis_title='Category', template='plotly_white')
    return fig


def profit_margin_by_category(category_margin: pd.DataFrame) -> go.Figure:
    fig = px.bar(category_margin, x='Category', y='Profit_Margin_%', title='Profit Margin % by Category', labels={'Profit_Margin_%': 'Profit Margin %'}, color='Profit_Margin_%', color_continuous_scale=['#d62728', '#f7c94d', '#2ca02c'])
    fig.update_traces(hovertemplate='Category: %{x}<br>Margin: %{y:.2f}%<extra></extra>')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False, yaxis=dict(ticksuffix='%'))
    return fig
