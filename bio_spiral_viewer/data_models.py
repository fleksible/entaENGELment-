"""Typed representations of the Bio Spiral Viewer data structures."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class ConsentWindow:
    """Represents the ETHICS membrane consent scope."""

    region: str
    expires_at: datetime
    epsilon_budget: float


@dataclass
class GovernanceState:
    """Snapshot of gate, ledger and crowd risk data."""

    gate_open: bool
    gate_reason: str
    psi_lock: bool
    cri_badge: str
    ledger_receipt: str
    consent: ConsentWindow
    retro_gauge_active: bool


@dataclass
class BodyFieldState:
    """Bio-resonant metrics derived from live feeds."""

    hrv_coherence: float
    plv: float
    leakage: float
    mi_twin_pass: float


@dataclass
class SpiralDriveChannel:
    """Single vortex driver around the spiral."""

    index: int
    weight: float
    phase_angle: float
    instantaneous_phase: float


@dataclass
class SpiralState:
    """Topological placement on the spiral / torus."""

    spiral_phase: float
    spinor_state: str
    df_flip_committed: bool
    cooldown_remaining: float
    eight_channel_drive: List[SpiralDriveChannel]


@dataclass
class ViewerState:
    """Composite of all state layers."""

    body: BodyFieldState
    spiral: SpiralState
    governance: GovernanceState


@dataclass
class IndexEntry:
    """Administrative manifest entry for primary indices."""

    identifier: str
    description: str
    artifacts: List[str]
    sub_indices: Optional[List["IndexEntry"]] = None


@dataclass
class SeedReference:
    """Reference to the seed/checkpoint files that boot a session."""

    name: str
    path: str
    summary: str


@dataclass
class ViewerManifest:
    """Complete manifest required to initialise the viewer."""

    indices: List[IndexEntry]
    seeds: List[SeedReference]
    governance_artifacts: List[str]
    konfab_artifacts: List[str]
    lyra_artifacts: List[str]
    overlay_artifacts: List[str]
