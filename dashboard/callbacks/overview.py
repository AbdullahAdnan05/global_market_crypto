# #  This work only for mysql because query are written according to it
# from datetime import datetime, timedelta
# from sqlalchemy import text
# from dash import Input, Output
# import pandas as pd
# from database.db_engine import _choose_engine

# def register_overview_callbacks(app):
#     # Dropdown: Populate with coins
#     @app.callback(
#         Output("coin-dropdown", "options"),
#         Input("coin-dropdown", "value")  # dummy input to trigger on load
#     )
#     def populate_dropdown(_):
#         engine = _choose_engine()
#         with engine.connect() as conn:
#             rows = conn.execute(text("SELECT DISTINCT coin_id FROM crypto_prices")).fetchall()
#         return [{"label": r[0].capitalize(), "value": r[0]} for r in rows]

#     # Price Line Chart
#     @app.callback(
#         Output("price-history", "figure"),
#         Input("coin-dropdown", "value")
#     )
#     def update_price_chart(coin_id):
#         if not coin_id:
#             return {}

#         engine = _choose_engine()
#         with engine.connect() as conn:
#             df = pd.read_sql(text("""
#                 SELECT timestamp, price
#                 FROM crypto_prices
#                 WHERE coin_id = :coin_id AND granularity = 'hourly'
#                 ORDER BY timestamp
#             """),
#             con=conn,
#             params={"coin_id":coin_id}
#             )

#         return {
#             "data": [{
#                 "x": df["timestamp"],
#                 "y": df["price"],
#                 "type": "line",
#                 "name": coin_id
#             }],
#             "layout": {
#                 "title": f"{coin_id.capitalize()} Price History",
#                 "xaxis": {"title": "Time"},
#                 "yaxis": {"title": "Price (USD)"}
#             }
#         }
#     @app.callback(
#         Output("volatility-chart", "figure"),
#         Input("coin-dropdown", "value")
#     )
#     def update_volatility_chart(coin_id):
#         if not coin_id:
#             return {}
#         engine = _choose_engine()
#         with engine.connect() as conn:
#             df = pd.read_sql(text("""
#                 SELECT computed_at, volatility_24h
#                 FROM crypto_metrics
#                 WHERE coin_id = :coin_id
#                 ORDER BY computed_at
#             """), con=conn, params={"coin_id": coin_id})
        
#         if df.empty:
#             return {
#                 "data": [],
#                 "layout": {"title": "No volatility data available"}
#             }
        
#         return {
#             "data": [{
#                 "x": df["computed_at"],
#                 "y": df["volatility_24h"],
#                 "type": "line",
#                 "name": "Volatility (24h)"
#             }],
#             "layout": {
#                 "title": f"{coin_id.capitalize()} (24h) Volatility",
#                 "xaxis": {"title": "Time"},
#                 "yaxis": {"title": "Volatility"},
#             }
#         }
#     @app.callback(
#     Output("top-gainer", "children"),
#     Output("top-loser", "children"),
#     Output("total-market-cap", "children"),
#     Output("btc-dominance", "children"),
#     Input("coin-dropdown", "value")
# )
#     def update_kpis(_):
#         engine = _choose_engine()
#         now = datetime.utcnow()
#         since_24h = now - timedelta(hours=24)

#         with engine.connect() as conn:
#             # 🎯 Get metrics in last 24h
#             metrics_df = pd.read_sql(text("""
#                 SELECT coin_id, cv_24h_pct, volatility_24h, computed_at
#                 FROM crypto_metrics
#                 WHERE granularity = 'hourly'
#                 AND computed_at >= :since
#             """), conn, params={"since": since_24h})

#             if metrics_df.empty:
#                 return "No data", "No data", "No data", "No data"

#             top_gainer = metrics_df.sort_values("cv_24h_pct", ascending=False).iloc[0]
#             top_loser = metrics_df.sort_values("cv_24h_pct", ascending=True).iloc[0]

