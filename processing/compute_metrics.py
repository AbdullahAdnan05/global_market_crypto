import pandas as pd
from sqlalchemy import text
from database.db_engine import get_engine
from datetime import datetime, timedelta

def compute_metrics(granularity="hourly") -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        query= text("""
            SELECT coin_id, symbol, price, timestamp
            FROM crypto_prices
            WHERE granularity = :granularity
                AND timestamp >= :since            
        """)
        since = datetime.utcnow() - timedelta(days=7)
        df = pd.read_sql(query, conn, params={"granularity": granularity, "since": since})
        
    if df.empty:
        print("NO data found for metrics")
        return pd.DataFrame()
    
    metrics = []
    
    for coin_id, group in df.groupby("coin_id"):
        symbol = group["symbol"].iloc[0]
        
        # # Before we was counting 
        # rolling_mean = group["price"].rolling(window=24, min_periods=1).mean().iloc[-1]
        # volatility = group["price"].tail(24).std()
        
        # ⏱ Filter by time instead of row count
        last_24h = group[group["timestamp"] >= datetime.utcnow() - timedelta(hours=24)]
        last_7d  = group[group["timestamp"] >= datetime.utcnow() - timedelta(days=7)]

        rolling_mean = last_7d["price"].mean()
        volatility = last_24h["price"].std()
        cv = (volatility / rolling_mean * 100 ) if rolling_mean else 0  # coefficient of variation

        metrics.append({
            "coin_id": coin_id,
            "symbol": symbol,
            "rolling_mean_7d": round(rolling_mean, 4),
            "volatility_24h": round(volatility, 4),
            "cv_24h_pct": round(cv, 2),
            "computed_at": datetime.utcnow(),
            "granularity": granularity
        })
    return pd.DataFrame(metrics)