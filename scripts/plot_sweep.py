from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--csv", required=True)
parser.add_argument("--x", required=True)
parser.add_argument("--y", default="mae")
parser.add_argument("--output", default=None)
args = parser.parse_args()

df = pd.read_csv(args.csv)
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot(df[args.x], df[args.y], marker="o")
ax.set_xlabel(args.x)
ax.set_ylabel(args.y.upper())
ax.grid(True, alpha=0.25)
fig.tight_layout()

out = args.output or str(Path(args.csv).with_suffix(".png"))
fig.savefig(out, dpi=220)
print(out)
