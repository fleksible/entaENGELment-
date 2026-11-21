# Prüfbericht: Audit-Polish Lean-Crosswalk v0.1 (Eingabegrenzen und Hash-Format)

**Datum:** 2026-11-21 · **Status:** ANNEX / DERIVED · Ergänzung zu
[2026-11-21_lean_crosswalk_draft.md](2026-11-21_lean_crosswalk_draft.md), der unverändert bleibt

**FOKUS:** Ungültige Eingaben dürfen kein Beweisurteil erzeugen

**Promotion-Effect:** none

## Auftrag und Grenze

[ANNEX] Konsolidierter Folgeauftrag aus zwei unabhängigen Reviews (ChatGPT,
Gemini) mit Ergänzung: FOKUS A `assess()`/`evidence_gate()` strikt fail-closed,
FOKUS B Hash-Format in `validate_card()`, FOKUS C Zählung im Annex-Vertrag.
Kleinster notwendiger Eingriff; keine neue Architektur.

[FAKT] Zuerst ausgeführt und gemessen in einer getrennten Arbeitskopie
(`git worktree`, detached) auf dem lokalen Draft-Stand, ohne Commits. Danach
unabhängige Gegenprüfung durch ChatGPT (nach deren Rückmeldung: Patches und
Polish-Diff isoliert angewendet, 44 rot / 20 grün vor und 94 grün nach der
Reparatur reproduziert; hier nicht nachgeprüft). Auf ausdrückliche Freigabe
als zwei lokale Commits übernommen: Commit 5 nur die
Gegenfälle, Commit 6 Reparatur, Vertrag und dieser Bericht. Kein Push, kein PR.

## Getesteter Stand

| Gegenstand | Stand |
| --- | --- |
| Basis `main` | `b4ad2a01a87871457d07704bb12d194c784c2bd4` |
| Draft-Head (vier lokale Commits) | `4b207a10a3e0bd0ab1071d83f1fc094f8e896d3e` |
| Messungen „Vorher“ und „Nachher“ | Arbeitskopie: Draft-Head + Änderungen unten, vor dem Commit |
| Commit 5, nur Gegenfälle | `f1de7027b9f74b4d51e2394fd2ee0a7e62aac6a8` |
| Commit 6, Reparatur + Vertrag + Bericht | enthält diesen Bericht; seine ID und der Nachlauf daran stehen im PR-Text, weil ein Commit seine eigene ID nicht enthalten kann |

Geänderte Dateien:

| Datei | Art |
| --- | --- |
| `src/core/lean_crosswalk.py` | Reparatur (FOKUS A, B) |
| `tests/unit/test_lean_crosswalk_eingabegrenzen.py` | neu, 64 Testfälle |
| `docs/annex/LEAN_CROSSWALK_v0_1.md` | eine Tabellenzeile (FOKUS C); beim Commit zusätzlich eine Zeile in Abschnitt 8, die den offenen `audit_raw()`-Befund registriert |
| `docs/audit/2026-11-21_lean_crosswalk_audit_polish.md` | dieser Bericht |

[FAKT] Unverändert: alle CSV-Tabellen (auch Zeilenenden), Lean-Fixtures,
Rohausgaben, die bestehenden 30 Tests, der frühere Prüfbericht. Keine GOLD-Pfade
(`index/`, `policies/`, `spec/`, `seeds/`, `VOIDMAP.yml`, `data/receipts/`) und
keine Workflows im gesamten Diff gegenüber `main` (geprüft per
`git diff origin/main --name-only`).

## Vorher: Verhalten am Draft-Head

[FAKT] Die im Auftrag genannten Beispiele wurden am Draft-Head reproduziert.
Eine Aufzählung von 45 ungültigen Eingaben an `assess()` ergab:

| Ergebnis am Draft-Head | Anzahl |
| --- | --- |
| `FORMAL_CLOSED` | 19 |
| andere Beweis- oder Deklarationsurteile | 8 |
| `RUN_FAILED` für nicht-boolesches `run_ok` | 3 |
| unbehandelte Exception (`TypeError`) | 2 |
| bereits `HOLD_INVALID_EVIDENCE` | 13 |

[FAKT] Darunter: `assess(True, 1, "")`, `assess(True, 1, {})`,
`assess(True, True, [])`, `assess("false", 1, [])` und jedes Gate-Flag mit
`"false"`, `"yes"` oder `1` ergaben `FORMAL_CLOSED`. `assess(True, 1, None)`
warf eine Exception. In `validate_card()` bestand eine Karte mit Herkunftswert
`""`, wenn auch `""` übergeben wurde.

[FAKT] Neue Gegenfälle gegen den Draft-Head: **44 rot, 20 grün**
(`python -m pytest tests/unit/test_lean_crosswalk_eingabegrenzen.py`).
Grün waren bereits die Fälle, die der Draft schon abfing (Bytes und Bytearray
als Ganzes; Bytes-, `None`-, Zahlen-, leere und verschachtelte Elemente in einer
Liste; `0`/`None` als Gate-Flag), die Vorrangprobe für `run_ok=False`, die
gültigen Behälter und die gültigen Hash-Fälle.

