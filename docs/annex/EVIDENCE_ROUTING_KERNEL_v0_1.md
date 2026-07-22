# EVIDENCE_ROUTING_KERNEL_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** partial
**Human-Decision-Boundary:** required
**Datum:** 2026-07-21
**Modul:** `src/core/evidence_routing.py` + öffentliche Ledger-Event-API in `src/core/ledger.py`

---

## 1. Zweck

Der Evidence Routing Kernel v0.1a ist die kleinste belastbare Laufzeitschicht, die
vorhandene Claim-Tags (`policies/claim_tags_v0_2.yaml`), Materialverweise,
Evidence-Relationen, Guard-Entscheidungen und menschliche Entscheidungen zu einem
deterministisch replaybaren Zustandsfluss verbindet.

Er berechnet Vorschläge und rekonstruiert Zustände. Er entscheidet nichts, was
dem Menschen vorbehalten ist.

## 2. Nicht-Ziele

- kein Truth-Maker und kein zweites Governance-System,
- keine automatische Claim-Promotion,
- keine CANON- oder GOLD-Entscheidung,
- keine VOIDMAP-Schließung, keine neuen kanonischen VOID-IDs,
- keine Policy-Mutation (`policies/` wird ausschließlich gelesen),
- keine Netzwerkzugriffe, keine Shell- oder Aktionsausführung,
- kein Action-Gate in dieser Phase,
- keine semantische Gleichsetzung verschiedener Wissensregister,
- keine Veröffentlichung privater oder biographischer Herkunft.

**Wichtig:** Die vollständige Claim-Policy wird durch diesen Kernel **nicht** live
enforced. Enforcement ist partial: Der Kernel prüft nur die hier dokumentierten
Strukturen, wenn er explizit aufgerufen wird. `tools/claim_lint.py` bleibt davon
unberührt und unangeglichen.

## 3. Wissenskanäle und Rollen

| Rolle | Trägt | Trägt nicht |
|---|---|---|
| Mensch (Projektinitiator) | Bedeutung, Zweck, Scope, Consent, Rücknahme, Claim-Status-Entscheidung, Freigabe/Ablehnung | strukturelle Validierung |
| Kernel (COMPUTATIONAL) | Validierung, Alias-Normalisierung, `allowed_next`-Berechnung, Proposals, fail-closed Guards, append-only Events, Replay, reduzierte Projektion | Retagging, Promotion, VOID-Schließung, Consent-Annahme, HumanDecision-Synthese |
| Policy (Draft-Register) | zulässige syntaktische Nachbarschaft | Wahrheit, Evidenz-Hinreichung, Zustimmung |
| Ledger | Integritätszeugnis (Hash-Chain) | Inhaltsbeweis |

## 4. Eventfluss

```
MaterialRef → ClaimCandidate → EvidenceRelation[] → TransitionRequest
    → GuardDecision (PROPOSE|HOLD|STOP)
    → HumanDecision (APPROVE|REJECT|DEFER|WITHDRAW)
    → Claim-State-Event (CLAIM_RETAGGED, nur nach APPROVE + erneuter Guard-Validierung)
    → ReplayState → ReducedPublicExport
```

Eventtypen (Envelope `{"type": ..., "payload": {...}}` über `ledger.event()`):
`MATERIAL_REGISTERED`, `CLAIM_CREATED`, `EVIDENCE_RELATION_RECORDED`,
`TRANSITION_REQUESTED`, `GUARD_DECISION_RECORDED`, `HUMAN_DECISION_RECORDED`,
`CLAIM_RETAGGED`, `RETRACTION_RECORDED`.

## 5. Typen

Alle Modelle sind Python-3.9-kompatible `dataclass`-Modelle mit geschlossenem
Feldschema (unbekannte Felder → fail-closed, `EVENT_SCHEMA_INVALID`):

- `MaterialRef` — reduzierter Materialverweis; `digest` ist Integritätsverweis,
  kein Wahrheitsbeweis; unbekannter Trust-Level wird zu `UNTRUSTED`; keine
  privaten Rohinhalte.
