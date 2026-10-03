# STARB-DP 算法说明

输入：

```text
D = {D_1, D_2, ..., D_T}, D_t ∈ R^(H×W)
epsilon > 0
alpha ∈ N+
m ∈ N+
```

评估预算：

```text
theta_t = epsilon / (2 alpha)
```

对任意完整 `alpha` 时间窗口：

```text
Σ theta_t = epsilon/2
```

对于空间子流 `S`：

```text
R_t(S) = epsilon/2
         - Σ_{tau=t-alpha+1}^{t-1} max_{(i,j)∈S} beta_tau(i,j)
```

单个位置的保守发布预算：

```text
beta_bar_t(i,j) = min_{S contains (i,j)} R_t(S)
beta_t(i,j) = beta_bar_t(i,j)/2
```

私有变化评估：

```text
A_t = MAE(D_t, O_(t-1))
A_tilde = A_t + Lap(1/(theta_t * area))
```

候选发布误差：

```text
P_t = 1 / beta_t
```

若 `A_tilde < P_t`，则复用旧结果，否则发布：

```text
O_t(i,j) = D_t(i,j) + Lap(1/beta_t(i,j))
```

实现内置预算审计，对所有空间子流和连续时间窗口检查：

```text
Σ max beta_t(i,j) <= epsilon/2
```