## Reparatur

- `evidence_gate()`: nur `run_ok is False` ergibt `RUN_FAILED` (höchster Vorrang);
  jeder der vier Schalter, der kein echtes `bool` ist, ergibt `HOLD_INVALID_EVIDENCE`.
- `assess()`: nach dem Gate und vor dem Deklarationsstatus wird geprüft:
  `decl_count` echtes `int` (kein `bool`), mindestens 0; `axioms` eine `list`,
  `tuple`, `set` oder `frozenset` aus Strings im bestehenden Axiomnamen-Format
  (nichtleer, ohne Leerzeichen, Komma, Klammern). Sonst `HOLD_INVALID_EVIDENCE`.
  Typannotation `AxiomInput` entsprechend.
- `validate_card()`: übergebener `origin_sha256` muss ein String mit genau
  64 Kleinbuchstaben-Hexzeichen sein. Sonst `PROVENANCE_DRIFT`, eingereiht in
  die übrigen Gründe, ohne vorzeitigen Rücksprung; bei unbrauchbarer Karte
  `("MALFORMED_CARD", "PROVENANCE_DRIFT")`. Keine Exception.
- Vertrag Abschnitt 6: „7 Status × (1 unveränderte Baseline + 7 Verfälschungen)
  = 56 Fälle, davon 49 tatsächliche Verfälschungen“.

## Nachher

[FAKT] Alle Messungen dieses Abschnitts wurden für diesen Bericht neu ausgeführt,
in der Arbeitskopie vor dem Commit.

[FAKT] Nachlauf am Commit-Stand: Commit 5 allein ergibt bei den drei
Crosswalk-Testmodulen 44 rot, 50 grün (20 neue + 30 bestehende).

| Prüfung | Ergebnis |
| --- | --- |
| neue Gegenfälle (64) | 64 grün |
| alle Crosswalk-Tests (64 neu + 30 bestehend) | 94 grün, Python 3.13.18 / 3.12.3 / 3.11.18 |
| Aufzählung der 45 ungültigen Eingaben | 45 × `HOLD_INVALID_EVIDENCE`, keine Exception |
| Vollsuite | 1379 bestanden, 2 übersprungen (Python 3.13.18) |
| `make verify` | Exit 0 |
| `ruff check src/ tools/ tests/` | ohne Befund |
| `black --check src/ tools/ tests/` | ohne Befund |
| `mypy src/ tools/` | ohne Befund (3.13.18, 3.12.3, 3.11.18) |
| `bandit -c .bandit.yaml -r src/ tools/` | ohne Befund |

[FAKT] Die bestehenden 30 Tests und alle 56 Negativfälle laufen unverändert grün.

[FAKT] Gegenprobe: Sieben gezielt zurückgebaute Teile der Reparatur wurden
jeweils von den Tests erkannt (bool-Prüfung der Schalter: 15 rot; `run_ok`
per Wahrheitswert: 3; `decl_count` ohne Typprüfung: 3; Text als Axiomliste: 8;
Namensformat ungeprüft: 2; Hashformat ungeprüft: 11; unbrauchbare Karte
verdeckt Hashfehler: 1).

[FAKT] Umgebung: Linux; Abhängigkeiten aus `uv.lock` mit uv 0.12.18 in
Umgebungen außerhalb des Repos; pytest 9.1.1.

## Nicht ausgeführt

- Lean: NOT_RUN.
- Vollsuite unter Python 3.11/3.12: NOT_RUN (dort nur Crosswalk-Tests und mypy).
- `make verify-all`, JS-/UI-Prüfungen, GitHub-CI: NOT_RUN.

## Fortbestehende Grenzen

- [ANNEX] HOLD: Die Hash-Prüfung belegt nur Typ, Format und Gleichheit des
  übergebenen Werts. Sie belegt **nicht**, dass der Hash aus einer echten
  Lean-Ausgabe berechnet wurde oder dass die Daten authentisch sind. Die
  End-to-End-Provenienz bleibt bis zu einer gesondert geprüften Evidenzerzeugung offen.
- [ANNEX] HOLD: erster echter Lean-4-Lauf, Prüfung der realen `#print axioms`-Ausgabe,
  semantische Prüfung zwischen Lean-Deklaration und menschlicher Aussage,
  Verständlichkeitstest der Karten.
- [INFERENZ] Dieselbe Fehlerklasse besteht noch in `audit_raw()`, außerhalb
  dieses Auftrags und nicht geändert: `exit_code=False` oder `0.0` gilt als
  erfolgreicher Lauf (in Python `False == 0`), und eine Ausgabe, die kein Text
  ist, löst eine Exception aus. Als offener Befund im Vertrag (Abschnitt 8) registriert; vor der ersten echten
Lean-Integration und vor einem Merge als eigener Folgeschritt zu beheben.
