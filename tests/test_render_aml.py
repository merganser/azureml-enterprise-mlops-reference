from pathlib import Path

import pytest

from scripts.render_aml import render


def test_render_replaces_named_values_and_preserves_azure_expressions(tmp_path):
    source = tmp_path / "source.yml"
    output = tmp_path / "output.yml"
    source.write_text("version: ${VERSION}\ninput: ${{parent.inputs.data}}\n", encoding="utf-8")
    render(str(source), str(output), ["VERSION=42"])
    assert output.read_text(encoding="utf-8") == "version: 42\ninput: ${{parent.inputs.data}}\n"


def test_render_rejects_missing_values(tmp_path):
    source = tmp_path / "source.yml"
    source.write_text("version: ${VERSION}\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="VERSION"):
        render(str(source), str(tmp_path / "output.yml"), [])
