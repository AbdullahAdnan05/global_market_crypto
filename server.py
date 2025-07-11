import dash
from dash import Dash
from dashboard.layout import get_layout
from dashboard.callbacks import register_callbacks
from dash_bootstrap_components.themes import CYBORG

app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=[CYBORG]
)

register_callbacks(app)
app.title = "Global Market Pulse"
app.layout = get_layout()

# Required by Gunicorn
server = app.server
