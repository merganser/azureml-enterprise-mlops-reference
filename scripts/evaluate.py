import argparse

from mlops_reference.evaluate import evaluate_model

parser = argparse.ArgumentParser()
parser.add_argument("--model-dir", required=True)
parser.add_argument("--test-csv", required=True)
parser.add_argument("--metrics-dir", required=True)
args = parser.parse_args()
evaluate_model(args.model_dir, args.test_csv, args.metrics_dir)
