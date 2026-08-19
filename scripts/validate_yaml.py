"""Render representative Azure ML templates and validate every YAML document."""

from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from render_aml import render

ROOT = Path(__file__).resolve().parents[1]


def validate_yaml(path: Path) -> None:
    with path.open(encoding="utf-8") as stream:
        documents = list(yaml.safe_load_all(stream))
    if not documents or any(document is None for document in documents):
        raise ValueError(f"Empty YAML document: {path.relative_to(ROOT)}")


def main() -> None:
    values = [
        "ASSET_VERSION=1.0.123",
        "COMPUTE_NAME=cpu-cluster",
        "CONTAINER_IMAGE=example.azurecr.io/mlops:abc123",
        "ENDPOINT_NAME=iris-test",
        "ENVIRONMENT_NAME=enterprise-mlops-runtime",
        "ENVIRONMENT_VERSION=1.0.123",
        "MODEL_NAME=iris-classifier",
        "MODEL_VERSION=1.0.123",
        "REGISTRY_NAME=example-registry",
    ]
    yaml_files = sorted((*ROOT.glob("**/*.yml"), *ROOT.glob("**/*.yaml")))
    with TemporaryDirectory() as temporary_directory:
        temporary = Path(temporary_directory)
        for path in yaml_files:
            content = path.read_text(encoding="utf-8")
            if "${" in content and "${{" not in content.replace("${{", ""):
                destination = temporary / path.name
                render(str(path), str(destination), values)
                validate_yaml(destination)
            else:
                validate_yaml(path)
    print(f"Validated {len(yaml_files)} YAML files")


if __name__ == "__main__":
    main()
