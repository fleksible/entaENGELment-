# Prüfbericht: Lean-Crosswalk v0.1 aus dem v0.3-Übergabepaket

**Datum:** 2026-11-21 · **Status:** ANNEX / DERIVED · Technischer Prüfbericht zum Draft-Vorschlag

**FOKUS:** v0.3-Mängel des Lean-Crosswalks rot→grün beheben, ohne Lean-Lauf zu behaupten

**Promotion-Effect:** none

## Auftrag und Grenze

[ANNEX] Das außerhalb des Repos erstellte Übergabepaket
ATLAS-CROSSWALK-LEAN-001 v0.3 wird als prüfbarer Vorschlag übernommen. Die vier
Mängel aus der Prüfung vom 2026-11-21 werden so behoben, dass jeder vorher
nachweislich rot und danach grün ist. Vertrag:
[LEAN_CROSSWALK_v0_1](../annex/LEAN_CROSSWALK_v0_1.md).

[FAKT] Keine Änderung an GOLD (`index/`, `policies/`, `spec/`, `seeds/`,
`VOIDMAP.yml`, `data/receipts/`), an bestehenden Modulen, Tests oder Workflows.
Nur neue Dateien. Keine Claim-Promotion, kein Retagging, keine HumanDecision.
Lean wurde nicht ausgeführt (NOT_RUN). Z3 ist nicht Teil des Repos.

[ANNEX] Der Vorschlag wurde zunächst nur im Gespräch vorgelegt. Push, Draft-PR
und jeder Merge brauchen eine eigene menschliche Freigabe.

## Basis und Commits

| Gegenstand | Stand |
| --- | --- |
| Basis `main` | `b4ad2a01a87871457d07704bb12d194c784c2bd4` |
| Commit 1, v0.3 unverändert übernommen | `18d2c5a22241e41542f13279abfca51f0d0766a2` |
| Commit 2, nur Gegenfälle (rot am Ausgangsstand) | `137d4824c02f8dcc2e6dc07b54d11436d42bc834` |
| Commit 3, Korrektur | `f6fa2b5658c21a6f1e467e3f4a269e5c01f81d3e` |
| `src/core/lean_crosswalk.py` | Blob `dd378b455621` (= v0.3 `reference.py`) → `324e38994814` |
| Übergabepaket | `ATLAS_Crosswalk_RepoHandoff_v0_3.zip`, sha256 `87826f60deafb2d2fa666c46e9472904e04ce9941f48f73cbfbaa702a6e61abf` |

[FAKT] Alle 15 Datei-Hashes des Pakets stimmten mit seinem Manifest überein.
`derivation_truth_table.csv` ist unverändert (sha256 `78e2f876…bcfe`, wie im Manifest).
Die JSON-Doppel der CSV-Tabellen wurden nicht übernommen: je Tabelle genau eine Vorgabe.

[FAKT] Umgebung: Linux, Python 3.13.18, Abhängigkeiten aus `uv.lock` mit
uv 0.12.18 in einer Umgebung außerhalb des Repos, pytest 9.1.1. Keine
Lean-Toolchain; die Installation war in der Prüfumgebung nicht zugelassen.

## Ausgangsbefund an v0.3

1. [FAKT] **Negativfälle nie ausgeführt.** Die 48 deklarierten Fälle wurden von
   keinem Test geladen. Gegen den v0.3-Kartenprüfer gefahren, wären 18 davon
   durchgerutscht (Herkunfts-Hash, angezeigte Axiomliste, freier Zusammenfassungstext:
   je 6 Fälle). Der Prüfer kannte diese Felder nicht.
2. [FAKT] **Status ohne Karte.** Die Klassifikation konnte `HOLD_INVALID_EVIDENCE`
   liefern, Kartenprüfer und 6×6-Matrix kannten den Status nicht. Eine korrekt
   gemeldete unbrauchbare Beweislage wäre auf jeder Karte abgelehnt worden.
3. [FAKT] **Selbstbezüglicher Matrixtest.** Der Test verglich nur die Tabelle mit
   einer Gleichheitsregel und rief den Kartenprüfer nie auf.
4. [FAKT] **Lean-Teil nicht aufrufbar.** Es fehlte eine Lake-Konfiguration, die
   `import CrosswalkProbe.Basic` auflösbar macht. Der Mischfall gab nur einen
   Status zurück; die Fremdaxiome gingen verloren.
