
# ____This is one I made before designing____
from dashboard.components.cards import overview_kpi_cards, market_metrics, analytics_metric_cards
from dashboard.components.graphs import overview_graphs, market_charts, analytics_graphs
from dashboard.components.tables import overview_price_table
from dashboard.components.controls import market_controls, analytics_controls
from dash import dcc, html
import dash_bootstrap_components as dbc

def get_layout():
    return dbc.Container([
        html.H1("Global Market Pulse", className="header-title"),
        
        dcc.Tabs(
            className="tab-container",
            children=[
            dcc.Tab(label="Overview", className="tab-style", selected_className="tab-selected-style", children=[
                dbc.Card([
                    dbc.CardBody([
                        overview_kpi_cards(),
                        html.Hr(),
                        overview_graphs(),
                        html.Hr(),
                        overview_price_table(),
                        html.Div(style={"marginBottom": "40px"})
                    ])
                ], style={
                    "backgroundColor": "#1e1e2f",  
                    "borderTop": "none",          
                    "borderRadius": "0 0 12px 12px",
                    "marginTop": "-10px",
                    "border": "2px solid #0d6efd" 
                })
            ]),
            dcc.Tab(label="Market Data", className="tab-style", selected_className="tab-selected-style", children=[
                dbc.Card([
                    dbc.CardBody([
                        market_controls(),
                        html.Hr(),
                        market_charts(),
                        html.Hr(),
                        market_metrics(),
                        html.Div(style={"marginBottom": "40px"})
                    ])
                ])
            ]),
            dcc.Tab(label="Analytics", className="tab-style", selected_className="tab-selected-style", children=[
                dbc.Card([
                    dbc.CardBody([
                        analytics_controls(),
                        html.Hr(),
                        analytics_graphs(),
                        html.Hr(),
                        analytics_metric_cards(),
                        html.Div(style={"marginBottom": "40px"})
                    ])
                ])
            ])
    ]
)

    ], fluid=True)