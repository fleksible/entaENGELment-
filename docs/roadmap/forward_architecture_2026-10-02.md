# Report: Forward Architecture 2026-10-02 (Phase 3 — reviewbarer Vorschlag)

**Datum:** 2026-10-02
**Fokus:** Abhängigkeitsfolge aus belegten Lücken
**Status:** PROPOSAL — keine Freigabe, keine Kanonisierung, kein VOID-Eintrag
**Basis:** [`../audit/repo_audit_2026-10-02.md`](../audit/repo_audit_2026-10-02.md) (Revision `6f4347f`)
**Vorgänger:** [`revolutionary_forward_architecture_2026-06-16.md`](revolutionary_forward_architecture_2026-06-16.md) — dessen Registry-/Glossar-Ideen werden hier **nicht** fortgeschrieben, weil der aktuelle Audit keinen konkreten Fehler belegt, den sie verhindern würden.

---

## Leitlinie

Jeder Schritt schließt an einen bestehenden Vertrag an (ERK v0.1a, Action Gate v0.1,
Bridge View, `docs/ci/PYTHON_LOCK.md`, ADR-Reihe). Kein zweiter Kernel, keine neue
globale Statusmaschine, keine neuen Payload-Felder ohne eigenes versioniertes Review.
Geschlossene Schemata (`_MODEL_SPECS`, `_RETAG_PAYLOAD_FIELDS`, `ReasonCode`) bleiben unverändert,
solange ein Schritt das nicht ausdrücklich als Review-Gegenstand führt.

## Abhängigkeitsfolge

```
S1 Rücknahme-Ordnung (AUD-01)          ── unabhängig, kleinstes Delta
S2 Quellfassungs-Bindung (AUD-05)      ── nach S1 (gleiche Retag-Stelle)
S3 Verify-Kopplung (AUD-04)            ── unabhängig
S4 Mehr-Akteur-Entscheidungsregel (AUD-03) ── semantisch, vor jeder Authentifizierung
S5 Authentifizierung / produktive Freigabe ── erst nach S1–S4, eigenes Vorhaben
S6 Hygiene: ADR-0001, Branches, AUD-06 ── jederzeit, menschliche Entscheidungen
```

### S1 — Rücknahme an Stream-Ordnung binden

| Feld | Inhalt |
|---|---|
| Zweck | WITHDRAW vor Anwendung blockiert den Retag unabhängig vom behaupteten `decided_at` |
| Anschluss | `_apply_retag_event`, `apply_approved_transition` (Spec §8, §13) |
| Kleinstes Delta | Replay: jedes bereits replayte WITHDRAW des Requests blockiert (Diff im Ergebnisbericht, Paket R1). `apply_approved_transition`: Aufrufer-Liste hat keine Ordnung → entweder jedes WITHDRAW blockiert oder Parameter-Doku schärfen (Entscheidung nötig) |
| Eintritt | Kevin/Fleks bestätigt: Stream-Ordnung ist maßgeblich |
| Abnahme | `xfail(strict)` in `TestWithdrawalBoundary` wird XPASS → Marker entfernen; alle ERK-Suiten grün |
| Pflege | keine neue Struktur |
| Rücknahme | `git revert` des Fix-Commits; Test fällt zurück auf xfail |

### S2 — Quellfassung an Bytes binden (optional, nur wenn gewollt)

| Feld | Inhalt |
|---|---|
| Zweck | Ein Retag darf nicht auf Material beruhen, dessen Quelle sich seit Registrierung geändert hat |
| Anschluss | `MaterialRef.digest` (existiert), `tools/erk_intake_adapter.py` (rechnet SHA-256 bei Intake) |
| Kleinstes Delta | **außerhalb** des Kernels: ein lesender Prüfer in `tools/`, der für `source: repo` den Digest der Datei an `revision` nachrechnet und Abweichung als Review-Kandidat meldet. Kernel bleibt dateifrei (Spec §2: keine Netz-/Dateizugriffe) |
| Eintritt | S1 erledigt; Entscheidung, ob Quellbindung überhaupt Ziel von v0.x ist |
| Abnahme | Negativfall-Fixture: geänderte Datei → Meldung; unveränderte → keine |
| Pflege | ein Tool + Test; keine neuen Event-Felder |
| Rücknahme | Tool entfernen (nach `NICHTRAUM/archive/`, G3) |

