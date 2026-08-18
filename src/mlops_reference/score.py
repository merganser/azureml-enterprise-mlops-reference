import json
import os

import mlflow
import pandas as pd


def init() -> None:
    global model
    model = mlflow.pyfunc.load_model(os.environ["AZUREML_MODEL_DIR"])


def run(raw_data: str) -> dict:
    payload = json.loads(raw_data)
    predictions = model.predict(pd.DataFrame(payload["input_data"]))
    return {"predictions": predictions.tolist()}
