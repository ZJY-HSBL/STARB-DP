import numpy as np
import pytest
from starbdp import STARBDP, STARBDPConfig

def test_shape_and_nonnegative():
    x = np.ones((10, 6, 6)) * 3
    res = STARBDP(STARBDPConfig(epsilon=1.0, alpha=4, spatial_order=3, seed=1)).fit_transform(x)
    assert res.released.shape == x.shape
    assert np.all(res.released >= 0)

def test_reproducibility():
    x = np.arange(160, dtype=float).reshape(10, 4, 4) % 7
    cfg = STARBDPConfig(epsilon=1.0, alpha=4, spatial_order=2, seed=123)
    a = STARBDP(cfg).fit_transform(x)
    b = STARBDP(cfg).fit_transform(x)
    assert np.array_equal(a.released, b.released)

def test_release_budget_audit():
    x = np.random.default_rng(0).poisson(3, size=(20, 8, 8)).astype(float)
    res = STARBDP(STARBDPConfig(epsilon=1.0, alpha=5, spatial_order=3, seed=2)).fit_transform(x)
    assert res.audit["within_bound"]

def test_invalid():
    with pytest.raises(ValueError):
        STARBDPConfig(epsilon=0).validate()
