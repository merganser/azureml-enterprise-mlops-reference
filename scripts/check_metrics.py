import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("metrics")
parser.add_argument("--minimum-accuracy", type=float, default=0.9)
args = parser.parse_args()
accuracy = float(json.loads(Path(args.metrics).read_text(encoding="utf-8"))["accuracy"])
if accuracy < args.minimum_accuracy:
    raise SystemExit(f"Quality gate failed: accuracy {accuracy:.4f} < {args.minimum_accuracy:.4f}")
print(f"Quality gate passed: accuracy {accuracy:.4f}")
