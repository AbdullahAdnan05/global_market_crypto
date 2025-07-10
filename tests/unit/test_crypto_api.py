import pandas as pd
import pytest
from ingestion.crypto_api import get_top_coins, fetch_latest_price   # will not exist yet

@pytest.mark.unit
def test_get_top_coins_returns_dataframe():
    df = get_top_coins(limit=5)    # this will raise ImportError today
    assert not df.empty
    assert {"id", "symbol", "price", "timestamp", "percentage_change_24h"} <= set(df.columns)


@pytest.mark.unit
def test_fetch_latest_price_returns_dataframe():
    # Act
    df = fetch_latest_price("bitcoin", "btc")

    # Assert type
    assert isinstance(df, pd.DataFrame), "Function should return a DataFrame"

    # Assert non-empty
    assert not df.empty, "DataFrame should not be empty"

    # Assert required columns exist
    expected_cols = {
        "coin_id", "symbol", "price", "market_cap", "volume",
        "percentage_change_24h", "timestamp", "granularity"
    }
    assert expected_cols.issubset(set(df.columns)), f"Missing columns: {expected_cols - set(df.columns)}"