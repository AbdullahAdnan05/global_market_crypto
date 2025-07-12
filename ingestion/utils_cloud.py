import time
from ingestion.crypto_api import fetch_latest_price
from ingestion.email_alerts import notify_error
from database.db_handler import insert_crypto_prices

def throttled_fetch_and_insert_cloud(coins, batch_size=5, delay_between_batches=90):
    """
    Cloud version of throttled fetch. Pushes data to PostgreSQL.
    """
    batches = [coins[i:i + batch_size] for i in range(0, len(coins), batch_size)]

    for batch_num, batch in enumerate(batches):
        print(f"📦 Cloud Batch {batch_num + 1}/{len(batches)}")

        for coin_id, symbol in batch:
            try:
                df = fetch_latest_price(coin_id, symbol)
                insert_crypto_prices(df, engine_type="cloud")
                print(f"✅ {symbol.upper()} inserted into cloud DB")
            except Exception as e:
                print(f"❌ Error fetching {coin_id}:", e)
                notify_error(str(e))
            time.sleep(6)

        if batch_num < len(batches) - 1:
            print(f"⏳ Waiting {delay_between_batches} sec before next batch...")
            time.sleep(delay_between_batches)
