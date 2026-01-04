"""Toy Dataset (Option B) — synthetische Resonanzsignale.

Ziel:
- sichere (in-silico) Demo-Daten generieren
- Core-Metriken aus src/core/metrics.py aufrufen

Hinweis:
MI/FD sind aktuell Minimal-Stubs; dieses Script ist ein "Proof of Wiring".
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from src.core.metrics import eci, fd, mi, pf, plv


def _wrap_pi(x: float) -> float:
    """Wrap angle to [-pi, pi]."""
    return ((x + math.pi) % (2.0 * math.pi)) - math.pi


@dataclass
class ToyDataset:
    t: list[float]
    a: list[float]
    b: list[float]
    phases: list[float]
    consent_signal: list[float]


def generate_mycel_signals(n: int = 256, seed: int = 42, coupling: float = 0.35) -> ToyDataset:
    """Generiert zwei gekoppelte Signale (a,b) mit leichter Drift.

    Args:
        n: Anzahl Samples
        seed: deterministischer Seed
        coupling: 0..1 Kopplungsstärke zwischen a und b

    Returns:
        ToyDataset
    """
    rng = random.Random(seed)
    t = [i / max(n - 1, 1) for i in range(n)]

    a: list[float] = []
    b: list[float] = []
    phases: list[float] = []
    consent_signal: list[float] = []

    # Two drifting oscillators + weak Kuramoto-style coupling
    phase_a = 0.0
    phase_b = 0.0
    drift = 0.02
    mismatch = 2.0  # b runs faster -> without coupling the difference drifts away
    phase_noise = 0.02
    coupling_scale = 0.02  # scales the effect of coupling on phase lock

    prev_a = 0.0
    prev_b = 0.0

    for _i, ti in enumerate(t):
        # Phase evolution with Kuramoto-style coupling
        phase_a += drift + (rng.random() - 0.5) * phase_noise
        phase_b += (drift * mismatch) + (rng.random() - 0.5) * phase_noise
        phase_b += coupling * coupling_scale * math.sin(phase_a - phase_b)

        # Store PHASE DIFFERENCE (wrapped) -> PLV now reflects coupling
        delta = _wrap_pi(phase_a - phase_b)
        phases.append(delta)

        base_a = math.sin(2.0 * math.pi * (ti * 3.0) + phase_a)
        base_b = math.sin(2.0 * math.pi * (ti * 3.0) + phase_b)
        noise_a = (rng.random() - 0.5) * 0.2
        noise_b = (rng.random() - 0.5) * 0.2

        # a is base_a + noise (with mild inertia)
        cur_a = 0.75 * prev_a + 0.25 * (base_a + noise_a)
        # b is partially coupled to a + its own noise
        cur_b = 0.70 * prev_b + 0.30 * (coupling * cur_a + (1.0 - coupling) * base_b + noise_b)

        a.append(cur_a)
        b.append(cur_b)

        # consent proxy signal: higher when coupling higher (still bounded)
        consent_signal.append(min(max(coupling + (rng.random() - 0.5) * 0.1, 0.0), 1.0))

        prev_a, prev_b = cur_a, cur_b

    return ToyDataset(t=t, a=a, b=b, phases=phases, consent_signal=consent_signal)


def compute_demo_metrics(ds: ToyDataset) -> dict[str, float]:
    """Runs Core-5 metrics on toy data."""
    return {
        "ECI": eci(ds.consent_signal),
        "PLV": plv(ds.phases),
        "MI": mi(ds.a, ds.b),
        "FD": fd(ds.a),
        "PF": pf(ds.a),
    }


def main() -> None:
    ds = generate_mycel_signals()
    m = compute_demo_metrics(ds)
    for k, v in m.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
