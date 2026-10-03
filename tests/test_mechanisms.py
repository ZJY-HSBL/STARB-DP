import numpy as np
from starbdp.mechanisms import perturb_mae

def test_reproducible_noise():
    a = perturb_mae(1.0, 0.1, 25, np.random.default_rng(42))
    b = perturb_mae(1.0, 0.1, 25, np.random.default_rng(42))
    assert a == b
