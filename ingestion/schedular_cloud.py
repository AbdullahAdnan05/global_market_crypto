import time
import schedule
from ingestion.utils_cloud import throttled_fetch_and_insert_cloud
from processing.compute_metrics import compute_metrics
from database.db_handler import insert_crypto_metrics
from ingestion.email_alerts import notify_error

#  Target coins for monitoring
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

#  Main scheduled job
def job():
    print("🔁 Running cloud scheduler job...", flush=True)

    try:
        # Step 1: Fetch and insert latest price data
        throttled_fetch_and_insert_cloud(COINS, batch_size=4, delay_between_batches=60)

        # Step 2: Compute & insert hourly metrics
        df_metrics = compute_metrics(granularity="hourly")
        if not df_metrics.empty:
            insert_crypto_metrics(df_metrics, engine_type="cloud")
            print(f"📊 Inserted {len(df_metrics)} metric rows into PostgreSQL.", flush=True)
        else:
            print("⚠️ No metrics computed.", flush=True)

    except Exception as e:
        print("❌ Job failed:", e, flush=True)
        notify_error(str(e))


#  Start the scheduler loop (every 30 minutes)
def start_scheduler():
    schedule.every(45).minutes.do(job)
    print("[Railway Worker] Cloud scheduler started. Running every 45 minutes...", flush=True)

    while True:
        schedule.run_pending()
        time.sleep(30)
