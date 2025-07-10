CREATE TABLE IF NOT EXISTS crypto_prices(
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_id VARCHAR(50),
    symbol VARCHAR(50),
    price DECIMAL(18, 4),
    market_cap BIGINT,
    volume BIGINT,
    percentage_change_24h FLOAT,
    granularity VARCHAR(10),
    timestamp DATETIME
);
CREATE TABLE IF NOT EXISTS crypto_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_id VARCHAR(50),
    symbol VARCHAR(50),
    rolling_mean_7d DECIMAL(18, 4),
    volatility_24h DECIMAL(18, 4),
    cv_24h_pct DECIMAL(18, 2),
    computed_at DATETIME,
    granularity VARCHAR(10)
);
