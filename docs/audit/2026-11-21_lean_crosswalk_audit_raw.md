# Prüfbericht: `audit_raw()`-Eingabegrenzen (Abschluss des lokalen Polish)

**Datum:** 2026-11-21 · **Status:** ANNEX / DERIVED · Ergänzung zu
[2026-11-21_lean_crosswalk_draft.md](2026-11-21_lean_crosswalk_draft.md) und
[2026-11-21_lean_crosswalk_audit_polish.md](2026-11-21_lean_crosswalk_audit_polish.md),
die beide unverändert bleiben

**FOKUS:** Kein Beweisurteil aus ungültigem Exit-Code oder unbrauchbarer Ausgabe

**Promotion-Effect:** none

## Auftrag und Grenze

[ANNEX] Abgegrenzter Folgeschritt zum in Commit 6 registrierten offenen Befund
`audit_raw()`, nach Abstimmung der Reviews (ChatGPT, Gemini) und ausdrücklicher
Freigabe für zwei lokale Commits (7: rot, 8: grün). Danach endet der lokale
Polish. `expected_decls` gehört bewusst nicht dazu (die `ValueError` bei
doppelten Einträgen ist gewollt). Kein Push, kein PR, kein Merge.

## Stand und Dateien

| Gegenstand | Stand |
| --- | --- |
| Basis `main` | `b4ad2a01a87871457d07704bb12d194c784c2bd4` |
| Ausgangsstand (Commit 6) | `ea6bee1b62470a65b1237091de1bedcbc415e51c` |
| Commit 7, nur Gegenfälle | `12d4e4048644ed057477ac5ddd1632ed6c57e18b` |
| Commit 8, Reparatur + Vertrag + Bericht | enthält diesen Bericht; ID und Nachlauf im PR-Text |

| Datei | Art |
| --- | --- |
| `tests/unit/test_lean_crosswalk_audit_raw_grenzen.py` | neu, 19 Testfälle (Commit 7) |
| `src/core/lean_crosswalk.py` | `audit_raw()` (Commit 8) |
| `docs/annex/LEAN_CROSSWALK_v0_1.md` | Abschnitt 4 präzisiert, Befund in Abschnitt 8 als behoben vermerkt (Commit 8) |
| `docs/audit/2026-11-21_lean_crosswalk_audit_raw.md` | dieser Bericht (Commit 8) |

## Vorher (an Commit 6)

[FAKT] Mit der Rohausgabe `ok_all.txt` und den fünf erwarteten Deklarationen:

| Eingabe | Ergebnis an Commit 6 |
| --- | --- |
| `exit_code=False`, `0.0` | Ausgabe gelesen, Urteile bis `FORMAL_CLOSED` |
| `exit_code=True`, `1.0`, `"0"`, `None`, `b"0"` | `RUN_FAILED` |
| Exit 0, Ausgabe `None`, Zeilenliste, `123` | Exception `AttributeError` |
| Exit 0, Ausgabe `bytes`, `bytearray` | Exception `TypeError` |
| `exit_code=False`, Ausgabe `None` | Exception `AttributeError` |
| `exit_code=1`, Ausgabe `None` | `RUN_FAILED` |

[FAKT] Neue Gegenfälle an Commit 7 (Code wie Commit 6): **13 rot, 6 grün**.
Grün waren der normale Erfolgsfall (Exit 0), die echten Fehlercodes 1, 2, −1,
137 und der Vorrangfall `audit_raw(1, None, …)`.

## Reparatur (Commit 8)

- Nur ein echtes `int` ist ein Exit-Code (`type(exit_code) is int`, also kein
  `bool`); sonst alle Deklarationen `HOLD_INVALID_EVIDENCE`.
- Exit-Code ungleich 0: alle `RUN_FAILED`, die Ausgabe wird nicht gelesen.
  Damit behält ein echter Fehlercode Vorrang vor einer unbrauchbaren Ausgabe.
- Exit 0, aber Ausgabe kein `str`: alle `HOLD_INVALID_EVIDENCE`, keine Exception.
- Vertrag: Abschnitt 4 nennt die Regel; der offene Befund in Abschnitt 8 ist als
  behoben vermerkt, nicht gelöscht.

## Nachher

[FAKT] Gemessen am Arbeitsstand vor Commit 8 (Commit 7 + Reparatur):

| Prüfung | Ergebnis |
| --- | --- |
| neue Gegenfälle (19) | 19 grün |
| alle Crosswalk-Tests (19 + 64 + 30) | 113 grün |
| Tabelle oben | alle ungültigen Fälle `HOLD_INVALID_EVIDENCE`, `audit_raw(1, None, …)` weiter `RUN_FAILED`, keine Exception |

[FAKT] Gegenprobe: vier zurückgebaute Teile der Reparatur wurden jeweils
erkannt (`isinstance` statt exaktem `int`, sodass `bool` durchrutscht: 2 rot;
Exit-Code-Typprüfung fehlt: 7; Ausgabe-Typprüfung fehlt: 5; Ausgabeprüfung vor
dem Exit-Code, Vorrang vertauscht: 1).

[ANNEX] Vollsuite, `make verify`, ruff, black, mypy und bandit sowie die Läufe
unter Python 3.12/3.11 werden nach Commit 8 auf einem sauberen Checkout
ausgeführt; das Ergebnis steht mit der Commit-ID im PR-Text.

## Was offen bleibt

- [ANNEX] HOLD: erster echter Lean-4-Lauf und Prüfung der realen `#print axioms`-Ausgabe.
- [ANNEX] HOLD: kryptografische Ende-zu-Ende-Provenienz – die Hash-Prüfung belegt
  nur das Format, nicht die Herkunft aus einem Lean-Lauf.
- [ANNEX] HOLD: semantische Zuordnung zwischen Lean-Deklaration und menschlicher Aussage.
- [ANNEX] HOLD: Verständlichkeitstest der Karten mit Menschen.
- [ANNEX] Der lokale Polish ist mit Commit 8 abgeschlossen. Weitere
  Eingabegrenzen (z. B. `expected_decls`) sind kein Teil davon.