### S3 — Verify-Event an tatsächlichen Lauf koppeln

| Feld | Inhalt |
|---|---|
| Zweck | `VERIFY_PASS` nur, wenn der Emitter selbst einen Exitcode 0 beobachtet hat |
| Anschluss | `tools/erk_verify_emit.py`, `spec/runtime_eventlog_v0_1.json` (GOLD, nur lesen) |
| Kleinstes Delta | Variante a) nur Doku: „dokumentiert eine Aufruferbehauptung" (Paket R3). Variante b) `--run "<cmd>"`, Emitter führt aus und schreibt nur bei Exit 0 — **neues Verhalten**, Review |
| Eintritt | Entscheidung a/b; solange kein CI-Aufrufer existiert, genügt a |
| Abnahme | a) Doku-Diff; b) Test: Exit ≠ 0 → kein Event |
| Rücknahme | revert |

### S4 — Mehr-Akteur-Entscheidungsregel

> **Stand 2026-10-02:** [ADR-0005](../decisions/ADR-0005-erk-human-decision-precedence.md) *Accepted* (A2) und umgesetzt.

| Feld | Inhalt |
|---|---|
| Zweck | Klären, ob REJECT/DEFER nach APPROVE (anderer oder gleicher Akteur) Wirkung hat |
| Anschluss | Spec §5 `HumanDecision`, §9.1 (`human_actor` = unauthentifiziertes Label) |
| Kleinstes Delta | zunächst nur ADR (nächste Nummer: ADR-0005) mit Alternativen: (1) letzter Stand zählt, (2) jedes REJECT ist Veto, (3) Status quo (nur WITHDRAW). Kein Code vor Entscheidung |
| Abnahme | ADR *Accepted*; danach Tests für die gewählte Regel |
| Pflege | ein ADR |
| Rücknahme | ADR auf *Superseded* |

### S5 — Authentifizierung und produktive Aktionsfreigabe

Bewusst **nicht** geplant. Voraussetzung: S1–S4 entschieden; Action Gate v0.1 bleibt
proposal-only. Ein synthetisches APPROVE beweist keine Einwilligung; bis zu einer
authentifizierten Identität bleibt jede reale Nebenwirkung HUMAN_AUTHORIZATION_REQUIRED.

### S6 — Hygiene (menschliche Entscheidungen, kein Code)

- ADR-0001 annehmen/ändern (AUD-10).
- 8 vollständig gemergte Remote-Branches löschen oder behalten (AUD-07) — Löschung nur durch Owner.
- AUD-06 / Issue #333: Release- und VOID-Workflow auf `python-locked` umstellen — Freigabe ausdrücklich offen laut #373.

## Forschung und Proxywerte

Kein neuer Schritt. VOID-010/011 (Issue #311) bleiben der zuständige Ort; Proxywerte
behaupten keine menschliche Wirkung, bevor Baselines und Falsifikatoren dort stehen.

## Austausch / ehemalige Bezüglichkeit

`docs/exchange_archive/` existiert (ADR-0002) mit README, INDEX und Vorlage. Kein neues
Scaffolding, kein Import. Dieser Audit erzeugt keinen Exchange-Record, weil kein
externer Austausch verarbeitet wurde.

## Validatoren

Vorhandene Gates decken Syntax/Referenzen ab (port-lint, verify-pointers --strict,
claim-lint, workflow-posture, voids-backlog-drift, voidmap-ui-drift). Kein neuer
Validator vorgeschlagen; einziger Kandidat wäre der S2-Prüfer, zunächst als Warnung.

## Offene Punkte

- [ ] ☐ S1: Stream-Ordnung als maßgeblich bestätigen?
- [ ] ☐ S2: Ist Quellbytes-Bindung Ziel?
- [ ] ☐ S3: Variante a oder b?
- [x] S4: ADR-0005 entschieden (A2) und umgesetzt
