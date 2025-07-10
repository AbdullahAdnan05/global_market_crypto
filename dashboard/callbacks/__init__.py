from dashboard.callbacks.overview import register_overview_callbacks
from dashboard.callbacks.market import register_market_callbacks
from dashboard.callbacks.analytics import register_analytics_callbacks

def register_callbacks(app):
    register_overview_callbacks(app)
    register_market_callbacks(app)
    register_analytics_callbacks(app)
