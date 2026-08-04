import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Layout basique pour tester
app.layout = html.Div([
    html.H1("Quantium Soul Foods - Dashboard Test", 
            style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Hr(),
    
    html.Div([
        html.H3("Configuration réussie !", style={'color': '#27ae60'}),
        html.P("Si vous voyez ce message, votre environnement Dash fonctionne correctement."),
        html.P("Prêt pour développer le dashboard Quantium !"),
    ], style={'margin': '20px', 'padding': '20px', 'border': '1px solid #bdc3c7', 'borderRadius': '5px'}),
    
    html.Div([
        html.H4("Test des données CSV"),
        html.P(id="data-status")
    ], style={'margin': '20px'}),
    
    dcc.Graph(id='test-graph')
])

# Callback simple pour tester les données
@app.callback(
    [dash.dependencies.Output('data-status', 'children'),
     dash.dependencies.Output('test-graph', 'figure')],
    [dash.dependencies.Input('test-graph', 'id')]  # Trigger automatique
)
def update_content(_):
    try:
        # Tenter de charger les données
        df = pd.read_csv('data/daily_sales_data_0.csv')
        status = f"✅ Données chargées avec succès ! {len(df)} lignes trouvées."
        
        # Créer un graphique simple si possible
        if not df.empty:
            # Supposer qu'il y a une colonne de date et une de ventes
            columns = df.columns.tolist()
            fig = px.line(df.head(10), 
                         title="Aperçu des données (10 premières lignes)",
                         labels={'index': 'Index', 'value': 'Valeur'})
        else:
            fig = px.scatter(title="Pas de données à afficher")
            
    except Exception as e:
        status = f"❌ Erreur lors du chargement des données: {str(e)}"
        fig = px.scatter(title="Erreur de chargement des données")
    
    return status, fig

# Lancer l'application
if __name__ == '__main__':
    print("🚀 Lancement du serveur Dash...")
    print("📊 Dashboard accessible sur: http://127.0.0.1:8050")
    print("⏹️  Pour arrêter: Ctrl+C")
    app.run_server(debug=True, host='127.0.0.1', port=8050)