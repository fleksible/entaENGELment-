# LEAN_CROSSWALK_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** none (kein Lean-Lauf, keine CI-Pflicht)
**Human-Decision-Boundary:** required
**Datum:** 2026-11-21
**Modul:** `src/core/lean_crosswalk.py`
**Herkunft:** ATLAS-CROSSWALK-LEAN-001 v0.3 (außerhalb des Repos erstellt), hier korrigiert
**Lean-Status:** NOT_RUN

---

## 1. Zweck

[SPEC-WIP] Der Lean-Crosswalk übersetzt die Ausgabe von Leans `#print axioms`
in ein sichtbares Urteil je Deklaration. Er unterscheidet, **welche Art von
Offenheit** vorliegt, damit ein fehlender Beweis, eine bewusst gesetzte
Zusatzannahme und ein gescheiterter Lauf nie unter demselben Namen erscheinen.

[SPEC-WIP] Er führt Lean nicht aus und entscheidet nichts, was dem Menschen
vorbehalten ist.

## 2. Nicht-Ziele

- keine Aussage darüber, ob eine Lean-Deklaration meint, was ein Mensch behauptet,
- keine Claim-Promotion, kein Kanon, keine VOIDMAP-Änderung,
- kein Schutz gegen bösartigen Lean-Meta-Code (die getrennte Prüfdatei ist eine Hygienegrenze),
- keine Z3-Abhängigkeit (der frühere Z3-Nachweis zu v0.2 bleibt außerhalb des Repos),
- keine automatische Umetikettierung bestehender Einträge (z. B. Kη-03).

## 3. Sieben Status in Vorrangordnung

Oben gewinnt. Die Liste steht genau einmal im Code (`STATUSES`).

| Status | Sichtbare Art | Deckel | Bedeutung |
| --- | --- | --- | --- |
| `RUN_FAILED` | `NO_VERDICT` | `NONE` | Lean-Prozess nicht erfolgreich beendet; Ausgabe wird nicht gelesen |
| `HOLD_INVALID_EVIDENCE` | `NO_VERDICT` | `NONE` | Format, Hash, Metadaten oder Vollständigkeit nicht belastbar |
| `HOLD_DECL_MISSING` | `NO_VERDICT` | `NONE` | erwartete Deklaration fehlt in der Ausgabe |
| `HOLD_DECL_DUPLICATE` | `NO_VERDICT` | `NONE` | erwartete Deklaration erscheint mehrfach |
| `OPEN_OBLIGATION` | `PROOF-VOID` | `FORMAL` | hängt direkt oder transitiv von `sorryAx` ab, auch wenn zugleich Fremdaxiome auftreten |
| `HOLD_TRUST_BOUNDARY` | `PROOF-DEPENDENCY` | `FORMAL` | kein `sorryAx`, aber mindestens ein nicht freigegebenes Axiom |
| `FORMAL_CLOSED` | `FORMAL-PROOF` | `FORMAL` | nur `propext`, `Classical.choice`, `Quot.sound` oder gar keine Axiome |

[SPEC-WIP] Axiomnamen werden exakt verglichen: `Foo.propext` ist nicht
`propext`. Jedes andere Axiom ist fremd, auch die `native_decide`-Axiome
älterer (`Lean.ofReduceBool`, `Lean.trustCompiler`) und neuerer Lean-Versionen
(ein eigenes Axiom je Aufruf).

[SPEC-WIP] Im Mischfall (`sorryAx` und Fremdaxiom) lautet das Urteil
`OPEN_OBLIGATION`; die Fremdaxiome bleiben als `foreign_axioms` im Urteil erhalten.

[SPEC-WIP] **`FORMAL_CLOSED` heißt nicht wahr.** Es heißt: Diese Lean-Deklaration
ist unter den Standardaxiomen bewiesen. Ob sie die menschliche Aussage trifft,
bleibt als `semantic_reentry: SEPARATE_UNREVIEWED` eine eigene, offene Prüfung.

## 4. Zwei getrennt prüfbare Grenzen

1. **Rohausgabe → Urteil** (`audit_raw`, `parse_print_axioms`): Exit-Code zuerst.
   Gelesen werden nur die dokumentierten Zeilenformen
   (`'X' depends on axioms: [a, b]`, `'X' does not depend on any axioms`,
   wahlweise mit Positionspräfix). Unbekannte Zeilen, umgebrochene Listen und
   unerwartete Deklarationen machen die ganze Ausgabe unbrauchbar.
   [SPEC-WIP] Bisher nur gegen handgeschriebene Proben geprüft
   (FIXTURE_ONLY / NOT_KERNEL_VERIFIED).
2. **Urteil → sichtbare Karte** (`build_card`, `validate_card`): Die Karte wird
   gegen Urteil und Herkunfts-Hash geprüft (Status, Art, Deckel, Reentry,
   Herkunft, Axiomliste, Zusammenfassung, Prosa-Markierung).

## 5. Zusammenfassung und freier Text

[SPEC-WIP] Die Zusammenfassung einer Karte kommt fest aus einer Vorlage je
Status und muss ihr genau entsprechen. Freier Text darf nur im Feld `notes`
stehen und bleibt `UNVERIFIED_PROSE`; er wird nicht inhaltlich geprüft und
nicht durch Stichwortsuche bewertet. Freier Text im Zusammenfassungsfeld führt
zu `UNVERIFIED_SUMMARY`.

## 6. Prüfvorgaben

Die Tabellen unter `tests/fixtures/lean_crosswalk/tables/` sind von Hand
gesetzt und werden nie aus dem Code erzeugt:

| Tabelle | Umfang |
| --- | --- |
| `derivation_truth_table.csv` | 24 Kombinationen aus Lauf × Deklarationsanzahl × sorryAx × Fremdaxiom (aus v0.3 unverändert) |
| `evidence_preflight_table.csv` | 16 Kombinationen der Vorprüfung |
| `audit_matrix.csv` | 7 × 7 erwarteter × sichtbarer Status |
| `audit_negative_cases.csv` | 7 Status × 8 Verfälschungen = 56 Fälle |

## 7. Lean-Testfälle

`tests/fixtures/lean_crosswalk/lean/` ist ein Lake-Projekt mit den Fällen A–E
(`CrosswalkProbe/Basic.lean`) und einer getrennten Prüfdatei
(`CrosswalkProbe/Audit.lean`). Toolchain-Pin `leanprover/lean4:v4.35.0`
(nicht gegen eine echte Installation geprüft).

Erster echter Lauf, sobald eine Lean-Umgebung verfügbar ist:

```bash
cd tests/fixtures/lean_crosswalk/lean
lake build
lake env lean CrosswalkProbe/Audit.lean > audit_stdout.txt; echo $?
```

Danach `audit_raw(exit_code, stdout, expected_decls)` gegen diese Ausgabe;
Befund mit `lean --version`, genauem Aufruf und Hashes von Quelle und Ausgabe festhalten.

## 8. Offene Punkte

- [ANNEX] HOLD: Erster echter Lean-Lauf; bis dahin ist der Leser für die Rohausgabe unbelegt.
- [ANNEX] HOLD: Ob die Kommandozeile ein Positionspräfix ausgibt und ob lange Axiomlisten umbrechen.
- [ANNEX] HOLD: Verständlichkeitstest: ob Menschen mathematische Aussagen durch die Karten besser verstehen, ist ein eigener Forschungsstrang.
