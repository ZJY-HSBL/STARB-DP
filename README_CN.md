# STARB-DP：时空自适应发布预算差分隐私框架

STARB-DP（SpatioTemporal Adaptive Release-Budget Differential Privacy）面向连续轨迹与位置统计数据发布场景，用于在时空相关数据流中控制隐私预算，同时尽量降低噪声对数据可用性的影响。

该实现以 `[T,H,W]` 时空计数张量为核心输入，将总隐私预算拆分为“评估预算”和“发布预算”，在连续 `alpha` 时间窗口与局部 `m×m` 空间子流约束下，根据局部变化决定是否发布新版本。

## 核心流程

### 1. 私有变化评估

当前真实网格 `D_t` 与上一公开结果 `O_(t-1)` 的局部近似误差：

```text
A = MAE(D_t, O_(t-1))
```

固定评估预算：

```text
theta = epsilon / (2 * alpha)
```

对于面积为 `q` 的局部区域，MAE 灵敏度按 `1/q` 处理，因此评估噪声尺度为：

```text
scale_eval = 1 / (theta * q)
```

### 2. 自适应发布预算

发布部分使用总预算的一半。对于空间子流 `S`，时刻 `t` 的剩余发布预算：

```text
R_t(S) = epsilon/2
         - Σ max(beta_tau(i,j))
```

其中求和范围是前 `alpha-1` 个时间点，`(i,j)` 位于该空间子流内部。

若某位置属于多个空间子流，则采用最严格的剩余预算：

```text
beta_bar_t(i,j) = min R_t(S)
beta_t(i,j) = 0.5 * beta_bar_t(i,j)
```

### 3. 再评估与选择性发布

候选发布误差：

```text
P = 1 / beta
```

若带噪近似误差满足：

```text
A_noisy < P
```

则复用上一公开结果；否则：

```text
O_t(i,j) = D_t(i,j) + Laplace(0, 1/beta_t(i,j))
```

只有真正发布时才记录发布预算消耗，跳过发布不会消耗该次发布预算。

## 特点

- 连续时间窗口隐私预算控制；
- 局部 `m×m` 空间子流；
- 评估预算 / 发布预算分离；
- 根据历史预算消耗动态分配当前预算；
- 发布决策本身进行差分隐私扰动；
- 支持 `sliding` 滑动空间窗口与 `partition` 不相交分块；
- 内置发布预算审计；
- 支持 GPS CSV 转换为时空计数网格；
- 支持 `epsilon / alpha / m` 参数扫描；
- 固定随机种子可复现实验。

## 安装

```bash
git clone <your-repository-url>
cd STARB-DP
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS：

```bash
source .venv/bin/activate
```

## 运行

```bash
python scripts/demo_synthetic.py
python scripts/run_experiment.py --config configs/default.yaml
pytest -q
```

参数扫描：

```bash
python scripts/sweep_epsilon.py
python scripts/sweep_alpha.py
python scripts/sweep_m.py
```

## GPS 数据转换

CSV 推荐字段：

```csv
user_id,timestamp,latitude,longitude
u001,2026-01-01T08:00:00,39.9042,116.4074
```

执行：

```bash
python scripts/preprocess_gps.py \
  --input data/raw/trajectory.csv \
  --output data/processed/stream.npz \
  --time-bin 10min \
  --cell-size-m 200
```

## 配置

```yaml
epsilon: 1.0
alpha: 120
spatial_order: 15
substream_mode: sliding
clip_nonnegative: true
seed: 42
minimum_beta: 1.0e-9
```

## 输出

标准实验会生成：

- `released.npy`
- `release_mask.npy`
- `beta_spent.npy`
- `mae_by_time.csv`
- `summary.json`

本仓库重点提供完整、可运行、可扩展、可审计的工程实现，不对算法原创性作声明。