5. [INFERENZ] **Zusätzlich gefunden:** `Audit.lean` begann mit einem
   `/-! … -/`-Moduldoc vor `import`. In Lean muss `import` vor jedem Befehl
   stehen; die Datei wäre am Kopf gescheitert. Nicht durch einen Lean-Lauf
   bestätigt, Moduldoc jetzt nach dem Import.

## Gegenfälle und Korrektur

[FAKT] Commit 2 erweitert die Vorgaben von Hand (Matrix 7×7 = 49 Zeilen,
Negativfälle 56, neue Vorprüfungstabelle mit 16 Zeilen; bestehende Zeilen
inhaltlich unverändert) und fügt `tests/unit/test_lean_crosswalk_gegenfaelle.py`
sowie handgeschriebene Rohausgaben unter `tests/fixtures/lean_crosswalk/raw/` hinzu.

| Stand | Ergebnis (`test_lean_crosswalk_gegenfaelle.py` + v0.3-Basistest) |
| --- | --- |
| Commit 2 (rot am Ausgangsstand) | 20 rot, 5 grün |
| Commit 3 (Korrektur) | 30 grün |

[FAKT] Am roten Stand grün waren nur die vier unberührten v0.3-Basistests und
die neue Vorprüfungstabelle (die Vorprüfung selbst war in v0.3 schon richtig).

[FAKT] Korrektur in Commit 3:

- eine Statusquelle `STATUSES` (7), daraus Art, Deckel, Hauptgrund und Vorlage;
- `assess()` liefert ein strukturiertes Urteil mit `axioms` und `foreign_axioms`;
- `validate_card()` prüft eine Karte gegen Urteil und Herkunft; unbekannte oder
  fehlende Kartenfelder ergeben `MALFORMED_CARD`;
- Zusammenfassung fest aus Vorlage, freier Text nur in `notes` als `UNVERIFIED_PROSE`,
  keine Stichwortprüfung;
- `audit_raw()` / `parse_print_axioms()`: Exit-Code zuerst, nur dokumentierte
  Zeilenformen, sonst `HOLD_INVALID_EVIDENCE`;
- `lakefile.toml` (Bibliothek baut nur `CrosswalkProbe.Basic`), `Audit.lean` beginnt mit `import`;
- im v0.3-Basistest: selbstbezüglicher Matrixtest entfernt (ersetzt durch den
  7×7-Lauf gegen den Kartenprüfer), Kartenregeln auf die neue Prüfung umgestellt,
  Formatierung nach black/ruff.

## Gegenprobe der Tests

[FAKT] Neun gezielt eingebaute Fehler im Modul wurden jeweils von mindestens
einem Test erkannt:

| Eingebauter Fehler | rote Tests |
| --- | --- |
| sorryAx verliert Vorrang vor Fremdaxiom | 8 |
| Fremdaxiome im Mischfall verschluckt | 2 |
| Axiomname per Endung statt exakt verglichen | 4 |
| Herkunfts-Hash nicht geprüft | 1 |
| Axiomliste der Karte nicht geprüft | 1 |
| Zusammenfassung nicht geprüft | 2 |
| unbekannte Zeilen toleriert | 2 |
| Exit-Code ignoriert | 2 |
| doppelte Deklaration nicht erkannt | 6 |

[FAKT] Vollsuite am Head: 1315 bestanden, 2 übersprungen. `make verify`
bestanden. `ruff check`, `black --check` (src/ tools/ tests/), `mypy src/ tools/`
und `bandit` auf dem neuen Modul ohne Befund.

## Was nicht belegt ist

- [ANNEX] HOLD: Kein Lean-Lauf. Die Rohausgabe-Proben sind handgeschrieben
  (FIXTURE_ONLY / NOT_KERNEL_VERIFIED). Ob Lean ein Positionspräfix ausgibt und
  ob lange Axiomlisten umbrechen, zeigt erst der erste echte Lauf; bis dahin
  führt jede Abweichung fail-closed zu `HOLD_INVALID_EVIDENCE`.
- [ANNEX] HOLD: Toolchain-Pin `v4.35.0` aus dem Paket übernommen, nicht geprüft.
- [ANNEX] HOLD: Die Wahrheitstafel prüft die Auswertung der Merkmale, nicht ihre
  Gewinnung aus einer echten Lean-Ausgabe. Diese zweite Grenze bleibt bis zum
  Lean-Lauf offen.
- [ANNEX] Der Verständlichkeitstest (ob Menschen durch die Karten mathematische
  Aussagen besser verstehen) ist ein eigener Strang und nicht Teil dieser Änderung.
