#!/usr/bin/env python3
"""[FACT] Reproduziert einen deklarierten Einzelschicht-Modellfall.

[RISK] Senkrechter Einfall, reale konstante Indizes und ideale Grenzflächen.
Keine Absorption, Dispersion, Farbwahrnehmung oder Materialmessung.
Vertrag: docs/annex/OPTISCHER_MODELLFALL_v0_1.md.
"""

from __future__ import annotations

import cmath
import json
import math

SOURCE_CODE_SHA256 = "54f000bb2e42b9f52dffaeff07d3acf71dc55721d4c4a3f03ef8e01417d1ac3d"
CASES: dict[str, tuple[float, float, float, float]] = {
    "A": (1.0, 1.5, 1.333, 200.0),
    "B": (1.333, 1.5, 1.333, 200.0),
    "C": (1.0, 1.6, 1.333, 187.5),
}
WAVELENGTHS_NM = (450, 550, 650)
ASSUMPTIONS = [
    "normal incidence",
    "one homogeneous film and ideal plane interfaces",
    "real positive refractive indices",
    "no absorption or dispersion",
    "wavelength and thickness in nanometres",
    "synthetic indices, no measured material",
]


def reflectance(wavelength_nm: float, n0: float, n1: float, n2: float, d_nm: float) -> float:
    """Reflexionsanteil im deklarierten Modell; unzulässige Werte ergeben ValueError."""
    if not all(math.isfinite(x) for x in (wavelength_nm, n0, n1, n2, d_nm)):
        raise ValueError("model parameters must be finite real numbers")
    if wavelength_nm <= 0 or min(n0, n1, n2) <= 0 or d_nm < 0:
        raise ValueError("wavelength and indices must be positive; thickness non-negative")

    r01 = (n0 - n1) / (n0 + n1)
    r12 = (n1 - n2) / (n1 + n2)
    z = cmath.exp(-4j * math.pi * n1 * d_nm / wavelength_nm)
    r = (r01 + r12 * z) / (1 + r01 * r12 * z)
    return abs(r) ** 2


def build_reference_report() -> dict[str, object]:
    """Deterministische Modellparameter und die neun Referenzwerte."""
    return {
        "schemaVersion": "thin-film-model-v0.1",
        "claimLayer": "MODEL",
        "sourceCodeSHA256": SOURCE_CODE_SHA256,
        "assumptions": ASSUMPTIONS,
        "cases": {
            name: {
                "parameters": dict(zip(("n0", "n1", "n2", "d_nm"), parameters, strict=True)),
                "reflectance": {
                    str(wavelength): reflectance(wavelength, *parameters)
                    for wavelength in WAVELENGTHS_NM
                },
            }
            for name, parameters in CASES.items()
        },
    }


def main() -> None:
    print(json.dumps(build_reference_report(), allow_nan=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
