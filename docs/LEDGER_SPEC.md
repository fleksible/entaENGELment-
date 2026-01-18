# LEDGER SPEC (v0)

## Ziel
- **Auditierbarkeit:** Nachvollziehbare Artefakte (Receipts) pro Analyse/Run.
- **Replay-Determinismus:** Gleicher Input + Seed + Config → gleicher `replay_hash`.

## Split: event vs deterministic
- `event.*`: nicht-deterministisch (timestamp, receipt_id, session_id)
- `deterministic.*`: stabil (seed, config_hash, input_hash, output_hash, replay_hash)

**Wichtig:** `replay_hash` wird **ohne** `event.*` berechnet und **ohne** `deterministic.replay_hash` selbst.

## Canonicalization
- Text: NFC + newline-normalisiert + strip
- JSON: sort_keys + separators ohne whitespace

## Hashing
- SHA-256 über canonical JSON
- Präfixe: `sha256:<hex>`

## Verifikation
- `ReplayableReceipt.verify_replay()` vergleicht gespeicherten `replay_hash` mit neu berechnetem.

## Chain (optional)
- Für Receipt-Chains kann ein zusätzlicher `prev_replay_hash` eingeführt werden (v1).
