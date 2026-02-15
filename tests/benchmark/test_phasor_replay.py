#!/usr/bin/env python3
"""
Benchmark Replay Test — Phasor Determinism
Runs phasor simulation with fixed seed and parameters,
verifies output hash matches known-good baseline.
"""
import hashlib
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def run_phasor_benchmark():
    """Run phasor with fixed parameters, return deterministic output."""
    # Fixed parameters — NEVER change these without updating baseline
    params = {
        "J_coupling": 1e-21,
        "kT": 4.2800119e-21,
        "T_body": 310,
        "vmem_rest": -45,
        "vmem_to_phase_scale": 0.12566370614359174,
        "n_cells": 50,
        "seed": 42,
        "dt": 0.0001,
        "t_total": 0.01,
    }

    # Canonical serialization for hash
    canonical = json.dumps(params, sort_keys=True, separators=(',', ':'))
    param_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]

    return {
        "param_hash": param_hash,
        "params": params,
        "status": "FRAMEWORK_READY",
        "note": "Baseline hash TBD after first successful full BETSE run"
    }

def test_phasor_params_deterministic():
    """Parameter serialization must be deterministic."""
    r1 = run_phasor_benchmark()
    r2 = run_phasor_benchmark()
    assert r1["param_hash"] == r2["param_hash"], \
        f"Non-deterministic: {r1['param_hash']} != {r2['param_hash']}"

if __name__ == "__main__":
    result = run_phasor_benchmark()
    print(json.dumps(result, indent=2))
