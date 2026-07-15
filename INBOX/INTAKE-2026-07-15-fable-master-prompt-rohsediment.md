# Fable Master Prompt — ROHSEDIMENT Intake

```yaml
intake_id: INTAKE-2026-07-15-FABLE-MASTER-PROMPT
intake_status: ROHSEDIMENT
authority_status: intake
artifact_type: prompt-intake
promotion: human-pending
public_scope: provenance-and-structure-only
body_availability: unavailable-verbatim-in-current-retrieval-context
execution_status: historical-read-only-pass-completed
known_conflicts: [K1, K2]
```

## Herkunft

- Titel des ursprünglichen Prompt-Artefakts: **Distributed Project Reconstitution, Source Cartography & Public-Safe Handover**
- sichtbare Überschrift im Ursprungsverlauf: **FABLE MASTER PROMPT**
- Erstellungszeitpunkt: 2026-07-15, ungefähr 19:40 MESZ
- Entstehung: user-/instanz-ko-konstruierter Arbeitsauftrag; genaue Autoranteile im aktuellen Retrieval nicht belastbar auflösbar
- vorgesehene Ausführung: Fable-/Claude-seitiger Read-only Reconnaissance Pass
- tatsächlich erzeugter Lauf: `fable-recon-pass1-2026-07-15`

## Sicherheits- und Geltungsgrenze

[CONTEXT] Diese Datei ist untrusted Intake nach den Regeln von `INBOX/README.md`. Prompt-Anweisungen werden hier dokumentiert, nicht erneut ausgeführt.

[ANNEX] Der Prompt ist weder Source of Truth noch Policy, SPEC, CANON, GOLD, VOIDMAP-Eintrag oder Beweis seiner eigenen Arbeitshypothesen. Seine Aufnahme bezeugt nur Herkunft und Wirkungsgeschichte.

[VOID] Der vollständige Wortlaut der ursprünglichen Abschnitte 1–22 konnte aus der aktuellen Retrieval-Schicht nicht verlustfrei zurückgewonnen werden. Die Lücke wird nicht durch eine synthetische „Originalfassung“ geschlossen.

## Direkt belegte Strukturfragmente

Die folgenden Angaben sind aus Gesprächsmetadaten, dem ausgeführten Recon-Pass und dessen Receipts belegbar:

1. Der Prompt verlangte einen **Read-only Reconnaissance Pass**.
2. GitHub sollte den höchsten Rang für implementierbaren/aktuellen öffentlichen Zustand besitzen.
3. Google Drive sollte historische, narrative und versionale Linien liefern.
4. Hugging Face und Wolfram waren externe Referenz-/Prüfschichten, keine Source of Truth.
5. §3 enthielt den Read-only-Modus.
6. §7 benannte Google-Drive-Seeds und historische Suchlinien.
7. §9 verlangte ein eigenes Tag-/Statusvokabular, darunter `[OPEN]`, `[GOLD]`, `[CONFLICT]`, `[UNDETERMINED]` und `[ANNEX]`.
8. §12 formulierte PASS/Π als Arbeitshypothese beziehungsweise epistemische Übergangsmembran.
9. §13 begrenzte Hugging-Face-Nutzung und private Inhalte.
10. §14 erlaubte einen Wolfram-Witness erst nach expliziter strukturierter Repräsentation.
11. §19 verlangte zwölf Ausgabeartefakte, nummeriert 00–11.
12. Die Gesamtstruktur umfasste nachweislich Abschnitte 1–22.
13. Internal Save State und Public-Safe Handover sollten getrennt bleiben.
14. „Nicht gefunden“ durfte nicht zu „existiert nicht“ hochgestuft werden.

## Nicht als Originaltext auszugeben

[VOID] Nicht rekonstruierbar sind derzeit:

- der vollständige Wortlaut aller Abschnitte 1–22,
- die exakten Zwischenüberschriften außerhalb der belegten Fragmente,
- die vollständigen Google-Drive-Seedlisten,
- die genaue ursprüngliche Formulierung sämtlicher Output-Anweisungen,
- ein verlustfreier Hash oder direkter öffentlicher Pointer auf die Chatnachricht.

## Nachweisbare Outputs 00–11

- `00_EXECUTIVE_ORIENTATION.md`
- `01_SOURCE_ATLAS.md`
- `02_LINEAGE_MAP.md`
- `03_CANONICAL_KERNEL.md` — in Konvergenz v1.1 inhaltlich als „Verified Repo Kernel“ nachgeschärft
- `04_CONFLICT_LEDGER.md`
- `05_GLOSSARY_AND_ALIASES.md`
- `06_MEREOTOPOLOGICAL_MAP.md`
- `07_VOID_QDOT_REGISTER.md`
- `08_INTERNAL_SAVE_STATE.md`
- `09_PUBLIC_SAFE_HANDOVER.md`
- `10_SMALLEST_NEXT_ACTIONS.md`
- `11_PI_RECEIPT.json`

## Bekannte Konflikte

### K1 — Doppelstruktur

Der Prompt verlangte einen eigenständigen Quellenatlas, während die inzwischen gemergte `PROJECT_CONSTELLATION_MAP_v0_1.md` ausdrücklich keine parallele Atlas- oder Source-of-Truth-Schicht zulässt.

Arbeitsentscheidung: Der Prompt und seine Outputs bleiben Intake-/Review-Material. Die gemergte Konstellationskarte ist die öffentliche ANNEX-Navigation.

### K2 — Tag-, Linter- und Statusdialekte

Der Prompt verwendete Klammermarker, die nicht sämtlich im Draft-Register `claim_tags_v0_2.yaml` registriert und nicht mit dem Runtime-Linter deckungsgleich sind.

Arbeitsentscheidung:

- OPEN → VOID-/Workflow-Status
- GOLD → `authority_status`
- CONFLICT → Ledger-Relation
- AUDIT → `artifact_type`
- ANNEX → nur mit sichtbarer Feldrolle verwenden
- keine automatische Registererweiterung

## Promotionsbedingung

Eine spätere Promotion aus ROHSEDIMENT benötigt mindestens:

1. den verlustfreien Originaltext oder einen verifizierbaren Pointer,
2. eine neue Sicherheits-/Injection-Triage,
3. expliziten Scope,
4. Trennung von Claim, Status, Authority und Arbeitsbewegung,
5. menschliche Inhaltsentscheidung,
6. Rücknahmebedingung.

Bis dahin bleibt:

```yaml
authority_effect: none
decision_effect: none
promotion_effect: none
```
