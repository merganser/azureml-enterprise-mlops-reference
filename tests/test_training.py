import json

import pandas as pd

from mlops_reference.evaluate import evaluate_model
from mlops_reference.train import train_model


class PredictZeros:
    def predict(self, features):
        return [0] * len(features)


def test_train_model_saves_mlflow_model_and_metadata(tmp_path, monkeypatch):
    train_csv = tmp_path / "train.csv"
    model_dir = tmp_path / "model"
    pd.DataFrame(
        {"feature_a": [0, 1, 0, 1], "feature_b": [1, 0, 0, 1], "label": [0, 1, 0, 1]}
    ).to_csv(train_csv, index=False)
    saved = {}
    monkeypatch.setattr(
        "mlops_reference.train.mlflow.sklearn.save_model",
        lambda model, path: saved.update(model=model, path=path),
    )
    result = train_model(str(train_csv), str(model_dir), seed=7)
    metadata = json.loads((model_dir / "training-metadata.json").read_text(encoding="utf-8"))
    assert result == model_dir
    assert saved["path"] == model_dir
    assert metadata == {"rows": 4, "seed": 7}


def test_evaluate_model_writes_accuracy(tmp_path, monkeypatch):
    test_csv = tmp_path / "test.csv"
    metrics_dir = tmp_path / "metrics"
    pd.DataFrame({"feature": [1, 2, 3], "label": [0, 0, 1]}).to_csv(test_csv, index=False)
    monkeypatch.setattr(
        "mlops_reference.evaluate.mlflow.sklearn.load_model", lambda path: PredictZeros()
    )
    accuracy = evaluate_model("model", str(test_csv), str(metrics_dir))
    metrics = json.loads((metrics_dir / "metrics.json").read_text(encoding="utf-8"))
    assert accuracy == 2 / 3
    assert metrics == {"accuracy": 2 / 3}