#             # 🎯 Get latest market cap
#             marketcap_df = pd.read_sql(text("""
#                 SELECT coin_id, market_cap
#                 FROM crypto_prices
#                 WHERE granularity = 'hourly' AND timestamp = (
#                     SELECT MAX(timestamp) FROM crypto_prices WHERE granularity = 'hourly'
#                 )
#             """), conn)
#             total_marketcap = marketcap_df["market_cap"].sum()

#             btc_row = marketcap_df[marketcap_df["coin_id"] == "bitcoin"]
#             btc_dominance = (btc_row["market_cap"].values[0] / total_marketcap) * 100 if not btc_row.empty else 0

#         return (
#             f"{top_gainer['coin_id'].capitalize()} ({top_gainer['cv_24h_pct']:.1f}%)",
#             f"{top_loser['coin_id'].capitalize()} ({top_loser['cv_24h_pct']:.1f}%)",
#             f"${total_marketcap:,.0f}",
#             f"{btc_dominance:.2f}%"
#         )
#     @app.callback(
#     Output("latest-price-table", "columns"),
#     Output("latest-price-table", "data"),
#     Input("coin-dropdown", "value")  # trigger update on page load or user interaction
# )
    
#     def update_price_table(_):
#         engine = _choose_engine()

#         with engine.connect() as conn:
#             # ✅ Get latest data per coin (even if timestamps are slightly different)
#             df = pd.read_sql(text("""
#                 SELECT t1.symbol, t1.price, t1.market_cap, t1.percentage_change_24h, t1.timestamp
#                 FROM crypto_prices t1
#                 JOIN (
#                     SELECT coin_id, MAX(timestamp) AS max_ts
#                     FROM crypto_prices
#                     WHERE granularity = 'hourly'
#                     GROUP BY coin_id
#                 ) t2 ON t1.coin_id = t2.coin_id AND t1.timestamp = t2.max_ts
#                 ORDER BY t1.market_cap DESC
#             """), conn)

#         # 🧼 Format columns
#         df["price"] = df["price"].round(2)
#         df["market_cap"] = df["market_cap"].apply(lambda x: f"${x:,.0f}")
#         df["percentage_change_24h"] = df["percentage_change_24h"].round(2).astype(str) + " %"
#         df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")

#         # 🧩 Prepare table structure
#         columns = [{"name": col.replace("_", " ").title(), "id": col} for col in df.columns]
#         data = df.to_dict("records")

#         return columns, data

# # ----------This will work for both postgres and mysql ------------
from datetime import datetime, timedelta
from sqlalchemy import text
from dash import Input, Output
import pandas as pd
from database.db_engine import _choose_engine
from config.settings import DEPLOYMENT


IS_CLOUD = DEPLOYMENT == "1"

