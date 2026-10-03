import numpy as np

def mae(original, released):
    return float(np.mean(np.abs(original - released)))

def rmse(original, released):
    return float(np.sqrt(np.mean((original - released) ** 2)))

def per_time_mae(original, released):
    return np.mean(np.abs(original - released), axis=(1, 2))

def summarize(original, released, release_mask):
    return {
        "mae": mae(original, released),
        "rmse": rmse(original, released),
        "release_rate": float(np.mean(release_mask)),
        "reuse_rate": float(1.0 - np.mean(release_mask)),
    }
