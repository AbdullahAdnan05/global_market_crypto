import requests
import pandas as pd
from datetime import datetime
from config.settings import COINGECKO_BASE_URL
import os

import requests
import pandas as pd
from config.settings import COINGECKO_BASE_URL

def fetch_coin_history(coinid: str, days:int = 30 ) ->pd.DataFrame:
    """
    Fetches historical market data for one coin.

    Returns a DataFrame with columns:
      - timestamp: datetime
      - price: float
    """
    url = f"{COINGECKO_BASE_URL}/coins/{coinid}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        # "interval": interval
    }
    
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    
    # Convert each key into a dataframe
    prices_df = pd.DataFrame(data['prices'], columns=["ts_ms", "price"])
    caps_df = pd.DataFrame(data['market_caps'], columns=["ts_ms", "market_cap"])
    vols_df = pd.DataFrame(data['total_volumes'], columns=["ts_ms", "volume"])
    
    # Convert timestamp from millisecond to datetime
    for df in (prices_df, caps_df, vols_df):
        df["timestamp"] = pd.to_datetime(df["ts_ms"], unit="ms")
        df.drop(columns="ts_ms", inplace=True)
        
    # Merge all dataframe on timestamp
    df = prices_df.merge(caps_df, on="timestamp").merge(vols_df, on="timestamp")
    
    return df

if __name__ == "__main__":
    coin = "bitcoin"      # change to any coin id you like
    out_dir = "data"
    os.makedirs(out_dir, exist_ok=True)

    print(f"Fetching 30 days hourly history for {coin}…")
    history_df = fetch_coin_history(coin, days=30)

    csv_path = os.path.join(out_dir, f"{coin}_30d_hourly.csv")
    history_df.to_csv(csv_path, index=False)
    print(f"✅ Saved {len(history_df)} rows to {csv_path}")