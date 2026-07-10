from importlib.metadata import version

import src
import tools


def test_runtime_versions_match_installed_distribution():
    installed = version("entaengelment")

    assert src.__version__ == installed
    assert tools.__version__ == installed
