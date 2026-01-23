# P4 Test Plan Index

This document describes the minimal set of tests required to validate the hardware components of the Ark ⟦CephaloCamouflage⟧ system at Phase P4 (Component Validation). Each test corresponds to a physical guard or system component. The goal is to provide reproducible, audit-ready receipts demonstrating that each constraint is enforced by physics and calibrated against a canonical reference suite.

## Required Receipts

The following receipts must all PASS before the P4 stage can be considered complete. Each receipt is defined as a separate YAML file under `ark/p4/receipts/`.

- `ARK-P4-INDEX-0000`: high-level index of invariants and required tests.
- `ARK-P4-PHI-0001`: Φ* guard (saturable absorber) intensity sweep.
- `ARK-P4-ENT-0002`: entropy guard (high-pass filter) gating test.
- `ARK-P4-MI-0003`: mutual-information proxy guard (JTC peak-width) classification.
- `ARK-P4-TAU-0004`: refractory guard (thermal recovery) measurement.
- `ARK-P4-TWIN-0005`: twin-pass voting interferometer truth table.
- `ARK-P4-CST-0006`: continuous self-test (pilot tone every 100 frames).
- `CALSET-PHI-0001`: calibration set for Φ* mapping (reference patterns).
- `ARK-MAP-PHI-0002`: mapping receipt linking Φ* to absorber intensity.
- `ARK-OVL-RO-0001`: overlay read-only contract (monitoring interface integrity).

Each receipt contains a `claims` section linking back to the manifest for normative requirements, a `procedure` that describes the experimental steps, an `acceptance` section that defines pass/fail criteria, and an `audit` block for attestation and review.
