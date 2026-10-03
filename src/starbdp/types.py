from dataclasses import dataclass
from typing import Literal
import numpy as np

@dataclass(frozen=True)
class STARBDPConfig:
    epsilon: float = 1.0
    alpha: int = 120
    spatial_order: int = 15
    substream_mode: Literal["sliding", "partition"] = "sliding"
    clip_nonnegative: bool = True
    seed: int | None = 42
    minimum_beta: float = 1e-9

    def validate(self) -> None:
        if self.epsilon <= 0:
            raise ValueError("epsilon must be > 0")
        if self.alpha <= 0:
            raise ValueError("alpha must be a positive integer")
        if self.spatial_order <= 0:
            raise ValueError("spatial_order must be a positive integer")
        if self.substream_mode not in {"sliding", "partition"}:
            raise ValueError("substream_mode must be sliding or partition")
        if self.minimum_beta <= 0:
            raise ValueError("minimum_beta must be > 0")

@dataclass
class STARBDPResult:
    released: np.ndarray
    release_mask: np.ndarray
    beta_spent: np.ndarray
    theta: float
    metrics: dict
    audit: dict
