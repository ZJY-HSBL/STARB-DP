import math
import numpy as np
import pandas as pd

def meters_per_degree_lat():
    return 111320.0

def meters_per_degree_lon(lat_deg):
    return 111320.0 * math.cos(math.radians(lat_deg))

def gps_csv_to_count_stream(df, time_bin="10min", cell_size_m=200.0,
                            lat_col="latitude", lon_col="longitude",
                            time_col="timestamp"):
    if cell_size_m <= 0:
        raise ValueError("cell_size_m must be positive")

    data = df.copy()
    data[time_col] = pd.to_datetime(data[time_col], utc=True, errors="raise")
    data = data.dropna(subset=[lat_col, lon_col, time_col])

    lat0 = float(data[lat_col].mean())
    lat_min = float(data[lat_col].min())
    lon_min = float(data[lon_col].min())

    dy = (data[lat_col].to_numpy() - lat_min) * meters_per_degree_lat()
    dx = (data[lon_col].to_numpy() - lon_min) * meters_per_degree_lon(lat0)

    data["_row"] = np.floor(dy / cell_size_m).astype(int)
    data["_col"] = np.floor(dx / cell_size_m).astype(int)
    data["_time_bin"] = data[time_col].dt.floor(time_bin)

    times = pd.Index(sorted(data["_time_bin"].unique()))
    tmap = {v: i for i, v in enumerate(times)}
    H = int(data["_row"].max()) + 1
    W = int(data["_col"].max()) + 1
    stream = np.zeros((len(times), H, W), dtype=float)

    grouped = data.groupby(["_time_bin", "_row", "_col"]).size()
    for (ts, r, c), count in grouped.items():
        stream[tmap[ts], int(r), int(c)] = float(count)

    meta = {
        "time_bin": time_bin,
        "cell_size_m": cell_size_m,
        "lat_origin": lat_min,
        "lon_origin": lon_min,
        "reference_latitude": lat0,
        "shape": list(stream.shape),
        "timestamps": [str(x) for x in times],
    }
    return stream, meta
