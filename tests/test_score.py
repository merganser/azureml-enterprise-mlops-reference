import json

import mlops_reference.score as score


class FakeModel:
    def predict(self, frame):
        return [1] * len(frame)


def test_run_returns_json_safe_predictions():
    score.model = FakeModel()
    result = score.run(json.dumps({"input_data": [{"a": 1}, {"a": 2}]}))
    assert result == {"predictions": [1, 1]}
