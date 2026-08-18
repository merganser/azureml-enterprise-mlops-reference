import argparse

from mlops_reference.preprocess import prepare

parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", required=True)
parser.add_argument("--test-size", type=float, default=0.2)
args = parser.parse_args()
prepare(args.output_dir, args.test_size)
