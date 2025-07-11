-- Table: crypto_prices
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50),
    symbol VARCHAR(50),
    price DECIMAL(18, 4),
    market_cap BIGINT,
    volume BIGINT,
    percentage_change_24h FLOAT,
    granularity VARCHAR(10),
    timestamp TIMESTAMP
);

-- Table: crypto_metrics
CREATE TABLE IF NOT EXISTS crypto_metrics (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50),
    symbol VARCHAR(50),
    granularity VARCHAR(10),
    volatility_7d FLOAT,
    volatility_30d FLOAT,
    cv_30d FLOAT,
    rolling_corr_btc_30d FLOAT,
    timestamp TIMESTAMP
);
