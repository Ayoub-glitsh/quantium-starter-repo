import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Initialize Dash application
app = dash.Dash(__name__)

# Basic layout for testing
app.layout = html.Div([
    html.H1("Quantium Soul Foods - Dashboard Test", 
            style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Hr(),
    
    html.Div([
        html.H3("Setup Successful!", style={'color': '#27ae60'}),
        html.P("If you see this message, your Dash environment is working correctly."),
        html.P("Ready to develop the Quantium dashboard!"),
    ], style={'margin': '20px', 'padding': '20px', 'border': '1px solid #bdc3c7', 'borderRadius': '5px'}),
    
    html.Div([
        html.H4("CSV Data Test"),
        html.P(id="data-status")
    ], style={'margin': '20px'}),
    
    dcc.Graph(id='test-graph')
])

# Simple callback to test data
@app.callback(
    [dash.dependencies.Output('data-status', 'children'),
     dash.dependencies.Output('test-graph', 'figure')],
    [dash.dependencies.Input('test-graph', 'id')]  # Automatic trigger
)
def update_content(_):
    try:
        # Try to load data
        df = pd.read_csv('data/daily_sales_data_0.csv')
        status = f"Data loaded successfully! {len(df)} rows found."
        
        # Create simple graph if possible
        if not df.empty:
            # Assume there's a date column and a sales column
            columns = df.columns.tolist()
            fig = px.line(df.head(10), 
                         title="Data Preview (first 10 rows)",
                         labels={'index': 'Index', 'value': 'Value'})
        else:
            fig = px.scatter(title="No data to display")
            
    except Exception as e:
        status = f"Error loading data: {str(e)}"
        fig = px.scatter(title="Data loading error")
    
    return status, fig

# Launch application
if __name__ == '__main__':
    print("Starting Dash server...")
    print("Dashboard accessible at: http://127.0.0.1:8050")
    print("To stop: Ctrl+C")
    app.run_server(debug=True, host='127.0.0.1', port=8050)