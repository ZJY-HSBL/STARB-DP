from pathlib import Path
import argparse, json, sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starbdp.preprocess import gps_csv_to_count_stream

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--time-bin", default="10min")
parser.add_argument("--cell-size-m", type=float, default=200.0)
parser.add_argument("--lat-col", default="latitude")
parser.add_argument("--lon-col", default="longitude")
parser.add_argument("--time-col", default="timestamp")
args = parser.parse_args()

df = pd.read_csv(args.input)
stream, meta = gps_csv_to_count_stream(
    df, args.time_bin, args.cell_size_m,
    args.lat_col, args.lon_col, args.time_col
)

out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
np.savez_compressed(out, stream=stream)

with open(out.with_suffix(".json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("saved:", out)
print("shape:", stream.shape)
