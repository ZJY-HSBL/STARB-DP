# STARB-DP

**SpatioTemporal Adaptive Release-Budget Differential Privacy**

STARB-DP is a research-grade implementation for privacy-preserving publication of streaming spatiotemporal count data. It combines temporal privacy windows, local spatial sub-stream constraints, adaptive release-budget allocation, private change evaluation, Laplace perturbation, and selective publication.

- [中文说明](README_CN.md)
- [English Documentation](README_EN.md)

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -e .
python scripts/demo_synthetic.py
python scripts/run_experiment.py --config configs/default.yaml
pytest -q
```

## Repository layout

```text
STARB-DP/
├─ configs/
├─ data/
│  ├─ raw/
│  ├─ processed/
│  └─ sample/
├─ docs/
├─ scripts/
├─ src/starbdp/
├─ tests/
├─ .github/workflows/
├─ README.md
├─ README_CN.md
├─ README_EN.md
├─ pyproject.toml
└─ LICENSE
```

## Core interface

```python
import numpy as np
from starbdp import STARBDP, STARBDPConfig

stream = np.random.poisson(3.0, size=(60, 20, 20)).astype(float)

cfg = STARBDPConfig(
    epsilon=1.0,
    alpha=20,
    spatial_order=5,
    substream_mode="sliding",
    seed=42,
)

result = STARBDP(cfg).fit_transform(stream)
print(result.metrics)
print(result.audit)
```

The core input shape is `[T, H, W]`, where each `H × W` frame is a spatial count grid.

MIT License.
