import json

from mlops_reference import score


class FakeModel:
    def predict(self, frame):
        return [1] * len(frame)


def test_run_returns_json_safe_predictions():
    score.model = FakeModel()
    result = score.run(json.dumps({"input_data": [{"a": 1}, {"a": 2}]}))
    assert result == {"predictions": [1, 1]}


def test_init_loads_model_from_azureml_directory(monkeypatch):
    fake_model = FakeModel()
    monkeypatch.setenv("AZUREML_MODEL_DIR", "/models/iris")
    monkeypatch.setattr(score.mlflow.pyfunc, "load_model", lambda path: fake_model)
    score.init()
    assert score.model is fake_model
