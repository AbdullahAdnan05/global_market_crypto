import pytest
from ingestion.schedular import job
from database.db_engine import get_engine
from sqlalchemy import text

@pytest.mark.integration
def test_full_pipeline_inserts_data():
    engine = get_engine()
    
    # Count before
    with engine.connect() as conn:
        before_prices = conn.execute(text("SELECT COUNT(*) FROM crypto_prices")).scalar()
        before_metrics = conn.execute(text("SELECT COUNT(*) FROM crypto_metrics")).scalar()

    # Run the full scheduled job
    job()

    # Count after
    with engine.connect() as conn:
        after_prices = conn.execute(text("SELECT COUNT(*) FROM crypto_prices")).scalar()
        after_metrics = conn.execute(text("SELECT COUNT(*) FROM crypto_metrics")).scalar()

    assert after_prices > before_prices, "❌ No new prices inserted"
    assert after_metrics > before_metrics, "❌ No new metrics inserted"
