import numpy as np

def laplace_noise(rng: np.random.Generator, scale: float, size=None):
    if scale < 0:
        raise ValueError("scale must be non-negative")
    if scale == 0:
        return np.zeros(size) if size is not None else 0.0
    return rng.laplace(0.0, scale, size=size)

def perturb_count(value, beta, rng, clip_nonnegative=True):
    if beta <= 0:
        raise ValueError("beta must be > 0")
    out = float(value + laplace_noise(rng, 1.0 / beta))
    return max(0.0, out) if clip_nonnegative else out

def perturb_mae(mae_value, theta, area, rng):
    if theta <= 0 or area <= 0:
        raise ValueError("theta and area must be positive")
    return float(mae_value + laplace_noise(rng, 1.0 / (theta * area)))