- `ClaimCandidate` — `claim_text` existiert nur im privaten Eventstream und
  entfällt im Public Export.
- `EvidenceRelation` — `relation_type` ∈ {`SUPPORTS`, `CONTRADICTS`,
  `CONTEXTUALIZES`, `MOTIVATES`, `MEASURES`, `IMPLEMENTS`, `PROVENANCE_ONLY`};
  nur `SUPPORTS`/`MEASURES`/`IMPLEMENTS` können eine Promotion tragen.
- `TransitionRequest` — Wunsch, kein Vollzug.
- `GuardDecision` — `PROPOSE|HOLD|STOP`, inkl. `policy_version` und
  `policy_digest`. Bewusst kein `PASS`: Guard-State und menschliche
  Claim-Entscheidung dürfen nicht zusammenfallen.
- `HumanDecision` — `APPROVE|REJECT|DEFER|WITHDRAW`; nur `APPROVE` kann nach
  erneuter Guard-Validierung ein `CLAIM_RETAGGED` erzeugen.
- `Retraction` — löscht nichts; erzeugt neuen append-only Zustand.
- `ReplayState` — rekonstruierter Zustand inkl. `rejected_events`, `warnings`
  und deterministischem `state_digest`.
- `ReducedPublicExport` — reine Allowlist-Projektion.

## 6. Reason-Codes

Geschlossenes Vokabular (`ReasonCode`-Enum, keine dynamischen Codes im
Eventstream): `POLICY_TRANSITION_ALLOWED`, `POLICY_TRANSITION_DENIED`,
`UNKNOWN_FROM_TAG`, `UNKNOWN_TO_TAG`, `ALIAS_NORMALIZED`, `MISSING_MATERIAL`,
`MISSING_EVIDENCE_RELATION`, `UNTRUSTED_MATERIAL`, `METAPHOR_IS_NOT_EVIDENCE`,
`PROVENANCE_IS_NOT_EVIDENCE`, `HUMAN_DECISION_REQUIRED`, `HUMAN_APPROVED`,
`HUMAN_REJECTED`, `HUMAN_DEFERRED`, `CONSENT_MISSING`, `VISIBILITY_VIOLATION`,
`RETRACTION_RECORDED`, `EVENT_SCHEMA_INVALID`, `EVENT_ORDER_INVALID`,
`POLICY_DIGEST_MISMATCH`, `UNKNOWN_EVENT_TYPE`, `EVIDENCE_CLAIM_MISMATCH`,
`GUARD_REFERENCE_MISMATCH`, `HUMAN_REFERENCE_MISMATCH`,
`REQUEST_REFERENCE_MISMATCH`, `DUPLICATE_STABLE_ID`.

### 6.1 Referentielle Integrität (Korrekturdelta v0.1a)

- **Evidence-Claim-Bindung:** Jede von einem `TransitionRequest` referenzierte
  `EvidenceRelation` muss an denselben Claim gebunden sein
  (`relation.claim_id == request.claim_id`). Abweichung → `STOP` mit
  `EVIDENCE_CLAIM_MISMATCH`; keine automatische Umhängung. Die Prüfung greift
  in der Guard-Bewertung, in `validate_evidence_relations(..., claim_id=...)`
  und beim Replay von `TRANSITION_REQUESTED`.
- **Exakte Retag-Referenzen:** Ein `CLAIM_RETAGGED` muss beim Replay das
  vollständige Feldschema tragen und an genau die referenzierte
  `GuardDecision` (`guard_decision_id` existiert, gehört zum Request, ist
  `PROPOSE`) und genau die referenzierte `HumanDecision` (`human_decision_id`
  existiert, gehört zum Request, ist `APPROVE`) gebunden sein. Ein beliebiger
  anderer PROPOSE-Guard für den Request genügt nicht. Abweichung →
  `GUARD_REFERENCE_MISMATCH` bzw. `HUMAN_REFERENCE_MISMATCH`, Event wird
  quarantänisiert, der Claim-Tag bleibt unverändert.
