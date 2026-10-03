from pathlib import Path
import json
import numpy as np
import pandas as pd
import yaml
from .types import STARBDPConfig
from .metrics import per_time_mae

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return STARBDPConfig(**yaml.safe_load(f))

def load_stream(path):
    path = Path(path)
    if path.suffix == ".npy":
        return np.load(path)
    if path.suffix == ".npz":
        z = np.load(path)
        key = "stream" if "stream" in z else list(z.keys())[0]
        return z[key]
    raise ValueError("supported formats: .npy and .npz")

def save_result(output_dir, original, result):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "released.npy", result.released)
    np.save(out / "release_mask.npy", result.release_mask)
    np.save(out / "beta_spent.npy", result.beta_spent)

    pd.DataFrame({
        "time_index": np.arange(original.shape[0]),
        "mae": per_time_mae(original, result.released),
        "release_rate": result.release_mask.mean(axis=(1, 2)),
        "beta_spent_max": result.beta_spent.max(axis=(1, 2)),
        "beta_spent_mean": result.beta_spent.mean(axis=(1, 2)),
    }).to_csv(out / "mae_by_time.csv", index=False)

    with open(out / "summary.json", "w", encoding="utf-8") as f:
        json.dump(
            {"metrics": result.metrics, "audit": result.audit, "theta": result.theta},
            f, ensure_ascii=False, indent=2
        )
