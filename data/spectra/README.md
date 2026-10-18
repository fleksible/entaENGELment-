# data/spectra/ — Sources-first-Tabelle (VOID-010)

Gerüst für die empirische Spektren-Taxonomie. Stand 2026-10-18: **nur Kopfzeile, keine Daten.**

- `spectra_sources.csv`: eine Zeile je Quelle × Subjekt × Band
- `spectra_sources.schema.json`: Spalten, Pflichtfelder, erlaubte Werte ([SPEC-WIP])
- Prüfung: `python tools/spectra_table_lint.py` bzw. `tests/unit/test_spectra_table_lint.py`

Quellenpflicht: jede Zeile braucht Zitat, DOI oder https-URL, Quellentyp
(`peer_reviewed` | `dataset` | `review`), Zugriffsdatum, Scope, Claim-Tag
(`[FACT]` | `[INFERENZ]` | `[HYPOTHESE]`) und eine Claim-Boundary.
Daten werden nur aus geprüften Quellen eingetragen, nie erfunden oder geschätzt.
Abschluss von VOID-010 laut Closing Path: ≥ 5 zitierte Quellen + Evidence-Bundle.
