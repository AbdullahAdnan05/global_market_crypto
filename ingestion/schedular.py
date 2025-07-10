import time
import schedule
from ingestion.utils import throttled_fetch_and_insert
from processing.compute_metrics import compute_metrics
from database.db_handler import insert_crypto_metrics
from ingestion.email_alerts import notify_error
# List of coin to track
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
    """
    Job that fetches prices for all tracked coins,
    inserts them into the database, computes metrics, and sends alerts on failure.
    """
    print("🔁 Running scheduled job...")

    try:
        # Step 1: Fetch and insert price data (in batches)
        throttled_fetch_and_insert(COINS, batch_size=4, delay_between_batches=60)

        # Step 2: Compute metrics from fresh prices
        df_metrics = compute_metrics(granularity="hourly")
        if not df_metrics.empty:
            insert_crypto_metrics(df_metrics)
            print(f"📊 Inserted {len(df_metrics)} metric rows.")
        else:
            print("⚠️ No metrics computed (data may be insufficient).")

    except Exception as e:
        print("❌ Job failed:", e)
        notify_error(str(e))
            
def start_schedular():
    """
    Starts the  schedular that runs every 10 mintues.
    """
    schedule.every(10).minutes.do(job)
    print("Schedular started (every 10 minutes)")
    
    while True:
        schedule.run_pending()
        time.sleep(30)
        
        
# For manual run or dedug
if __name__=="__main__":
    job() # run immediately once
    start_schedular()
    