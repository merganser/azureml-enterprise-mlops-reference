import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", default="promotion-manifest.json")
    args = parser.parse_args()
    digest = hashlib.sha256(Path("pyproject.toml").read_bytes()).hexdigest()
    manifest = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_commit": args.commit,
        "asset_version": args.version,
        "container_image": args.image,
        "source_digest": digest,
        "environment": {"name": "enterprise-mlops-runtime", "version": args.version},
        "components": [
            {"name": name, "version": args.version}
            for name in ("preprocess", "train", "evaluate")
        ],
    }
    Path(args.output).write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
