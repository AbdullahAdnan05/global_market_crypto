# from ingestion.crypto_api import get_top_coins
# df = get_top_coins(limit=5)
# print(df.columns)

# from database.db_handler import create_table_from_sql
# create_table_from_sql()
# from scripts.fetch_history import fetch_coin_history
# import os

# if __name__ == "__main__":
#     coin = "bitcoin"      # change to any coin id you like
#     out_dir = "data"
#     os.makedirs(out_dir, exist_ok=True)

#     print(f"Fetching 30 days hourly history for {coin}…")
#     history_df = fetch_coin_history(coin, days=90)

#     csv_path = os.path.join(out_dir, f"{coin}_30d_hourly.csv")
#     history_df.to_csv(csv_path, index=False)
#     print(f"✅ Saved {len(history_df)} rows to {csv_path}")

# from scripts.backfill_history import run_backfill

# run_backfill()

# from ingestion.email_alerts import notify_error

# if __name__ == "__main__":
#     notify_error("🧪 This is a test alert from Global Market Pulse.")


# from ingestion.schedular import job
# job()

# from processing.compute_metrics import compute_metrics
# df = compute_metrics()
# print(df.head())

# # scripts/run_metrics_pipeline.py
# from processing.compute_metrics import compute_metrics
# from database.db_handler import insert_crypto_metrics

# df = compute_metrics()
# if not df.empty:
#     insert_crypto_metrics(df)
#     print("✅ Metrics inserted.")
# else:
#     print("⚠️ No data to insert.")

# from scripts.migrate_mysql_to_postgres import migrate_table

# migrate_table("crypto_prices")
# migrate_table("crypto_metrics")

# from ingestion.schedular_cloud import job, start_scheduler

# if __name__ == "__main__":
#     job()
#     start_scheduler()

from server import app


if __name__ == "__main__":
    from os import getenv
    port = int(getenv("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)