- **Request-Bindung und frische Guard-Prüfung:** `claim_id`, normalisierte
  `from_tag`/`to_tag` und `visibility` des Retags müssen exakt dem gespeicherten
  `TransitionRequest` entsprechen (`REQUEST_REFERENCE_MISMATCH` sonst). Ein
  gespeichertes `PROPOSE` wird vor der Mutation aus aktuellem Replay-Zustand
  und geladener Policy neu berechnet. Nur ein identisches frisches `PROPOSE`
  darf angewendet werden; ein historischer oder manipulierter Guard ist keine
  Autorität.
- **Digest-Bindung des Retags:** `retag.policy_digest` muss dem Digest der
  referenzierten GuardDecision entsprechen; ist zusätzlich eine Policy
  geladen, auch deren Digest. Bei Drift wird das Retag-Event nicht angewendet
  (`POLICY_DIGEST_MISMATCH`, sichtbar unter `rejected_events`) — eine Warnung
  allein genügt nicht. Ein GuardDecision-Event mit abweichendem Digest bleibt
  als historischer Datensatz gespeichert und wird mit Warnung markiert.
- **ID-Eindeutigkeit:** `material_id`, `claim_id`, `relation_id`,
  `request_id`, Guard-`decision_id`, Human-`decision_id` und `retraction_id`
  sind je Eventstream eindeutig. Wiederverwendung überschreibt nie den
  vorhandenen Replay-Datensatz; das zweite Event landet mit
  `DUPLICATE_STABLE_ID` unter `rejected_events`. Unterschiedliche
  HumanDecision-IDs für denselben Request bleiben als append-only
  Entscheidungsgeschichte zulässig.
- **Human-Approve-Grenze:** `APPROVE` gilt nur als anwendbare Freigabe, wenn
  für denselben Request eine konkrete `GuardDecision(PROPOSE)` existiert.
  `REJECT`, `DEFER` und `WITHDRAW` dürfen auch ohne anwendbares Proposal als
  Entscheidungsgeschichte aufgezeichnet werden.

Menschliche Erläuterungen sind optionaler Freitext außerhalb des kontrollierten
Reason-Code-Slots.

## 7. Zwölf Invarianten

Nummerierung identisch mit `tests/ethics/test_erk_invariants.py`
(`test_invariant_01_...` bis `test_invariant_12_...`):

1. **Policy is not truth** — eine erlaubte Policy-Kante führt nie allein zum Retagging.
2. **Human approval required** — jedes tatsächliche Retagging benötigt ein passendes HumanDecision-Approve.
3. **Metaphor is not evidence** — Metapher oder Rosetta darf keine Promotion begründen.
4. **Provenance is not evidence** — Materialpointer und Ledger-Receipt beweisen keinen Claim.
5. **VOID is valid** — ein Claim darf unbegrenzt in `[VOID]` verbleiben.
6. **Retraction is append-only** — Rücknahme löscht oder überschreibt keine Historie.
7. **Guard state is not claim state** — `PROPOSE/HOLD/STOP` verändert den Claim-Tag nicht.
8. **Untrusted stays bounded** — untrusted Material führt niemals direkt zu Retagging.
9. **Consent fails closed** — fehlender erforderlicher Consent erzeugt HOLD oder STOP.
10. **Replay is deterministic** — identischer Stream plus identische Policy ergibt identischen State-Digest.
11. **Public export is reduced** — private und unbekannte Felder fehlen vollständig im Export.
12. **Policy drift is visible** — ein Digest-Wechsel wird erkannt und nie still akzeptiert.

## 8. Replay-Semantik

„Deterministischer Replay" bedeutet in v0.1a ausschließlich:

> Derselbe persistierte, gleich geordnete Eventstream und dieselbe Policy-Version
> erzeugen denselben `ReplayState`, denselben Reduced Export und denselben
> `state_digest`.

