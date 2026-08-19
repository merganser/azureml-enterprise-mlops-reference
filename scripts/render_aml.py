import argparse
import re
from pathlib import Path


def render(source: str, output: str, replacements: list[str]) -> None:
    content = Path(source).read_text(encoding="utf-8")
    for item in replacements:
        key, value = item.split("=", 1)
        content = content.replace(f"${{{key}}}", value)
    unresolved = re.findall(r"\$\{([A-Z][A-Z0-9_]*)\}", content)
    if unresolved:
        raise SystemExit(f"Unresolved template values: {', '.join(unresolved)}")
    Path(output).write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("values", nargs="*")
    args = parser.parse_args()
    render(args.source, args.output, args.values)


if __name__ == "__main__":
    main()
