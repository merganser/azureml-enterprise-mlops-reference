import json
from pathlib import Path

import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score


def load_model(model_path: str):
    return mlflow.sklearn.load_model(model_path)


def evaluate_model(model_dir: str, test_csv: str, metrics_dir: str) -> float:
    frame = pd.read_csv(test_csv)
    model = load_model(model_dir)
    accuracy = float(accuracy_score(frame["label"], model.predict(frame.drop(columns="label"))))
    output = Path(metrics_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "metrics.json").write_text(json.dumps({"accuracy": accuracy}), encoding="utf-8")
    return accuracy
