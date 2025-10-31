"""Utilities to load viewer state from JSON resources."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .data_models import (
    BodyFieldState,
    ConsentWindow,
    GovernanceState,
    IndexEntry,
    SeedReference,
    SpiralDriveChannel,
    SpiralState,
    ViewerManifest,
    ViewerState,
)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_viewer_state(path: Path) -> ViewerState:
    payload = _load_json(path)

    body_payload = payload["body"]
    spiral_payload = payload["spiral"]
    governance_payload = payload["governance"]

    body = BodyFieldState(
        hrv_coherence=body_payload["hrv_coherence"],
        plv=body_payload["plv"],
        leakage=body_payload["leakage"],
        mi_twin_pass=body_payload["mi_twin_pass"],
    )

    channels = [
        SpiralDriveChannel(
            index=channel["index"],
            weight=channel["weight"],
            phase_angle=channel["phase_angle"],
            instantaneous_phase=channel["instantaneous_phase"],
        )
        for channel in spiral_payload["eight_channel_drive"]
    ]

    spiral = SpiralState(
        spiral_phase=spiral_payload["spiral_phase"],
        spinor_state=spiral_payload["spinor_state"],
        df_flip_committed=spiral_payload["df_flip_committed"],
        cooldown_remaining=spiral_payload["cooldown_remaining"],
        eight_channel_drive=channels,
    )

    consent_payload = governance_payload["consent"]
    consent = ConsentWindow(
        region=consent_payload["region"],
        expires_at=datetime.fromisoformat(consent_payload["expires_at"]),
        epsilon_budget=consent_payload["epsilon_budget"],
    )

    governance = GovernanceState(
        gate_open=governance_payload["gate_open"],
        gate_reason=governance_payload["gate_reason"],
        psi_lock=governance_payload["psi_lock"],
        cri_badge=governance_payload["cri_badge"],
        ledger_receipt=governance_payload["ledger_receipt"],
        consent=consent,
        retro_gauge_active=governance_payload["retro_gauge_active"],
    )

    return ViewerState(body=body, spiral=spiral, governance=governance)


def load_manifest(path: Path) -> ViewerManifest:
    payload = _load_json(path)

    indices = [
        _parse_index(entry)
        for entry in payload.get("indices", [])
    ]

    seeds = [
        SeedReference(name=item["name"], path=item["path"], summary=item["summary"])
        for item in payload.get("seeds", [])
    ]

    return ViewerManifest(
        indices=indices,
        seeds=seeds,
        governance_artifacts=payload.get("governance_artifacts", []),
        konfab_artifacts=payload.get("konfab_artifacts", []),
        lyra_artifacts=payload.get("lyra_artifacts", []),
        overlay_artifacts=payload.get("overlay_artifacts", []),
    )


def _parse_index(payload: Dict[str, Any]) -> IndexEntry:
    return IndexEntry(
        identifier=payload["identifier"],
        description=payload["description"],
        artifacts=list(payload.get("artifacts", [])),
        sub_indices=[_parse_index(item) for item in payload.get("sub_indices", [])]
        if payload.get("sub_indices")
        else None,
    )


def iter_artifact_paths(manifest: ViewerManifest, base_path: Path) -> Iterable[Path]:
    """Yield all referenced artifact paths relative to ``base_path``."""

    seen: List[str] = []

    def _queue(items: Iterable[str]) -> None:
        for rel_path in items:
            if rel_path not in seen:
                seen.append(rel_path)
                yield_path = base_path / rel_path
                if yield_path.exists():
                    yield yield_path

    yield from _queue(manifest.governance_artifacts)
    yield from _queue(manifest.konfab_artifacts)
    yield from _queue(manifest.lyra_artifacts)
    yield from _queue(manifest.overlay_artifacts)
    for seed in manifest.seeds:
        if seed.path not in seen:
            seen.append(seed.path)
            candidate = base_path / seed.path
            if candidate.exists():
                yield candidate
