from pathlib import Path
import argparse
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starbdp import STARBDP
from starbdp.io import load_config, load_stream, save_result

def synthetic(seed=0, shape=(120, 20, 20)):
    rng = np.random.default_rng(seed)
    x = rng.poisson(3.0, size=shape).astype(float)
    x[30:60, 4:10, 4:10] += 8
    x[75:100, 12:17, 2:8] += 12
    return x

parser = argparse.ArgumentParser()
parser.add_argument("--config", default=str(ROOT / "configs/default.yaml"))
parser.add_argument("--input", default=None)
parser.add_argument("--output", default=str(ROOT / "outputs/run"))
args = parser.parse_args()

cfg = load_config(args.config)
stream = load_stream(args.input) if args.input else synthetic()
result = STARBDP(cfg).fit_transform(stream)
save_result(args.output, stream, result)

print("metrics:", result.metrics)
print("audit:", result.audit)
print("saved:", args.output)
