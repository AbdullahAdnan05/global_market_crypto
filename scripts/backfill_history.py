import requests
import pandas as pd
import time
from datetime import datetime
from config.settings import COINGECKO_BASE_URL
from database.db_handler import insert_crypto_prices
from sqlalchemy import text
from database.db_engine import get_engine

def is_coin_already_fetched(coin_id: str) -> bool:
    """
    Returns True if coin_id already has rows in the crypto_prices table.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM crypto_prices WHERE coin_id = :coin_id"),
            {"coin_id": coin_id}
        )
        count = result.scalar()
        return count > 0


def fetch_with_retry(url, params, retries=3, delay=5):
    for i in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"⏳ Retry {i+1}/{retries} — {e}")
            time.sleep(delay)
    raise Exception(f"❌ Failed after {retries} retries")

def fetch_coin_history(coin_id, symbol, days, granularity):
    url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    data = fetch_with_retry(url, params)

    df_price = pd.DataFrame(data["prices"], columns=["ts", "price"])
    df_mc = pd.DataFrame(data["market_caps"], columns=["ts", "market_cap"])
    df_vol = pd.DataFrame(data["total_volumes"], columns=["ts", "volume"])

    df = df_price.merge(df_mc, on="ts").merge(df_vol, on="ts")
    df["timestamp"] = pd.to_datetime(df["ts"], unit="ms")
    df = df.drop(columns=["ts"])

    df["coin_id"] = coin_id
    df["symbol"] = symbol
    df["percentage_change_24h"] = None
    df["granularity"] = granularity

    return df[["coin_id", "symbol", "price", "market_cap", "volume", "percentage_change_24h", "timestamp", "granularity"]]

def run_backfill():
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

    failed = []

    for coin_id, symbol in COINS:
        if is_coin_already_fetched(coin_id):
            print(f"⏭️  Skipping {coin_id} — already in database")
            continue
        try:
            print(f"\n📦 {coin_id} — 90d (hourly)")
            hourly_df = fetch_coin_history(coin_id, symbol, 90, "hourly")
            time.sleep(2)

            print(f"📦 {coin_id} — 180d (daily)")
            daily_df = fetch_coin_history(coin_id, symbol, 180, "daily")
            time.sleep(2)

            df_all = pd.concat([hourly_df, daily_df])
            df_all = df_all.drop_duplicates(subset=["coin_id", "timestamp"])
            df_all = df_all.sort_values("timestamp")

            insert_crypto_prices(df_all)
            print(f"✅ {coin_id} — Inserted {len(df_all)} rows")

        except Exception as e:
            print(f"❌ Failed {coin_id} — {e}")
            failed.append(coin_id)

    print("\n🏁 Backfill finished.")
    if failed:
        print("⚠️ Failed coins:", failed)
    else:
        print("✅ All coins inserted successfully.")

if __name__ == "__main__":
    run_backfill()
