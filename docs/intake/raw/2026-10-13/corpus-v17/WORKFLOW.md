# Korpusnachtrag: Arbeitsfolge und Gates

**MODELL / Arbeitsvertrag · DERIVED / REVIEW-PENDING**

Dieser Nachtrag übernimmt die Kategorien und Grenzen des
[v10-Workflows](../../2026-10-07/corpus-v10/WORKFLOW.md).
Die dort bereits archivierten Skills werden verlinkt und nicht erneut kopiert.

| Schritt | Ergebnis | Grenze |
|---|---|---|
| Fixieren | Repo-Commit, v17-Eingang und v18-Folgestand getrennt | Änderungsmarker sind keine Entstehungsdaten |
| Rekonstruieren | v10 + Delta → v17; v17 + Folgeschritt → v18 | Keine stille Änderung historischer Relationen/Konflikte |
| Zählen | Einträge, Lesestand, Punkte, Relationen, Konflikte, Tags | Lesefortschritt erhöht keine Evidenzautorität |
| Zuordnen | 96 Quellen → CSV; C01–C19 → Audit | Kopien zählen nicht als unabhängige Belege |
| Prüfen | Manifest, Tabellen, CSV, Fortsetzungen, Negativproben | Allgemeine Repo-Gates decken die Zähler nicht ab |
| Review | Konkreter Diff und Ergebnisse | CODEOWNERS-Review und Publikationsentscheid bleiben gesondert |

## Konkrete Aufrufe

```bash
python3 docs/intake/raw/2026-10-13/corpus-v17/verify_counts.py --export-only
python3 docs/intake/raw/2026-10-13/corpus-v17/test_verify_counts.py
python3 tools/claim_lint.py --scope docs/intake/raw/2026-10-13/corpus-v17,docs/audit
make verify
make verify-js
```

Mit privatem Original zusätzlich:

```bash
python3 docs/intake/raw/2026-10-13/corpus-v17/verify_counts.py \
  --input-v18 /pfad/zum/privaten/Index.md
ENTA_V18_INPUT=/pfad/zum/privaten/Index.md \
  python3 docs/intake/raw/2026-10-13/corpus-v17/test_verify_counts.py
```

`verify_counts.py` verlangt genau einen ausdrücklich gewählten Prüfumfang,
`--export-only` oder `--input-v18 PATH`. Ohne Wahl oder mit beiden Optionen bricht er
mit CLI-Fehler und Exit 2 ab. Die Statuswerte `PASS_EXPORT_ONLY` und
`PASS_WITH_V18_INPUT` unterscheiden die Läufe maschinenlesbar; beide nennen ihre
ungeprüften Bereiche mit. `test_verify_counts.py` braucht nur die Standardbibliothek
und überspringt den Lauf gegen das echte Original, solange `ENTA_V18_INPUT` fehlt.

`claim_lint.py` akzeptiert `--scope` mit Verzeichnissen, keine positionalen Dateipfade.
Sein Lauf ohne `--strict` ist eine Warnprüfung; seine Treffer in diesem Paket sind
Stichwortfehlalarme auf `verify`, `require` und `requires`, keine ungetaggten
Behauptungen. Der Pre-Commit-Hook wird zwar durch
geänderte Markdown-/JSON-Dateien ausgelöst, scannt aber weiter nur
`index,spec,receipts,tools`; Intake-Inhalte bleiben dabei außen vor.
`verify-json` prüft Legacy-Receipts und ist kein Parser für dieses Delta.
`verify_counts.py` parst beide JSON-Dateien selbst und prüft alle Manifest-Hashes;
eine zusätzliche Shell-Umwandlung des Manifests ist unnötig.
Der neue Verifier ist noch nicht an CI angeschlossen. Er muss auf dem konkret
reviewten Stand explizit ausgeführt werden; eine grüne CI allein bestätigt ihn nicht.

## Intake-Helper und Dateianzahl

`make intake` ruft `tools/intake_add.py` auf. Er erzeugt einen numerischen Record
und eine flache Einstiegskopie, ohne Optionen für eine selbst gewählte Record-ID
oder einen vorhandenen Bundle-Unterordner. Deshalb folgt dieser Diff genau diesem
Format: `INTAKE-2026-10-13-001`, Einstieg `docs/intake/raw/2026-10-13/corpus-v17-reconcile.md`.
Die Einstiegskopie zeigt auf das Bundle, der Record wurde nach Erzeugung ausgefüllt.
Die eingereichte Liste hatte bereits zehn Pfade einschließlich `INDEX.md`; mit
dieser tatsächlichen Helper-Einstiegskopie sind es elf geänderte/angelegte Dateien.
Der Folgepatch zum Prüfumfang legt `test_verify_counts.py` dazu: zwölf Dateien,
zehn davon im Manifest. `INDEX.md` bleibt als erweiterbarer Einstieg ungehasht,
und das Manifest hasht sich weiterhin nicht selbst.

Manifest und Payload gehören in denselben vollständigen prüfbaren Diff.
Ein frühes Commit mit Hashes noch nicht vorhandener Dateien wäre kein vollständiges
Prüfpaket. Der vorbereitete Diff ist daher atomar; eine Aufteilung muss für jeden
Zwischenstand ein passendes Manifest liefern.

## Nächste fachliche Arbeit

C19 (Enforcement-Status) zuerst. C05 als eigener kleiner Vorschlag:
deklarierte negative Boundary-Fixture, ein Test mit konkretem Ablehnungsgrund,
gezielte Kenogramm-Anker. Die vorhandenen Inline-Gegenfälle bleiben erhalten.
Die Spec fordert Counterfixtures, aber nicht ausdrücklich eine separate JSON-Datei.
Dieser Vorschlag verbessert die Zuordnung; er behauptet keine automatisch erfüllte Promotion.
Danach C04/C06/C07/C08 jeweils mit einem Beispiel; C09–C14 erst nach geklärtem
Prüfobjekt; C16/C17 bleiben an ihren konkreten Quellengates.
