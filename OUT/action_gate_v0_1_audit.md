# Report: Action-Gate v0.1 — Computable Stitching Spine

**Datum:** 2026-07-23
**Fokus:** Computable Stitching Spine v0.1

## Ziel

Die computationale Seite des Repos anschlussfähiger machen, indem die im
Evidence Routing Kernel v0.1a dokumentierte offene Grenze („kein Action-Gate",
`docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` §2/§14) mit dem kleinsten sicheren,
**nicht ausführenden** Delta geschlossen wird: einer Action-Gate-Schnittstelle,
die eine extern gefundene Handlungsanweisung ausschließlich in ein inertes
`ActionProposal`-Manifest übersetzt.

## Ausgangslage (read-only Audit)

- Der Evidence Routing Kernel (`src/core/evidence_routing.py`, 1664 Z.) ist
  bereits implementiert und gemergt (PR #314). Kernobjekte, Policy-Kopplung,
  Guard/Human-Kette, Replay, Retraction, Reduced Export und die zwölf Invarianten
  existieren samt Tests.
- Nachweisbar fehlend: die Action-Gate-Schnittstelle. `grep` auf
  `action_gate|action_proposal|proposed_command|requested_version|filesystem_effects`
  über `src/ tools/ tests/ docs/` → 0 Treffer.
- Offene PRs zum Auditzeitpunkt: #320, #319, #299, #298, #245 — keine berührt
  `src/core/`. PR #304 und #312 sind bereits gemergt (tesser3TAKT-UI, disjunkt).

## Aktionen

- [x] `src/core/action_gate.py` neu: `ActionProposal` (frozen dataclass, exakt die
      geforderten Manifest-Felder), `ResponsibilityClass`-Enum
      (COMPUTATIONAL/IN_BETWEEN/HUMAN_ONLY), geschlossenes `ActionReasonCode`-Enum,
      reine `build_action_proposal(...)`-Funktion mit fail-closed HOLD-Regeln.
- [x] Wiederverwendung bestehender Typen/Konstanten aus `evidence_routing.py`
      (`MaterialRef`, `GUARD_HOLD/PROPOSE`, Trust-/Visibility-Konstanten,
      `normalize_trust`) — keine Paralleltypen, keine neue Runtime-Dependency.
- [x] `src/core/__init__.py`: stabile Exports der neuen Symbole ergänzt.
- [x] `tests/unit/test_action_gate.py` (35 Tests) und
      `tests/ethics/test_action_gate_no_execution.py` (9 Tests).
- [x] Fixture `tests/fixtures/erk/action_gate_setup_doc.md` (inerte Setup-Doku
      mit `curl … | bash`-Zeile als reine Daten).
- [x] Draft-Spec `docs/annex/ACTION_GATE_v0_1.md` ([SPEC-WIP], ANNEX).
- [x] Prüfungen ausgeführt (siehe unten).

## Ausgeführte Prüfungen

- `python -m pytest tests/unit/test_action_gate.py tests/ethics/test_action_gate_no_execution.py`
  → **44 passed**.
- `python -m pytest tests/ethics tests/unit/test_evidence_routing.py tests/integration/test_erk_ledger.py tests/unit/test_erk_tools.py`
  → **102 passed** (keine Regression im ERK-Umfeld).
- `ruff check` auf die drei neuen Python-Dateien → **All checks passed**.
- `black --line-length 100 --target-version py311` → angewendet, sauber.
- `mypy src/core/action_gate.py` → keine Fehler aus dem neuen Modul; einziger
  gemeldeter Punkt ist der **vorbestehende** fehlende `types-PyYAML`-Stub in
  `evidence_routing.py` (nicht durch dieses Delta verursacht).

## Nicht getan (bewusst)

- Kein `make verify`/`make test`/`make verify-all` als Gesamtlauf: Die
  Dev-Toolchain ließ sich nicht vollständig via `requirements-dev.txt`
  installieren (Konflikt mit debian-vorinstalliertem `cryptography`, RECORD
  fehlt). Es wurden nur `pyyaml` und `pytest` in den aktiven Interpreter
  installiert, um den scope-relevanten Testumfang zu fahren. `verify-js` ist
  nicht anwendbar (reiner Python-ANNEX-Scope).
- Kein Kontext-Rot-/Drift-Check implementiert — als Phase-2-Kandidat in
  `docs/annex/ACTION_GATE_v0_1.md` §8 dokumentiert, ohne neues Backlog und ohne
  `VOIDMAP.yml`-Mutation.
- Keine Ledger-Emission des Manifests (v0.1 erzeugt nur ein Manifest).
- Keine Änderung an `index/`, `policies/`, `spec/`, `VOIDMAP.yml`,
  `data/receipts/`, `NICHTRAUM/` oder an Dateien der PRs #304/#312.
- Keine automatische Installation, kein Netzwerk, keine Shell-Ausführung.

## Risiken

- `verification_status` ist eine Zusicherung des Aufrufers, keine
  kryptografische Prüfung — dokumentierte Grenze (§8).
- Die Registry-Allowlist ist bewusst klein und bedeutet Bekanntheit, nicht
  Vertrauen zur Ausführung.
- Voller `make verify`-Lauf steht wegen Toolchain-Installationskonflikt aus;
  CI muss dies vor Merge grün bestätigen (G6).

## Offene Punkte

- [ ] ☐ Voller `make verify` / `make test-ethics` im CI-Kontext grün bestätigen.
- [ ] ☐ Menschliche Entscheidung über Phase-2-Drift-Check (HOLD).
- [ ] ☐ Menschliche Entscheidung über spätere Ledger-Adapter-Kopplung (LOOP).

## Reentry-Status

- **PASS-KANDIDAT:** technische ANNEX-Implementierung nach grünen scope-Tests.
- **HOLD:** Claim-Promotion, GOLD-/CANON-/VOIDMAP-/öffentliche Bedeutungsentscheidung.
- **LOOP:** semantische Stitching-Entscheidung, spätere Architekturpromotion,
  Ledger-Adapter, Drift-Check-Schwellen.

Keine Selbstattestation als endgültiger PASS.

## Artefakte

- `src/core/action_gate.py`
- `src/core/__init__.py`
- `tests/unit/test_action_gate.py`
- `tests/ethics/test_action_gate_no_execution.py`
- `tests/fixtures/erk/action_gate_setup_doc.md`
- `docs/annex/ACTION_GATE_v0_1.md`
- `OUT/action_gate_v0_1_audit.md`
