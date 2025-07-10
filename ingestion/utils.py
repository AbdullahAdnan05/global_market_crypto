# ingestion/utils.py

import time
from ingestion.crypto_api import fetch_latest_price
from ingestion.email_alerts import notify_error
from database.db_handler import insert_crypto_prices

def throttled_fetch_and_insert(coins, batch_size=5, delay_between_batches=60):
    """
    Fetch coin data in batches with delay to avoid rate limiting.

    Args:
        coins (list of tuples): List like [("bitcoin", "btc"), ("ethereum", "eth"), ...]
        batch_size (int): How many coins to process in one batch.
        delay_between_batches (int): Seconds to wait between batches.
    """
    batches = [coins[i:i+batch_size] for i in range(0, len(coins), batch_size)]

    for batch_num, batch in enumerate(batches):
        print(f"📦 Batch {batch_num + 1}/{len(batches)}")

        for coin_id, symbol in batch:
            try:
                df = fetch_latest_price(coin_id, symbol)
                insert_crypto_prices(df)
                print(f"✅ {symbol.upper()} inserted")
            except Exception as e:
                print(f"❌ Error fetching {coin_id}:", e)
                notify_error(str(e))
            time.sleep(2)

        if batch_num < len(batches) - 1:
            print(f"⏳ Waiting {delay_between_batches} seconds before next batch...")
            time.sleep(delay_between_batches)
