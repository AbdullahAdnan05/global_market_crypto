from dash import Input, Output
from database.db_engine import get_engine
from sqlalchemy import text 
import pandas as pd

def register_market_callbacks(app):
    @app.callback(
    Output("market-coin-dropdown", "options"),
    Input("market-coin-dropdown", "value")  # dummy trigger
)
    def populate_market_dropdown(_):
        engine = get_engine()
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT DISTINCT coin_id FROM crypto_prices")).fetchall()
        return [{"label": r[0].capitalize(), "value": r[0]} for r in rows]
    
    @app.callback(
        Output("market-price-volume-graph", "figure"),
        Input("market-coin-dropdown", "value"),
        Input("market-range-dropdown", "value")
    )
    def update_price_volume_graph(coin_id, days):
        if not coin_id or not days:
            return {}

        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT timestamp, price, volume
                FROM crypto_prices
                WHERE coin_id = :coin_id
                  AND granularity = 'hourly'
                  AND timestamp >= NOW() - INTERVAL :days DAY
                ORDER BY timestamp
            """), conn, params={"coin_id": coin_id, "days": int(days)})

        if df.empty:
            return {}

        fig = {
            "data": [
                {
                    "x": df["timestamp"],
                    "y": df["price"],
                    "type": "line",
                    "name": "Price",
                    "yaxis": "y1"
                },
                {
                    "x": df["timestamp"],
                    "y": df["volume"],
                    "type": "bar",
                    "name": "Volume",
                    "yaxis": "y2",
                    "opacity": 0.4
                }
            ],
            "layout": {
                "title": f"{coin_id.capitalize()} — Price & Volume",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Price (USD)", "side": "left"},
                "yaxis2": {
                    "title": "Volume",
                    "overlaying": "y",
                    "side": "right"
                },
                "legend": {"x": 0, "y": 1.2}
            }
        }
        return fig
    
    @app.callback(
    Output("market-price", "children"),
    Output("market-change-24h", "children"),
    Output("market-cap", "children"),
    Input("market-coin-dropdown", "value")
    )
    def update_market_kpis(coin_id):
        if not coin_id:
            return "N/A", "N/A", "N/A"

        engine = get_engine()
        with engine.connect() as conn:
            latest_ts = conn.execute(text("""
                SELECT MAX(timestamp)
                FROM crypto_prices
                WHERE coin_id = :coin_id AND granularity = 'hourly'
            """), {"coin_id": coin_id}).scalar()

            if not latest_ts:
                return "N/A", "N/A", "N/A"

            row = conn.execute(text("""
                SELECT price, market_cap, percentage_change_24h
                FROM crypto_prices
                WHERE coin_id = :coin_id
                AND timestamp = :ts
                AND granularity = 'hourly'
            """), {"coin_id": coin_id, "ts": latest_ts}).fetchone()

        if not row:
            return "N/A", "N/A", "N/A"

        price, market_cap, change = row
        price_text = f"${price:,.2f}"
        cap_text = f"${market_cap:,.0f}"
        change_text = f"{change:.2f} %" if change is not None else "N/A"

        return price_text, change_text, cap_text
