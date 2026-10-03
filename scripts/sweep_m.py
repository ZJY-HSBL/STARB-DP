from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from starbdp import STARBDP, STARBDPConfig

def build_stream(seed=123):
    rng = np.random.default_rng(seed)
    x = rng.poisson(3.0, size=(80, 16, 16)).astype(float)
    x[20:40, 3:8, 3:8] += 8
    x[50:70, 10:14, 7:12] += 10
    return x

x = build_stream()
rows = []
for m in [3, 5, 7, 9]:
    res = STARBDP(STARBDPConfig(epsilon=1.0, alpha=20, spatial_order=m, seed=42)).fit_transform(x)
    rows.append({"m": m, **res.metrics, **res.audit})
out = ROOT / "outputs/sweep_m.csv"
out.parent.mkdir(exist_ok=True)
pd.DataFrame(rows).to_csv(out, index=False)
print(out)
