# Report: Hospitality Entry Slice v0.1

**Datum:** 2026-09-23  
**Fokus:** Gastfreundlicher Repo-Einstieg

## Ziel

Die öffentlichen Einstiegspunkte des Repositories so setzen, dass nicht-technische
Leser ohne Kompetenzbeweis, Rollenwahl oder Zustimmung zur Projektdeutung eintreten
können, ohne Governance-, Test- oder Sicherheitsgrenzen abzuschwächen.

## Aktionen

- [x] `README.md` als Haustür neu gesetzt: Lesen vor Installieren/Beitragen.
- [x] `WELCOME.md` als Gastgeber neu strukturiert: intentionsbasierte Wege statt Rollenklassifikation.
- [x] Humor gegen Statusgefälle eingesetzt, nicht gegen Leserkompetenz.
- [x] KI-Kollaboration transparent benannt, ohne AI-Marketing oder Authentizitätsperformance.
- [x] `docs/START_HERE.md` als explizite technische Werkstatt gerahmt.
- [x] GitHub-Grundbegriffe für Neueinsteiger ergänzt.
- [x] `CONTRIBUTING.md` sozial niederschwelliger eröffnet, technische Qualitätsgates unverändert gelassen.
- [x] `docs/intake/raw/HOSPITALITY_ENTRY_GRAMMAR_v0_1.md` als DERIVED/HOLD-Intake ergänzt.

## Tone-Guards

```text
welcome != persuasion
warmth != fake_human_authenticity
ai_transparency != ai_marketing
self_irony != reader_irony
boundary != gatekeeping_of_person
contribution_standard != competence_test
no_question_yet == valid_entry_state
exit == legitimate
```

Besonders geprüft wurde, dass KI-Skepsis weder ironisiert noch als Defizit behandelt
wird. Die Entry-Texte versuchen nicht, Vertrauen in KI herzustellen; sie legen nur
die Herkunft der Zusammenarbeit offen.

## Verifikation

Vollständig grüne PR-CI auf Head
`ca2662a841a6ad657840726be7b49fa5d8409f80`:

- CI Pipeline - entaENGELment Framework: SUCCESS
- Metatron Guard: SUCCESS
- Policy Lint: SUCCESS
- Python Quality: SUCCESS
- Smoke Tests: SUCCESS
- Tests: SUCCESS
- DeepJump CI: SUCCESS

## Nicht getan

- Keine Änderung an GOLD-Dateien.
- Keine Policy-Promotion.
- Keine Änderung an `VOIDMAP.yml`.
- Keine Runtime-/Wire-Änderung.
- Keine Änderung am tesser3TAKT-Transport.
- Kein Rosetta-v0.2-/zGWSTN-/FEP-/Ledger-Umbau.
- Keine Abschwächung von Test-, Review- oder Merge-Gates.
- Kein User-Profiling, keine Rollenpflicht, keine Persistenz.

## Risiken

- Der neue Ton ist bewusst persönlicher; ein fremder Reader muss noch prüfen,
  ob er als Gastfreundschaft und nicht als künstliche Nahbarkeit gelesen wird.
- Die KI-Transparenz kann je nach Leser als positiver oder negativer Marker wirken;
  sie darf deshalb nicht weiter zu einer Überzeugungssektion ausgebaut werden.
- `WELCOME.md` bleibt eine Orientierung, keine Policy oder Autoritätsquelle.
- Die Hospitality Grammar bleibt HOLD bis ein Reader ohne Entstehungskontext
  die Wege verständlich und nicht herablassend findet.

## Offene Punkte

- [ ] Fremdleser-Reentry: nicht-technischer Leser.
- [ ] Fremdleser-Reentry: AI-skeptischer, technisch versierter Leser.
- [ ] Prüfen, ob der Satz „Die Tür ist ein Angebot, kein Funnel.“ warm statt werblich wirkt.
- [ ] UI-Root-Entry separat prüfen; nicht Teil dieses Docs-Slices.

## Artefakte

- `README.md`
- `WELCOME.md`
- `docs/START_HERE.md`
- `CONTRIBUTING.md`
- `docs/intake/raw/HOSPITALITY_ENTRY_GRAMMAR_v0_1.md`
