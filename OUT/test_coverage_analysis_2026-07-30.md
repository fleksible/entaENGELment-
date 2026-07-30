# Report: Test-Coverage-Analyse 2026-07-30

**Datum:** 2026-07-30
**Fokus:** Test-Coverage analysieren

## Ziel

Ist-Zustand der Testabdeckung erfassen (Python + JS/TS) und priorisierte Bereiche
vorschlagen, in denen Tests verbessert werden sollten. Abgrenzung gegen die beiden
Vorgänger-Analysen vom 2026-06-20 (`OUT/test_coverage_analysis.md`,
`docs/audit/2026-06-20_test_coverage_analysis.md`): dieser Report nennt nur, was
**heute noch offen** ist, plus **neue Befunde**, die damals nicht sichtbar waren.

> **Statusnachtrag (gleicher PR):** **P0-1** und **P0-2** wurden nach explizitem
> Go des Users umgesetzt — siehe [Nachtrag](#nachtrag-umsetzung-p0-1--p0-2) am Ende.
> Dabei kam ein **neuer Befund** zutage: drei der fünf Fractalsense-JS-Dateien sind
> syntaktisch unvollständig und nicht parsebar. Der Rest dieses Reports beschreibt
> weiterhin den Analyse-Stand *vor* diesen beiden Änderungen.

## Methodik

- `pytest --cov=src --cov=tools` (Line + zusätzlich `--cov-branch`), 601 Tests, alle grün.
  Dependencies lokal nachinstalliert (pytest, pytest-cov, numpy, scipy, pyyaml, jsonschema).
- `jest --coverage` gegen die echte `jest.config.js` **tatsächlich ausgeführt** (Jest 30 in
  Scratchpad installiert, per Symlink eingebunden, danach entfernt) — die Vorgänger-Reports
  konnten das nicht und mussten spekulieren.
- `node --experimental-strip-types --test ui-app/test/*.test.mjs` ausgeführt.
- Alle 14 Workflows in `.github/workflows/` gegen die tatsächlich ausgeführten
  Testkommandos gelesen; `deepjump-ci.yml` → `deepjump-audit.reusable.yml` nachverfolgt.
- Uncovered Lines programmatisch auf ihre umgebende Funktion gemappt, um Lücken-Cluster
  statt Einzelzeilen zu bewerten.

## Ist-Zustand

### Python (`src/` + `tools/`)

**601 Tests, alle grün. 74 % Line-Coverage, 72 % Branch-Coverage** (4235 Statements,
1098 unabgedeckt / 1674 Branches, 278 partial).

Fortschritt seit 2026-06-20: **186 → 601 Tests, 62 % → 74 %**. Die neuen Kernmodule
(`action_gate.py` 92 %, `evidence_bridge_adapter.py` 98 %, `evidence_routing.py` 88 %,
`bridge_view.py` 88 %) sind auf dem Happy Path gut abgedeckt.

Verteilung: `tests/unit` 409, root-`tests/*.py` 115, `tests/stability` 35,
`tests/ethics` 27, `tests/integration` 13, `tests/benchmark` 1, `tests/cpt` 1.

### JS/TS

- `__tests__/` (Jest): **45 Tests, 3 Suites** — gewachsen von 1 auf 3 Dateien.
- `ui-app/test/`: **23 Tests, 497 Zeilen**, `node:test` — laufen lokal in 0,4 s grün.
  (Die Juni-Analyse sagte „ui-app hat keine einzige Testdatei" — das ist überholt.)
- `Fractalsense/tests/` (pytest): eigene Suite, läuft in `test.yml`.

### CI — was wo wirklich läuft

| Workflow | Auf PR? | Python-Tests | Coverage-Gate |
|---|---|---|---|
| `deepjump-ci.yml` → reusable | ja | `pytest tests/` (alle 601) | nein (kein `--cov`) |
| `ci-smoke.yml` | ja | `tests/unit`, `integration`, `ethics` (449) | nein |
| `ci.yml` | **nein** (`if: != pull_request`) | alle + `--cov` | `--fail-under=50` |
| `test.yml` | ja | nur `Fractalsense/` | Jest-Thresholds (s. P0-1) |

Die vollständige Suite läuft also auf PRs (via DeepJump) — **aber kein Coverage-Gate**.

---

## Vorschläge (priorisiert)

### P0-1 — Der JS-Coverage-Threshold ist wirkungslos (verifiziert) — ✅ UMGESETZT

`jest.config.js` setzt `roots: ['<rootDir>/__tests__']` **und**
`collectCoverageFrom: ['Fractalsense/**/*.js', ...]`. Jest crawlt nur die Pfade unter
`roots`, deshalb wird **keine einzige Datei unter `Fractalsense/` instrumentiert**. Die
Coverage-Tabelle bleibt leer, das Ergebnis ist „0 von 0", und die konfigurierten
`coverageThreshold`-Werte (branches 50 / functions 60 / lines 60 / statements 60)
greifen **vakuum-grün** durch.

Gemessen (unverändertes Repo-Setup):

```
File      | % Stmts | % Branch | % Funcs | % Lines |
All files |       0 |        0 |       0 |       0 |
Test Suites: 2 passed  Tests: 45 passed        # keine Threshold-Verletzung
```

Gegenprobe mit auf Repo-Root erweiterten `roots` — dieselben Tests, dieselben Quellen:

```
 app.js              |  0 | 0 | 0 | 0 | 4-221
 sensor-simulator.js |  0 | 0 | 0 | 0 | 7-251
Jest: Coverage for statements (0%) does not meet "global" threshold (60%)
Jest: Coverage for branches (0%) does not meet "global" threshold (50%)
Jest: Coverage for lines (0%) does not meet "global" threshold (60%)
Jest: Coverage for functions (0%) does not meet "global" threshold (60%)
```

Konsequenz: **1778 Zeilen ausgelieferter JS-Code** (`app.js`, `fractal-visualizer.js`,
`presentation-mode.js`, `resonance-enhancer.js`, `sensor-simulator.js`) werden als
„nichts" gemessen, und `test.yml` bleibt grün. Der Schwellenwert suggeriert einen
Schutz, den es nicht gibt.

Vorschlag:
1. `roots` um `<rootDir>/Fractalsense` erweitern (oder `roots` entfernen und über
   `testMatch` steuern) — damit wird der Threshold überhaupt erst scharf.
2. Threshold danach auf den **ehrlichen Ist-Wert** setzen und schrittweise anheben,
   statt auf einen Wunschwert, der nur wirkt, weil nichts gemessen wird.
3. `__tests__/unit/fractal-math.test.js` importiert `calculateMandelbrot` nicht,
   sondern **re-implementiert die Funktion inline** (Zeile 13). Solange das so bleibt,
   erzeugt auch ein korrekter `roots`-Wert keine echte Abdeckung. Die Mathe-Funktionen
   aus `fractal-visualizer.js` exportierbar machen und den Test dagegen laufen lassen.
   (Bereits im Juni-Report benannt, weiterhin offen.)

### P0-2 — `ui-app`s 23 Tests laufen in keinem Workflow (verifiziert) — ✅ UMGESETZT

`ui-app/test/*.test.mjs` (497 Zeilen, 23 Tests) laufen lokal grün, werden aber von
**keiner** CI-Pipeline ausgeführt:

- `ci-js-workspace.yml` → `pnpm turbo run typecheck lint build` — kein `test`.
- `test.yml` → Jest + `pnpm --filter entaengelment-ui build` — kein `test`.
- `turbo.json` **definiert** eine `test`-Task, `package.json` hat `turbo:test` —
  niemand ruft sie auf.
- `JS_VERIFY_CMD` im `Makefile` = `pnpm turbo run typecheck lint build` — ebenfalls ohne `test`.

Vorschlag: `test` in `ci-js-workspace.yml` und in `JS_VERIFY_CMD` aufnehmen
(`pnpm turbo run typecheck lint build test`). Das ist der billigste Gewinn im ganzen
Report: vorhandene, grüne Tests bekommen zum Nulltarif Gate-Wirkung.

Ergänzend: 4 von 7 `ui-app/lib/*.ts` sind ungetestet. Abgedeckt sind nur die drei
`tesser3takt-*`-Module. Ungetestet u. a. **`voidmap-parser.ts`** — parst die GOLD-Quelle
`VOIDMAP.yml` und ist genau das Ziel von `tools/voidmap_ui_drift_check.py`, das selbst
bei 0 % liegt. Beide Seiten des Drift-Checks sind also ungetestet.

### P0-3 — Die Fail-Closed-Pfade sind der schwächste Teil des Kernels

`src/core/evidence_routing.py` sieht mit 88 % Line / 84 % Branch gesund aus. Die
unabgedeckten Zeilen clustern aber fast vollständig auf den **Ablehnungspfaden**:

| Funktion | unabgedeckt | Art |
|---|---|---|
| `_apply_event` | 16 | 12× `raise EvidenceRoutingError` |
| `evaluate_transition_request` | 15 | `hold=True` / `stop=True` + ReasonCodes |
| `apply_approved_transition` | 15 | 9× `raise EvidenceRoutingError` |
| `_apply_retag_event` | 11 | 11× `raise EvidenceRoutingError` |
| `replay_events` | 6 | `EVENT_SCHEMA_INVALID`, `UNKNOWN_EVENT_TYPE` |

Insgesamt ~28 unabgedeckte `raise EvidenceRoutingError`-Stellen. Zusätzlich sind
**6 von 27 `ReasonCode`-Membern in keinem Test referenziert**:

- `VISIBILITY_VIOLATION`
- `EVENT_ORDER_INVALID`
- `UNKNOWN_EVENT_TYPE`
- `ALIAS_NORMALIZED`
- `HUMAN_DEFERRED`
- `HUMAN_REFERENCE_MISMATCH`

Die letzten beiden hängen an der Human-Approval-Invariante (ERK-Invariant 02).

Für ein Consent-First-System, dessen Zweck das **Verweigern** ist, ist „Happy Path grün,
Verweigerungspfade ungetestet" das umgekehrte Risikoprofil. Ein Regress, der eine
Ablehnung in ein stilles Durchlassen verwandelt, würde von der Suite nicht bemerkt.

Vorschlag: tabellengetriebener Test, der für **jeden** `ReasonCode` einen Input
konstruiert und asserted, dass er erzeugt wird — plus je ein Negativtest pro
`raise`-Cluster. Damit wird die Fail-Closed-Eigenschaft zur getesteten Zusage statt zur
Code-Lesart.

### P0-4 — Ledger: In-Memory-Verifier und Chain-Resume ungetestet

Auffällige Asymmetrie in `src/core/ledger.py`:

- `verify_chain_from_file()` hat 6 solide Manipulationstests
  (`tests/unit/test_ledger_file_integrity.py`): kaputtes JSON, Extra-Feld, fehlendes
  Feld, geändertes Payload, Nicht-Objekt.
- **`Ledger.verify_chain()` (in-memory) hat beide `return False`-Zweige unabgedeckt**
  (Zeilen 348, 352). Kein Test beweist, dass der In-Memory-Verifier einen gebrochenen
  Link oder einen Hash-Mismatch überhaupt erkennt.

Weitere unabgedeckte Stellen mit Audit-Relevanz:

- **`_load_last_hash()` (164–183)** — das Wiederaufsetzen der Hash-Kette auf einer
  bestehenden Datei. Komplett ungetestet. Ein Fehler hier bricht die Kettenkontinuität
  über Prozessgrenzen hinweg **still** — also genau die Append-Only-Garantie, auf der
  die Receipts beruhen.
- `verify_chain_from_file`: nicht existierende Datei → `return True` (406) und der
  `except (OSError, UnicodeError, …)` → `return False` (420). Beides ist dokumentiertes
  Verhalten ohne Test. Besonders „fehlende Datei = valide leere Kette" hat eine
  Fail-Open-Form und sollte durch einen Test festgenagelt werden, damit die Entscheidung
  bewusst bleibt.
- `Ledger.from_env()` (442–446) — env-getriebene Konstruktion ungetestet.

### P1-1 — HMAC-Evidence: Primitive getestet, Policy-Hülle nicht

`tools/status_emit.py` 28 %, `tools/status_verify.py` 47 %.

Gut: `sign_payload`, `canonical_json` und `verify_payload` **inklusive** Negativfälle
(`test_verify_payload_invalid`, `test_verify_payload_missing_sig`) sind abgedeckt. Die
Krypto-Primitive sind also nicht das Problem.

Ungetestet ist die **Policy drumherum** — wann sich das System weigert, zu signieren
bzw. zu verifizieren:

- `get_secret()`: der UNSIGNED-Fallback ohne Secret **und** das harte `OSError`, wenn
  `CI` gesetzt und kein Secret vorhanden ist. Genau diese zwei Verhalten beschreibt
  `CLAUDE.md` ausführlich — ohne Test.
- `status_verify.main()` (33–61): die Exit-Code-Zusage — `exit(2)` in CI ohne Secret,
  `exit(0)` im lokalen Skip-Modus, `exit(1)` bei Mismatch.
- `build_receipt`, `emit_receipt`, `emit_badge`, `get_git_info`,
  `compute_state_fingerprint`, `main()` — der gesamte Receipt-Zweig (v1.2) ist
  unabgedeckt; der einzige Test (`tests/test_status_emit.py`) fährt nur den
  `--status`-Happy-Path mit Secret per Subprocess.

Vorschlag: Contract-Tests auf die Exit-Codes und den UNSIGNED-Übergang. Das ist die
Stelle, an der „unsigned evidence" von „signed evidence" getrennt wird — sie sollte
nicht auf Codelesung beruhen.

### P1-2 — Guard-Tools: Helper getestet, `main()` nicht

Durchgehendes Muster (Helper via Import in `tests/test_tools_coverage.py` abgedeckt,
CLI-Einstieg nicht):

| Tool | Cover | Gate-Relevanz | Lücke |
|---|---|---|---|
| `metatron_check.py` | 43 % | **G4-Gate auf jedem PR** (`metatron-guard.yml`) | `main()` (91–136) |
| `port_lint.py` | 50 % | blockierend in `deepjump-ci.yml` + `make verify` | `main()`, Marker-Sequenz |
| `receipt_lint.py` | 52 % | **blockierend im pre-commit** + CI | `lint_file`-Fehlerzweige, `main()` |
| `snapshot_guard.py` | 57 % | `make snapshot` (--strict) | `main()` (68–98) |

`metatron_check.py` ist der Guard, der jeden PR auf `FOKUS:` prüft — sein Exit-Code-Pfad
ist ungetestet. „Guard-the-guard"-Lücke, in `tools/README.md` selbst als Roadmap-Punkt
vermerkt.

### P1-3 — Vier Tools weiterhin bei 0 % (unverändert seit Juni)

| Tool | Stmts | Status |
|---|---|---|
| `intake_add.py` | 96 | via `make intake`, ungetestet |
| `intake_shadow_copy.py` | 78 | **läuft als aktiver PostToolUse-Hook** (`.claude/settings.json`) |
| `voidmap_ui_drift_check.py` | 54 | **gegatet durch `make verify-governance`** |
| `verify_cards.py` | 89 | nur manuell (`cards/README.md`), in keinem Target/Workflow |

`intake_shadow_copy.py` läuft bei jedem dokumentartigen Write mit — ungetestet im
laufenden Betrieb. `voidmap_ui_drift_check.py` ist ein Gate, das selbst nicht geprüft wird.

### P2-1 — Coverage-Instrumentierung selbst

- **Kein Coverage-Gate auf PRs.** `--fail-under=50` steht nur im `build`-Job von
  `ci.yml`, und der ist `if: github.event_name != 'pull_request'`. Der PR-Pfad
  (`deepjump-audit.reusable.yml`) fährt `pytest tests/ -v` **ohne `--cov`**. Coverage
  kann in einem PR frei zurückfallen. (Der PR-Gate-Split ist bewusst und dokumentiert —
  aber der Coverage-Anteil fehlt darin.) War P3 im Juni-Report, weiterhin offen.
- **`--fail-under=50` bei 74 % Ist-Stand** = 24 Punkte Spielraum. Selbst auf dem
  Push-Pfad dürfte ein Viertel der Abdeckung verschwinden, ohne rot zu werden.
  Vorschlag: auf ~72 % einfrieren (Branch-Wert, konservativ) und per PR nachziehen.
- **Branch-Coverage ist nicht aktiviert** (`[tool.coverage.run]` ohne `branch = true`).
  Da die Lücken fast ausschließlich **Verweigerungs-Branches** sind (P0-3), ist genau
  diese Kennzahl die aussagekräftige. Aktivierung kostet eine Zeile und senkt die
  Zahl ehrlich von 74 % auf 72 %.

### P2-2 — Zwei Konfigurations-/Hygiene-Befunde in der Suite

- **Die deklarierten pytest-Marker sind tot.** `pyproject.toml` registriert
  `unit`/`integration`/`ethics` und setzt `--strict-markers`, aber **kein Test benutzt
  `@pytest.mark.*`** außer `parametrize`. Belegt:
  `pytest -m ethics` → `601 deselected / 0 selected` — still, ohne Fehler.
  `CLAUDE.md` führt die Marker als Konvention. Entweder anwenden oder aus der Config
  entfernen; aktuell liefert jede `-m`-Selektion lautlos nichts.
- **`tests/ethics/T3_fail_safe_expired_consent.py` wird nie eingesammelt** — der Name
  passt nicht auf `python_files = ["test_*.py"]`. Inhaltlich eine ältere Fassung von
  `test_fail_safe_expired_consent.py` (1 Test ohne Docstrings vs. 4 Tests mit). Toter
  Nachbar in der Ethics-Suite. Gemäß G3 nach `NICHTRAUM/archive/` verschieben, nicht löschen.

### P3 — Kleinere Lücken

- `src/core/eci.py` (66 % Branch): `permutation_test()` **vollständig** unabgedeckt,
  `save_specified_eci()` unabgedeckt, beide `ValueError`-Guards unabgedeckt,
  Default-Weights-Pfad unabgedeckt. Reine Funktionen, sehr billig zu testen.
- Trivial-Stubs bei 0 %: `src/cglg/gate_logic.py`, `src/cglg/mutual_perception.py`,
  `src/tools/cauchy_detector.py`, `src/meta_backprop.py` (2–4 Statements). `gate_logic.py`
  und `meta_backprop.py` sind explizit als Stubs mit Claim-Tag dokumentiert — dort ist
  0 % vertretbar. `mutual_perception.py` und `cauchy_detector.py` sind dagegen
  undokumentierte Einzeiler, wobei `cauchy_detector.py` in `CLAUDE.md` als
  Modul-Einstiegspunkt geführt wird. Je ein Characterization-Test würde das Verhalten
  festnageln und die Doku-Realität-Differenz sichtbar machen.
- `tests/verify_deep_jump.py` liegt in `tests/`, ist aber ein CLI-Utility (P9-Runbook),
  kein Test — wird nicht eingesammelt und ist selbst ungetestet.

---

## Empfohlene Reihenfolge

1. **P0-2** — `test` in `ci-js-workspace.yml` + `JS_VERIFY_CMD`. Ein Wort, 23 Tests
   bekommen Gate-Wirkung.
2. **P0-1** — `roots` in `jest.config.js` korrigieren, Threshold auf Ist-Wert setzen.
   Macht einen wirkungslosen Gate scharf.
3. **P2-1** — `branch = true`, `--fail-under` auf Ist-Stand, Coverage-Gate auf den
   PR-Pfad. Verhindert, dass die folgenden Gewinne wieder wegerodieren.
4. **P0-4** + **P0-3** — Ledger-Manipulationstests und ReasonCode-Vollständigkeitstest.
   Das inhaltliche Kernrisiko.
5. **P1-1** / **P1-2** / **P1-3** — Contract-Tests für Exit-Codes und die 0 %-Tools.

## Nicht getan (bewusst)

- **Keine Tests geschrieben, kein Produktivcode geändert.** Die Analyse selbst lief
  read-only (Pattern B / Witness Mode). Umgesetzt wurden anschließend nur die beiden
  Config-/CI-Änderungen aus P0-1 und P0-2 (nach explizitem Go, s. Nachtrag) — alle
  übrigen Vorschläge bleiben unimplementiert.
- **Keine GOLD-Pfade** (`index/`, `policies/`, `VOIDMAP.yml`, `spec/`, `seeds/`) berührt.
- **`pyproject.toml` unverändert** — P2-1 (`branch = true`, `--fail-under` anheben,
  Coverage-Gate in den PR-Pfad) ist weiterhin nur ein Vorschlag und braucht nach G0
  einen eigenen Checkpoint.
- **Die drei unvollständigen Fractalsense-Dateien wurden NICHT repariert** — das ist ein
  Fokus-Switch nach G4 und erfordert eine eigene Entscheidung (s. Nachtrag).
- `NICHTRAUM/`, `INBOX/` nicht angefasst (G2/G5).
- `Plugins/SynthosiaCore/` (C++/UE) nicht bewertet — außerhalb des Python/JS-Radius.
- Pakete außerhalb von `[tool.coverage.run] source` (`audit/`, `bio_spiral_viewer/`,
  `scripts/`, `mapping/`, `ledger/`) diesmal nicht neu vermessen; der Juni-Report deckt
  sie ab und der Befund („blinder Fleck in der Coverage-Config") gilt unverändert.
- Der `electron-packaging-glob-compat`-Suite fehlte in dieser Sandbox `electron-builder`;
  sie schlug lokal fehl. **Kein Repo-Befund** — in CI ist die Dependency vorhanden.

## Risiken

- **Zwei grüne Gates messen faktisch nichts:** der Jest-Threshold (P0-1, verifiziert)
  und der Python-Coverage-Gate auf PRs (existiert dort nicht, P2-1). Grünes CI wird
  aktuell als stärkere Zusage gelesen, als es ist.
- **Das Risikoprofil ist invertiert:** in einem Fail-Closed-Framework sind die
  Verweigerungspfade (P0-3) und die Audit-Trail-Kontinuität (P0-4) die am wenigsten
  getesteten Teile. Ein Regress in Richtung „lässt durch" ist derzeit leiser als einer
  in Richtung „blockt zu viel".
- Die 74 % überschätzen die Lage, weil Pakete außerhalb der Coverage-Config nicht
  mitgezählt werden (siehe Juni-Report) und weil ein Teil der Tool-Coverage aus
  Subprocess-Aufrufen stammt, die Coverage nicht mitschreibt.

## Offene Punkte

- [x] P0-1 (jest `roots`) und P0-2 (`test` in JS-CI) umgesetzt — s. Nachtrag.
- [ ] ☐ **Neu/dringend:** Sollen die drei syntaktisch unvollständigen Fractalsense-Dateien
      (`fractal-visualizer.js`, `presentation-mode.js`, `resonance-enhancer.js`) repariert
      werden? Fokus-Switch nach G4 — nicht in diesem PR angefasst.
- [ ] ☐ `--fail-under` auf 72 % anheben und Coverage-Gate in den PR-Pfad aufnehmen?
- [ ] ☐ Marker (`unit`/`integration`/`ethics`) anwenden oder aus `pyproject.toml`
      entfernen — welche Richtung ist gewollt?
- [ ] ☐ `tests/ethics/T3_fail_safe_expired_consent.py` nach `NICHTRAUM/archive/`
      verschieben (G3)?
- [ ] ☐ Ist `tools/verify_cards.py` weiterhin gewollt (nur manuell aufrufbar), oder
      Kandidat für ein Gate?

---

## Nachtrag: Umsetzung P0-1 + P0-2

**Datum:** 2026-07-30 · **Anlass:** explizites Go des Users auf „fix the jest roots and
add test to the JS CI". Damit ist der G0-Checkpoint für genau diese zwei Punkte erteilt.

### Geänderte Dateien

| Datei | Änderung |
|---|---|
| `jest.config.js` | `roots` um `<rootDir>/Fractalsense` erweitert; `coverageThreshold` auf 0 (ehrlicher Ist-Wert) |
| `.github/workflows/ci-js-workspace.yml` | `pnpm turbo run typecheck lint build` → `… build test` |
| `Makefile` | `JS_VERIFY_CMD` ebenso um `test` erweitert |
| `CLAUDE.md`, `EPISTEMIC_HYGIENE.md`, `docs/runbooks/pipeline_essentials.md` | Kommando-Referenzen nachgezogen (sonst Doku-Drift) |

`testMatch` blieb unverändert, und `Fractalsense/` enthält keine `*.test.js` — die
Test-**Discovery** ändert sich also nicht (vor und nach der Änderung: 45 Jest-Tests).
Nur die Coverage-**Instrumentierung** greift jetzt.

### Neuer Befund: drei Quelldateien sind nicht parsebar

Sobald real gemessen wird, meldet Jest:

```
Failed to collect coverage from Fractalsense/presentation-mode.js
Failed to collect coverage from Fractalsense/fractal-visualizer.js
Failed to collect coverage from Fractalsense/resonance-enhancer.js
SyntaxError: Unexpected token, expected "," (461:9)
```

Ursache ist **kein** Jest-/Babel-Problem: die drei Dateien sind **mitten im Statement
abgeschnitten** und haben keine schließenden Klammern.

| Datei | Zeilen | letzte Zeile |
|---|---|---|
| `fractal-visualizer.js` | 460 | `resolution: this.resol` (Identifier bricht ab) |
| `presentation-mode.js` | 405 | nach `case 'changeSoundType':` bricht ab |
| `resonance-enhancer.js` | 436 | nach `// Zufällige Position` bricht ab |

Diese Dateien werden im Browser per `<script>` geladen und würden dort mit demselben
`SyntaxError` fehlschlagen — das ist also kein reines Test-Thema, sondern **defekter
Quellcode**. Er war bisher unsichtbar, weil ihn niemand geparst hat: kein Test
importiert die Dateien, und die Coverage-Instrumentierung erreichte sie nie.

**Nicht repariert.** Das Wiederherstellen abgeschnittenen Codes ist ein Fokus-Switch nach
G4 (mein Fokus war „Test-Coverage analysieren", nicht „Fractalsense reparieren") und
erfordert Rekonstruktion verlorener Logik — das ist keine mechanische Änderung.

FOKUS-SWITCH: Test-Coverage analysieren -> Fractalsense-Quelldateien reparieren
Grund: Die korrigierte Coverage-Instrumentierung deckte auf, dass drei Quelldateien
       syntaktisch unvollständig sind (nicht parsebar, im Browser ebenfalls defekt).
Frage: Sollen die drei Dateien in einem eigenen Task repariert werden — und existiert
       eine vollständige Fassung (Backup / Git-History / externe Quelle), oder muss die
       abgeschnittene Logik neu geschrieben werden?

### Warum `coverageThreshold` jetzt auf 0 steht

Der korrigierte `roots`-Wert macht die Messung echt — und die echte Zahl ist **0 %**
(kein Test importiert die Quellen; `fractal-math.test.js` re-implementiert
`calculateMandelbrot` inline). Die alten Werte 50/60/60/60 wären damit sofort rot.

Da „CI rot machen" nicht Teil des Auftrags war, steht der Threshold jetzt auf dem
gemessenen Ist-Wert 0, mit ausführlichem Kommentar in `jest.config.js`. Das ist
**bewusst kein Zielwert, sondern ein Ratchet-Boden**: vorher war der Gate unsichtbar
wirkungslos, jetzt ist er sichtbar bei 0 und kann mit jedem echten Test angehoben werden.

> ☐ Offen: Soll stattdessen der Threshold hoch bleiben und CI bewusst rot laufen, bis
> echte Tests existieren? Das wäre die härtere Variante — Entscheidung liegt beim User.

### Verifikation

| Check | Ergebnis |
|---|---|
| `jest --coverage` (echte Config) | exit 0; Coverage-Tabelle zeigt jetzt Dateien statt leer |
| Jest-Testanzahl vor/nach | 45 / 45 — Discovery unverändert |
| `node --test ui-app/test/*.test.mjs` | 23 Tests grün |
| `pytest` (volle Suite) | 601 passed |
| `tools/workflow_posture_check.py` | PASS, 14 Workflows |
| `tools/claim_lint.py --scope index,spec,receipts,tools` | keine ungetaggten Claims |
| `tools/port_lint.py` | OK |
| `tools/verify_pointers.py --strict` | alle Core-Pointer valide |

`pnpm turbo run … test` war lokal nicht ausführbar (kein Workspace-Install in dieser
Sandbox) — dafür ist es **in CI auf diesem Commit belegt**:

- `CI — JS/TS Workspace` (Run 30513800187, PR + Push): `success`.
  Log: `Running typecheck, lint, build, test in 3 packages` → `entaengelment-ui:test`
  → `# tests 23 · # pass 23 · # fail 0` → `Tasks: 5 successful, 5 total`
  (vorher 4 Tasks, s. `OUT/PR260_stabilization_report.md`). Die 23 `ui-app`-Tests
  gaten also ab jetzt real.
- `Tests` (Run 30513800212): alle 6 Jobs `success`, inkl. Schritt
  „Run JavaScript tests with coverage". Die Coverage-Tabelle ist in CI jetzt
  **gefüllt statt leer** — `app.js` und `sensor-simulator.js` erscheinen mit 0 %, und
  die drei nicht parsebaren Dateien werden mit `SyntaxError` protokolliert. Der
  Coverage-Artifact enthält 21 Dateien.
  `Test Suites: 3 passed · Tests: 50 passed` — Discovery unverändert (die
  `electron-packaging-glob-compat`-Suite läuft in CI mit, weil `electron-builder` dort
  installiert ist; in dieser Sandbox fehlte nur diese Dependency).

Damit ist beides belegt: die Messung ist jetzt echt (P0-1) und die `ui-app`-Tests
laufen im Gate (P0-2) — bei durchgehend grüner CI.

## Artefakte

- `OUT/test_coverage_analysis_2026-07-30.md` (dieser Report)
- `jest.config.js`, `.github/workflows/ci-js-workspace.yml`, `Makefile` (P0-1 / P0-2)
