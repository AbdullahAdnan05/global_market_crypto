import time
import schedule
from ingestion.utils_cloud import throttled_fetch_and_insert_cloud
from processing.compute_metrics import compute_metrics
from database.db_handler import insert_crypto_metrics
from ingestion.email_alerts import notify_error

COINS = [
    ("bitcoin", "btc"),
    ("ethereum", "eth"),
    ("solana", "sol"),
    ("cardano", "ada"),
    ("ripple", "xrp"),
    ("dogecoin", "doge"),
    ("tron", "trx"),
    ("avalanche-2", "avax"),
    ("polkadot", "dot"),
    ("chainlink", "link"),
    ("litecoin", "ltc"),
]

def job():
    print("🔁 Running cloud scheduler job...")

    try:
        # Step 1: Fetch and insert price data (into Postgres)
        throttled_fetch_and_insert_cloud(COINS, batch_size=4, delay_between_batches=60)

        # Step 2: Compute metrics and insert into Postgres
        df_metrics = compute_metrics(granularity="hourly")
        if not df_metrics.empty:
            insert_crypto_metrics(df_metrics, engine_type="cloud")
            print(f"📊 Inserted {len(df_metrics)} metric rows into PostgreSQL.")
        else:
            print("⚠️ No metrics computed.")

    except Exception as e:
        print("❌ Job failed:", e)
        notify_error(str(e))


def start_scheduler():
    schedule.every(10).minutes.do(job)
    print("⏳ Cloud scheduler started (every 10 mins)")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    job()
    start_scheduler()
