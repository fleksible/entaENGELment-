import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import src
import tools


def _project_version() -> str:
    try:
        return version("entaengelment")
    except PackageNotFoundError:
        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        content = pyproject.read_text(encoding="utf-8")
        project_section = content.split("[project]", maxsplit=1)[1]
        match = re.search(r'^version\s*=\s*"([^"]+)"', project_section, re.MULTILINE)
        assert match is not None, "[project].version missing from pyproject.toml"
        return match.group(1)


def test_runtime_versions_match_project_metadata():
    expected = _project_version()

    assert src.__version__ == expected
    assert tools.__version__ == expected
