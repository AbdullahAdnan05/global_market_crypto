# # -----------------This is pure logic without designs

# from dash import dcc, html

# def market_controls():
#     return html.Div([
#         html.H5("Select Coin", className="mt-3"),
#         dcc.Dropdown(
#             id = "market-coin-dropdown",
#             placeholder= "Select coin ..",
#             className="mb-3"
#         ),
#         html.H5("Select Date range", className="mt-3"),
#         dcc.Dropdown(
#             id="market-range-dropdown",
#             options=[
#                 {"label": "7 Days", "value": "7"},
#                 {"label": "30 Days", "value": "30"},
#                 {"label": "90 Days", "value": "90"},
#             ],
#             placeholder="Select time range...",
#             className="mb-3"
#         )
#     ])
    
# def analytics_controls():
#     return html.Div([
#         html.H5("Select Coin", className="mt-3"),
#         dcc.Dropdown(id="analytics-coin-dropdown", placeholder="Choose a coin...")
#     ])

from dash import dcc, html

def market_controls():
    return html.Div([
        html.H5("Select Coin", className="mt-4 text-primary fw-bold"),
        dcc.Dropdown(
            id="market-coin-dropdown",
            placeholder="Select coin ...",
            className="mb-3"
        ),

        html.H5("Select Date Range", className="mt-4 text-primary fw-bold"),
        dcc.Dropdown(
            id="market-range-dropdown",
            options=[
                {"label": "7 Days", "value": "7"},
                {"label": "30 Days", "value": "30"},
                {"label": "90 Days", "value": "90"},
            ],
            placeholder="Select time range...",
            className="mb-3"
        )
    ])


def analytics_controls():
    return html.Div([
        html.H5("Select Coin", className="mt-4 text-primary fw-bold"),
        dcc.Dropdown(
            id="analytics-coin-dropdown",
            placeholder="Choose a coin...",
            className="mb-3"
        )
    ])