def register_overview_callbacks(app):

    @app.callback(
        Output("coin-dropdown", "options"),
        Input("coin-dropdown", "value")
    )
    def populate_dropdown(_):
        engine = _choose_engine()
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT DISTINCT coin_id FROM crypto_prices")).fetchall()
        return [{"label": r[0].capitalize(), "value": r[0]} for r in rows]

    @app.callback(
        Output("price-history", "figure"),
        Input("coin-dropdown", "value")
    )
    def update_price_chart(coin_id):
        if not coin_id:
            return {}
        engine = _choose_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT timestamp, price
                FROM crypto_prices
                WHERE coin_id = :coin_id AND granularity = 'hourly'
                ORDER BY timestamp
            """), con=conn, params={"coin_id": coin_id})

        return {
            "data": [{
                "x": df["timestamp"],
                "y": df["price"],
                "type": "line",
                "name": coin_id
            }],
            "layout": {
                "title": f"{coin_id.capitalize()} Price History",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Price (USD)"}
            }
        }

    @app.callback(
        Output("volatility-chart", "figure"),
        Input("coin-dropdown", "value")
    )
    def update_volatility_chart(coin_id):
        if not coin_id:
            return {}
        engine = _choose_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT computed_at, volatility_24h
                FROM crypto_metrics
                WHERE coin_id = :coin_id
                ORDER BY computed_at
            """), con=conn, params={"coin_id": coin_id})

        if df.empty:
            return {
                "data": [],
                "layout": {"title": "No volatility data available"}
            }

        return {
            "data": [{
                "x": df["computed_at"],
                "y": df["volatility_24h"],
                "type": "line",
                "name": "Volatility (24h)"
            }],
            "layout": {
                "title": f"{coin_id.capitalize()} (24h) Volatility",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Volatility"}
            }
        }

    @app.callback(
    Output("top-gainer", "children"),
    Output("top-loser", "children"),
    Output("total-market-cap", "children"),
    Output("btc-dominance", "children"),
    Input("coin-dropdown", "value")
)

    def update_kpis(_):
        engine = _choose_engine()
        now = datetime.utcnow()
        since_24h = now - timedelta(hours=24)

        with engine.connect() as conn:
            # 📊 Get valid CV data for last 24h
            metrics_df = pd.read_sql(text("""
                SELECT coin_id, cv_24h_pct
                FROM crypto_metrics
                WHERE granularity = 'hourly' AND computed_at >= :since
            """), conn, params={"since": since_24h})

            # Drop missing values to avoid crash
            metrics_df = metrics_df.dropna(subset=["cv_24h_pct"])

            if metrics_df.empty:
                return "No data", "No data", "No data", "No data"

            top_gainer = metrics_df.sort_values("cv_24h_pct", ascending=False).iloc[0]
            top_loser = metrics_df.sort_values("cv_24h_pct", ascending=True).iloc[0]

            gainer_coin = top_gainer["coin_id"].capitalize()
            gainer_cv   = f"{top_gainer['cv_24h_pct']:.1f}%" if top_gainer["cv_24h_pct"] is not None else "N/A"

            loser_coin  = top_loser["coin_id"].capitalize()
            loser_cv    = f"{top_loser['cv_24h_pct']:.1f}%" if top_loser["cv_24h_pct"] is not None else "N/A"

            # ✅ Get latest market cap timestamp
            latest_ts = conn.execute(text("""
                SELECT MAX(timestamp)
                FROM crypto_prices
                WHERE granularity = 'hourly'
            """)).scalar()

            if not latest_ts:
                return f"{gainer_coin} ({gainer_cv})", f"{loser_coin} ({loser_cv})", "No data", "No data"

            # ✅ Get market cap rows for latest timestamp
            marketcap_df = pd.read_sql(text("""
                SELECT coin_id, market_cap
                FROM crypto_prices
                WHERE granularity = 'hourly' AND timestamp = :ts
            """), conn, params={"ts": latest_ts})

            total_marketcap = marketcap_df["market_cap"].sum()

            btc_row = marketcap_df[marketcap_df["coin_id"] == "bitcoin"]
            btc_dominance = (btc_row["market_cap"].values[0] / total_marketcap) * 100 if not btc_row.empty else 0

        return (
            f"{gainer_coin} ({gainer_cv})",
            f"{loser_coin} ({loser_cv})",
            f"${total_marketcap:,.0f}",
            f"{btc_dominance:.2f}%"
        )

    @app.callback(
        Output("latest-price-table", "columns"),
        Output("latest-price-table", "data"),
        Input("coin-dropdown", "value")
    )
    def update_price_table(_):
        engine = _choose_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT t1.symbol, t1.price, t1.market_cap, t1.percentage_change_24h, t1.timestamp
                FROM crypto_prices t1
                JOIN (
                    SELECT coin_id, MAX(timestamp) AS max_ts
                    FROM crypto_prices
                    WHERE granularity = 'hourly'
                    GROUP BY coin_id
                ) t2 ON t1.coin_id = t2.coin_id AND t1.timestamp = t2.max_ts
                ORDER BY t1.market_cap DESC
            """), conn)

        df["price"] = df["price"].round(2)
        df["market_cap"] = df["market_cap"].apply(lambda x: f"${x:,.0f}")
        df["percentage_change_24h"] = df["percentage_change_24h"].round(2).astype(str) + " %"
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")

        columns = [{"name": col.replace("_", " ").title(), "id": col} for col in df.columns]
        data = df.to_dict("records")

        return columns, data
