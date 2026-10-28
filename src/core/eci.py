"""
src/core/eci.py
Simple Ethical Consent Index (ECI) implementation with a bootstrap helper.

ECI = w1*likert_norm + w2*behavior_proxy + w3*physio_proxy_norm
Weights must sum to 1 (function normalizes otherwise).

``permutation_test`` is deliberately disabled (raises ``NotImplementedError``)
until a statistical test design is specified; see its docstring.
"""

import json
import math
import numbers
import os

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
    physio_proxy: float | None,
    weights: dict[str, float] | None = None,
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
    values: list[float],
    n_bootstrap: int = 1000,
    ci: float = 0.95,
    seed: int | None = None,
) -> tuple[float, float]:
    """Percentile bootstrap confidence interval of the mean.

    Fail-closed: empty, non-1-D or non-finite data, ``n_bootstrap < 1`` and a
    confidence level outside the open interval (0, 1) raise ``ValueError``
    instead of returning a seemingly valid interval. (Earlier versions returned
    ``(0.0, 0.0)`` for empty data.) Constant finite data yield a degenerate
    interval ``(c, c)``.

    Args:
        values: 1-D sequence of finite observations.
        n_bootstrap: Number of bootstrap resamples (integer >= 1).
        ci: Confidence level in (0, 1).
        seed: Optional seed for a local ``numpy.random.Generator``; with the same
            seed the result is reproducible. The global NumPy RNG is not used.

    Returns:
        (lower, upper) percentile bounds of the resampled means.
    """
    if isinstance(n_bootstrap, bool) or not isinstance(n_bootstrap, numbers.Integral):
        raise ValueError(f"n_bootstrap must be an integer, got {n_bootstrap!r}")
    if n_bootstrap < 1:
        raise ValueError(f"n_bootstrap must be >= 1, got {n_bootstrap}")
    if (
        isinstance(ci, bool)
        or not isinstance(ci, numbers.Real)
        or not math.isfinite(ci)
        or not 0.0 < ci < 1.0
    ):
        raise ValueError(f"ci must be a number in the open interval (0, 1), got {ci!r}")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, numbers.Integral)):
        raise ValueError(f"seed must be an integer or None, got {seed!r}")
    try:
        arr = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"values must be numeric: {exc}") from exc
    if arr.ndim != 1 or arr.size == 0:
        raise ValueError("values must be a non-empty 1-D sequence")
    if not np.all(np.isfinite(arr)):
        raise ValueError("values must be finite (no NaN or infinity)")

    rng = np.random.default_rng(seed)
    n = arr.size
    # Positive scaling commutes with means and percentiles. Keep both the
    # resampled sum and percentile interpolation away from float overflow.
    scale = float(np.max(np.abs(arr))) or 1.0
    normalized = arr / scale
    means = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        means[i] = rng.choice(normalized, size=n, replace=True).mean()
    lower = np.percentile(means, (1 - ci) / 2 * 100)
    upper = np.percentile(means, (1 + ci) / 2 * 100)
    return float(lower * scale), float(upper * scale)


def permutation_test(observed: float, samples: list[float], n_perm: int = 1000) -> float:
    """[TODO] Disabled: null hypothesis and test design are not specified.

    The former implementation permuted a single sample and compared its mean
    with ``observed``. Permuting a sample does not change its mean, so the result
    was a step function (``1/(n_perm+1)`` if ``observed`` exceeded the sample
    mean, otherwise ``1``) without statistical meaning (finding B3 in
    ``docs/audit/2026-10-28_repo_checkup.md``).

    Behaviour change: the function now always raises ``NotImplementedError``.
    This is a provisional shutdown of a wrong computation, not a statistical
    repair. The signature is kept only so the entry point stays discoverable;
    it does not imply compatibility. ``calibration.permutation_pvalue`` is
    optional in ``spec/eci.spec.json`` and is omitted when no p-value is
    computed. No substitute p-value is produced.

    A replacement needs these decisions first (none exists in the repo's primary
    material; they must not be derived from the name ECI or the term consent):

    - target quantity and test statistic;
    - unit of observation (what is resampled);
    - null hypothesis (e.g. two groups exchangeable vs. one sample symmetric
      around a reference value);
    - exchangeability assumption that justifies the resampling under H0.

    Raises:
        NotImplementedError: always.
    """
    raise NotImplementedError(
        "permutation_test is disabled: null hypothesis and test design are not "
        "specified (finding B3). The former single-sample permutation could not "
        "change the mean and produced meaningless p-values; no substitute p-value "
        "is computed."
    )


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
