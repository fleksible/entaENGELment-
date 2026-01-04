"""
src/core/eci.py
Simple Ethical Consent Index (ECI) implementation with bootstrap and permutation helpers.

ECI = w1*likert_norm + w2*behavior_proxy + w3*physio_proxy_norm
Weights must sum to 1 (function normalizes otherwise).
"""

import json
import os
from typing import Optional

import numpy as np


def normalize_weights(w: dict[str, float]) -> dict[str, float]:
    s = sum(w.values())
    if s == 0:
        raise ValueError("Sum of weights must be > 0")
    return {k: float(v) / s for k, v in w.items()}


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def compute_eci(
    likert_norm: float,
    behavior_proxy: float,
    physio_proxy: Optional[float],
    weights: Optional[dict[str, float]] = None,
) -> float:
    """
    Compute ECI in 0..1.
    likert_norm, behavior_proxy, physio_proxy expected in 0..1 (physio may be None).
    weights keys: w_likert, w_behavior, w_physio
    If physio_proxy is None, its weight is redistributed proportionally to the other two.
    """
    if weights is None:
        weights = {"w_likert": 0.5, "w_behavior": 0.4, "w_physio": 0.1}
    weights = normalize_weights(weights)

    lik = clamp01(likert_norm)
    beh = clamp01(behavior_proxy)
    phys = clamp01(physio_proxy) if physio_proxy is not None else None

    if phys is None:
        # redistribute w_physio proportionally to the other two
        total = weights["w_likert"] + weights["w_behavior"]
        if total <= 0:
            raise ValueError("Invalid weight configuration for redistribution")
        w_l = weights["w_likert"] / total
        w_b = weights["w_behavior"] / total
        eci = w_l * lik + w_b * beh
    else:
        eci = weights["w_likert"] * lik + weights["w_behavior"] * beh + weights["w_physio"] * phys

    return clamp01(eci)


# -----------------------
# Simple bootstrap & permutation helpers for validation
# -----------------------
def bootstrap_ci(
    values: list[float], n_bootstrap: int = 1000, ci: float = 0.95
) -> tuple[float, float]:
    arr = np.array(values)
    n = len(arr)
    if n == 0:
        return (0.0, 0.0)
    means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(arr, size=n, replace=True)
        means.append(sample.mean())
    lower = np.percentile(means, (1 - ci) / 2 * 100)
    upper = np.percentile(means, (1 + ci) / 2 * 100)
    return float(lower), float(upper)


def permutation_test(observed: float, samples: list[float], n_perm: int = 1000) -> float:
    arr = np.array(samples)
    count = 0
    for _ in range(n_perm):
        perm = np.random.permutation(arr)
        if perm.mean() >= observed:
            count += 1
    p = (count + 1) / (n_perm + 1)
    return float(p)


# -----------------------
# CLI helpers (minimal)
# -----------------------
def save_specified_eci(path: str, eci_obj: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(eci_obj, f, indent=2)


if __name__ == "__main__":
    # quick smoke
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--likert", type=float, default=6.0, help="Likert 1..7")
    parser.add_argument("--behavior", type=float, default=0.5, help="Behavior proxy 0..1")
    parser.add_argument("--physio", type=float, default=None, help="Physio proxy 0..1")
    parser.add_argument("--out", type=str, default="validation/eci_example.json")
    args = parser.parse_args()

    lik_norm = (args.likert - 1) / 6.0
    eci_val = compute_eci(lik_norm, args.behavior, args.physio)
    obj = {
        "version": "0.1",
        "eci": {
            "likert_norm": lik_norm,
            "behavior_proxy": args.behavior,
            "physio_proxy": args.physio,
            "weights": {"w_likert": 0.5, "w_behavior": 0.4, "w_physio": 0.1},
            "eci_value": eci_val,
        },
    }
    save_specified_eci(args.out, obj)
    print(f"ECI saved to {args.out} -> {eci_val:.4f}")
