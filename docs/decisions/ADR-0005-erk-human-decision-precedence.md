# ADR-0005: Wirkung späterer Human-Entscheidungen auf eine Freigabe (ERK v0.1a)

- **Status:** Accepted (A2, umgesetzt)
- **Datum:** 2026-10-02
- **Kontext-Fokus:** REJECT/DEFER nach APPROVE im Evidence Routing Kernel
- **Herkunft:** Audit 2026-10-02, Befund AUD-03 / Review-Paket R4
  ([`../audit/repo_audit_2026-10-02.md`](../audit/repo_audit_2026-10-02.md),
  [`../audit/repo_audit_result_2026-10-02.md`](../audit/repo_audit_result_2026-10-02.md))
- **Entscheidung durch:** Kevin/Fleks, 2026-10-02: **A2**

> Entschieden am 2026-10-02 durch Kevin/Fleks: A2. Umsetzung im Folge-Commit auf
> dem Audit-Branch (PR #377). Abschnitte „Context“ bis „Vorschlag“ dokumentieren den
> Stand vor der Entscheidung.

## Context

Der Evidence Routing Kernel (`src/core/evidence_routing.py`, Spec
[`../annex/EVIDENCE_ROUTING_KERNEL_v0_1.md`](../annex/EVIDENCE_ROUTING_KERNEL_v0_1.md))
kennt vier menschliche Entscheidungen: `APPROVE | REJECT | DEFER | WITHDRAW` (Spec §5).
Ein `CLAIM_RETAGGED` braucht genau ein referenziertes `APPROVE` desselben Requests
(Spec §6.1). Als Rücknahme vor Anwendung ist nur `WITHDRAW` definiert (Spec §13);
seit Commit `be7b25e` gilt dafür die Stream-Ordnung (AUD-01).

Für `REJECT` und `DEFER` legt der Vertrag keine Wirkung auf eine bestehende Freigabe fest.
Beobachtet an Revision `bc87b67` (Probe mit der Fixture
`tests/fixtures/erk/human_approved_retag.jsonl`, synthetische Events):

| Stream vor dem Retag | Ergebnis |
|---|---|
| APPROVE → REJECT (gleiches `human_actor`-Label) | Retag angewendet (`[MODEL]`) |
| APPROVE → REJECT (anderes Label) | Retag angewendet |
| REJECT → APPROVE | Retag angewendet |
| DEFER → APPROVE | Retag angewendet |
| APPROVE → DEFER | Retag angewendet |

Das ist vertragskonform, aber eine nach der Freigabe aufgezeichnete Ablehnung oder
Zurückstellung bleibt ohne Wirkung. Zusätzlich gilt: `human_actor` ist ein nicht
authentifiziertes Rollenlabel (Spec §9.1). Jede Regel, die zwischen Personen
unterscheidet, stützt sich derzeit nur auf behauptete Labels.

## Alternativen

| | Regel | Wirkung auf die Tabelle oben | Vorteil | Nachteil |
|---|---|---|---|---|
| **A1** Status quo | Nur `WITHDRAW` hebt eine Freigabe auf; REJECT/DEFER sind reine Entscheidungsgeschichte | unverändert | keine Änderung; klare Einzelregel | eine spätere Ablehnung kann übersehen werden, ohne dass der Retag stoppt |
| **A2** Letzter Stand zählt | Zum Zeitpunkt des Retags muss die **im Stream letzte** Human-Entscheidung des Requests das referenzierte `APPROVE` sein | APPROVE→REJECT und APPROVE→DEFER blockieren; REJECT→APPROVE und DEFER→APPROVE bleiben erlaubt | gleiches Prinzip wie AUD-01 (Stream-Ordnung); erlaubt Umentscheiden; ohne Identitätsannahmen | DEFER nach APPROVE blockiert, bis ein neues APPROVE folgt |
| **A3** REJECT als Veto | Jedes `REJECT` des Requests blockiert dauerhaft, egal wann | auch REJECT→APPROVE blockiert | maximal vorsichtig | Umentscheiden nur über einen neuen Request; blockiert ohne Identitätsprüfung auch durch beliebige Labels |
| **A4** Akteursgebunden | Nur eine spätere Entscheidung **desselben** `human_actor` hebt auf | APPROVE→REJECT (gleiches Label) blockiert, anderes Label nicht | bildet „eigene Freigabe zurücknehmen“ ab | stützt sich auf unauthentifizierte Labels; täuscht Personenbindung vor, die es nicht gibt |

## Vorschlag (Empfehlung, nicht beschlossen)

**A2 — Letzter Stand zählt.** Gründe:

1. Sie setzt dasselbe Prinzip fort, das mit AUD-01 bereits entschieden wurde: Die Stream-Ordnung
   ist maßgeblich, nicht behauptete Zeitstempel.
2. Sie ist fail-closed: Steht nach einer Freigabe noch Ablehnung oder Zurückstellung, wird nicht
   angewendet.
3. Sie braucht keine Annahme über Identität (anders als A4) und verhindert kein legitimes
   Umentscheiden (anders als A3).

Kleinstes technisches Delta bei Annahme (erst nach Entscheidung umsetzen):

- `_apply_retag_event`: Nach dem referenzierten `APPROVE` darf in
  `_human_decisions_for_request(state, request_id)` (Einfügereihenfolge = Stream-Ordnung)
  keine weitere Entscheidung folgen, die kein `APPROVE` ist; sonst `EVENT_ORDER_INVALID`.
  Kein neuer Reason-Code, kein neues Feld.
- `apply_approved_transition(human_decisions=...)`: Die übergebene Sequenz hat keine
  garantierte Ordnung. Offene Unterfrage: Sequenz als stream-geordnet definieren (Doku +
  Test) oder dort weiterhin nur `WITHDRAW` prüfen und die volle Regel dem Replay überlassen.
- Tests: die fünf Fälle der Tabelle als Gegenfälle in `TestWithdrawalBoundary` bzw. einer
  eigenen Klasse.

## Maßgebliche Fassung (A2)

**Ein `CLAIM_RETAGGED` ist nur anwendbar, wenn das referenzierte `APPROVE` die im
Stream letzte Human-Entscheidung desselben Requests ist.** Das ist die Fassung aus der
Alternativentabelle, die Kevin/Fleks am 2026-10-02 entschieden hat.

Folgen daraus:

| Stream vor dem Retag | Retag referenziert | Ergebnis |
|---|---|---|
| APPROVE(1) → REJECT/DEFER | 1 | abgewiesen |
| REJECT/DEFER → APPROVE(1) | 1 | angewendet |
| APPROVE(1) → REJECT → APPROVE(3) | 1 / 3 | abgewiesen / angewendet |
| APPROVE(1) → APPROVE(2) | 1 / 2 | abgewiesen / angewendet |

## Umsetzung (A2)

- `_apply_retag_event`: Das referenzierte `APPROVE` muss der letzte Eintrag von
  `_human_decisions_for_request()` (Einfügereihenfolge = Stream-Ordnung) sein; sonst
  `EVENT_ORDER_INVALID`. Kein neuer Reason-Code, kein neues Event-Feld.
- `apply_approved_transition(human_decisions=...)`: Eine übergebene Historie gilt als
  vollständig und stream-geordnet. Sie muss die Freigabe unverändert enthalten
  (sonst `HUMAN_REFERENCE_MISMATCH`), und die Freigabe muss die letzte Entscheidung des
  Requests darin sein (sonst `EVENT_ORDER_INVALID`). Entscheidungen anderer Requests
  zählen nicht. Eine **leere** Historie (Default) prüft keine Präzedenz und behauptet
  nichts über spätere Entscheidungen; maßgeblich bleibt `replay_events()`.
- `compute_state_digest()`: Die Reihenfolge der Human-Entscheidungen geht als geordnete
  ID-Liste `human_decision_order` in den State-Digest ein (Spec §8). Zuvor erzeugten
  A→R und R→A mit gleichen Records denselben Digest, obwohl dasselbe Folge-Retag
  unterschiedlich anwendbar war (Review R377-01). Digest-Werte ändern sich dadurch für
  Streams mit Human-Entscheidungen; im Repo sind keine Digest-Werte persistiert.
- Tests: `tests/unit/test_evidence_routing.py::TestDecisionPrecedence` und
  `::TestApplyDecisionHistory`.

**Korrekturhinweis:** Commit `36c8569` hatte eine lockerere Variante umgesetzt („nach dem
referenzierten `APPROVE` kein `REJECT`/`DEFER`“, ein weiteres `APPROVE` danach unschädlich)
und sie hier als „Präzisierung“ geführt. Das entsprach nicht der entschiedenen Fassung; der
Review von PR #377 (R377-03) hat die Abweichung aufgedeckt. Der Code folgt seit dem
Korrektur-Commit der maßgeblichen Fassung oben.

## Folgen

- **A1:** keine Codeänderung; Spec §13 sollte dann ausdrücklich sagen, dass REJECT/DEFER eine
  bestehende Freigabe nicht aufheben.
- **A2/A3/A4:** Verhaltensänderung im Kernel, die strenger wird. Bestehende Fixtures sind nicht
  betroffen (keine enthält REJECT/DEFER nach APPROVE); Spec §5/§13 müssen ergänzt werden.
- Keine der Alternativen ersetzt eine Authentifizierung. Bis dahin bleiben alle Akteursangaben
  Behauptungen (Spec §9.1).

## Essenzschutz

- Consent-First: Die Frage betrifft, wann eine Freigabe als noch gültig gilt; jede Alternative
  außer A1 verschärft nur, keine lockert.
- Guard-Zustand (`PROPOSE|HOLD|STOP`) und Human-Entscheidung bleiben getrennt (Invariante 7);
  kein `PASS`, kein neues Statusvokabular.
- Keine Gleichsetzung mit tesser3TAKT-Review (`PASS|HOLD|LOOP|STOP`) oder UI-BoundaryTransition
  (Spec §11).
- Ein synthetisches APPROVE/REJECT in Tests beweist keine reale Einwilligung oder Ablehnung.

## Referenzen

- Spec: `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` §5, §6.1, §9.1, §11, §13
- Code: `src/core/evidence_routing.py` — `_apply_retag_event`, `apply_approved_transition`,
  `_human_decisions_for_request`
- Tests: `tests/unit/test_evidence_routing.py::TestWithdrawalBoundary`
- Vorgänger-Entscheidung: AUD-01 / Commit `be7b25e` (WITHDRAW an Stream-Ordnung gebunden)
- Roadmap: `docs/roadmap/forward_architecture_2026-10-02.md` S4

## Rücknahme

- Solange *Proposed*: Datei kann nach `NICHTRAUM/archive/` verschoben werden (G3), ohne Wirkung.
- Nach *Accepted* und Umsetzung: Revert des Umsetzungs-Commits; ADR auf *Superseded* setzen
  und den Nachfolger verlinken.
