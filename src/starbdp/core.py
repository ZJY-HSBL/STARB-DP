import numpy as np
from .types import STARBDPConfig, STARBDPResult
from .grid import iter_spatial_windows, build_cell_membership
from .budget import evaluation_budget, candidate_beta_grid, audit_release_budget
from .mechanisms import perturb_mae, perturb_count
from .metrics import summarize

class STARBDP:
    def __init__(self, config: STARBDPConfig):
        config.validate()
        self.config = config
        self.rng = np.random.default_rng(config.seed)

    def fit_transform(self, stream: np.ndarray) -> STARBDPResult:
        x = np.asarray(stream, dtype=float)
        if x.ndim != 3:
            raise ValueError("stream must have shape [T, H, W]")
        if min(x.shape) <= 0:
            raise ValueError("stream dimensions must be non-empty")

        T, H, W = x.shape
        cfg = self.config

        windows = list(iter_spatial_windows(H, W, cfg.spatial_order, cfg.substream_mode))
        membership = build_cell_membership(H, W, windows)
        eval_blocks = list(iter_spatial_windows(H, W, cfg.spatial_order, "partition"))

        released = np.zeros_like(x)
        release_mask = np.zeros_like(x, dtype=bool)
        beta_spent = np.zeros_like(x)
        theta = evaluation_budget(cfg.epsilon, cfg.alpha)
        prev = np.zeros((H, W), dtype=float)

        for t in range(T):
            beta_candidate = candidate_beta_grid(
                t, H, W, windows, membership, beta_spent,
                cfg.epsilon, cfg.alpha, cfg.minimum_beta
            )
            out = prev.copy()

            for block in eval_blocks:
                current = x[t, block.r0:block.r1, block.c0:block.c1]
                old = prev[block.r0:block.r1, block.c0:block.c1]

                local_mae = float(np.mean(np.abs(current - old)))
                noisy_mae = perturb_mae(local_mae, theta, block.area, self.rng)

                beta_block = beta_candidate[block.r0:block.r1, block.c0:block.c1]
                effective_beta = max(float(np.min(beta_block)), cfg.minimum_beta)
                publication_error = 1.0 / effective_beta

                if noisy_mae >= publication_error:
                    for i in range(block.r0, block.r1):
                        for j in range(block.c0, block.c1):
                            b = max(float(beta_candidate[i, j]), cfg.minimum_beta)
                            out[i, j] = perturb_count(
                                x[t, i, j], b, self.rng, cfg.clip_nonnegative
                            )
                            release_mask[t, i, j] = True
                            beta_spent[t, i, j] = b

            released[t] = out
            prev = out

        metrics = summarize(x, released, release_mask)
        audit = audit_release_budget(beta_spent, windows, cfg.epsilon, cfg.alpha)
        audit["evaluation_half_budget_per_full_window"] = theta * cfg.alpha
        audit["evaluation_half_budget_limit"] = cfg.epsilon / 2.0
        audit["evaluation_within_bound"] = bool(
            theta * cfg.alpha <= cfg.epsilon / 2.0 + 1e-12
        )

        return STARBDPResult(
            released=released,
            release_mask=release_mask,
            beta_spent=beta_spent,
            theta=theta,
            metrics=metrics,
            audit=audit,
        )
