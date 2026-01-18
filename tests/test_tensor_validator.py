"""Tests for tensor mapping validator."""

from mapping.tensor_validator import validate_tensor_mapping


def test_tensor_mapping_valid():
    res = validate_tensor_mapping("mapping/TENSOR_MAPPING.yml")
    assert res.ok, f"Errors: {res.errors}\nWarnings: {res.warnings}"


def test_tensor_mapping_missing_metadata(tmp_path):
    p = tmp_path / "bad.yml"
    p.write_text("concepts: []\n", encoding="utf-8")
    res = validate_tensor_mapping(str(p))
    assert not res.ok
