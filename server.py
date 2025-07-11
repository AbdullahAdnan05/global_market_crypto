import dash
from dashboard.layout import get_layout
from dashboard.callbacks import register_callbacks
from dash_bootstrap_components.themes import CYBORG

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[CYBORG]
                )

register_callbacks(app)
app.title = "Global Market Pulse"
app.layout = get_layout()

# if __name__== "__main__":
#     app.run(debug=True)
    
if __name__ == "__main__":
    from os import getenv
    port = int(getenv("PORT", 8050))
    app.run_server(debug=False, host="0.0.0.0", port=port)
