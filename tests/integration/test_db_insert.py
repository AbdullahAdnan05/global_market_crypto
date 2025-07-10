import pytest
from ingestion.crypto_api import get_top_coins
from database.db_handler import insert_crypto_prices
from sqlalchemy import text
from database.db_engine import get_engine

# @pytest.mark.integration
# it will not work as the schema has been changed
def test_insert_crypto_prices():
    """
    Integration test to verify crypto prices can be fetched and inserted into the database.
    """
    df = get_top_coins(limit=2)
    insert_crypto_prices(df)
    
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT count(*) FROM crypto_prices"))
        count = result.scalar()
        assert count > 0 