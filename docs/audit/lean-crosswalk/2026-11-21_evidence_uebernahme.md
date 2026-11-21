# Prüfbericht: Übernahme der Lean-Evidence in PR #478

**Datum:** 2026-11-21 · **Status:** ANNEX / DERIVED

**FOKUS:** Lean-Evidence unverändert verankern und vor dem Merge nachprüfen

**Promotion-Effect:** none

## Auftrag und Mandat

[ANNEX] Kevins Auftrag vom 2026-11-21 („Lean-Crosswalk v0.1 – Evidence übernehmen
und PR #478 kontrolliert mergen“): Evidence-Archiv und unabhängige Gegenprüfung
unverändert einchecken, Status differenziert ergänzen, in einem eigenen Commit nur
Evidence und Dokumentation, danach finale Prüfung und Merge unter Bedingungen.
Das Mandat umfasst ausdrücklich den Merge nach `main`, nur wenn alle genannten
Bedingungen erfüllt sind; bei unerwarteten Befunden bleibt der PR offen.

## Was beim Einchecken selbst nachgeprüft wurde

[FAKT] Alle Punkte wurden in dieser Übernahme neu ausgeführt; Lean wurde dabei
nicht gestartet.

| Prüfung | Ergebnis |
| --- | --- |
| SHA-256 des Archivs | `ef036331…ee68`, wie gemeldet |
| `SHA256SUMS` gegen alle Dateien | 64/64 OK, keine fehlende und keine unaufgeführte Datei |
| Sechs archivierte Quellen gegen den PR-Head | 6/6 Git-Blob-IDs identisch mit `0b50c4d` |
| Exit-Codes aller elf aufgezeichneten Schritte | 0 |
| `raw/audit_stdout.txt` | 413 Bytes, 5 LF-Zeilen, kein CR, kein Positionspräfix, längste Zeile 102 Bytes |
| Lean-Version laut Archiv | `Lean (version 4.35.0, …, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release)` |
| Replay mit `tools/read-audit.py` (vorher gelesen) gegen den Leser vom PR-Head | Exit 0, Ausgabe bytegleich zu `results/audit_raw.json` und `raw/reader_stdout.txt` |
| Eigener Direktaufruf von `audit_raw()` auf die Originalbytes | A, B, E `OPEN_OBLIGATION` (E mit `foreign_axioms`), C `FORMAL_CLOSED`, D `HOLD_TRUST_BOUNDARY` |
| Gegenprüfungs-Datei | bytegleich zum Upload (SHA-256 `14fe373b…9119`) |

[FAKT] Inhaltsprüfung vor dem Einchecken: keine Zugangsdaten, Tokens, Schlüssel oder
E-Mail-Adressen; keine Muster aus der Injection-Liste (G5). Personenbezogene Daten
enthält das Archiv nicht; die Umgebungsdateien nennen nur technische Pfade eines
Prüfrechners (`/workspace/scratch/…`, `/opt/codex/downloads/…`).

[ANNEX] Das Archiv wird als Ganzes abgelegt und nicht entpackt. So bleibt sein
Hash nachprüfbar, und die enthaltenen Build-Dateien (u. a. `Basic.c`, `Basic.olean`)
geraten nicht in Lint- oder Analysepfade des Repos.

## Was sich mit diesem Commit im Repo ändert

- `docs/audit/lean-crosswalk/`: Archiv, Gegenprüfung, Evidence-Index, dieser Bericht.
- `docs/annex/LEAN_CROSSWALK_v0_1.md`: Nachweisstatus im Kopf, Toolchain-Pin als
  real aufgelöst, Leser-Abschnitt und offene Punkte nachgetragen.

[FAKT] Code, Tests, Fixtures, frühere Prüfberichte, GOLD-Pfade und Workflows
bleiben unverändert. Die im Archiv gesicherte Fassung des Vertrags entspricht dem
Stand `0b50c4d`; nach diesem Commit weicht nur diese eine Doku-Datei davon ab, die
übrigen fünf archivierten Quellen bleiben bytegleich mit dem Branch.

## Grenzen

- [ANNEX] Die Ausführung des Lean-Laufs ist durch das Archiv belegt, nicht durch
  einen erneuten Lauf. Die 594-MB-Toolchain liegt nicht im Archiv; ihre Prüfsumme
  wurde beim Lauf gemessen und mit dem veröffentlichten Wert verglichen.
- [ANNEX] HOLD: Ende-zu-Ende-Provenienz Karte ↔ Lean-Rohdaten, semantische
  Zuordnung Formalisierung ↔ menschliche Aussage, Verständlichkeitstest, allgemeine
  Gültigkeit des Lesers außerhalb von A–E.
