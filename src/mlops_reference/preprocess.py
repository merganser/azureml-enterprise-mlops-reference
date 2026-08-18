from pathlib import Path

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def prepare(output_dir: str, test_size: float = 0.2, seed: int = 42) -> tuple[Path, Path]:
    """Create deterministic train/test CSV files from a public sample dataset."""
    iris = load_iris(as_frame=True)
    frame = iris.frame.rename(columns={"target": "label"})
    train, test = train_test_split(
        frame, test_size=test_size, random_state=seed, stratify=frame["label"]
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    train_path, test_path = destination / "train.csv", destination / "test.csv"
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    return train_path, test_path
