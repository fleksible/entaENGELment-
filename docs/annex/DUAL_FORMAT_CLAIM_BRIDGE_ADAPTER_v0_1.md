# DUAL_FORMAT_CLAIM_BRIDGE_ADAPTER_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** partial (nur was der Adapter beim Aufruf prüft)
**Promotion-Effect:** none
**Human-Decision-Boundary:** required
**Modul:** `src/core/evidence_bridge_adapter.py`
**Source:** Synthbiosis Systematlas v1.1 / `01_DUAL_FORMAT_CLAIM_BRIDGE.md`
(Bundle-Witness: `INBOX/INTAKE-2026-07-21-synthbiosis-system-atlas-v1_1.md`;
Feld-Mapping: `docs/annex/SYNTHBIOSIS_MODULE_ADAPTER_MAP_v0_1.md` §2.1)
**Validation-Refresh:** 2026-07-26 (Post-Merge-Hardening nach PR #325)

```yaml
source_relation:
  relation: reduced_public_adapter
  source_identity: not_claimed
  semantic_equivalence: not_claimed
  known_loss_required: true
```

---

## 1. Zweck

Eine **Brücke** überträgt genau *eine* benannte Eigenschaft aus einem
Quellregister in ein Zielregister — unter sichtbarem Verlust. Der Adapter
übersetzt einen solchen Bridge-Record in Vorschlagsobjekte des Evidence
Routing Kernel:

```
BridgeRecord → MaterialRef + EvidenceRelation (+ optional ClaimCandidate)
```

[ANNEX] Der Adapter ist **reine Übersetzung**. Er emittiert kein Ledger-Event,
schreibt keine Datei, öffnet keine Verbindung und verändert keinen Claim-Tag.
Ob und wann die Vorschläge in einen Eventstream gelangen, entscheidet der
Aufrufer — und dort greifen Guard und `HumanDecision` unverändert.

## 2. Was eine vollständige Brücke beantworten muss

Die Pflichtfelder entsprechen den sechs Brückenfragen des Quellmoduls:

| Frage | Feld |
|---|---|
| Was ist die Quellform? | `source_register` + `source_pointer` + `source_digest` |
| Welche *einzelne* Eigenschaft wird übertragen? | `transferred_property` |
| Welche Relation soll erhalten bleiben? | `preserved_relation` |
| Was geht verloren? | `known_loss` (mindestens ein Eintrag) |
| Woran würde die Brücke scheitern? | `falsifier` |
| Wie wird sie zurückgenommen? | `rollback` |

[FACT] Fehlt eines dieser Felder, verweigert der Adapter die Übersetzung
(`BridgeAdapterError`, fail-closed). Insbesondere ist `known_loss` **Pflicht**:
Eine Brücke ohne benannten Verlust behauptet implizit Verlustfreiheit — und
damit Identität zwischen den Registern.

## 3. Registerreichweite (Kernregel)

[MODEL] Wie weit ein Quellregister relational reichen darf, ist strukturell
begrenzt. Promotionsfähig sind im Kernel nur `SUPPORTS`, `MEASURES` und
`IMPLEMENTS`.

| Quellregister | Entscheidung für v0.1 | spätere Öffnung |
|---|---|---|
| `myth`, `metaphor` | **nie** promotionsfähig | unverändert — Metapher ist keine Evidenz (Invariante 3) |
| `psychological` | **nie** promotionsfähig | unverändert — keine Diagnose, kein Claim über eine Person |
| `ui` | **nie** promotionsfähig | unverändert — ein UI-Frame ist kein Wahrheitszeuge |
| `formal` | nur Kontext/Provenienz | `SUPPORTS`/`IMPLEMENTS` erst mit formalem Review-Witness und gebundener Zieldomäne; **niemals pauschal** `MEASURES` |
| `governance` | nur `CONTEXTUALIZES`, `MOTIVATES`, `PROVENANCE_ONLY` | höchstens `IMPLEMENTS` innerhalb explizit dokumentierter Authority-/Scope-Grenzen |
| `physical`, `biological` | `CONTEXTUALIZES`, `MOTIVATES`, `PROVENANCE_ONLY` ohne M5; `SUPPORTS`, `MEASURES`, `IMPLEMENTS` nur mit `m5_review_pointer`; `CONTRADICTS` ist in v0.1 nicht geöffnet | unverändert |

[FACT] Diese Matrix ist als geschlossenes, registerbezogenes Vokabular
implementiert. Dass eine Relation im Kernel bekannt oder nicht
promotionsfähig ist, reicht nicht: `CONTRADICTS` darf beispielsweise nicht aus
einem Bridge-Record am Register-Gate vorbeilaufen. Da v0.1 dafür in keinem
Register eine explizite Öffnungsbedingung definiert, wird die Relation überall
abgelehnt.

[FACT] **In v0.1 ist damit kein Register ohne dokumentiertes Gate
promotionsfähig.** Der Grund liegt im Kernel: `evaluate_transition_request()`
prüft für `PROPOSE` strukturell nur, ob die Relation promotionsfähig ist, ob
die Materialart keine Metapher ist und ob Trust nicht `UNTRUSTED` lautet. Ein
`REVIEWED`-Governance-Dokument könnte dort sonst mit `MEASURES` ein
strukturell grünes Signal erhalten, das seine Reichweite überschätzt — es
promoviert zwar nicht autonom (die `HumanDecision` bleibt), aber das Signal
wäre irreführend.

[INFERENZ] Für `formal` fehlt dem Record derzeit die entscheidende
Unterscheidung: Er kennt weder `target_register`/`claim_domain` noch einen
formalen Review-Pointer und kann deshalb „Beweis einer Grapheneigenschaft"
nicht von „Formel stützt Behauptung über die Welt" trennen. Bis diese Bindung
existiert: Kontext, nicht Promotion.

[FACT] Ein Verstoß führt zum **Abbruch, nicht zur Degradierung** — auch nicht
zu einer sichtbaren. Eine automatische Abstufung wäre keine Übersetzung mehr,
sondern eine Entscheidung: Der Aufrufer sagte `MEASURES`, der Adapter
erzeugte `CONTEXTUALIZES`. Stattdessen nennt der Fehlertext die zulässigen
Relationstypen und weist darauf hin, dass ein **Mensch** einen neuen,
ausdrücklich anders lautenden Record einreichen kann.

Zusätzlich setzt der Adapter für mythische und metaphorische Register die
Materialart auf `metaphor`. Damit greift der Kernel-Guard
(`NON_EVIDENCE_MATERIAL_KINDS`) **unabhängig vom Adapter** — die Grenze hält
auch dann, wenn jemand den Adapter umgeht und das Material direkt registriert.

## 4. Der Kontext überlebt die Übersetzung

[FACT] `BridgeTranslation` trägt einen unveränderlichen `BridgeContext` mit den
sechs Brückenantworten plus `m5_review_pointer`. Er erscheint auch in
`to_dict()`.

Ohne ihn wäre die Übersetzung eine Behauptung ohne Beschriftung: Man sähe die
Relation, aber weder die übertragene Eigenschaft noch den Verlust, den
Falsifikator, den Rücknahmeweg — und bei physischen Registern auch nicht, **aus
welchem Grund das M5-Gate passiert werden durfte**. Ein validierter und danach
verworfener `known_loss` widerspricht der Regel „Known Loss muss sichtbar
bleiben" direkt.

`known_loss` wird intern als Tupel geführt. Ein blanker String wird abgelehnt:
Er ist iterierbar und ginge sonst zeichenweise als Liste durch.

## 5. Weitere Grenzen

- **Kein Rohinhalt:** Es gehen nur `source_pointer`, `source_digest` und
  Metadaten weiter. Der Quellausdruck selbst wird nie übernommen.
  `source_digest` ist Pflichttext.
- **`protected_origin`** setzt die Sichtbarkeit auf `private` — nach unten,
  nie nach oben.
- **Trust-Default `UNTRUSTED`** (G5). Untrusted Material kann keine
  Promotionsfähigkeit erzeugen.
- **Verbotene Tags:** Der Adapter vergibt `[FACT]`, `[SPEC]` und `[CANON]`
  niemals selbst — auch nicht über einen Alias wie `[FAKT]`. Ein
  `ClaimCandidate` trägt höchstens ein Einstiegstag; jede Höherstufung läuft
  über Guard und `HumanDecision`. Sobald ein Candidate vorgeschlagen wird, ist
  eine geladene `ClaimPolicy` Pflicht; ohne Policy fällt der Adapter
  fail-closed aus, statt Alias-/Unknown-Tag-Prüfung zu überspringen.
- **Claim-Bindung:** Ohne neuen `ClaimCandidate` ist eine nicht-leere
  `claim_id` Pflicht. Mit Candidate ist nicht-leerer `claim_text` Pflicht; nur
  auf diesem Pfad darf die Claim-ID deterministisch aus `bridge_id` abgeleitet
  werden.
- **Identität und Attribution:** `bridge_id` und `actor` müssen nicht-leere,
  kanonische Strings ohne Rand-Whitespace sein. Das gilt ebenso für Claim-ID,
  Quell-/Digest- und M5-Pointer. So kollidieren keine anonymen oder optisch
  identischen IDs und es entstehen keine ERK-Vorschläge mit ungültiger
  Attribution.
- **Schema-Pin:** Nur `bridge.v0.1` wird interpretiert. Zukünftige oder
  unbekannte Versionen werden nicht still unter v0.1-Semantik umgedeutet.
- **Geschlossenes Feldschema:** Unbekannte Felder im Eingabe-Mapping werden
  mit `UNKNOWN_FIELD`, fehlende Pflichtfelder mit `MISSING_REQUIRED_FIELD`
  abgelehnt. Mapping-Intake akzeptiert nur ein eingebautes `dict`, damit ein
  frei implementiertes Mapping beim Lesen keinen Aufrufercode ausführen kann.

## 6. Zwei getrennte Befundvokabulare

[ANNEX] Der Adapter braucht Begriffe für Übersetzungsfehler, die der Kernel
nicht kennt. Diese leben in einem **eigenen** Enum `BridgeReason` und
erscheinen ausschließlich im Rückgabeobjekt (`BridgeTranslation.notes`) oder in
der Fehlermeldung.

Sie werden **nie** in ein Event, nie in `EvidenceRelation.reason_codes` und nie
in einen Claim geschrieben. Für alles, was der Kernel bereits benennt
(`METAPHOR_IS_NOT_EVIDENCE`, `PROVENANCE_IS_NOT_EVIDENCE`,
`UNTRUSTED_MATERIAL`), verwendet der Adapter dessen `ReasonCode` unverändert.
Ein Test hält diese Trennung fest.

[CONTEXT] `BridgeReason` ist kein Projektstatus, kein Claim-Tag und keine
Entscheidungsleiter — es ist adapter-lokal, wie `HOLD` im Change-Gate
gate-lokal ist.

## 7. Verhältnis zu den anderen Modulen

**M1 ↔ ERK:** Der Adapter erzeugt Vorschläge; der Kernel entscheidet über
Struktur (Guard) und der Mensch über Geltung (`HumanDecision`). Der Adapter
kann keine `HumanDecision` synthetisieren und nichts retaggen.

**M1 ↔ M5:** `falsifier` ist im Bridge-Record Pflicht, wird aber vom Adapter
nur auf Vorhandensein geprüft. Ob er trägt, entscheidet das Research Gate
(`docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md`). Physische und biologische
Register brauchen für Promotionsfähigkeit einen dokumentierten
`m5_review_pointer`.

**M1 ↔ tesser3TAKT:** Keine Berührung. Der Adapter kennt kein
Navigationsvokabular und übersetzt keines.

## 8. Known Loss

- Der Adapter prüft **Struktur, nicht Inhalt**: ob eine behauptete Relation
  sachlich trägt, entscheidet er nicht.
- Die vier Minimaltests des Quellmoduls (Josephson–Jesus, 7×9–Yggdrasil,
  RCC-8–Photonik, „Liebe"–HRV) sind als Tests umgesetzt, nicht als
  JSONL-Fixtures.
- Eine menschenlesbare Anzeige, die Quelle, Status, Verlust und Rücknahme
  gleichzeitig zeigt, bleibt offen — sie ist im Quellmodul das
  Exit-Kriterium für Implementierungsreife.
- Die Registerliste ist ein erster Schnitt und braucht menschliche
  Bestätigung.

## 9. Rücknahme

Modul, Test und dieses Dokument nach `NICHTRAUM/archive/` verschieben und den
additiven Export-Block in `src/core/__init__.py` zurücknehmen (G3). Kein
bestehendes Modul importiert den Adapter; der Kernel bleibt unverändert
lauffähig.

## 10. Offene Punkte

- [ ] ☐ Menschenlesbare Bridge-Anzeige (Exit-Kriterium des Quellmoduls).
- [ ] ☐ Ein Aufrufpfad, der Vorschläge tatsächlich als Events schreibt, ist
      bewusst nicht Teil dieser Phase.
- [ ] ☐ Bestätigung der Register-zu-Relationstyp-Matrix.
