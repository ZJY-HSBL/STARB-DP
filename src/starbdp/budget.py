import numpy as np

def evaluation_budget(epsilon, alpha):
    return epsilon / (2.0 * alpha)

def substream_remaining_budget(t, window, beta_spent, epsilon, alpha):
    start = max(0, t - alpha + 1)
    used = 0.0
    for tau in range(start, t):
        block = beta_spent[tau, window.r0:window.r1, window.c0:window.c1]
        used += float(np.max(block)) if block.size else 0.0
    return max(0.0, epsilon / 2.0 - used)

def candidate_beta_grid(t, height, width, windows, membership, beta_spent,
                        epsilon, alpha, minimum_beta):
    remaining = [
        substream_remaining_budget(t, w, beta_spent, epsilon, alpha)
        for w in windows
    ]
    out = np.full((height, width), minimum_beta, dtype=float)
    for i in range(height):
        for j in range(width):
            ids = membership[i][j]
            if ids:
                conservative = min(remaining[k] for k in ids)
                out[i, j] = max(minimum_beta, 0.5 * conservative)
    return out

def audit_release_budget(beta_spent, windows, epsilon, alpha, atol=1e-9):
    T = beta_spent.shape[0]
    limit = epsilon / 2.0
    worst = 0.0
    worst_at = None
    for k, w in enumerate(windows):
        per_t = np.array([
            float(np.max(beta_spent[t, w.r0:w.r1, w.c0:w.c1]))
            for t in range(T)
        ])
        for end in range(T):
            start = max(0, end - alpha + 1)
            total = float(per_t[start:end + 1].sum())
            if total > worst:
                worst = total
                worst_at = {"window_index": k, "start": start, "end": end}
    return {
        "release_half_budget_limit": limit,
        "worst_release_window_spend": worst,
        "within_bound": bool(worst <= limit + atol),
        "worst_case": worst_at,
    }
