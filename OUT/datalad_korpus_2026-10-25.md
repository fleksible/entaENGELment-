# Report: Privates Korpus als DataLad-Dataset

**Datum:** 2026-10-25
**Fokus:** DataLad-Korpus einrichten

## Ziel

Die Originale des Projektkorpus (Drive-Ordner „entaENGELment Sortieren“) inhaltsadressiert,
versioniert und mit wiederholbaren Verarbeitungsschritten führen, privat und lokal, mit
Anschluss an Save States. Entscheidungen des Owners: lokal und erweiterbar, ganzer Drive-Ordner,
erster Lauf Textextraktion plus Inventar, eigener Branch und PR.

## Aktionen

- [x] `tools/corpus_datalad.py`: `init` (nur außerhalb von Git-Arbeitsbäumen), `import` (Kopie mit SHA-256-Abgleich, Import-Record, `datalad save`), `extract`, `inventory` (beide per `datalad run`), `sources` (Einträge für `reentry_crate`)
- [x] `tools/corpus_code/extract_text.py` und `inventory.py`: nur Standardbibliothek, werden beim `init` nach `code/` kopiert; deterministisch für `datalad rerun`; Zip-Archive werden nur gelesen und gehasht, nie entpackt
- [x] Öffentlicher Anker ohne Dateinamen (`public_anchor.json`) nach PRIVACY_BOUNDARY.md
- [x] 15 Tests; der End-to-end-Test läuft mit DataLad/git-annex und wird ohne sie übersprungen
- [x] Prototyp mit synthetischen Dateien (DataLad 1.7.1, git-annex 10.20240129, pdftotext 24.02): init → import → extract → inventory; `datalad rerun` ohne neuen Commit (bytegleich); `git annex fsck` meldet eine manipulierte Datei
- [x] Gegentest mit `reentry_crate` fand einen Fehler (annex-Symlinks kollidierten im Payload); behoben in PR #427 (`e0abca7`)
- [x] Runbook `docs/runbooks/DATALAD_KORPUS_v0_1.md`; Tool-Zeile in `CLAUDE.md`

## Nicht getan

- Kein Dataset aus echten Korpusdaten angelegt: Es gehört auf den Rechner des Owners; dieser Container ist flüchtig
- Keine Drive-Inhalte heruntergeladen oder ins Repo übernommen; kein Remote (Drive/GitHub) eingerichtet
- Keine neuen Projektabhängigkeiten (DataLad und git-annex sind externe Programme, nur für den Lauf nötig)

## Risiken

- `inventory.json` enthält Einzelhashes und Dateinamen: privat halten (Bestätigungsangriff über bekannte Dateien)
- Extrahierter Text ist eine Lesehilfe; maßgeblich bleibt das Original im annex
- Die Drive-Datei-ID wird nicht zugeordnet (der Connector liefert keine Prüfsummen); Herkunft endet beim Export-Ordner
- Ohne `pdftotext` werden PDFs als `skipped` geführt

## Offene Punkte

- [ ] ☐ Dataset auf dem eigenen Rechner nach Runbook anlegen und den Drive-Ordner importieren
- [ ] ☐ Zuordnung zur Drive-Datei-ID (z. B. über rclone mit Prüfsummen) als späterer Schritt
- [ ] ☐ Entscheidung über Remote (Drive-Speicher, privates GitHub) und über einen öffentlichen Anker
- [ ] ☐ Anschluss an die Korpussuche aus PR #426 (`--corpus` auf `derived/text/`)

## Artefakte

- `tools/corpus_datalad.py`
- `tools/corpus_code/__init__.py`
- `tools/corpus_code/extract_text.py`
- `tools/corpus_code/inventory.py`
- `tests/unit/test_corpus_datalad.py`
- `docs/runbooks/DATALAD_KORPUS_v0_1.md`
- `CLAUDE.md` (Tool-Zeile)
