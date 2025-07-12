import requests
import pandas as pd
from datetime import datetime
from config.settings import COINGECKO_BASE_URL
import time

def get_top_coins(limit=5) -> pd.DataFrame:
    """
    Fetches the top cryptocurrencies by market cap.

    Args:
        limit (int): Number of coins to fetch. Default is 5.

    Returns:
        pd.DataFrame: DataFrame with columns ['id', 'symbol', 'price', 'timestamp']
    """
    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency":"usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch from CoinGecko: {e}")
    
    # Normalize to DataFrame
    df = pd.DataFrame([{
        "id": coin['id'],
        "symbol": coin["symbol"],
        "price": coin["current_price"],
        "market_cap": coin["market_cap"],
        "percentage_change_24h": coin['price_change_percentage_24h'],
        "timestamp": coin["last_updated"]
    } for coin in data ])
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    return df


def fetch_latest_price(coin_id: str, symbol: str) -> pd.DataFrame:
    """
    Fetches rich price data from CoinGecko with retry logic on 429 errors.

    Returns:
        pd.DataFrame with price, market_cap, volume, etc.
    """
    url = f"{COINGECKO_BASE_URL}/coins/{coin_id}"
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true"
    }

    for attempt in range(3):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            break
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"⚠️ 429 Too Many Requests — sleeping 20s and retrying (attempt {attempt + 1}/3)")
                time.sleep(20)
            else:
                raise
        except Exception as e:
            raise RuntimeError(f"❌ Failed to fetch {coin_id}: {e}")

    data = response.json()
    market = data["market_data"]
    timestamp = pd.to_datetime(market["last_updated"])

    row = {
        "coin_id": coin_id,
        "symbol": symbol,
        "price": market["current_price"]['usd'],
        "market_cap": market["market_cap"]["usd"],
        "volume": market["total_volume"]["usd"],
        "percentage_change_24h": market["price_change_percentage_24h"],
        "timestamp": timestamp,
        "granularity": "hourly"
    }

    return pd.DataFrame([row])
