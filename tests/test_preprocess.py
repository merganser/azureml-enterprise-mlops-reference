import pandas as pd

from mlops_reference.preprocess import prepare


def test_prepare_is_deterministic_and_stratified(tmp_path):
    train_path, test_path = prepare(str(tmp_path))
    train, test = pd.read_csv(train_path), pd.read_csv(test_path)
    assert len(train) == 120
    assert len(test) == 30
    assert set(train["label"]) == {0, 1, 2}
