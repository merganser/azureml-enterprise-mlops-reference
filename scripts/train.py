import argparse

from mlops_reference.train import train_model

parser = argparse.ArgumentParser()
parser.add_argument("--train-csv", required=True)
parser.add_argument("--model-dir", required=True)
args = parser.parse_args()
train_model(args.train_csv, args.model_dir)
