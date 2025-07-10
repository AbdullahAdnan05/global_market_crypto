# # --------------This is pure logic without design ----------------

# from dash import dash_table, html

# def overview_price_table():
#     return html.Div([
#         html.H5("Latest Market Data", className="mt-4"),
#         dash_table.DataTable(
#             id="latest-price-table",
#             columns=[],  # filled dynamically
#             data=[], # filled dynamically
#             style_table={'overflowX': 'auto'},
#             style_cell={'textAlign': 'left'},
#         )
#     ], className="mb-5")

from dash import dash_table, html

def overview_price_table():
    return html.Div([
        html.H5("Latest Market Data", className="mt-4 text-secondary fw-bold"),
        dash_table.DataTable(
            id="latest-price-table",
            columns=[],  # filled dynamically
            data=[],     # filled dynamically
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '8px'},
            style_header={
                'backgroundColor': '#e9ecef',
                'fontWeight': 'bold',
                'border': '1px solid #dee2e6'
            },
            style_data={
                'border': '1px solid #dee2e6'
            }
        ),
        html.Div(className="mb-5")  # spacing after table
    ])
