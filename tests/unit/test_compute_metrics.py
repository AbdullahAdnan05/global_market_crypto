import pytest
import pandas as pd
from processing.compute_metrics import compute_metrics

@pytest.mark.unit
def test_compute_metrics_structure():
    df = compute_metrics()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    required_cols = {
        "coin_id",
        "symbol",
        "rolling_mean_7d",
        "volatility_24h",
        "cv_24h",
        "computed_at",
        "granularity"
    }

    assert required_cols.issubset(df.columns)