Nicht behauptet wird: dass erneutes Ausführen derselben Befehle identische UUIDs
erzeugt; dass neu erzeugte Ledger-Events identische Zeitstempel besitzen; dass
Ledger-Hash und State-Digest dieselbe Funktion haben.

Der `state_digest` entsteht aus einer kanonisch sortierten JSON-Darstellung des
rekonstruierten Zustands (ohne volatile Felder wie Laufzeit oder Objektadressen).
Wenn der Aufrufer keine historische Policy übergibt, lädt Replay verpflichtend
die Repository-Policy; einen policy-freien Retag-Pfad gibt es nicht.

Unzulässige Reihenfolgen (Retagging vor Claim-Erstellung, HumanDecision für
unbekannten Request, Transition ohne GuardDecision, Approve nach Withdrawal,
Retag ohne Human-Approve) werden fail-closed als `rejected_events` sichtbar
quarantänisiert. Keine stillen Reparaturen.

## 9. Privacy-Reduktion

`reduce_public_export()` arbeitet mit expliziter Allowlist. Standardmäßig nicht
exportiert: `claim_text`, private Locator, private Source-Pfade, biographische
Herkunft (`origin`), Gesprächsauszüge, Actor-Details, unbekannte Zusatzfelder,
Rohmaterial, interne Notes — und **rohe interne IDs** (`claim_id`,
`material_id`, `request_id`, `decision_id`, `retraction_id`).
Records mit `visibility: private` werden vollständig ausgelassen; auch Anzahl,
Tag, Materialart oder Zustandsänderung dieser Records werden nicht exportiert.

Beziehungen innerhalb eines Exports werden über **exportlokale Referenzen**
dargestellt (z.B. `claim:c001`, `material:m001`, `request:q001`, `guard:g001`,
`retraction:r001`). Diese Referenzen entstehen deterministisch aus der
kanonisch sortierten Reihenfolge der internen Records — sie werden nicht aus
dem Rohwert gehasht und behaupten keine Anonymität. Zwei Exporte desselben
`ReplayState` sind identisch. Kann eine Beziehung nicht ohne Roh-ID
dargestellt werden, wird sie weggelassen statt durchgereicht.

Exportierbar sind nur: Schema-Version, exportlokale Referenzen, Claim-Tag,
geschlossene Statuswerte, Retraction-Status, reduzierte Materialart (`kind`
aus geschlossenem Vokabular oder `other`, normalisiertes `trust`), erlaubte
Reason-Codes und Policy-Version/-Digest. `export_digest` bindet nur diese
reduzierte Projektion. Der private `state_digest` wird nicht veröffentlicht,
weil er sonst Änderungen im privaten Zustand beobachtbar machen würde.

Ein Hash wird nicht als Anonymisierung behauptet: Digests im Export sind
Integritätsverweise. Wenn eine Eingabe bekannt ist, ist ihr Digest
rekonstruierbar — der Export lässt private Felder deshalb ganz weg, statt sie
nur zu hashen.

### 9.1 Integrität ≠ Authentizität ≠ Autorisierung ≠ Wahrheit

Diese vier Begriffe sind im Kernel strikt getrennt:

| Begriff | Was der Kernel leistet | Was er nicht leistet |
|---|---|---|
| **Integrität** | Ledger-Hash-Chain ist tamper-evident innerhalb dokumentierter Annahmen: nachträgliche Veränderung der Aufzeichnung wird erkennbar. | Der Hash beweist nicht Authentizität, Autorenschaft oder Wahrheit. |
| **Authentizität** | — | `human_actor` is an asserted actor label, not authenticated human identity. Der Kernel authentifiziert niemanden; es gibt keine Signatur- oder Identitätsprüfung in v0.1a. |
| **Autorisierung** | Ein Retagging erfordert ein explizites `HumanDecision(APPROVE)`-Event, gebunden an genau einen Request, Guard und Policy-Digest. | Der Kernel prüft nicht, ob die Person hinter dem Label berechtigt war, das Event zu erzeugen. |
| **Wahrheit** | — | Kein Event, Hash, Digest oder Tag macht einen Claim wahr (SoT is not a truth-maker). |

