import json
from pathlib import Path

import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_model(train_csv: str, model_dir: str, seed: int = 42) -> Path:
    frame = pd.read_csv(train_csv)
    model = RandomForestClassifier(n_estimators=100, random_state=seed)
    model.fit(frame.drop(columns="label"), frame["label"])
    output = Path(model_dir)
    output.mkdir(parents=True, exist_ok=True)
    mlflow.sklearn.save_model(model, output)
    (output / "training-metadata.json").write_text(
        json.dumps({"rows": len(frame), "seed": seed}), encoding="utf-8"
    )
    return output
