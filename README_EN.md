# STARB-DP: SpatioTemporal Adaptive Release-Budget Differential Privacy

STARB-DP is an implementation for privacy-preserving release of streaming spatiotemporal count data.

The method jointly constrains temporal privacy windows and local spatial sub-streams while adapting publication budgets to recent spending and local data dynamics.

## Core pipeline

At timestamp `t`, compare the current count grid `D_t` with the previous public output `O_(t-1)` using local MAE.

```text
theta = epsilon / (2 * alpha)
A_noisy = MAE(D_t, O_(t-1)) + Laplace(1 / (theta * area))
```

For a local spatial sub-stream `S`:

```text
R_t(S) = epsilon/2
         - sum of timestamp-wise max beta spending
           over the previous alpha-1 timestamps
```

For a cell covered by multiple sub-streams:

```text
beta_bar_t(i,j) = min R_t(S)
beta_t(i,j) = 0.5 * beta_bar_t(i,j)
```

The expected publication error scale is approximated by:

```text
P = 1 / beta
```

If `A_noisy < P`, the previous public result is reused. Otherwise:

```text
O_t(i,j) = D_t(i,j) + Laplace(0, 1/beta_t(i,j))
```

Only actual releases are counted as publication-budget spending.

## Features

- temporal-window accounting;
- local spatial sub-stream constraints;
- split evaluation/publication budgets;
- adaptive remaining-budget computation;
- private release decisions;
- selective publication;
- sliding or disjoint spatial windows;
- budget auditing;
- GPS-to-grid preprocessing;
- epsilon / alpha / spatial-order sweeps;
- deterministic experiments.

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
python scripts/demo_synthetic.py
python scripts/run_experiment.py --config configs/default.yaml
pytest -q
```

This repository focuses on a complete, executable, extensible, and auditable implementation and does not make a claim of algorithmic originality.
