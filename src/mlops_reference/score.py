import json
import os

import mlflow
import pandas as pd


def load_model(model_path: str):
    return mlflow.pyfunc.load_model(model_path)


def init() -> None:
    global model
    model = load_model(os.environ["AZUREML_MODEL_DIR"])


def run(raw_data: str) -> dict:
    payload = json.loads(raw_data)
    predictions = model.predict(pd.DataFrame(payload["input_data"]))
    values = predictions.tolist() if hasattr(predictions, "tolist") else list(predictions)
    return {"predictions": values}
