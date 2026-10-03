import pandas as pd
from starbdp.preprocess import gps_csv_to_count_stream

def test_preprocess():
    df = pd.DataFrame({
        "timestamp": ["2026-01-01T00:00:00Z", "2026-01-01T00:05:00Z"],
        "latitude": [39.9, 39.9001],
        "longitude": [116.4, 116.4001],
    })
    stream, meta = gps_csv_to_count_stream(df, time_bin="10min", cell_size_m=200)
    assert stream.ndim == 3
    assert stream.sum() == 2
