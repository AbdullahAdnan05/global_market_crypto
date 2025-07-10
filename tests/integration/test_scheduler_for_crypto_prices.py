# tests/integration/test_scheduler.py

import pytest
from sqlalchemy import text
from ingestion.schedular import job
from database.db_engine import get_engine

@pytest.mark.integration
def test_scheduler_job_inserts_new_rows():
    engine = get_engine()

    with engine.connect() as conn:
        before = conn.execute(text("SELECT COUNT(*) FROM crypto_prices")).scalar()

    job()  # Run the scheduled job

    with engine.connect() as conn:
        after = conn.execute(text("SELECT COUNT(*) FROM crypto_prices")).scalar()

    assert after > before, f"Expected new rows inserted. Before: {before}, After: {after}"
