# Report: Gegenlese der GOLD-Änderungen aus #407 und #408

**Datum:** 2026-10-23. Die Gegenlese erfolgt **nachträglich**: #407 und #408 wurden am
2026-10-18 gemergt. Sie belegt keinen Review vor diesen Merges.

**Fokus:** Gegenlese GOLD-PRs 407/408

**Status:** ANNEX · DERIVED · ohne Status-, Autoritäts- oder Promotionswirkung

**Geprüfter Stand:** `main@a99d55deeb38bf33564ebabb45841656fd45496a` (Merge #415, 2026-10-23 19:34 +0200)

**Vergleichsstand:** `main@e173790d4d883f1098fd37d6813dab7e608d2b96` (Merge #414, 2026-10-23 10:45 +0200)

**Prüfende Instanz:** Claude in Claude Code, Session vom 2026-10-23. #407 und #408 stammen
aus derselben Modellfamilie und Werkzeugkette. Diese Gegenlese ist darum eine
**Selbstprüfung der Agentenlinie**: keine unabhängige Gegenlese und kein Diogenes-Review.

## Ziel

Prüfen, ob in #407/#408 Änderungen, Belege und Statusentscheidungen zusammenpassen. Der Prüfumfang:

- VOID-011 `CLOSED` und VOID-010 `IN_PROGRESS` samt neuem Termin
- Runtime-Event-Spec mit Checker und Privacy-Regeln
- Codex-Befunde und ihre Korrekturen
- der tatsächlich dokumentierte Review-Nachweis

Getrennt werden drei Ebenen: technische Korrektheit, Review-Nachweis und menschliche Statusentscheidung.

## 1. Stand und spätere Änderungen

[FACT] Nach dem Vergleichsstand `e173790` kam nur #415 hinzu: drei Dokumente unter
`docs/annex/` und `docs/audit/`. Seit #408 (`f266f3b`) liefen #410–#415.

- Sie ändern **keine** GOLD- oder Receipt-Pfade.
- Sie ändern keine der geprüften Dateien.

`git diff f266f3b a99d55d` berührt im Python-Teil nur:

- `tools/thin_film_reflectance.py` mit seinem Test
- `tools/intake_shadow_copy.py`
- Lock-Dateien aus #410

Der Drift-Check des VOID-011-Exports besteht auf `a99d55d` unverändert.

| Geprüfte Datei | SHA-256 auf `a99d55d` |
|---|---|
| `VOIDMAP.yml` | `890f6400ba24bb5b8a994e419034929440f88270ab262d351d768b7cafbdc4f3` |
| `spec/runtime_eventlog_v0_1.json` | `fe7ae580b2e4b218e63d2c3d996f2789adf20da11bf01352a5474b19ed670a89` |
| `tools/eventlog_spec_check.py` | `62de579e4340a6659d27122aae26b6b805991b355d523d25be42850bd502aa57` |
| `tools/void011_metrics_export.py` | `71a129cb871007c3d29c89ce18d8b2f2c1f36e50d4d56892e94dafeea6614984` |
| `src/core/metrics.py` | `cbeb64d95c46445014c626f734dbd27280b60c34fa52f9bf511b797fa277c7cb` |
| `src/tools/toy_resonance_dataset.py` | `002d3857301225e8075fe2999f1a28d27ba67e5d781fb9ba174386ef8df5dc28` |
| `data/metrics/void011_resonance_metrics.csv` | `6bc5f43605cd6b7040c79a38d241ff831b6b37d50cfb9199abfb7f1e6bc120c9` |
| `data/metrics/void011_resonance_metrics.meta.json` | `65faa36c98234e03702602d2060c4b25af1c93b54b1d15e0bf1f447ec9f0f667` |
| `tools/spectra_table_lint.py` | `e04f5cd3d404e0a8542282e4a23d13b765f6c783a832670cfa3b12b139589ba0` |
| `data/spectra/spectra_sources.csv` | `c0534b3c4645b2530e5d626a5b6cbe7ff04d7ee0352a360bd41acbfe8d2ed86b` |
| `data/spectra/spectra_sources.schema.json` | `dfaf0da5cd5a4628aa06c6ca63222fd46a3bbc86c2e911dfb7aad73bbb964c53` |

## 2. Quellen

**GitHub-API**

- **PR #407:** Head `7449e91`, Merge `e74cd6f`. Gelesen: Body, Commits, Reviews, 6 Review-Threads, Kommentare, 39 Check-Runs.
- **PR #408:** Head `579a154`, Merge `f266f3b`. Gelesen: Body, Reviews, 1 Review-Thread, Kommentare, 38 Check-Runs.
- **Issues** #311 und #278 mit allen Kommentaren.
- **Suchen** nach „Diogenes“ in PRs und Issues des Repos.

**Repo-Dateien**

- Prüfgegenstand: `VOIDMAP.yml`, `spec/runtime_eventlog_v0_1.json`, die Werkzeuge
  `tools/void011_metrics_export.py`, `tools/eventlog_spec_check.py` und
  `tools/spectra_table_lint.py` samt Tests, `data/metrics/`, `data/spectra/` und
  `tests/fixtures/erk/*.jsonl`.
- Vergleichscode: `src/core/metrics.py`, `src/tools/toy_resonance_dataset.py` und `src/core/evidence_routing.py` (ERK).

**Vorberichte**

- [2026-10-18_gold_changes.md](2026-10-18_gold_changes.md)
- [2026-10-18_gesamtcheck.md](2026-10-18_gesamtcheck.md)

**Diogenes-Prozess**

- Review-Historie in [2026-07-14_tesser3takt_reentry_gap_audit.md](2026-07-14_tesser3takt_reentry_gap_audit.md) (§ 6)
- [2026-07-28_consolidation_reentry.md](2026-07-28_consolidation_reentry.md)
- PR #297 sowie die Integrationshinweise in #389 und #391

## 3. Ausgeführte Prüfungen

| # | Prüfung | Ergebnis |
|---|---|---|
| P1 | `make verify` auf `a99d55d` | 731 Tests + 165 Subtests grün. Port-Lint, Core-Pointer und Claim-Lint ok. 4 optionale `out/`-Pfade fehlen wie bisher. |
| P2 | `make verify-governance` | 15 Workflows erfüllen den Posture-Vertrag. 22 VOIDs sind mit dem UI-Spiegel synchron. |
| P3 | `python tools/void011_metrics_export.py --check` | `[CHECK] Up to date` |
| P4 | `render()` unter `PYTHONHASHSEED` 0, 1, 12345, random | identische CSV- und Meta-Hashes (siehe § 1); `csv_sha256` im Meta = Dateihash |
| P5 | `source_sha256` im Meta gegen die Dateien | alle drei stimmen |
| P6 | Higuchi-FD gegen unabhängige Referenz (Anhang A) | siehe § 4.1 |
| P7 | MI-Bias und Streuung über 200 Permutationen (Anhang B) | siehe § 4.1 |
| P8 | Mutationsproben M1–M9 in einem Wegwerf-Worktree | alle 9 erkannt (Tabelle § 4.4) |
| P9 | Randfälle des Eventlog-Checkers (18 privat, 4 Export, 5 Typfälle) | siehe § 4.3 |
| P10 | `eventlog_spec_check.py` über alle 5 ERK-Fixtures, privat und `--export` | privat 0 Befunde; Export: je Datei 1 Befund, erwartbar (s. u.) |
| P11 | ERK-Modell mit hash-only `CLAIM_CREATED` | ERK lehnt `claim_hash` als unbekanntes Feld ab |
| P12 | Einbindung der Checker in `Makefile`, Workflows und Hooks | keine direkte Einbindung; Wirkung nur über `pytest` |
| P13 | Gates auf dem Korrektur-Branch (#417) | siehe Liste unter der Tabelle |

P13 im Einzelnen:

- `make verify`: 741 Tests + 165 Subtests
- `make verify-governance`, `make lint`, `make type-check` und `black --check`: grün
- Export-Check: unverändert

[FACT] Weder JS/TS- noch Fractalsense-Dateien sind betroffen. `make verify-js` und
`npm run test:py` wurden darum nicht ausgeführt.

## 4. Befunde

### 4.1 VOID-011 — `CLOSED` (geschlossen 2026-10-18)

**Technisch**

- [FACT] **Closing Path wörtlich erfüllt.** Gefordert ist „toy_resonance_dataset + robust
  implementation + tests + SIMULATION_PROXY evidence receipt“. Vorhanden sind:
  - deterministischer Export unter `data/metrics/` (die VOID-Doku nennt `data/metrics/` oder `data/receipts/` als Ort)
  - jede der 42 Zeilen mit `SIMULATION_PROXY`
  - `claim_boundary` im Meta
  - `csv_sha256` und, seit #408, `source_sha256`
  - Drift-Check und 7 Exporttests

  Alle neun Evidence-Pfade in `VOIDMAP.yml` existieren.
- [FACT] **Determinismus.** Lokal (Python 3.13) sind die Hashes unter vier Hash-Seeds identisch.
  In CI lief `test_committed_export_matches_regeneration` auf Linux für Python 3.10–3.14 grün.
  Offen bleiben Byte-Gleichheit über Betriebssysteme und CPU-Architekturen; sie wird nicht behauptet.
- [FACT] **Toy-Grenze.** Toy-Daten erscheinen nirgends als reale Resonanzmessung:
  - CSV-Tag, Meta-`claim_boundary` und die VOID-011-Doku („kein Nachweis über reale Resonanz“) sind konsistent.
  - Einziger weiterer Verbraucher ist die Evidence-Pfadliste in `ui-app/lib/voidmap-parser.ts`.
- [FACT] **Higuchi-FD-Korrektur.** Sie ist richtig. `fd()` stimmt mit einer unabhängig
  geschriebenen Higuchi-Referenz (Higuchi 1988, `k_max = 4`) überein, wo nicht geklemmt wird.
  Der alte Wert lag exakt um 1 tiefer.

  | Reihe | `fd()` | Referenz ungeklemmt `k_max` 4 / 8 | vor dem Fix (ungeklemmt) |
  |---|---|---|---|
  | weißes Rauschen n = 512 | 2.000 | 2.006 / 1.999 | 1.006 |
  | Random Walk n = 512 | 1.516 | 1.516 / 1.552 | 0.516 |
  | Gerade n = 16 | 1.000 | 1.000 / 1.000 | 0.000 |
  | Toy-Signal `a`, Seed 7 | 1.0086 | 1.0086 / 1.0125 | 0.0086 |
  | Toy-Signal `a`, Seed 42 | 1.0064 | 1.0064 / 1.0101 | 0.0064 |

- [INFERENZ] **Grenzen der FD-Werte:**
  - Bei weißem Rauschen liegt die ungeklemmte Steigung über 200 Seeds zwischen 1.94 und 2.07.
    In 55 % der Fälle klemmt `fd()` auf 2.0. Der Referenztest `1.9 ≤ fd ≤ 2.0` wird teils
    durch die Klemmung erfüllt.
  - Die Exportwerte hängen an `k_max = 4`. Das Meta nennt `k_max` nicht; nur `source_sha256` bindet ihn.
- [FACT] **MI-Bias.** Die Aussage „~0,5 nats bei Unabhängigkeit, verschwindet mit n nicht“
  stimmt: Unabhängige Reihen ergeben 0.47 / 0.46 / 0.54 / 0.55 nats für n = 64 / 256 / 1024 / 4096.
  Ursache ist das √n-Binning. `MI_EXCESS` steigt je Seed mit der Kopplung.
- [INFERENZ] **`MI_EXCESS` bei schwacher Kopplung.** Bei S7-C0.1 ist `MI_EXCESS` mit 0.013 nats
  **nicht von Unabhängigkeit unterscheidbar**:
  - z = 0.75 gegen 200 Permutationen (SD ≈ 0.032 nats)
  - Permutations-p ≈ 0.24

  Bei S42-C0.1 ist er es (z = 3.65). Ab Kopplung 0.35 liegt z über 5.
  Das Meta führt die Streuung der Baseline nicht. Die Monotonie belegt also eine Ordnung,
  aber keinen Nachweis geteilter Information bei schwacher Kopplung.
- [FACT] **Drei der sieben Kennzahlen tragen keine Kopplungsinformation:**
  - Das Signal `a` ist je Seed über alle Kopplungen bytegleich. FD und PF sind darum je Seed konstant.
  - `ECI` ist `clamp01(mean(consent_signal))` und ergibt Kopplung + fester Versatz
    (−0.00255 bzw. −0.00084), ist also ein Parameterecho. Die Docstring von `eci()` sagt das
    selbst („KEIN validiertes Consent-Maß“); Meta und VOID-Doku sagen es nicht.

  Das ist kein Fehler, aber eine Lesegrenze.
- [FACT] **VOIDMAP-Notiz.** Die Notiz zu VOID-011 nennt nur `csv_sha256`. `MI_BASELINE`,
  `MI_EXCESS` und `source_sha256` kamen in #408 nach der Schließung dazu. Die Notiz ist
  damit unvollständig, aber nicht falsch.

**Review-Nachweis**

- [FACT] Die Schließung wurde **5 Sekunden nach dem Codex-Review** gemergt; 6 Befunde waren
  offen, davon 2 × P1. Merge war um 04:11:47Z, Review um 04:11:42Z. Issue #311 schloss um
  04:11:49Z automatisch.
- [FACT] Der P2-Befund zur fehlenden Implementierungsbindung (Codex: „The documented VOID-011
  plan explicitly requires a code revision“) wurde erst in #408 behoben, 26 Minuten später.
  Im Moment der Schließung fehlte der Evidence also die Quellbindung. Heute ist sie vorhanden
  und per Mutationsprobe M8 wirksam.

**Statusentscheidung (menschlich)**

- [INFERENZ] Die technische Basis trägt `CLOSED` innerhalb der `SIMULATION_PROXY`-Grenze.
  Ein Fehler, der die Schließung entwerten würde, wurde nicht gefunden.
- Ob die Schließung trotz dünnem Review-Nachweis stehen bleibt, entscheidet der Owner.
  Diese Gegenlese empfiehlt keine Statusänderung.

### 4.2 VOID-010 — `IN_PROGRESS`, Ziel 2027-01-31

**Technisch**

- [FACT] **Stand in `VOIDMAP.yml`:** `status: IN_PROGRESS`, `target_date: "2027-01-31"`,
  `closed: null`. Die Notiz vom 2026-10-18 begründet die Verlängerung (Forschungs-VOID,
  ≥ 5 begutachtete Quellen ausstehend).
- [FACT] **Tabelle leer.** `data/spectra/spectra_sources.csv` hat 1 Zeile, nur die Kopfzeile
  mit 14 Spalten. Das Schema ist `[SPEC-WIP]`. Es gibt keine empirischen Daten; README und
  VOID-Doku sagen das zutreffend.
- [FACT] **Was der Lint prüft und was nicht.** Der Lint mit 14 Tests prüft die Quellenpflicht
  je Zeile. Die **Abschlussbedingung prüft er nicht**:
  - keine Mindestzahl an Zeilen oder verschiedenen Quellen
  - `source_type` erlaubt `dataset`, das nicht begutachtet sein muss
  - ein DOI-Muster belegt kein Peer-Review

  Ein künftiger Abschluss braucht deshalb eine menschliche Quellenprüfung.
- [FACT] **Irreführende Ausgabe.** Für die leere Tabelle meldet der Lint `[OK] …: Quellenpflicht erfüllt`.
  Das ist nur leer wahr. Korrektur: siehe #417, Commit 2.

**Review- und Entscheidungsnachweis**

- [FACT] Die VOIDMAP-Notiz nennt „Owner-OK, issue #311“. Issue #311 enthält aber **keinen**
  Kommentar vom 2026-10-18; die letzten Owner-Kommentare stammen vom 2026-07-29 und
  2026-09-30. Das OK steht nur in agentenverfassten Texten:
  - Commit `30be2d1`
  - Merge-Nachricht `e74cd6f`: „Owner-OK vom 2026-10-18 (Auswahl + Merge-Freigabe)“
  - [2026-10-18_gold_changes.md](2026-10-18_gold_changes.md)
- [FACT] #311 schloss durch den Merge von #407. Formal stimmt das: VOID-010 ist durch den neuen
  Termin nicht mehr überfällig. Inhaltlich bleibt VOID-010 offen.

**Statusentscheidung (menschlich)**

- Termin und `IN_PROGRESS` sind konsistent. Zu bestätigen ist nur, dass der neue Termin
  tatsächlich die Owner-Entscheidung ist.

### 4.3 Runtime-Events und Privacy

**Spec auf `a99d55d`**

- Status `draft` und `[SPEC-WIP]`.
- `field_rules.enforcement`: „Checked by tools/eventlog_spec_check.py and its tests only; no runtime enforcement is claimed.“

| Anforderung | Stand | Belegt durch | Offen |
|---|---|---|---|
| `VOID_CLOSED` braucht `evidence_ref` **oder** `review_ref` | `required_one_of` | Tests; M4 erkannt | „Gültig“ heißt nur: vorhanden und nicht leer. Es gibt keine Existenz-, Format- oder Auflösungsprüfung: `does/not/exist.csv`, `0` und `false` werden akzeptiert. Im Repo gibt es **keinen Producer** für `VOID_CLOSED` und kein Fixture-Event; geprüft wird nur an synthetischen Tests. |
| `CLAIM_CREATED`: Text, Hash oder Ref; `claim_text` im reduzierten Export verboten | `required_one_of` + `reduced_forbidden_fields` | Tests | `claim_text` wird im Export auch leer, als `null` und im Envelope abgewiesen: streng, gut. `claim_hash` wird nicht auf sha256 geprüft; `"x"` passiert, obwohl `reduced_note` sha256 verlangt. |
| `CLAIM_RETAGGED`: sinnvolle `reason` oder `reason_codes` | `required_one_of` (seit #408) | Tests; M2 und M3 erkannt | „Sinnvoll“ prüft der Spec-Check nicht. `["NONSENSE"]`, der String `"HUMAN_APPROVED"` statt einer Liste und `reason: "."` passieren. Der ERK-Replay ist strenger: Er verlangt eine Liste bekannter `ReasonCode`s inkl. `HUMAN_APPROVED` und `POLICY_TRANSITION_ALLOWED`. |
| Leere Werte, Leerzeichen und ungültige Listeneinträge ablehnen | Leerzeichen seit #408; Listeneinträge `""`, `"  "`, `null` seit `579a154` | Tests; M1 und M2 erkannt | **Fehler:** `{}`, `[{}]` und Strings aus reinen Formatzeichen (U+200B, U+FEFF) galten als gefüllt; z. B. `VOID_CLOSED` mit `evidence_ref: {}`. Die Spec verlangt „non-empty“. **Korrektur:** #417, Commit 1. |

[FACT] **ERK-Fixtures**

- Die 5 Fixture-Dateien enthalten 28 Events. Davon liegen 7 im Spec-Vokabular:
  5 × `CLAIM_CREATED` und 2 × `CLAIM_RETAGGED`.
- Privat sind alle 7 konform. Mit `--export` scheitert je Datei das `CLAIM_CREATED` an
  `claim_text`. Das ist erwartbar, denn die Fixtures sind private Logs.
- 21 Events (`MATERIAL_REGISTERED`, `GUARD_DECISION_RECORDED` u. a.) liegen außerhalb des
  Spec-Vokabulars und werden übersprungen.
- Der Satz „Die ERK-Fixtures erfüllen den Vertrag“ in `RUNTIME_EVENTLOG_SPINE_v0_1.md`
  stimmt heute. Er umfasst nur diese 7 Events.

[FACT] **Unterschiedliche Formate; Zuordnungsvertrag offen**

- Der allgemeine Draft-Eventvertrag `runtime_eventlog_v0_1` erlaubt für
  `CLAIM_CREATED` Text, Hash oder Referenz. Seine reduzierte Eventform verlangt
  weiterhin `actor` und `claim_id`; das ist ein Event-Envelope-Vertrag.
- Das private ERK-Modell `ClaimCandidate` verlangt `claim_text`. Ein stattdessen
  direkt eingesetztes `claim_hash` wird als unbekanntes Feld abgewiesen. Diese
  Gegenprobe zeigt die Grenze dieses privaten Modells, keine Pflicht, sämtliche
  nach einem anderen Vertrag gültigen Events unverändert in dieses Modell einzulesen.
- `reduce_public_export` erzeugt einen reduzierten Zustands-Snapshot mit eigenem
  Schema `erk_public_export.v0.2`, keinen Stream reduzierter `CLAIM_CREATED`-Events.
  Roh-IDs und Actor-Details entfallen; Beziehungen verwenden exportlokale Referenzen.
- [INFERENZ] Zwischen Draft-Events, privatem Claim-Modell und öffentlichem Snapshot
  fehlt eine erklärte Zuordnung für einen tatsächlich gewünschten Transfer. Die
  Unterschiede allein belegen keinen defekten ERK-Export und entscheiden nicht,
  welcher Vertrag geändert werden soll. Private IDs oder Actor-Details werden
  deshalb weder wieder eingeführt noch veröffentlicht. Ein späterer Adapter oder
  Vertragsdiff braucht seinen eigenen Zweck, Erhalt/Verlust und Gegenfälle.

[FACT] **Weitere Lücken im Checker, ohne Korrektur**

- Fehlende, klein geschriebene oder mit Leerzeichen versehene `type`-Werte werden still übersprungen.
  Das CLI endet mit 0, auch wenn 0 Events geprüft wurden.
- Eine Zeile, die kein JSON-Objekt ist, oder ein `type` als Liste lässt den Checker abstürzen.
  Das ist fail-closed (Exit ≠ 0), aber ohne Befundtext.

[FACT] **Tatsächlicher Enforcement-Umfang**

- `eventlog_spec_check.py` ist weder in `Makefile`, Workflows noch Hooks eingebunden.
  Er wirkt nur über `pytest`, das CI ausführt, und dort nur auf synthetische Events und die 7 Fixture-Events.
- Der ERK (`src/core/evidence_routing.py`) liest die Spec nicht. `tools/erk_verify_emit.py`
  übernimmt nur Event-Namen für `VERIFY_PASS`/`VERIFY_PASS_UNSIGNED` aus ihr.
- **Spec- und Fixture-Prüfung sind kein Nachweis einer Runtime-Durchsetzung.** Eine solche ist
  weder implementiert noch behauptet; die Spec sagt das selbst richtig.

### 4.4 Codex-Befunde aus #407 und ihre Korrekturen in #408

| Thread | Befund | Korrektur | Nachprüfung 2026-10-23 |
|---|---|---|---|
| #407 P2 | Leerzeichen-Werte gelten als vorhanden | `c35d11b` | M1 (Strip entfernt): 4 Tests rot. Rest: `{}` und Formatzeichen → #417 |
| #407 P2 | `NaN`/`inf` passieren den Spektren-Lint | `c35d11b` | M5: 2 Tests rot |
| #407 P2 | Überzählige CSV-Zellen passieren | `c35d11b` | M6: 1 Test rot |
| #407 P1 | Fixture-Test prüft nur `CLAIM_CREATED`; `CLAIM_RETAGGED` verletzt die Spec | `c35d11b` + GOLD-CHANGE `798d542` | M3 (Spec zurück auf `reason` Pflicht): 2 Tests rot |
| #407 P2 | Meta bindet die Implementierung nicht | `d100dc3` (`source_sha256`) | M8 (Kommentar in Quelle ohne Neuexport): Drift erkannt. Gebunden sind Inhaltshashes der drei Quellen, nicht ein Commit. Die Quellen nutzen außer sich selbst nur die Python-Stdlib (`math`, `random`); eine Änderung dort fiele erst beim Neuerzeugen als Drift auf. |
| #407 P1 | Bericht in `OUT/` statt `docs/audit/` (G6) | `c35d11b` (`git mv`) | Datei liegt unter `docs/audit/` |
| #408 P2 | `reason_codes` mit leeren Einträgen | `579a154` | M2: 4 Tests rot |

Zusätzlich geprüft:

- M4: VOID_CLOSED ohne `review_ref`-Alternative → 2 Tests rot
- M7: FD wieder 1/k → 3 Tests rot
- M9: ein CSV-Tag auf `[FACT]` → Drift-Check und 1 Test rot

[FACT] **Zeitlinie** (UTC, 2026-10-18)

| Zeit | Ereignis |
|---|---|
| 04:03:56 | #407 eröffnet |
| 04:04:51 | CI auf `7449e91` abgeschlossen: 39 Check-Runs, alle `success` oder `skipped` |
| 04:11:42 | Codex-Review mit 6 Befunden |
| 04:11:47 | Merge #407 |
| 04:11:49 | #311 und #278 geschlossen |
| 04:25:44 | #408 eröffnet |
| 04:25:49–04:26:00 | Antworten auf die #407-Threads, Threads aufgelöst |
| 04:31:08 | Codex-Review auf `8a6c9ae` mit 1 Befund |
| 04:31:43 | Fix `579a154` |
| 04:32:45 | CI auf `579a154` abgeschlossen: 38 Check-Runs, alle `success` oder `skipped` |
| 04:34:06 | Codex-Re-Review ohne Befund |
| 04:37:14 | Merge #408 |

[INFERENZ] #408 folgte dem Muster „Befund vor Merge beheben, erneut prüfen“. #407 nicht.

### 4.5 Review-Nachweis: was tatsächlich dokumentiert ist

**Claude-Autorenschaft: sichtbar** [FACT]

- Alle 13 Nicht-Merge-Commits beider PRs tragen `author=Claude <noreply@anthropic.com>`,
  Co-Authored-By-Trailer und den Session-Link.
- Die PR-Bodies enden mit „Generated by Claude Code“.
- Die Thread-Antworten stehen unter dem Konto `fleksible`, tragen aber den Claude-Code-Footer.
  Sie sind agentenverfasst, nicht vom Owner.

**Codex-Reviews: sichtbar** [FACT]

- Bot `chatgpt-codex-connector[bot]`, automatisch ausgelöst.
- Alle 7 Threads sind aufgelöst.
- #408 schließt mit „has_any_findings: false“ auf `579a154`.

**Menschlicher Review: nicht als Artefakt vorhanden** [FACT]

- Es gibt keine Approval-Reviews. Die „Reviews“ des Kontos `fleksible` auf #407/#408 sind die
  agentenverfassten Thread-Antworten ohne eigenen Text.
- Gemergt hat das Konto `fleksible`. Die Merge-Nachricht von #407 ist agententypisch formuliert,
  und der Gesamtcheck-Bericht führt „#407 gemergt“ als Aktion der Session.
- Ob ein Mensch oder der Agent mit dem Owner-Konto den Merge ausgelöst hat, lässt sich aus
  GitHub-Daten nicht unterscheiden.

**Owner-Entscheidungen: nur agentenseitig dokumentiert** [FACT]

Betroffen sind:

- Schließung von VOID-011
- neuer Termin für VOID-010
- `reason` oder `reason_codes` in der Spec
- MI-Baseline
- Claim-Tags „Status quo“

Belegt sind sie in Commit-Texten, Merge-Nachricht und Berichten von Claude.
Owner-verfasste Belege auf GitHub vom 2026-10-18 gibt es nicht.

**Diogenes: kein identifizierbarer Beleg** [FACT]

Durchsucht wurden:

- Repo-Volltext: Treffer nur in Dokumenten vom Juli und älteren `OUT/`-Berichten
- GitHub-PR-Suche: Treffer nur #297, #389 und #391
- Issue-Suche: kein Treffer
- Bodies, Threads und Kommentare von #407 und #408
- beide Berichte vom 2026-10-18

Für #407 und #408 fand sich kein Diogenes-Beleg. Der bisherige Befund ist damit bestätigt.

- [INFERENZ] Eine Gegenlese außerhalb von Repo und GitHub, etwa im Chat, ist damit **nicht
  ausgeschlossen**. Sie ist nur nicht belegt.

**Governance-Abgleich** [FACT]

- **`annex.md`, GOLD-Prozess:** Die Regel „Review erforderlich vor Merge“ ist für #407 nicht
  durch ein Review-Artefakt erfüllt. Der PR-Body bat selbst: „Bitte vor dem Merge reviewen:
  Drei Commits ändern GOLD-Dateien.“ Das Label `GOLD-CHANGE` fehlt; das ist dokumentiert.
- **G6:** CI war vor beiden Merges grün. Der #407-Bericht lag beim Merge in `OUT/`.
- **#278:** Leitplanke „draft/spec-wip unless reviewed“ eingehalten (Spec bleibt `draft`).
  Die Triage vom 2026-09-30 sah vor: „issue stays open for reviewed contract changes“.
  Geschlossen wurde das Issue vor Behebung der Review-Befunde.

**Bestehender Diogenes-Prozess**

Diogenes-Prüfungen laufen bisher **user-relayed**. Sie werden append-only als Review-Historie
eingetragen, mit `source`, `scope`, `result`, `limits`, `independence`, `authority_effect`,
`decision_effect`, `promotion_effect` und `open_human_decisions`. Aus dieser Session ist der
Prozess nicht auslösbar. Die Übergabe dafür steht in § 6.

### 4.6 Review-Historie (append-only)

**2026-10-18 — Codex-Review #407**

- `source`: GitHub-Bot, automatisch
- `scope`: Commit `7449e91`
- `result`: 6 Befunde (2 × P1, 4 × P2), alle nach dem Merge in #408 behoben

**2026-10-18 — Codex-Review #408**

- `source`: GitHub-Bot, automatisch
- `scope`: `8a6c9ae`, Re-Review `579a154`
- `result`: 1 Befund (P2), vor dem Merge behoben; Re-Review ohne Befund

**2026-10-23 — Claude-Gegenlese (diese Session)**

- `id`: claude-gegenlese-2026-10-23
- `source`: direct
- `review_kind`: nachträgliche Gegenlese nach Merge; Selbstprüfung derselben Agentenlinie
- `independence`: none. Gleiche Modellfamilie und Werkzeugkette wie die Autorin von #407/#408.
  Kein Diogenes-Review, keine menschliche Prüfung.
- `attested_refs`: `main@a99d55d`; `#407@7449e91` → `e74cd6f`; `#408@579a154` → `f266f3b`
- `scope`: GOLD-Diffs beider PRs, Begleitwerkzeuge, Tests, Fixtures und GitHub-Metadaten.
  Prüfungen P1–P13. Ausführung und Gegenproben statt nur Lektüre.
- `result`: technisch weitgehend bestätigt. Zwei kleine ANNEX-Fehler; Korrekturvorschlag #417.
  Review- und Entscheidungsnachweis lückenhaft.
- `limits`:
  - Session-Transkript vom 2026-10-18 nicht gelesen (keine Repo-Quelle)
  - keine Plattform-übergreifende Reproduktion
  - GitHub-Suche indexbasiert
- `authority_effect`: none
- `decision_effect`: none
- `promotion_effect`: none

**2026-10-24 — Codex-Nachprüfung der Berichtsaussagen**

- `source`: direct; heutiger Auftrag zur Bearbeitung der vorgelegten ANNEX-Korrekturen
- `scope`: fünf ERK-Fixtures und §4.3, privates `ClaimCandidate`, öffentliche
  `reduce_public_export`-Implementierung und eigener Export-Schemaname am Stand `a99d55d`
- `result`: 28 Events (5 + 7 + 5 + 3 + 8), sieben im Spec-Vokabular und 21 außerhalb.
  Die vorherigen Zahlen 31/24 waren Zählfehler und wurden in §4.3 korrigiert.
  Die bisherige Schlussfolgerung „Spec und Runtime laufen auseinander“ wurde auf
  die tatsächlich verschiedenen Formate und den offenen Zuordnungsvertrag begrenzt.
- `limits`: gezielter Anschlussreview mit Kenntnis dieses Berichts; kein blinder,
  vollständiger oder Diogenes-Review und keine neue Nachprüfung aller P1–P13-Fachbefunde.
- `validation`: `make verify` (731 Tests und 165 Subtests), `make verify-governance`
  und `git diff --check` am unveränderten ausführbaren Basisstand bestanden.
- `independence`: gemeinsame Repo-/Berichtsquellen; keine unabhängige Evidenzpromotion
- `authority_effect`: none
- `decision_effect`: keine Änderung historischer GOLD- oder Owner-Entscheidungen
- `promotion_effect`: none

**Diogenes:** ausstehend. Übergabe in § 6.

## 5. Übersicht: drei Ebenen

| Gegenstand | Technische Korrektheit | Review-Nachweis | Menschliche Statusentscheidung |
|---|---|---|---|
| VOID-011 `CLOSED` | trägt innerhalb `SIMULATION_PROXY`; FD-Fix korrekt; Lesegrenzen bei MI_EXCESS (schwach), ECI, FD und PF | Codex ja, nach dem Merge behoben; kein menschliches oder Diogenes-Artefakt | Owner-OK nur agentenseitig dokumentiert; zu bestätigen |
| VOID-010 Termin 2027-01-31 | konsistent; Tabelle leer; Lint prüft den Abschluss nicht | wie oben | Owner-OK nur agentenseitig dokumentiert; zu bestätigen |
| Spec `VOID_CLOSED` / `CLAIM_CREATED` | Vertrag prüfbar; Leerwert-Lücke (`{}`, Formatzeichen) → #417; Formatgrenzen bei Hash und reduzierten Feldern; Zuordnung offen | Codex ja | offen: Reduktions-Feldsatz, Hash-Format, Ref-Gültigkeit |
| Spec `CLAIM_RETAGGED` | prüfbar; Codes ohne Vokabular | Codex ja, vor dem Merge behoben | offen: Vokabular im Spec-Check, ja oder nein |
| Runtime-Durchsetzung | nicht vorhanden, nicht behauptet | — | — |

## 6. Übergabe an eine Diogenes-Gegenlese (user-relayed)

Vorschlag für Scope und Prüffragen. Das Ergebnis wäre als eigener, datierter Eintrag an
§ 4.6 anzuhängen, nicht in diese Gegenlese einzuarbeiten.

1. **Selbstprüfung:** Reichen § 4.1–4.3 der Selbstprüfung, oder fehlt ein Gegenbeispiel,
   das eine gleich trainierte Instanz übersieht?
2. **VOID-011:** Trägt „robust implementation“ im Closing Path die Schließung, obwohl
   - `mi()` unverändert einen Bias von ~0,5 nats hat,
   - FD mit `k_max = 4` nahe der Klemmgrenzen arbeitet und
   - drei von sieben Kennzahlen keine Kopplungsinformation tragen?
3. **Formatzuordnung:** Welcher konkrete Transfer zwischen Draft-Event, privatem
   Claim-Modell und öffentlichem Snapshot wird benötigt? Welche Information soll
   erhalten bleiben und welche darf die öffentliche Privacy-Grenze nicht passieren?
4. **Zirkularität:** Wiegt es, dass Owner-OKs nur agentenseitig dokumentiert sind? Reicht
   eine nachträgliche Owner-Bestätigung als Beleg?

## Aktionen

- [x] AGENTS.md, CLAUDE.md, `.claude/rules/` und frühere Diogenes-Belege gelesen
- [x] Aktuellen Stand ermittelt (`a99d55d`) und spätere Änderungen #410–#415 abgeglichen
- [x] PR-, Review-, Check- und Issue-Daten über die GitHub-API gelesen
- [x] Repo-Gates und gezielte Prüfungen P1–P13 ausgeführt
- [x] Korrekturvorschlag auf separatem Branch als Draft-PR #417: nur ANNEX, zwei Commits
- [x] Dieser Bericht

## Nicht getan

- Kein Merge, keine Issue-Schließung oder -Wiedereröffnung, keine Statusänderung oder -promotion
- Keine Änderung an GOLD-Dateien (`VOIDMAP.yml`, `spec/`, `policies/`) oder Receipts
- Kein Diogenes-Review: Der Prozess ist user-relayed und aus dieser Session nicht auslösbar
- Session-Transkript vom 2026-10-18 nicht ausgewertet; Owner-OKs nur nach Repo- und GitHub-Lage beurteilt
- Keine ERK-Änderung, kein Vokabular und keine Formatprüfung im Spec-Check (Inhaltsfragen, s. u.)
- Kein `make verify-js` und kein Fractalsense-Lauf: weder JS- noch Fractalsense-Dateien sind betroffen

## Risiken

- [RISK] Diese Gegenlese stammt von derselben Agentenlinie wie das Geprüfte. Gemeinsame blinde
  Flecken sind wahrscheinlicher als bei einer unabhängigen Prüfung.
- [RISK] Solange die Owner-OKs nur agentenseitig belegt sind, ruht die GOLD-Legitimation von
  #407 auf Texten der ausführenden Instanz.
- [RISK] Ohne erklärten Zuordnungsvertrag kann eine direkte Übergabe eines hash-only
  Draft-Events an das private ERK-Claim-Modell scheitern. Eine solche Pipeline ist
  hier nicht als bestehender Runtime-Pfad nachgewiesen; ein Snapshot ist kein Eventstream.

## Offene Punkte

- [ ] ☐ Owner: Die Owner-OKs vom 2026-10-18 bestätigen oder korrigieren, und zwar an einem
      Owner-verfassten Ort (z. B. Kommentar in #311 bzw. #278). Betroffen:
      - VOID-011 `CLOSED`
      - VOID-010 → 2027-01-31
      - `reason` oder `reason_codes`
      - MI-Baseline
      - Claim-Tags „Status quo“
- [ ] ☐ Owner: Draft-PR #417 prüfen. Commit 2 ist optional.
- [ ] ☐ Owner, GOLD-Spec: Inhaltsfragen klären
  - Zuerst Transferzweck und Formatzuordnung klären; keine Roh-IDs oder Actor-Details
    allein zur Angleichung des öffentlichen ERK-Snapshots wieder einführen.
  - Wird `claim_hash` auf sha256 festgelegt?
  - Muss eine Ref auflösbar sein?
  - Prüft der Spec-Check `reason_codes` gegen das ERK-Vokabular?
- [ ] ☐ Diogenes-Gegenlese nach § 6 (user-relayed), als eigener Eintrag
- [ ] ☐ Optional: MI-Baseline-Streuung ins VOID-011-Meta; VOIDMAP-Notiz zu VOID-011 um
      #408-Nachtrag ergänzen (GOLD, nur nach OK)
- [ ] ☐ VOID-010: vor dem Abschluss festlegen, was als „begutachtete Quelle“ zählt
      (`dataset` ja oder nein); Mindestzahl ggf. im Lint

## Artefakte

- `docs/audit/2026-10-23_gold_pr407_408_gegenlese.md` (dieser Bericht)
- Draft-PR #417, Branch `claude/gold-pr-407-408-review-68jvdk-korrektur`:
  - `tools/eventlog_spec_check.py`, `tests/unit/test_eventlog_spec_check.py`
  - `tools/spectra_table_lint.py`, `tests/unit/test_spectra_table_lint.py`

## Anhang A — FD-Referenz (gekürzt)

```python
import math, statistics

def higuchi_raw(x, kmax):  # Higuchi 1988, ohne Klemmung
    N, lk, ll = len(x), [], []
    for k in range(1, kmax + 1):
        Lm = []
        for m in range(1, k + 1):
            M = (N - m) // k
            s = sum(abs(x[m - 1 + i * k] - x[m - 1 + (i - 1) * k]) for i in range(1, M + 1))
            Lm.append(s * (N - 1) / (M * k) / k)
        lk.append(math.log(1 / k)); ll.append(math.log(statistics.fmean(Lm)))
    n, sx, sy = len(lk), sum(lk), sum(ll)
    return (n * sum(a * b for a, b in zip(lk, ll)) - sx * sy) / (n * sum(v * v for v in lk) - sx * sx)
# Vergleich: src.core.metrics.fd(x) gegen higuchi_raw(x, 4) auf Rauschen, Random Walk,
# Gerade, Sinus und generate_mycel_signals(256, seed, c).a
```

## Anhang B — MI-Permutationsstreuung (gekürzt)

```python
import random, statistics
from src.core.metrics import mi
from src.tools.toy_resonance_dataset import generate_mycel_signals

ds = generate_mycel_signals(256, 7, 0.1)
vals = []
for k in range(200):
    s = list(ds.b); random.Random(10_000 + k).shuffle(s); vals.append(mi(ds.a, s))
z = (mi(ds.a, ds.b) - statistics.fmean(vals)) / statistics.stdev(vals)  # ≈ 0.75
```
