#!/usr/bin/env python3
"""Reproduzierbarer Mess-Harness für Befund B9 (Checkup 2026-10-28).

Misst, wie ``compute_hessian_numerical`` + ``classify_stability`` +
``stability_gate`` eine Funktion mit bekannter (analytischer) Hessian
klassifizieren, wenn nur ein additiver Offset C variiert. Mathematisch ändert
f -> f + C die Hessian nicht; jede Klassenänderung ist numerisch bedingt.

Aufruf aus dem Repo-Root (misst den ausgecheckten Code):

    python docs/audit/harness/b9_hessian_offset_matrix.py

Ausgabe: JSON mit Umgebung, Parametern und Zählungen je Testmatrix.
Die Zahlen gelten nur für diese Matrix und diesen Code-Stand.
"""

from __future__ import annotations

import itertools
import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.stability_guard import stability_gate  # noqa: E402
from src.stability.hessian_void import (  # noqa: E402
    classify_stability,
    compute_hessian_numerical,
)

EPS = 1e-5  # Default-Schrittweite von compute_hessian_numerical
THRESHOLD = 1e-6  # Default-Toleranz von classify_stability
GRID_AXIS = [-3.0, -1.5, -0.7, 0.0, 0.3, 1.0, 2.2]
OFFSETS = [0.0, 1.0, 10.0, 100.0, 1e3, 1e4]

# Analytische Referenzen: Hessian ist konstant und offset-unabhängig.
FUNCTIONS = {
    "flat: x^2 + 1e-8*y^2 + C (H=diag(2, 2e-8), Referenz FLAT)": (
        lambda q, c: q[0] ** 2 + 1e-8 * q[1] ** 2 + c,
        "FLAT",
    ),
    "stable: x^2 + y^2 + C (H=diag(2, 2), Referenz STABLE)": (
        lambda q, c: q[0] ** 2 + q[1] ** 2 + c,
        "STABLE",
    ),
    "saddle: x^2 - y^2 + C (H=diag(2, -2), Referenz UNSTABLE)": (
        lambda q, c: q[0] ** 2 - q[1] ** 2 + c,
        "UNSTABLE",
    ),
}


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _measure(func, point: np.ndarray, offset: float) -> tuple[str, bool, bool]:
    H = compute_hessian_numerical(lambda q: func(q, offset), point, eps=EPS)
    status, _ = classify_stability(H, threshold=THRESHOLD)
    allow_without_consent, _ = stability_gate(H, consent_available=False)
    allow_with_consent, _ = stability_gate(H, consent_available=True)
    return status, allow_without_consent, allow_with_consent


def _summarize(cases, func, reference: str) -> dict:
    statuses: Counter[str] = Counter()
    by_offset: dict[float, Counter[str]] = {}
    allow_without = 0
    allow_with = 0
    for point, offset in cases:
        status, a_without, a_with = _measure(func, np.asarray(point, dtype=float), offset)
        statuses[status] += 1
        by_offset.setdefault(offset, Counter())[status] += 1
        allow_without += int(a_without)
        allow_with += int(a_with)
    summary = {
        "reference_class": reference,
        "n_cases": len(cases),
        "classified": dict(sorted(statuses.items())),
        "misclassified": len(cases) - statuses[reference],
        "gate_allow_without_consent": allow_without,
        "gate_allow_with_consent": allow_with,
    }
    if len(by_offset) <= len(OFFSETS):
        summary["classified_by_offset"] = {
            f"{offset:g}": dict(sorted(counts.items()))
            for offset, counts in sorted(by_offset.items())
        }
    return summary


def main() -> None:
    grid_cases = [
        ((x, y), c)
        for (x, y), c in itertools.product(itertools.product(GRID_AXIS, GRID_AXIS), OFFSETS)
    ]
    rng = np.random.default_rng(0)
    sweep_cases = []
    for _ in range(400):
        point = rng.uniform(-3, 3, 2)
        offset = float(10 ** rng.uniform(0, 4))
        sweep_cases.append((tuple(point), offset))

    flat_func = FUNCTIONS["flat: x^2 + 1e-8*y^2 + C (H=diag(2, 2e-8), Referenz FLAT)"][0]
    single_cases = {}
    for point, offset in [
        ((1.0, 1.0), 0.0),
        ((1.0, 1.0), 10.0),
        ((0.3, 0.7), 0.0),
        ((0.3, 0.7), 10.0),
    ]:
        status, a_without, a_with = _measure(flat_func, np.asarray(point), offset)
        single_cases[f"flat at {point}, C={offset:g}"] = {
            "status": status,
            "gate_allow_without_consent": a_without,
            "gate_allow_with_consent": a_with,
        }

    result = {
        "harness": "docs/audit/harness/b9_hessian_offset_matrix.py",
        "git_commit": _git_commit(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "parameters": {
            "eps (finite-difference step)": EPS,
            "threshold (classify_stability)": THRESHOLD,
            "grid_axis": GRID_AXIS,
            "offsets": OFFSETS,
            "sweep": "400 Fälle, numpy default_rng(0): Punkt ~ U(-3,3)^2, C = 10^U(0,4)",
        },
        "single_cases": single_cases,
        "grid_7x7_points_x_6_offsets": {
            name: _summarize(grid_cases, f, ref) for name, (f, ref) in FUNCTIONS.items()
        },
        "seeded_sweep_400": {
            name: _summarize(sweep_cases, f, ref) for name, (f, ref) in FUNCTIONS.items()
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
