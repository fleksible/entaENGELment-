"""Counterfixtures for missing, changed, stale and duplicated SBOM evidence."""

import copy

import pytest

from tools.python_lock import verify_sbom


def evidence():
    packages = {"entaengelment": "0.1.0", "pyyaml": "6.0.3"}
    receipt = {"lock_digest": "current", "packages": packages}
    installed = {"packages": packages.copy()}
    bom = {
        "metadata": {"component": {"name": "entaengelment", "version": "0.1.0"}},
        "components": [{"name": "PyYAML", "version": "6.0.3"}],
    }
    return bom, receipt, installed


def test_sbom_accepts_project_metadata_and_normalizes_package_names():
    verify_sbom(*evidence(), "current")


def test_stale_lock_receipt_is_rejected():
    with pytest.raises(ValueError, match="current uv.lock"):
        verify_sbom(*evidence(), "new-lock")


def test_installation_change_after_receipt_is_rejected():
    bom, receipt, installed = evidence()
    installed["packages"]["pyyaml"] = "6.0.2"
    with pytest.raises(ValueError, match="environment drifted"):
        verify_sbom(bom, receipt, installed, "current")


@pytest.mark.parametrize("mutation", ["missing", "extra", "version", "duplicate", "unversioned"])
def test_sbom_mismatch_fails_closed(mutation):
    bom, receipt, installed = evidence()
    if mutation == "missing":
        bom["components"] = []
    elif mutation == "extra":
        bom["components"].append({"name": "unlocked", "version": "1"})
    elif mutation == "version":
        bom["components"][0]["version"] = "6.0.2"
    elif mutation == "duplicate":
        bom["components"].append(copy.deepcopy(bom["components"][0]))
    else:
        del bom["components"][0]["version"]
    with pytest.raises(ValueError):
        verify_sbom(bom, receipt, installed, "current")
