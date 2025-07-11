# ---------------It work for bot not need to change 
from dash import Output, Input
from sqlalchemy import text
from database.db_engine import _choose_engine
import pandas as pd

def register_analytics_callbacks(app):
    """
    Registers the analytics callbacks for:
    - Populating coin dropdown
    - Rendering three line graphs: Volatility, Rolling Mean, CV
    """

    @app.callback(
        Output("analytics-coin-dropdown", "options"),
        Input("analytics-coin-dropdown", "value")  # Dummy trigger for page load
    )
    def populate_analytics_dropdown(_):
        """
        Dynamically fills the analytics dropdown with unique coin IDs.
        """
        engine = _choose_engine()
        with engine.connect() as conn:
            rows = conn.execute(
                text("SELECT DISTINCT coin_id FROM crypto_metrics")
            ).fetchall()
        
        return [{"label": r[0].capitalize(), "value": r[0]} for r in rows]

    @app.callback(
        Output("analytics-volatility-graph", "figure"),
        Output("analytics-mean-graph", "figure"),
        Output("analytics-cv-graph", "figure"),
        Input("analytics-coin-dropdown", "value")
    )
    def update_analytics_graphs(coin_id):
        """
        Generates three time-series graphs for the selected coin:
        - 24h Volatility
        - 7-day Rolling Mean
        - Coefficient of Variation (%)
        """
        if not coin_id:
            return {}, {}, {}

        engine = _choose_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT computed_at, volatility_24h, rolling_mean_7d, cv_24h_pct
                FROM crypto_metrics
                WHERE coin_id = :coin_id AND granularity = 'hourly'
                ORDER BY computed_at
            """), conn, params={"coin_id": coin_id})

        if df.empty:
            return {}, {}, {}

        df["computed_at"] = pd.to_datetime(df["computed_at"])

        # 🎯 Volatility graph
        fig_volatility = {
            "data": [{
                "x": df["computed_at"],
                "y": df["volatility_24h"],
                "type": "line",
                "name": "Volatility"
            }],
            "layout": {
                "title": "Volatility History (24h Std Dev)",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Volatility"}
            }
        }

        # 📊 Rolling Mean graph
        fig_mean = {
            "data": [{
                "x": df["computed_at"],
                "y": df["rolling_mean_7d"],
                "type": "line",
                "name": "7-Day Rolling Mean"
            }],
            "layout": {
                "title": "Rolling Mean (7D)",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Avg Price (USD)"}
            }
        }

        # 📈 Coefficient of Variation graph
        fig_cv = {
            "data": [{
                "x": df["computed_at"],
                "y": df["cv_24h_pct"],
                "type": "line",
                "name": "Coefficient of Variation"
            }],
            "layout": {
                "title": "Coefficient of Variation (CV %)",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "CV (%)"}
            }
        }

        return fig_volatility, fig_mean, fig_cv
    
    @app.callback(
        Output("analytics-volatility", "children"),
        Output("analytics-cv", "children"),
        Output("analytics-avg-price", "children"),
        Input("analytics-coin-dropdown", "value")
    )
    def update_analytics_kpis(coin_id):
        if not coin_id:
            return "N/A", "N/A", "N/A"

        engine = _choose_engine()
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT volatility_24h, cv_24h_pct, rolling_mean_7d
                FROM crypto_metrics
                WHERE coin_id = :coin_id AND granularity = 'daily'
                ORDER BY computed_at DESC
                LIMIT 1
            """), {"coin_id": coin_id}).fetchone()

        if not row:
            return "N/A", "N/A", "N/A"

        volatility, cv, mean = row

        volatility_text = f"{volatility:.2f}" if volatility else "N/A"
        cv_text         = f"{cv:.2f}%" if cv else "N/A"
        mean_text       = f"${mean:,.2f}" if mean else "N/A"

        return volatility_text, cv_text, mean_text
