import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Initialize Dash application
app = dash.Dash(__name__)
app.title = "Quantium Soul Foods - Sales Analytics Dashboard"

# Load data
def load_data():
    """Load and prepare sales data"""
    try:
        df = pd.read_csv('data/formatted_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        # Return empty DataFrame with expected structure if file not found
        return pd.DataFrame(columns=['sales', 'date', 'region'])

# Load the data
df = load_data()

# Define layout
app.layout = html.Div([
    # Header Section
    html.Div([
        html.H1("Soul Foods Sales Analytics", className="header-title"),
        html.P("Interactive dashboard for Pink Morsel sales analysis", className="header-subtitle")
    ], className="header-container"),
    
    # Main Content
    html.Div([
        # Control Panel Card
        html.Div([
            html.H3("Filter by Region", className="control-title"),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': 'All Regions', 'value': 'All'},
                    {'label': 'North', 'value': 'north'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'West', 'value': 'west'}
                ],
                value='All',
                className="radio-items",
                labelStyle={'display': 'block', 'margin-bottom': '10px'}
            )
        ], className="control-panel-card"),
        
        # Chart Card
        html.Div([
            html.H3("Sales Trends Over Time", className="chart-title"),
            dcc.Graph(
                id='sales-chart',
                config={'displayModeBar': True, 'displaylogo': False}
            )
        ], className="chart-card"),
        
        # Statistics Cards
        html.Div([
            html.Div(id="stats-cards")
        ], className="stats-container")
        
    ], className="main-container"),
    
    # Footer
    html.Div([
        html.P("© 2024 Quantium Analytics - Soul Foods Dashboard", className="footer-text")
    ], className="footer")
])

# Callback for updating chart based on region selection
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('stats-cards', 'children')],
    [Input('region-filter', 'value')]
)
def update_dashboard(selected_region):
    """Update chart and statistics based on selected region"""
    
    if df.empty:
        # Return empty chart if no data
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="No data available. Please ensure formatted_data.csv is in the data/ folder.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16)
        )
        empty_fig.update_layout(
            title="Sales Data Not Available",
            showlegend=False,
            plot_bgcolor='white'
        )
        
        stats_cards = html.Div([
            html.P("Data not available", className="stat-value"),
        ], className="stat-card")
        
        return empty_fig, [stats_cards]
    
    # Filter data based on selection
    if selected_region == 'All':
        filtered_df = df.copy()
        title_suffix = "All Regions"
    else:
        filtered_df = df[df['region'] == selected_region].copy()
        title_suffix = selected_region.capitalize()
    
    if filtered_df.empty:
        # Handle case where filtered data is empty
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text=f"No data available for {title_suffix}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16)
        )
        empty_fig.update_layout(title=f"Sales Trends - {title_suffix}")
        return empty_fig, []
    
    # Aggregate daily sales
    if selected_region == 'All':
        # Group by date and sum all regions
        daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
        
        # Also create regional breakdown for All view
        regional_sales = filtered_df.groupby(['date', 'region'])['sales'].sum().reset_index()
        
        # Create multi-line chart for all regions
        fig = px.line(
            regional_sales,
            x='date',
            y='sales',
            color='region',
            title=f"Sales Trends - {title_suffix}",
            labels={'sales': 'Sales ($)', 'date': 'Date', 'region': 'Region'},
            color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        )
    else:
        # Single region view
        daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
        
        fig = px.line(
            daily_sales,
            x='date',
            y='sales',
            title=f"Sales Trends - {title_suffix}",
            labels={'sales': 'Sales ($)', 'date': 'Date'},
            line_shape='linear'
        )
        
        # Customize single line color
        fig.update_traces(line_color='#2E86C1', line_width=3)
    
    # Update chart layout
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(size=18, family="Inter, sans-serif"),
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            title_font=dict(size=14)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            title_font=dict(size=14),
            tickformat='$,.0f'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=60, b=0),
        height=400
    )
    
    # Calculate statistics
    total_sales = filtered_df['sales'].sum()
    avg_daily_sales = filtered_df.groupby('date')['sales'].sum().mean()
    max_daily_sales = filtered_df.groupby('date')['sales'].sum().max()
    min_daily_sales = filtered_df.groupby('date')['sales'].sum().min()
    
    # Create statistics cards
    stats_cards = [
        html.Div([
            html.H4("Total Sales", className="stat-label"),
            html.P(f"${total_sales:,.0f}", className="stat-value"),
        ], className="stat-card"),
        
        html.Div([
            html.H4("Avg Daily Sales", className="stat-label"),
            html.P(f"${avg_daily_sales:,.0f}", className="stat-value"),
        ], className="stat-card"),
        
        html.Div([
            html.H4("Peak Daily Sales", className="stat-label"),
            html.P(f"${max_daily_sales:,.0f}", className="stat-value"),
        ], className="stat-card"),
        
        html.Div([
            html.H4("Lowest Daily Sales", className="stat-label"),
            html.P(f"${min_daily_sales:,.0f}", className="stat-value"),
        ], className="stat-card")
    ]
    
    return fig, stats_cards

# Run the application
if __name__ == '__main__':
    print("Starting Soul Foods Dashboard...")
    print("Dashboard accessible at: http://127.0.0.1:8050")
    print("To stop: Ctrl+C")
    app.run(debug=True, host='127.0.0.1', port=8050)