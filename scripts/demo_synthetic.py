from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starbdp import STARBDP, STARBDPConfig

rng = np.random.default_rng(123)
x = rng.poisson(2.0, size=(48, 16, 16)).astype(float)
x[12:24, 3:7, 3:7] += 8
x[30:42, 9:13, 10:14] += 12

cfg = STARBDPConfig(
    epsilon=1.0,
    alpha=12,
    spatial_order=4,
    substream_mode="sliding",
    seed=42,
)

result = STARBDP(cfg).fit_transform(x)
print("metrics:", result.metrics)
print("audit:", result.audit)
