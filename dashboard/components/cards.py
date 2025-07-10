# # ------------------------This is logic without designing it-------------------------
# from dash import html
# import dash_bootstrap_components as dbc

# def overview_kpi_cards():
#     return dbc.Row([
#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Total Market Cap"),
#             dbc.CardBody(html.H4("Loading...", id="total-market-cap", className="card-title text-primary"))
#         ]), md=3),
        
#         dbc.Col(dbc.Card([
#             dbc.CardHeader("BTC Dominance"),
#             dbc.CardBody(html.H4("loading...", id="btc-dominance", className="card-title text-warning"))
#         ]),md=3),
        
#             dbc.Col(dbc.Card([
#             dbc.CardHeader("Top Gainer (24h)"),
#             dbc.CardBody(html.H4("loading...", id="top-gainer", className="card-title  text-success"))
#         ]),md=3),
        
#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Top Loser (24h)"),
#             dbc.CardBody(html.H4("loading..", id="top-loser", className="card-title text-danger"))
#         ]),md=3),
#     ], className="mb-4")
    
# def market_metrics():
#     return dbc.Row([
#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Current Price"),
#             dbc.CardBody(html.H4("Loading...", id="market-price"))
#         ]), md=4),

#         dbc.Col(dbc.Card([
#             dbc.CardHeader("24h Change"),
#             dbc.CardBody(html.H4("Loading...", id="market-change-24h"))
#         ]), md=4),

#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Current Market Cap"),
#             dbc.CardBody(html.H4("Loading...", id="market-cap"))
#         ]), md=4),
#     ])
    

# def analytics_metric_cards():
#     return dbc.Row([
#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Current Volatility"),
#             dbc.CardBody(html.H4("Loading...", id="analytics-volatility"))
#         ]), md=4),

#         dbc.Col(dbc.Card([
#             dbc.CardHeader("CV (%)"),
#             dbc.CardBody(html.H4("Loading...", id="analytics-cv"))
#         ]), md=4),

#         dbc.Col(dbc.Card([
#             dbc.CardHeader("7-Day Avg Price"),
#             dbc.CardBody(html.H4("Loading...", id="analytics-avg-price"))
#         ]), md=4),
#     ])

# ----------------------- basic logic end here ----------------------------
from dash import html
import dash_bootstrap_components as dbc

# ============================
# 1. Overview Tab KPI Cards
# ============================
def overview_kpi_cards():
    return dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Market Cap", className="text-white bg-primary"),
            dbc.CardBody(html.H4("Loading...", id="total-market-cap", className="card-title text-primary")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=3, className="mb-3"),

        dbc.Col(dbc.Card([
            dbc.CardHeader("BTC Dominance", className="text-white bg-secondary"),
            dbc.CardBody(html.H4("Loading...", id="btc-dominance", className="card-title text-secondary")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=3, className="mb-3"),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Top Gainer (24h)", className="text-white bg-success"),
            dbc.CardBody(html.H4("Loading...", id="top-gainer", className="card-title text-success")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=3, className="mb-3"),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Top Loser (24h)", className="text-white bg-danger"),
            dbc.CardBody(html.H4("Loading...", id="top-loser", className="card-title text-danger")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=3, className="mb-3"),
    ], className="mb-4")

# ============================
# 2. Market Tab KPI Cards
# ============================
def market_metrics():
    return dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Current Price", className="text-white bg-info"),
            dbc.CardBody(html.H4("Loading...", id="market-price", className="card-title text-info")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=4 , className="mb-3"),

        dbc.Col(dbc.Card([
            dbc.CardHeader("24h Change", className="text-white bg-warning"),
            dbc.CardBody(html.H4("Loading...", id="market-change-24h", className="card-title text-warning")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=4, className="mb-3"),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Current Market Cap", className="text-white bg-primary"),
            dbc.CardBody(html.H4("Loading...", id="market-cap", className="card-title text-primary")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=4, className="mb-3"),
    ])

# ============================
# 3. Analytics Tab KPI Cards
# ============================
def analytics_metric_cards():
    return dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Current Volatility", className="text-white bg-secondary"),
            dbc.CardBody(html.H4("Loading...", id="analytics-volatility", className="card-title text-secondary")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=4, className="mb-3"),

        dbc.Col(dbc.Card([
            dbc.CardHeader("CV (%)", className="text-white bg-danger"),
            dbc.CardBody(html.H4("Loading...", id="analytics-cv", className="card-title text-danger")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=4, className="mb-3"),

        dbc.Col(dbc.Card([
            dbc.CardHeader("7-Day Avg Price", className="text-white bg-success"),
            dbc.CardBody(html.H4("Loading...", id="analytics-avg-price", className="card-title text-success")),
        ], color="light", className="shadow-sm p-3"), xs=12, sm=6, md=4, className="mb-3"),
    ])
