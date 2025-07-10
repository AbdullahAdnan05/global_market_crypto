import requests
import pandas as pd
from datetime import datetime
from config.settings import COINGECKO_BASE_URL

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

def fetch_latest_price(coin_id:str, symbol: str)-> pd.DataFrame:
    url = f"{COINGECKO_BASE_URL}/coins/{coin_id}"
    params = {"localiztion": "false", "tickers": "false", "market_data": "true"}
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
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