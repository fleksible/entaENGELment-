# Claim-Tag Runtime Mapping v0.1

**Status:** [ANNEX] — `artifact_type: analysis` · keine Policy- oder Linter-Änderung  
**Datum:** 2026-07-15  
**Scope:** `policies/claim_tags_v0_2.yaml`, `tools/claim_lint.py`, `EPISTEMIC_HYGIENE.md`

## 0. Zweck und Grenze

[ANNEX] Diese Datei kartiert drei vorhandene Vokabularschichten. Sie ersetzt keine davon und promoviert keine neue Source of Truth.

[FACT] Das Draft-Register, der Runtime-Linter und die Langform-Konvention sind derzeit nicht deckungsgleich. Alignment bedeutet deshalb nicht, den Linter mechanisch „auf das Register hochzuziehen“, sondern Rollen und Übergänge explizit zu entscheiden.

## 1. Drei Ebenen

| Ebene | Quelle | Rolle | Technische Erzwingung |
|---|---|---|---|
| A · Draft-Register | `policies/claim_tags_v0_2.yaml` | erweitertes epistemisches Vokabular und Transitionen | laut eigener `compatibility_notes` noch nicht vollständig |
| B · Runtime-Linter | `tools/claim_lint.py` | erkennt Assertionsmuster und akzeptiert fünf Marker | strict in CI, Default-Scope `index,spec,receipts,tools` |
| C · Langform-Konvention | `EPISTEMIC_HYGIENE.md` | menschenlesbare Architektur-/Merge-Hygiene | dokumentarisch; „mirrors“ die Disziplin, nicht den exakten Linter-Satz |

## 2. Inventar

### A · Draft-Register v0.2

- ROHSEDIMENT
- `[METAPHER]`
- `[HYPOTHESE]`
- `[INFERENZ]`
- `[MODEL]`
- `[FACT]`
- `[SPEC-WIP]`
- `[SPEC]`
- `[CANON]`
- `[VOID]`
- `[ROSETTA]`
- `[ANNEX]`
- `[CONTEXT]`
- `[BRIDGE-WIP]`
- `[UI-LAB]`
- SIMULATION_PROXY

Aliase: `[FAKT]→[FACT]`, `[HYP]→[HYPOTHESE]`, `[MET]→[METAPHER]`, `[MODELL]→[MODEL]`.

### B · Runtime-Linter

`VALID_TAGS = {[FACT], [HYP], [MET], [TODO], [RISK]}`

[FACT] `[TODO]` und `[RISK]` sind in Ebene B gültig, fehlen aber als Tags in Ebene A. Die Ebenen sind daher teildisjunkt, nicht bloß „eng“ versus „weit“.

### C · Langform-Konvention

- `[FACT]`
- `[MODEL]`
- `[HYPOTHESIS]`
- `[METAPHOR]`

[INFERENZ] Ebene C spiegelt die epistemische Intention, nicht die exakte maschinenlesbare Syntax von A oder B.

## 3. Mapping-Entscheidungen v0.1

| Token/Feld | Rolle in v0.1 | Begründung |
|---|---|---|
| `[FACT]` | gemeinsamer epistemischer Tag | in A, B und C vorhanden |
| `[HYP]` | Legacy-Linter-Alias zu `[HYPOTHESE]` | Alias in A dokumentiert |
| `[MET]` | Legacy-Linter-Alias zu `[METAPHER]` | Alias in A dokumentiert |
| `[TODO]` | auxiliary workflow marker | Aufgabe, kein epistemischer Wahrheitsstatus |
| `[RISK]` | auxiliary risk marker | Risikohinweis, kein epistemischer Wahrheitsstatus |
| `[ANNEX]` | registrierter Tag **oder** `authority_status: annex` | Doppelrolle nur mit sichtbarem Feld zulässig |
| OPEN | VOID-/Workflow-Status | kein Claim-Tag |
| GOLD | `authority_status`/Governance-Domänenstatus | kein Claim-Tag |
| CONFLICT | Ledger-Relation | kein Claim-Tag |
| AUDIT | `artifact_type` | kein Claim-Tag |
| QDOT | lokales Review-/Frageobjekt | kein Claim-Tag, kein zweites VOID-System |

## 4. Verbindliche Leseregeln für nachfolgende Dokumente

1. Ein Klammermarker darf nicht gleichzeitig Claim-, Domain-, Workflow- und Authority-Rolle tragen.
2. Domain-Kennzeichnungen werden als Feld oder Klartext geführt, beispielsweise `domain: DEV`, nicht als `[DEV]` im Claim-Slot.
3. `[ANNEX]` benötigt im Zweifel eine Feldangabe: `claim_status` oder `authority_status`.
4. „Linter-valid“ bedeutet nur: innerhalb des tatsächlich ausgeführten Scopes vom aktuellen Tool akzeptiert.
5. „Registerkonform“ bedeutet nicht „runtime-erzwungen“.
6. „Dokumentiert“ bedeutet nicht „implementiert“, „getestet“ oder „enforced“.
7. Eine spätere Toolangleichung benötigt einen eigenen Code-/Policy-PR und Tests.

## 5. Keine stillen Änderungen

Dieser Mapping-Pass verändert ausdrücklich nicht:

- `policies/claim_tags_v0_2.yaml`,
- `tools/claim_lint.py`,
- `EPISTEMIC_HYGIENE.md`,
- `VOIDMAP.yml`,
- bestehende Receipts.

## 6. Nachfolgende technische Optionen

[VOID] Vor einer Runtime-Angleichung sind getrennt zu entscheiden:

1. Soll der Linter Register-Tags nur als gültig akzeptieren oder zusätzlich Transitionen prüfen?
2. Bleiben `[TODO]` und `[RISK]` auxiliary marker oder werden sie als eigene Policy-Felder modelliert?
3. Wird der Scope auf `docs/` und `policies/` erweitert oder entsteht dort ein separater Dokument-Linter?
4. Wie werden Aliasformen normalisiert, ohne historische Receipts umzuschreiben?
5. Welche Failure- und Rücknahmebedingungen gelten bei False Positives?

## 7. Reentry

**PASS-KANDIDAT:** Mapping als ANNEX-Analyse.  
**HOLD:** Policy-, Linter-, VOIDMAP- und CANON-Änderungen.  
**LOOP:** spätere technische Entscheidung mit Tests und eigenem Review.  
**STOP:** Gleichsetzung von Registerkonformität, Runtime-Erzwingung und Authority.
