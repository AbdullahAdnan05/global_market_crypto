import pandas as pd
from sqlalchemy import text
from database.db_engine import get_engine
from datetime import datetime, timedelta

def compute_metrics_for_past(granularity="hourly", days=90):
    """
    Compute rolling metrics from past for a given granularity (hourly/daily).
    Uses real timestamp filtering logic instead of fixed row counts.
    """
    engine = get_engine()
    with engine.connect() as conn:
        coins = conn.execute(text("SELECT DISTINCT coin_id FROM crypto_prices WHERE granularity = :g"), {"g": granularity}).fetchall()

    all_metrics = []

    for coin_id_tuple in coins:
        coin_id = coin_id_tuple[0]
        print(f"🔄 {coin_id} ({granularity})")

        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT symbol, price, timestamp
                FROM crypto_prices
                WHERE coin_id = :coin_id AND granularity = :granularity
                ORDER BY timestamp
            """), conn, params={"coin_id": coin_id, "granularity": granularity})

        if df.empty:
            continue

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        start_time = df["timestamp"].min() + timedelta(days=7)
        end_time = df["timestamp"].max()

        # Move window every 6 hours (configurable)
        interval = timedelta(hours=6)

        current = start_time
        while current <= end_time:
            last_24h = df[(df["timestamp"] >= current - timedelta(hours=24)) & (df["timestamp"] <= current)]
            last_7d  = df[(df["timestamp"] >= current - timedelta(days=7)) & (df["timestamp"] <= current)]

            if len(last_24h) < 5 or len(last_7d) < 10:
                current += interval
                continue

            symbol = df["symbol"].iloc[0]
            mean_7d = last_7d["price"].mean()
            vol_24h = last_24h["price"].std()
            cv = (vol_24h / mean_7d) * 100 if mean_7d else 0

            all_metrics.append({
                "coin_id": coin_id,
                "symbol": symbol,
                "rolling_mean_7d": round(mean_7d, 4),
                "volatility_24h": round(vol_24h, 4),
                "cv_24h_pct": round(cv, 2),
                "computed_at": current,
                "granularity": granularity
            })

            current += interval

    return pd.DataFrame(all_metrics)


if __name__ == "__main__":
    print("⏳ Backfilling metrics...")

    dfs = []
    dfs.append(compute_metrics_for_past(granularity="hourly", days=90))
    dfs.append(compute_metrics_for_past(granularity="daily", days=180))

    full_df = pd.concat(dfs)
    print(f"📈 {len(full_df)} total rows generated.")

    # Insert into DB
    engine = get_engine()
    with engine.begin() as conn:
        full_df.to_sql("crypto_metrics", con=conn, if_exists="append", index=False)

    print("✅ Backfill completed.")

# scripts/backfill_metrics.py

# import pandas as pd
# from sqlalchemy import text
# from database.db_engine import get_engine
# from datetime import datetime, timedelta

# def compute_metrics_for_past(granularity="daily", days=180):
#     """
#     Compute rolling metrics from historical crypto_prices data (daily).
#     """
#     engine = get_engine()
#     with engine.connect() as conn:
#         coins = conn.execute(text("""
#             SELECT DISTINCT coin_id 
#             FROM crypto_prices 
#             WHERE granularity = :g
#         """), {"g": granularity}).fetchall()

#     all_metrics = []

#     for (coin_id,) in coins:
#         print(f"🔄 {coin_id} ({granularity})")

#         with engine.connect() as conn:
#             df = pd.read_sql(text("""
#                 SELECT symbol, price, timestamp
#                 FROM crypto_prices
#                 WHERE coin_id = :coin_id AND granularity = :granularity
#                 ORDER BY timestamp
#             """), conn, params={"coin_id": coin_id, "granularity": granularity})

#         if df.empty:
#             continue

#         df["timestamp"] = pd.to_datetime(df["timestamp"])
#         start_time = df["timestamp"].min() + timedelta(days=7)
#         end_time = df["timestamp"].max()

#         current = start_time
#         interval = timedelta(days=1)

#         while current <= end_time:
#             last_24h = df[(df["timestamp"] >= current - timedelta(hours=24)) & (df["timestamp"] <= current)]
#             last_7d = df[(df["timestamp"] >= current - timedelta(days=7)) & (df["timestamp"] <= current)]

#             # if len(last_24h) < 5 or len(last_7d) < 7:
#             #     current += interval
#             #     continue

#             symbol = df["symbol"].iloc[0]
#             mean_7d = last_7d["price"].mean()
#             vol_24h = last_24h["price"].std()
#             cv = (vol_24h / mean_7d * 100) if mean_7d else 0

#             all_metrics.append({
#                 "coin_id": coin_id,
#                 "symbol": symbol,
#                 "rolling_mean_7d": round(mean_7d, 4),
#                 "volatility_24h": round(vol_24h, 4),
#                 "cv_24h_pct": round(cv, 2),
#                 "computed_at": current,
#                 "granularity": granularity
#             })

#             current += interval

#     return pd.DataFrame(all_metrics)

# # === Entry Point ===
# if __name__ == "__main__":
#     print("⏳ Backfilling DAILY metrics only...")

#     df = compute_metrics_for_past(granularity="daily", days=180)

#     print(f"📊 Generated {len(df)} rows.")

#     if not df.empty:
#         engine = get_engine()
#         with engine.begin() as conn:
#             df.to_sql("crypto_metrics", con=conn, if_exists="append", index=False)

#         print("✅ Inserted into DB.")
#     else:
#         print("⚠️ No data to insert.")
