# Report: Witness-Wächter v0.2 – Doku-Übernahme

**Datum:** 2026-11-06
**Fokus:** Witness-Konzept ins Annex

## Ziel

Den v0.2-Entwurf des Witness-Wächters als reine Dokumentation in den Annex übernehmen,
offene Einwände prüfen und nötige Doku-Korrekturen einarbeiten. DESIGN_ONLY und
NOT_RUN für die Praxisprüfungen P1–P4 bleiben erhalten.

Mandat (Kevin, 2026-11-06, wörtlich): „Dokumentationsentwurf ins ANNEX. Prüfe offene
Einwände, behebe nötige Dokumentationskorrekturen und erstelle einen reinen Doku-PR.
Nach bestandenen erforderlichen Checks und kurzem Prüfbericht darfst du diesen
selbstständig mergen. Erhalte DESIGN_ONLY und die Praxisprüfungen auf NOT_RUN. Das
Mandat umfasst ausschließlich die Dokumentation; Installation, Aktivierung und
Umsetzung des Wächters bleiben außerhalb dieses Auftrags.“

## Aktionen

- [x] Entwurf übernommen nach `docs/annex/WITNESS_WAECHTER_v0_2.md`; SHA-256 der Lieferung
  `59d9b9076acb58b452a6d7305a5faa85f3e2d089d5251e226da4cd652660e742`
- [x] Textabgleich Lieferung ↔ Annex-Fassung: nur die sechs in Abschnitt 11 der Notiz
  benannten Korrekturen
- [x] Offene Einwände geprüft (Tabelle unten)
- [x] Eigene isolierte Git-Nachproben (unten), kein Agententest
- [x] `make verify` und `make verify-governance` lokal bestanden
- [x] CHANGELOG-Eintrag

| Einwand | Ergebnis | Behandlung |
| --- | --- | --- |
| R1–R7 aus dem Review zu v0.1 | In v0.2 bereits berücksichtigt (Abschnitt 2 der Notiz) | Keine weitere Änderung |
| Messbasis „Git-Index“ kollidiert mit R1 | Eine Messung per `git status` würde selbst Abweichungen erzeugen | Index inhaltlich vergleichen; Messung mit `GIT_OPTIONAL_LOCKS=0` |
| MCP-Sperre `mcp__*` unbelegt | Offizielle Berechtigungsreferenz bestätigt das Deny-Muster für alle Server | Quelle C4 ergänzt |
| `--tools` (CLI-Referenz) | Seite von dieser Umgebung aus nicht abrufbar | Herkunft offengelegt: aus dem Entwurf, nicht erneut geöffnet |
| Satz „kein Auftrag … zu mergen“ | Ohne Zusatz missverständlich nach dem neuen Doku-Mandat | Mandatssatz ergänzt |
| Private Bibliothekslinks | Für Repo-Leser nicht auflösbar | Durch IDs ersetzt und markiert |

## Nachproben (Git 2.43.0, frische Temp-Repos, `GIT_CONFIG_GLOBAL=/dev/null`)

| Probe | Ergebnis |
| --- | --- |
| `git status` nach mtime-Änderung | Indexdatei-Hash `255e2087f2c7` → `ac46506f8064`; vorgemerkter Inhalt gleich (`git write-tree` unverändert) |
| dasselbe mit `GIT_OPTIONAL_LOCKS=0` | Indexdatei unverändert |
| `git diff` mit Treiber nur in `.gitattributes` | Geschützte Datei unverändert |
| `git diff` mit Textconv-Treiber in `.git/config` | Geschützte Datei verändert |
| dasselbe mit `--no-textconv --no-ext-diff` | Geschützte Datei unverändert |
| `.gitignore` mit `out/`, Datei `OUT/r.md` | `core.ignorecase=false`: nicht ignoriert; `true`: ignoriert |

## Nicht getan

- Keine Installation, Aktivierung oder Umsetzung eines Wächters; kein Hook, keine Settings-Änderung.
- `.claude/skills/witness_mode/SKILL.md` und `.gitignore` unverändert.
- P1–P4 nicht ausgeführt (NOT_RUN).
- v0.1 und der Review liegen weiter nur außerhalb des Repos.

## Risiken

- Reine Dokumentation, keine Laufzeitwirkung.
- Verweise auf die externe Claude-Code-Doku können veralten; die Notiz nennt das Abrufdatum.

## Offene Punkte

- [ ] ☐ P1–P4 am tatsächlichen Ausführungsort
- [ ] ☐ Ignore-Befund `out/` ↔ `OUT/` auf Dateisystemen ohne Groß-/Kleinschreibung
- [ ] ☐ Witness-Anleitung (Skill-Datei) vereinheitlichen
- [ ] ☐ Ob v0.1 und der Review ins Repo-Intake gehören

## Artefakte

- `docs/annex/WITNESS_WAECHTER_v0_2.md`
- `docs/audit/2026-11-06_witness_waechter_v0_2_doku.md`
- `CHANGELOG.md`

CI-Ergebnis am finalen Head: im Prüfkommentar des PRs.
