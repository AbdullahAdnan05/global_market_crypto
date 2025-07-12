# # ----------THis is without designing pure logic --------------------

# from dash import dcc, html

# def overview_graphs():
#     return html.Div([
#         dcc.Dropdown(id="coin-dropdown", placeholder="Select a coin ...."),
#         html.Hr(),
#         html.H5("Price History", className="mt-3 section-title"),
#         dcc.Graph(id="price-history"),
#         html.Hr(),
#         html.H5("Rolling Volaility"),
#         dcc.Graph(id="volatility-chart")
#     ])
    
# def market_charts():
#     return html.Div([
#         html.H5("Price and Volume Chart", className="mt-2"),
#         dcc.Graph(id="market-price-volume-graph")
#     ])
    
# def analytics_graphs():
#     return html.Div([
#         html.H5("Volatility History"),
#         dcc.Graph(id="analytics-volatility-graph"),

#         html.H5("Rolling Mean (7D)"),
#         dcc.Graph(id="analytics-mean-graph"),

#         html.H5("Coefficient of Variation (%)"),
#         dcc.Graph(id="analytics-cv-graph"),
#     ])

from dash import dcc, html

# ======================
#     Overview Tab
# ======================
def overview_graphs():
    return html.Div([
        html.H5("Select a coin", className="mt-3 text-primary fw-bold"),
        dcc.Dropdown(id="coin-dropdown", placeholder="Select a coin ....", className="mb-3"),
        html.H5("Price History", className="mt-3 text-primary fw-bold"),
        dcc.Graph(id="price-history", className="mb-4"),

        html.H5("Rolling Volatility", className="text-info fw-bold"),
        dcc.Graph(id="volatility-chart")
    ])


# ======================
#     Market Tab
# ======================
def market_charts():
    return html.Div([
        html.H5("Price and Volume Chart", className="mt-2 text-primary fw-bold"),
        dcc.Graph(id="market-price-volume-graph")
    ])


# ======================
#     Analytics Tab
# ======================
def analytics_graphs():
    return html.Div([
        html.H5("Volatility History", className="text-warning fw-bold"),
        dcc.Graph(id="analytics-volatility-graph", className="mb-4"),

        html.H5("Rolling Mean (7D)", className="text-success fw-bold"),
        dcc.Graph(id="analytics-mean-graph", className="mb-4"),

        html.H5("Coefficient of Variation (%)", className="text-info fw-bold"),
        dcc.Graph(id="analytics-cv-graph")
    ])