## 10. Policy-Digest und Drift

Beim Laden erfasst der Kernel Version und SHA-256-Digest der ungeänderten
Policy-Datei. Jede `GuardDecision` trägt beide Werte. `apply_approved_transition()`
verweigert fail-closed (`POLICY_DIGEST_MISMATCH`), wenn der Digest seit der
Guard-Entscheidung gewechselt hat; `replay_events()` macht abweichende Digests
als Warnung sichtbar. Drift wird nie still akzeptiert.

## 11. Abgrenzung zu anderen Übergangssystemen

Drei verschiedene Übergangsbegriffe im Projekt sind **nicht** gleichzusetzen:

| System | Übergang | Rolle |
|---|---|---|
| Claim-Tag-Transition (dieser Kernel) | z.B. `[HYPOTHESE] → [MODEL]` | epistemischer Repo-Status |
| tesser3TAKT Review-Transition | `PASS \| HOLD \| LOOP \| STOP` | lokale Navigations-/Reviewentscheidung |
| UI BoundaryTransition (PR #312) | `EXIT → ENTRY` | UI-lokaler Frame-/Grenzvertrag |

v0.1a implementiert ausschließlich Claim-Tag-Transition-Proposals und deren
Human-Decision-Kette. Keine der anderen Transitionen wird importiert oder
dupliziert; ihre Typen werden weder kopiert noch als Core-Typen neu definiert.

## 12. Spätere Adapterpunkte (dokumentiert, nicht gekoppelt)

- Ein Bridge-Record der Dual-Format Claim Bridge könnte als `MaterialRef` plus
  `EvidenceRelation(MOTIVATES|CONTEXTUALIZES)` abgebildet werden.
- Eine tesser3TAKT-HOLD-Entscheidung könnte als externes Guard-Signal
  referenziert werden (eigener Adapter, kein Core-Typ).
- Ein UI-Adapter für PR-#312-Frames müsste `BoundaryTransition` außerhalb von
  `src/core/` übersetzen.

Alle Kopplungen erfolgen ausschließlich über separate, später zu genehmigende
Adapter.

## 13. Rücknahme und Deaktivierung

- Ein genehmigter Übergang wird durch `HumanDecision(WITHDRAW)` (vor Anwendung)
  oder `Retraction` (nach Anwendung) zurückgenommen — beides append-only, nichts
  wird gelöscht oder überschrieben.
- Der Kernel selbst ist ANNEX: Er kann durch Entfernen der Aufrufe deaktiviert
  werden, ohne GOLD-Bereiche, Policies oder Receipts zu berühren.
- Bereits geschriebene Events bleiben als Historie bestehen (G3: nie löschen).

## 14. Bekannte Grenzen

- Kein Action-Gate; der Kernel führt nichts aus.
- `tools/claim_lint.py` ist nicht angeglichen; Linter-Vokabular ≠ Register-Vokabular
  (siehe `docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md`).
- Consent wird nur als Claim-Status (`CONSENT_MISSING`/`CONSENT_REVOKED`)
  modelliert, nicht als eigenes Consent-Registry.
- `human_actor` ist eine nicht authentifizierte Rollenbehauptung; es gibt
  keine kryptografische Identitätslösung in v0.1a (siehe §9.1).
- Die Policy ist ein Draft-Register ([SPEC-WIP]); ihre Kanten sind syntaktische
  Nachbarschaft, keine inhaltliche Freigabe.
- Replay validiert Reihenfolge und Struktur, nicht die inhaltliche Qualität von
  Evidenz — das bleibt menschliche Review-Arbeit.
- Der Ledger beweist Integrität der Aufzeichnung, nicht die Wahrheit des
  Aufgezeichneten.
