# 数据准备

推荐 GPS CSV：

```csv
user_id,timestamp,latitude,longitude
```

执行：

```bash
python scripts/preprocess_gps.py \
  --input data/raw/trajectory.csv \
  --output data/processed/stream.npz \
  --time-bin 10min \
  --cell-size-m 200
```

转换流程：

1. 时间戳离散化；
2. 经纬度近似转换到局部米制坐标；
3. 以 `cell-size-m` 划分网格；
4. 对每个时间片和网格统计记录数量；
5. 输出 `[T,H,W]` 计数张量。
