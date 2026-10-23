from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.thin_film_reflectance import CASES, build_reference_report, reflectance

REFERENCE = json.loads(
    (
        Path(__file__).resolve().parents[2]
        / "docs/validation/fixtures/thin_film_reference_v0_1.json"
    ).read_text(encoding="utf-8")
)


@pytest.mark.parametrize("name", ["A", "B", "C"])
@pytest.mark.parametrize("wavelength", [450, 550, 650])
def test_original_inline_reference_values(name: str, wavelength: int) -> None:
    expected = REFERENCE["cases"][name]["reflectance"][str(wavelength)]
    assert reflectance(wavelength, *CASES[name]) == pytest.approx(expected, rel=1e-12, abs=1e-15)


def test_environment_change_does_not_require_changing_the_film() -> None:
    assert CASES["A"][1:] == CASES["B"][1:]
    assert reflectance(550, *CASES["A"]) > 20 * reflectance(550, *CASES["B"])


def test_equal_optical_thickness_does_not_imply_equal_reflectance() -> None:
    a, c = CASES["A"], CASES["C"]
    assert a[1] * a[3] == c[1] * c[3] == 300
    assert abs(reflectance(550, *a) - reflectance(550, *c)) > 0.001


def test_zero_thickness_matches_the_direct_interface_across_the_spectrum() -> None:
    direct = ((1.0 - 1.333) / (1.0 + 1.333)) ** 2
    for wavelength in range(400, 701):
        assert reflectance(wavelength, 1, 1.5, 1.333, 0) == pytest.approx(direct, abs=1e-14)


def test_matching_indices_remove_reflection_across_the_spectrum() -> None:
    for wavelength in range(400, 701):
        assert reflectance(wavelength, 1.333, 1.333, 1.333, 200) == 0


def test_quarter_wave_matching_layer_has_zero_reflection_at_its_design_wavelength() -> None:
    wavelength = 550
    n1 = 1.5
    # Independent analytic control: n1^2 = n0*n2, d = wavelength/(4*n1).
    assert reflectance(wavelength, 1, n1, 2.25, wavelength / (4 * n1)) < 1e-24


def test_reference_spectra_stay_within_the_lossless_model_bounds() -> None:
    for wavelength in range(400, 701):
        for parameters in CASES.values():
            assert 0 <= reflectance(wavelength, *parameters) <= 1


@pytest.mark.parametrize(
    "parameters",
    [
        (0, 1, 1.5, 1.333, 200),
        (float("nan"), 1, 1.5, 1.333, 200),
        (550, 0, 1.5, 1.333, 200),
        (550, 1, float("inf"), 1.333, 200),
        (550, 1, 1.5, 1.333, -1),
        (550, 1, 1.5, 1.333, float("nan")),
    ],
)
def test_invalid_model_parameters_are_rejected(
    parameters: tuple[float, float, float, float, float],
) -> None:
    with pytest.raises(ValueError):
        reflectance(*parameters)


def test_deterministic_report_preserves_reference_values_and_model_status() -> None:
    report = build_reference_report()
    for key in ("schemaVersion", "claimLayer", "sourceCodeSHA256", "assumptions"):
        assert report[key] == REFERENCE[key]
    assert report["claimLayer"] == "MODEL"
    for name in CASES:
        assert report["cases"][name]["parameters"] == REFERENCE["cases"][name]["parameters"]
        assert report["cases"][name]["reflectance"] == pytest.approx(
            REFERENCE["cases"][name]["reflectance"], rel=1e-12, abs=1e-15
        )
