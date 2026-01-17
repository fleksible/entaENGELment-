"""High level orchestration for presenting the Bio Spiral state."""

from __future__ import annotations

from dataclasses import asdict

from .data_models import ViewerState
from .metrics import compute_drive_balance, compute_resonance_score


def format_viewer_state(state: ViewerState) -> dict[str, object]:
    """Create a dictionary ready for presentation layers."""

    resonance_score = compute_resonance_score(state.body)
    drive_balance = compute_drive_balance(state.spiral.eight_channel_drive)

    body_block = {
        "HRV coherence": round(state.body.hrv_coherence, 3),
        "PLV": round(state.body.plv, 3),
        "Leakage": round(state.body.leakage, 3),
        "Twin-Pass MI": round(state.body.mi_twin_pass, 3),
        "R(t)": round(resonance_score, 3),
    }

    spiral_block = {
        "Spiral phase": round(state.spiral.spiral_phase, 3),
        "Spinor": state.spiral.spinor_state,
        "DF flip": "committed" if state.spiral.df_flip_committed else "cooldown",
        "Cooldown": round(state.spiral.cooldown_remaining, 2),
        "Drive balance": round(drive_balance, 3),
    }

    governance_block = {
        "Gate": "OPEN" if state.governance.gate_open else "HOLD",
        "Gate reason": state.governance.gate_reason,
        "ψ-lock": "stable" if state.governance.psi_lock else "broken",
        "Retro gauge": "active" if state.governance.retro_gauge_active else "forward",
        "CRI badge": state.governance.cri_badge,
        "Ledger": state.governance.ledger_receipt,
        "Consent": {
            "region": state.governance.consent.region,
            "expires_at": state.governance.consent.expires_at.isoformat(),
            "epsilon": state.governance.consent.epsilon_budget,
        },
    }

    return {
        "body": body_block,
        "spiral": spiral_block,
        "governance": governance_block,
        "raw": asdict(state),
    }
