# STARB-DP Algorithm

Given `D_t ∈ R^(H×W)`:

```text
theta = epsilon / (2 alpha)
```

For a local spatial sub-stream `S`:

```text
R_t(S) = epsilon/2
         - sum over previous alpha-1 timestamps
           of max beta spending inside S.
```

For a cell covered by multiple sub-streams:

```text
beta_bar_t(i,j) = min R_t(S)
beta_t(i,j) = beta_bar_t(i,j)/2
```

Private local-change evaluation:

```text
A_noisy = MAE(D_t, O_(t-1)) + Lap(1/(theta * area))
```

Release threshold:

```text
P = 1/beta
```

If `A_noisy < P`, reuse the previous public result. Otherwise:

```text
O_t(i,j) = D_t(i,j) + Lap(1/beta_t(i,j))
```

The audit module checks the publication half-budget over all spatial sub-streams and temporal windows.
