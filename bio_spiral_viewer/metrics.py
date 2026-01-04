"""Metric computation helpers for the Bio Spiral Viewer."""

from __future__ import annotations

from collections.abc import Iterable

from .data_models import BodyFieldState, SpiralDriveChannel


def compute_resonance_score(body: BodyFieldState) -> float:
    """Compute R(t) = MI_TwinPass * PLV * (1 - Leakage)."""

    return body.mi_twin_pass * body.plv * (1.0 - body.leakage)


def compute_drive_balance(channels: Iterable[SpiralDriveChannel]) -> float:
    """Return a normalised balance index for the eight-channel drive."""

    weights = [channel.weight for channel in channels]
    total = sum(weights)
    if not weights or total == 0:
        return 0.0
    max_weight = max(weights)
    min_weight = min(weights)
    return 1.0 - (max_weight - min_weight) / total
