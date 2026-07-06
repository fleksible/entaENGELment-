# Report: Repository-Qualitäts-Audit (Full-Depth)

**Datum:** 2026-07-06
**Fokus:** Repo-Qualitäts-Audit komplett

## Ziel

Vollständige Qualitäts-, Sicherheits- und Hygiene-Analyse des gesamten Repositories
(Code, Tests, CI/CD, Konfiguration, Dependencies, Dokumentation) mit priorisierten
Handlungsempfehlungen. Alle Befunde basieren auf tatsächlich gelesenen Dateien und
auf real ausgeführten Checks (pytest, coverage, ruff, black, mypy, verify_pointers,
claim_lint, port_lint) in dieser Session.

---

## 1. Executive Summary

**Repo-Gesundheits-Score: 6.5 / 10**

Das Repository hat einen ungewöhnlich disziplinierten **Kern** (`src/`, `tools/`,
`tests/`, `.github/workflows/`): 186 Tests grün in ~2 s, 62 % Gesamt-Coverage,
ruff/black sauber, SHA-gepinnte GitHub-Actions, ein selbstgebauter
Governance-Layer (Pointer-Verify mit Path-Traversal-Schutz inkl. eigener
Security-Regressionstests, Claim-Lint, Workflow-Posture-Check, Drift-Checks).
Das ist deutlich über dem Niveau typischer Forschungs-Repos.

Dem gegenüber steht eine **ungepflegte Peripherie**, die den Score drückt:

- Ein **HMAC-Verifikations-Oracle** in `tools/status_verify.py` (gibt bei
  Signatur-Mismatch die korrekt berechnete Signatur aus — kritisch für das
  Vertrauensmodell des Receipt-Systems).
- Eine **faktisch kaputte und unsichere Electron-Restanwendung** im Root
  (`main.js`: `nodeIntegration: true`, `contextIsolation: false`, lädt eine
  Datei, die es unter diesem Namen nicht gibt; `electron` fehlt komplett in
  den devDependencies).
- `Fractalsense/` liegt **vollständig außerhalb der Lint-/Type-/Format-Membran**
  und enthält ZIP-Blobs, `.min.js`-Artefakte und GUI-Code in einer Datei namens
  `test_resonance.py`.
- **Fragmentiertes Dependency-Management** (pyproject + requirements.txt +
  verwaistes `uv.lock` + zwei weitere requirements-Dateien in Fractalsense),
  fast nichts gepinnt.
- Die Jest-Tests testen eine **Kopie** des Mandelbrot-Codes statt des
  Produktionscodes.

Der Kern verdient 8/10, die Peripherie 4/10. Der größte Hebel: die Peripherie
entweder in die Verify-Membran holen oder ehrlich nach `NICHTRAUM/archive/`
verschieben (G3-konform) — siehe Abschnitt 7.

---

## 2. Projekt-Überblick & Architektur

**Zweck:** Consent-First-Framework für resonante Multi-Agent-Systeme mit
auditierbarem Proof-Protokoll (DeepJump: Verify → Status → Snapshot) und
Governance-Guards G0–G6. Explizit experimentell, kein Production-Use.

**Tech-Stack & Schichten:**

| Schicht | Inhalt | Zustand |
|---|---|---|
| Python-Kern | `src/core`, `src/cglg`, `src/stability`, `src/tools` (Metriken, Gates, Ledger) | gepflegt, getestet |
| DeepJump-CLIs | `tools/` (17 Skripte: verify_pointers, claim_lint, status_emit …) | gepflegt, teils ungetestet |
| Tests | `tests/` (unit/integration/ethics/stability/benchmark/cpt), 186 Tests | grün, schnell |
| JS/TS-Workspace | `ui-app/` (Next.js 16, React 19, Tailwind 4), `packages/` via pnpm+Turbo | modern, strikt (tsconfig strict + noUncheckedIndexedAccess) |
| Insel 1 | `Fractalsense/` (Python-Tk-GUI + Vanilla-JS + ZIPs + Doku-Dumps) | ungepflegt |
| Insel 2 | Electron-Rest im Root (`main.js`, `Index.html`, package.json `build`) | kaputt |
| Insel 3 | `bio_spiral_viewer/` (Konsolen-Viewer) | ordentlich |
| Governance/GOLD | `index/`, `policies/`, `VOIDMAP.yml`, `spec/`, `seeds/` | konsistent, Drift-geprüft |
| Audit-Trail | `data/receipts/`, `receipts/` (IMMUTABLE) | append-only, Lint-geschützt |
| Doku | `docs/` (30 Unterverzeichnisse, 112 Markdown-Dateien) + ~15 lose Root-Dokumente | inhaltsreich, aber gesprawlt |

**Passt die Architektur zusammen?** Der bewusste "Inseln + Membran"-Ansatz
(SYNTHBIOSIS.md: Python-Domäne souverän, JS-Workspace additiv) ist als Konzept
dokumentiert und funktioniert für `ui-app/`. Er wird aber als Rechtfertigung
benutzt, `Fractalsense/` und den Electron-Rest gar nicht zu warten — dort ist
die Membran keine Grenze, sondern ein blinder Fleck.

---

## 3. Was gut läuft / Stärken

1. **Test-Suite: 186 Tests, 100 % grün, 2,2 s Laufzeit** (empirisch verifiziert).
   Schnelle Tests werden ausgeführt — das ist mehr wert als große, langsame Suiten.
2. **Echte Security-Regressionstests:** `tests/test_verify_pointers_security.py`
   testet Directory-Traversal-Abwehr (`../../outside.txt`) inkl. Positiv-Fall
   (`..` innerhalb des Repos erlaubt). Das sieht man selten.
3. **CI-Posture als Code:** `tools/workflow_posture_check.py` erzwingt
   `permissions:` + `concurrency:` in jedem Workflow — und tatsächlich erfüllt
   **jeder** der 13 Workflows beides (empirisch geprüft). Actions sind auf
   Commit-SHAs gepinnt (eine Ausnahme, s. u.).
4. **Reusable Workflow mit durchdachtem Detail:** `deepjump-audit.reusable.yml`
   dokumentiert im Kommentar sogar die Self-Cancellation-Falle von
   `github.workflow` in Concurrency-Groups — das zeugt von echtem Verständnis.
5. **Receipt-Lint mit Duplicate-Key-Loader:** `tools/receipt_lint.py` patcht
   PyYAML so, dass doppelte Keys hart fehlschlagen ("silently overwrite" wird
   explizit als Audit-Drift-Risiko benannt). Blocking im pre-commit-Hook.
6. **Dependabot für 3 Ökosysteme** (pip, npm, github-actions) mit dokumentierter
   Korrektur des pnpm-Workspace-Directory-Problems; `pnpm.overrides` patchen
   bekannte CVE-Ranges (form-data, postcss, undici).
7. **HMAC-Grundhandwerk korrekt:** kanonisches JSON, `hmac.compare_digest`
   (timing-safe), Secret-Maskierung via `::add-mask::` in CI, CI-Abbruch wenn
   `CI` gesetzt aber kein Secret.
8. **Bandit-Konfiguration mit begründeten Skips** (`.bandit.yaml` erklärt jeden
   Skip einzeln) statt pauschalem Abschalten.
9. **Drift-Checks als Gates:** `voids_backlog_gen.py --check` und
   `voidmap_ui_drift_check.py` verhindern, dass generierte Doku bzw. der
   UI-Mirror von `VOIDMAP.yml` wegdriften.
10. **`.gitignore` und Hooks sauber**, `CODEOWNERS`, `SECURITY.md`,
    `CONTRIBUTING.md`, PR-Template mit erzwungenem `FOKUS:`-Marker
    (automatisch geprüft via `metatron-guard.yml`).
11. **ui-app auf aktuellem Stack** (Next 16, React 19, ESLint 9 flat config,
    TS strict, statischer Export) mit sauber dokumentiertem
    VOIDMAP-Mirror-Kontrakt in `ui-app/lib/voidmap-parser.ts`.

---

## 4. Probleme & Verbesserungspotenziale

### 4.1 Kritisch / Sicherheitsrelevant

#### K1 — HMAC-Oracle: Verifier verrät die gültige Signatur

`tools/status_verify.py:29`:

```python
if hmac.compare_digest(target_hmac, computed_hmac):
    return True, "OK"
return False, f"Mismatch: {computed_hmac} != {target_hmac}"
```

**Problem:** Bei fehlgeschlagener Verifikation wird `computed_hmac` — also die
*korrekte* HMAC-Signatur für genau diese Payload unter dem geheimen Schlüssel —
im Klartext ausgegeben (`main()` druckt die Message nach stdout, in CI landet
sie im Log). Wer eine manipulierte Status-Datei durch den Verifier schleusen
kann (z. B. via PR, das den CI-Verify-Schritt triggert), bekommt die gültige
Signatur für seine Fälschung geliefert, ohne das Secret zu kennen. Das hebelt
das gesamte Vertrauensmodell der signierten Receipts aus.

**Fix (minimal-invasiv):**

```python
return False, "Mismatch: HMAC signature does not match payload"
```

Optional für Debugging: nur einen gekürzten Hash der *erwarteten* (gelieferten)
Signatur loggen, niemals die berechnete.

#### K2 — Electron-App: unsicher konfiguriert UND funktional kaputt

`main.js`:

```js
webPreferences: {
  nodeIntegration: true,
  contextIsolation: false
}
...
win.loadFile('index.html');
```

**Drei Probleme in 15 Zeilen:**

1. `nodeIntegration: true` + `contextIsolation: false` ist seit Jahren das
   dokumentierte Electron-Security-Antipattern: Jedes im Renderer geladene
   Skript hat vollen Node-/Dateisystem-Zugriff. `Index.html` ist eine 49-KB-App
   mit Inline-JS — jede XSS oder eingeschleuste Ressource wird zur RCE.
2. `loadFile('index.html')` — die Datei im Repo heißt **`Index.html`**
   (großes I). Auf case-sensitiven Dateisystemen (Linux, CI, AppImage-Target!)
   lädt die App nichts.
3. `electron` ist **gar nicht deklariert** (root `package.json` hat nur
   `electron-builder`), d. h. `npm start` (`electron .`) schlägt mit
   "command not found" fehl. Die App ist seit unbestimmter Zeit nicht startbar
   — die unsichere Konfiguration wurde also nie bemerkt.

**Empfehlung:** Entscheiden, ob die Electron-Hülle lebt oder nicht. Wenn ja:
`contextIsolation: true`, `nodeIntegration: false`, Preload-Script, Datei
umbenennen, `electron` als devDependency. Wenn nein (empfohlen, da `ui-app/`
die Rolle übernommen hat): `main.js`, `Index.html` und den `build`-Block der
package.json G3-konform nach `NICHTRAUM/archive/` verschieben.

#### K3 — Secrets via CLI-Argument

`tools/status_emit.py:250` und `tools/status_verify.py:35` akzeptieren
`--secret` als Kommandozeilen-Flag:

```python
parser.add_argument("--secret", help="Optional CLI secret (ENV preferred)", default="")
```

**Problem:** argv ist auf Mehrbenutzersystemen über `/proc/<pid>/cmdline` bzw.
`ps` für andere Prozesse lesbar und landet in der Shell-History. "ENV preferred"
im Helptext ist keine Kontrolle. Zudem ist die Semantik inkonsistent:
`build_status_payload` nutzt `get_secret() or args.secret`, der Receipt-Pfad
(`build_receipt`) ignoriert `--secret` komplett.

**Fix:** Flag entfernen (ENV-only) oder auf `--secret-file <path>` umstellen.

### 4.2 Hoch (sollte bald angegangen werden)

#### H1 — Ledger: Hash-Kette wird nach Reload nie verifiziert, Appends sind race-anfällig

`src/core/ledger.py` ist das Herzstück des "auditierbaren Audit-Trails", aber:

- `verify_chain()` (Z. 232–247) prüft **nur `self._events` im Speicher**. Beim
  Öffnen einer bestehenden Datei lädt `_load_last_hash()` nur den letzten Hash;
  eine manipulierte Historie in der Datei fällt nie auf. `load_ledger()`
  (Z. 261–284) verifiziert gar nichts und **überspringt kaputte Zeilen
  stillschweigend** (`except json.JSONDecodeError: continue`) — genau das
  Gegenteil von "no silent failures" (G6).
- `_emit()` öffnet die Datei pro Event neu im Append-Modus ohne Locking
  (Z. 149–152). Zwei parallele Prozesse (das CLI `gate_toggle.py` erzeugt via
  `ENTA_LEDGER_PATH` genau dieses Szenario) verzahnen ihre Ketten:
  `prev_hash` beider Prozesse zeigt auf ihr jeweils eigenes letztes Event,
  die Datei-Kette ist danach irreparabel gebrochen — unentdeckt, siehe Punkt 1.

**Fix:** (a) `verify_chain(path=...)`-Variante, die die Datei liest und die
Kette inkl. `prev_hash`-Verkettung prüft; in `_load_last_hash` mindestens die
letzte Zeile gegen `compute_hash()` validieren. (b) `fcntl.flock` (bzw.
portables Locking) um den Append + Re-Read des letzten Hashes vor jedem Write.
(c) Kaputte Zeilen beim Laden als Fehler melden, nicht überspringen.

#### H2 — Jest-Tests testen eine Kopie, nicht den Code

`__tests__/unit/fractal-math.test.js:11-14`:

```js
// Since FractalVisualizer is a class that depends on DOM, we'll extract
// and test the pure math functions directly
describe('Fractal Math Functions', () => {
  // Pure implementation of calculateMandelbrot for testing
  function calculateMandelbrot(a, b, maxIterations = 100) { ... }
```

**Problem:** Die einzige JS-Test-Datei importiert `fractal-visualizer.js`
niemals — sie testet eine im Test **reimplementierte** Mandelbrot-Funktion.
Ein Bug im Produktionscode kann diese Tests prinzipiell nicht brechen; die in
`jest.config.js` konfigurierten Coverage-Thresholds (60 % lines auf
`Fractalsense/**/*.js`) sind mit real 0 % erreichter Produktcode-Coverage
unerfüllbar bzw. werden nur deshalb nicht zum Problem, weil `pnpm run test:js`
ohne `--coverage` läuft. Das ist Scheinsicherheit.

**Fix:** Die Mathe-Funktionen aus `fractal-visualizer.js` als Modul
exportieren (`module.exports` guard für Browser-Kompatibilität) und im Test
importieren. Danach Coverage-Step ehrlich machen.

#### H3 — Kritische Tools ohne jeden Test

Empirische Coverage (pytest --cov, diese Session):

| Tool | Coverage | Brisanz |
|---|---|---|
| `tools/intake_shadow_copy.py` | **0 %** | läuft als PostToolUse-Hook bei **jedem** Write/Edit einer Claude-Session |
| `tools/intake_add.py` | 0 % | Teil des Calm-Intake-Kontrakts (Pattern F) |
| `tools/verify_cards.py` | 0 % | Verifier |
| `tools/voidmap_ui_drift_check.py` | 0 % | Gate in `verify-governance` |
| `tools/status_emit.py` | 28 % | erzeugt die signierten Receipts |
| `tools/status_verify.py` | 49 % | prüft die Signaturen |

Gerade der Shadow-Copy-Hook ist gut designt (Fail-soft, Exclude-Listen,
Dedupe — laut Docstring), aber genau diese Invarianten ("schreibt NIE außerhalb
`docs/intake/raw/auto/`") sind untestiert. Ein Regressions-Bug hier schreibt
unbemerkt in GOLD-Pfade.

**Fix:** Mindestens je einen Kontrakt-Test pro Tool: Hook mit synthetischem
stdin-Payload (Capture-Fall, Exclude-Fall, kaputtes JSON → Exit 0),
status_emit/verify als Roundtrip (emit → verify OK; tamper → verify FAIL).

#### H4 — Dependency-Management: vier Quellen der Wahrheit, fast nichts gepinnt

- `pyproject.toml` `[project.dependencies]` **und** `requirements.txt`
  duplizieren dieselben drei Pakete (numpy/scipy/pyyaml) — zwei Stellen, die
  auseinanderlaufen können.
- `uv.lock` (392 KB) liegt im Repo, wird aber **von nichts referenziert**
  (kein Treffer in Makefile, Workflows, Doku) — ein verwaister Lockfile, der
  Reproduzierbarkeit suggeriert, die es nicht gibt.
- Python-Deps sind durchgehend `>=`-Ranges; einzig `black==24.10.0` ist
  gepinnt (Inkonsistenz ohne erkennbaren Grund). CI-Läufe sind damit nicht
  reproduzierbar; ein numpy-Major-Bump kann CI von heute auf morgen brechen
  (der mypy-Kommentar in pyproject.toml Z. 111–114 dokumentiert genau so einen
  Vorfall mit numpy ≥ 2.5).
- Dazu `Fractalsense/requirements-dev.txt` und
  `Fractalsense/web_prototype_requirements.txt` als weitere Welten.

**Fix:** requirements.txt auf `-e .` bzw. pip-compile/uv umstellen — **eine**
Quelle. Entweder `uv.lock` in CI aktivieren (`uv sync --frozen`) oder die Datei
nach `NICHTRAUM/archive/` verschieben. Constraints-Datei für CI-Pinning.

#### H5 — `Fractalsense/` liegt komplett außerhalb der Qualitäts-Membran

`make lint/format/type-check` decken nur `src/ tools/ tests/` ab. Folgen:

- 2 518 Zeilen Python (`main.py`, `sound_generator.py`, …) ohne ruff, black,
  mypy — stilistisch ein anderes Repo (Tabs/Spacing, keine Typen).
- **`Fractalsense/test_resonance.py` ist gar kein Test**, sondern 376 Zeilen
  Tk-GUI-Code (ttk.Buttons, Sound-Playback) mit `test_*`-Namen. Da
  `Fractalsense/pytest.ini` `testpaths = tests` setzt, wird die Datei zufällig
  nicht eingesammelt — würde jemand pytest im Ordner anders aufrufen,
  explodiert die Collection.
- Committete Build-/Binärartefakte: `*.min.js` neben den Quellen, drei
  `.zip`-Archive (u. a. `fractal_sense_entaengelment.zip`), dazu ~20
  Markdown-Dumps (`detailed_response.md`, `todo.md`, `feasibility_analysis.md` …),
  die nach Pattern F eigentlich nach `docs/intake/` gehörten.

**Fix:** `test_resonance.py` → `resonance_gui.py` umbenennen; ZIPs und
`.min.js` nach `NICHTRAUM/archive/`; Ordner in ruff/black-Scope aufnehmen
(notfalls mit eigenem, milderem per-Verzeichnis-Regelsatz).

#### H6 — Root-`package.json`: falsche Lizenz, falscher Name

```json
"name": "user",
"license": "ISC",
"description": ""
```

**Problem:** `"license": "ISC"` widerspricht der Apache-2.0-`LICENSE` des
Repos — für ein Projekt mit eigener `LICENSE_REVIEW.md` ein echter
Compliance-Schnitzer. `"name": "user"` ist ein npm-init-Artefakt. Der
`build`-Block (electron-builder, NSIS/DMG/AppImage) konfiguriert eine App, die
nicht baubar ist (siehe K2). Nebenbei: `"mac"`-Block ist falsch eingerückt.

**Fix:** `name: "entaengelment"`, `license: "Apache-2.0"`, Beschreibung
setzen; `build`-Block mit der Electron-Entscheidung aus K2 zusammen behandeln.

### 4.3 Mittel

#### M1 — Namenskollision: zwei verschiedene `stability_guard.py`

`src/core/stability_guard.py` (Hessian-basiert, 3 Funktionen) und
`src/stability/stability_guard.py` (Taxonomie→Gate-Mapping mit Ledger/Strict)
sind **zwei verschiedene Module mit identischem Dateinamen** und
überlappender Domäne. `from stability_guard import ...`-Verwechslungen sind
vorprogrammiert. → Eines umbenennen (z. B. `hessian_gate.py`) oder
konsolidieren.

#### M2 — Wegwerf-Module ohne Kontrakt

```python
# src/cglg/gate_logic.py (komplette Datei)
def gate(phi: float, threshold: float = 0.6) -> bool:
    return phi >= threshold

# src/cglg/mutual_perception.py (komplette Datei)
def mutual_perception(a, b):
    return (a + b) / 2

# src/tools/throat_vector.py (komplette Datei)
def throat_vector(x, y, z):
    return (x**2 + y**2) ** 0.5 / (z + 1e-6)
```

Keine Docstrings, keine Typen (bei zweien), keine Validierung. Konkret bei
`throat_vector`: bei `z = -1e-6` → `ZeroDivisionError`, bei `z < -1e-6` kippt
das Vorzeichen — vermutlich nicht intendiert. Der Kontrast zur restlichen
`src/`-Qualität (vgl. `gate_toggle.py`) ist stark. → Entweder auf das Niveau
der Nachbarmodule heben oder als `[TODO]`-Stubs kennzeichnen.

#### M3 — `eci.py`: unseeded Legacy-RNG macht Validierung nicht reproduzierbar

`src/core/eci.py:73/85` nutzt `np.random.choice` / `np.random.permutation`
(globaler Legacy-RNG, kein Seed-Parameter). Für ein Framework, dessen
Snapshot-Guard "strikte Seeds" bewirbt, sind ausgerechnet Bootstrap-CI und
Permutationstest nicht reproduzierbar. → `rng: np.random.Generator`-Parameter
(`np.random.default_rng(seed)`) durchreichen.

#### M4 — Drei parallele Fraktal-Explorer

Root-`Index.html` (49 KB Inline-App "Fraktale Explorer mit
Chaos-Klang-Turing-Maschine"), `Fractalsense/index.html` (+ eigene JS-Module)
und `ui-app/app/fractalsense` (TypeScript-Port). Drei Implementierungen
derselben Idee, nur eine (ui-app) ist in CI verifiziert. → Die beiden
Alt-Versionen archivieren oder als historisch markieren.

#### M5 — `verify_pointers.py` scannt nur `*.yaml`, nicht `*.yml`

`tools/verify_pointers.py:199`: `index_dir.rglob("*.yaml")`. `VOIDMAP.yml`
wird nur über einen Spezialfall (Z. 203–205) erfasst. Legt jemand eine
`index/foo.yml` an, wird sie kommentarlos nie geprüft — ein stiller blinder
Fleck im wichtigsten Gate. → `rglob("*.y*ml")` bzw. beide Patterns.

#### M6 — Totes Test-Duplikat

`tests/ethics/T3_fail_safe_expired_consent.py` ist eine ältere Kopie von
`test_fail_safe_expired_consent.py` (gleicher Testname, gleiche Assertion).
Wegen des `T3_`-Präfixes sammelt pytest sie nie ein (`python_files = test_*`)
— toter Code, der bei Umbenennung plötzlich doppelt liefe. → Archivieren.

#### M7 — `test_core5_metrics.py`: Docstring mitten in der Datei, redundante Smoke-Tests

Der Modul-Docstring steht nach der ersten Testfunktion (Z. 12–16) — Artefakt
eines Merges; `test_metrics_exist_and_return_numbers` dupliziert die fünf
Einzeltests darunter. Generell prüfen viele Unit-Tests nur `isinstance(x,
float)` statt bekannter Werte (z. B. PLV für identische Phasen == 1.0, MI für
unabhängige vs. identische Signale). → Docstring hochziehen, Duplikat
entfernen, 3–4 Werte-Assertions ergänzen.

#### M8 — `make all` führt die Test-Suite doppelt aus

`all: verify test snapshot` — `verify` → `verify-core` enthält bereits `test`.
Kostet aktuell nur ~2 s, skaliert aber mit der Suite. → `all: verify snapshot`.

#### M9 — Silent-Failure-Muster in Release/SBOM-Workflows

`sbom.yml`: `cyclonedx-py ... || true` — schlägt die SBOM-Generierung fehl,
wird ein grüner Lauf ohne Artefakt produziert. `release.yml`:
`pip install -e ".[dev]" || pip install -e . || true`. Beides widerspricht G6
("keine silent failures"). → `|| true` entfernen bzw. durch explizites
`continue-on-error: true` mit Warn-Annotation ersetzen.

#### M10 — Eine Action nicht SHA-gepinnt

`.github/workflows/ci-js-workspace.yml:46`: `actions/setup-node@v6` — einzige
tag-gepinnte Action im Repo (alle anderen SHA-gepinnt, `test.yml` pinnt
setup-node korrekt auf `48b55a0...`). → Auf denselben SHA pinnen.

#### M11 — Jest-Umgebung mit Major-Versions-Mismatch

Root `package.json`: `jest ^29.7.0` mit `jest-environment-jsdom ^30.4.1`.
Jest erwartet Test-Environments derselben Major-Version; die 29/30-Mischung
funktioniert bestenfalls zufällig. → beide auf dieselbe Major (29 **oder** 30).

#### M12 — VOIDMAP-UI-Mirror: `version`-Feld driftet bereits

`ui-app/lib/voidmap-parser.ts` sagt `version: '1.0'`, `VOIDMAP.yml` ist
`"1.1"`. Der Drift-Check vergleicht nur `status/priority/title` — genau das
dokumentierte Loch wird schon genutzt. → `version` + `last_updated` in den
Byte-Vergleich aufnehmen.

### 4.4 Klein / Schönheitsfehler / Nice-to-have

- **Ungültige noqa-Direktive:** `tools/status_verify.py:42` `# noqa: claim-lint`
  — ruff warnt bei jedem Lauf ("expected a comma-separated list of codes").
  Claim-Lint-Ausnahmen brauchen einen eigenen Marker, kein `# noqa`.
- **`status_emit.py`:** Dateiname-Timestamp via `datetime.now()` ohne
  Zeitzone (Payload nutzt korrekt UTC) — Receipts aus verschiedenen Zeitzonen
  sortieren falsch; `"repo": "entaENGELment"` ist hartkodiert.
- **`status_verify.verify_payload()` mutiert den übergebenen dict**
  (`data.pop("signatures")`) — überraschender Seiteneffekt für Aufrufer.
- **`Ledger.close()`** ist ein No-op, `self._file` (Z. 107) wird nie benutzt —
  toter Zustand.
- **Root-Clutter:** `ark_cephalo_manifest_v2.json`, `resonance_checkpoint.yaml`,
  `hardware_requirements_summary.md`, `REPOSITORY_ESSENZ_ANALYSE.md` (30 KB) u. a.
  liegen lose im Root statt in `docs/`/`data/`.
- **`pdf_canvas/`:** PDFs mit Non-ASCII-Sonderzeichen im Dateinamen
  (U+2011 non-breaking hyphen, „·") — bereitet auf Windows-Checkouts und in
  Shell-Skripten Ärger.
- **Docs-Sprawl:** 112 Markdown-Dateien in 30 `docs/`-Unterordnern plus ~15
  Root-Dokumente; `docs/spec/` **und** `docs/specs/` koexistieren.
  `masterindex.md` hilft, aber die Doppelstruktur verwirrt.
- **`tests/test_verify_pointers_security.py:20`:** Fallback
  `shutil.which("python") or "/usr/local/bin/python"` — auf python3-only-Systemen
  ohne diese Binärdatei schlägt der Test aus dem falschen Grund fehl.
- **mypy lokal:** 6 × `Library stubs not installed for "yaml"` trotz
  installiertem `types-PyYAML` (Debian-System-PyYAML außerhalb site-packages).
  Kein Repo-Bug (CI installiert via pip und ist grün), aber ein Setup-Hinweis
  für `make install-dev` in der Doku wäre nett.
- **black `target-version = py312`** erzeugt unter Python 3.11 eine Warnung
  beim `--check` (AST-Safety-Check) — kosmetisch, aber irritierend.

---

## 5. Kategorisierte Zusammenfassung

| Kategorie | Bewertung | Kernaussage |
|---|---|---|
| **Security** | ⚠️ gemischt | Handwerk gut (compare_digest, Traversal-Schutz, Pinning, Masking), aber ein echtes HMAC-Oracle (K1), Electron-Antipattern (K2), Secret-in-argv (K3) |
| **Testing** | ✅➖ | 186 Tests grün/schnell, 62 % Coverage; aber 0 %-Inseln bei kritischen Tools (H3), JS-Tests testen Kopie (H2), viele Smoke-only-Asserts (M7) |
| **Code Quality & Hygiene** | ✅ Kern / ❌ Peripherie | src/tools/tests sauber (ruff/black grün); Fractalsense/Electron außerhalb jeder Membran (H5, K2) |
| **Architektur & Struktur** | ➖ | Membran-Konzept gut für ui-app; Inseln + Root-Clutter + 3× Fraktal-Explorer + Namenskollision stability_guard (M1, M4) |
| **Dependencies** | ⚠️ | 4 Quellen der Wahrheit, uv.lock verwaist, kaum Pins, jest/jsdom-Mismatch (H4, M11); Dependabot + Overrides positiv |
| **CI/CD** | ✅ | 13 Workflows, alle mit permissions+concurrency, SHA-Pins (1 Ausnahme), Posture-Check als Code; Abzug für `\|\| true` (M9, M10) |
| **Documentation** | ✅➖ | Ungewöhnlich reichhaltig (CLAUDE.md, WELCOME, Runbooks); aber Sprawl, spec/specs-Doppel, AI-Dump-Dateien in Fractalsense |
| **Maintainability** | ➖ | Kern gut wartbar; Peripherie erhöht kognitive Last erheblich; G3 (nie löschen) braucht diszipliniertes Archivieren, sonst wächst Ballast unbegrenzt |

---

## 6. Priorisierte Handlungsempfehlungen

| # | Maßnahme | Befund | Aufwand |
|---|---|---|---|
| 1 | HMAC-Oracle entfernen (computed_hmac nie ausgeben) | K1 | **schnell** (1 Zeile + Test) |
| 2 | Electron-Entscheidung: fixen oder archivieren (inkl. package.json `license`/`name`) | K2, H6 | **schnell** (archivieren) / mittel (fixen) |
| 3 | `--secret`-CLI-Flags entfernen bzw. `--secret-file` | K3 | **schnell** |
| 4 | Ledger: Datei-Ketten-Verify + Locking + laute Fehler | H1 | **mittel** |
| 5 | Kontrakt-Tests für intake_shadow_copy, status_emit/verify-Roundtrip, verify_cards | H3 | **mittel** |
| 6 | Jest-Test auf echten Produktionscode umstellen (Export aus fractal-visualizer.js) | H2 | **schnell–mittel** |
| 7 | Dependency-Konsolidierung: uv.lock aktivieren oder archivieren; requirements ↔ pyproject deduplizieren; jest/jsdom angleichen | H4, M11 | **mittel** |
| 8 | Fractalsense: test_resonance.py umbenennen, ZIPs/.min.js archivieren, in Lint-Scope aufnehmen | H5 | **mittel** |
| 9 | `verify_pointers` auch `*.yml` scannen; VOIDMAP-Drift-Check um `version` erweitern | M5, M12 | **schnell** |
| 10 | stability_guard-Namenskollision auflösen; One-Liner-Module dokumentieren/validieren | M1, M2 | **schnell** |
| 11 | `\|\| true` aus sbom/release entfernen; setup-node SHA-pinnen; `make all` Doppel-Test | M9, M10, M8 | **schnell** |
| 12 | Root-Clutter + totes Test-Duplikat + Docs spec/specs konsolidieren (G3-konform via NICHTRAUM/archive) | M4, M6, 4.4 | **aufwändig** (viele kleine PRs) |

---

## 7. Abschließende Einschätzung

Der größte Hebel ist nicht ein einzelner Bugfix, sondern eine **Grenzziehung**:
Dieses Repo hat eine der besten selbstgebauten Verify-Membranen, die man in
einem Forschungs-Repo finden kann — aber sie umschließt nur etwa die Hälfte des
Repos. Alles, was innerhalb liegt (`src/`, `tools/`, `tests/`, Workflows), ist
nachweislich gesund; praktisch jeder ernste Befund dieses Audits liegt
**außerhalb** (Electron-Root, Fractalsense, verwaiste Lockfiles, Doku-Dumps)
oder in **ungetesteten Rändern** der Membran selbst (status_verify-Oracle,
Ledger-Reload, 0 %-Tools).

Konkret als Ein-Satz-Strategie: *"Jede Datei im Repo ist entweder Teil der
Verify-Membran (gelintet, getypt, getestet) oder explizit als Archiv/Intake
markiert — nichts dazwischen."* Mit den Quick-Wins #1–#3 (zusammen < 1 Tag)
sind die sicherheitsrelevanten Befunde vom Tisch; mit #4–#8 steigt der Score
realistisch auf 8/10.

---

## Aktionen

- [x] Komplette Verzeichnisstruktur erfasst (526 Dateien, 100+ Verzeichnisse)
- [x] Alle Root-Configs gelesen (pyproject, package.json, Makefile, jest, turbo, tsconfig, pnpm-workspace, .bandit.yaml, .gitignore, dependabot)
- [x] Alle 13 GitHub-Workflows geprüft (permissions, concurrency, Pinning)
- [x] `src/` vollständig, `tools/` (Kern-CLIs) gelesen; Fractalsense, ui-app, bio_spiral_viewer, __tests__ stichprobenartig tief
- [x] Empirisch ausgeführt: pytest (186 passed), pytest --cov (62 %), ruff (pass + 1 Warnung), black --check (pass), mypy (6 env-bedingte Fehler), verify_pointers --strict (pass, 4 optional missing), claim_lint (pass), port_lint (pass)
- [x] Report nach OUT/ geschrieben

## Nicht getan

- Keine Fixes angewendet (Audit-Auftrag = Analyse; Plan-First / G0)
- `make verify-js` / `pnpm install` nicht ausgeführt (Zeit/Netz; ui-app-Verhalten aus Quellcode + CI-Konfig beurteilt)
- Kein Deep-Dive in alle 112 docs/-Markdown-Dateien und alle Receipt-JSONs (Struktur + Stichproben)
- bandit/pip-audit nicht lokal ausgeführt (CI deckt beides ab)

## Risiken

- HMAC-Oracle (K1) bleibt bis zum Fix aktiv ausnutzbar, sofern CI-Logs öffentlich sind
- mypy-Befund ist environment-abhängig (Debian-System-PyYAML) — vor Fix in CI reproduzieren

## Offene Punkte

- [ ] ☐ Entscheidung Electron: fixen oder archivieren (K2)
- [ ] ☐ Entscheidung uv.lock: aktivieren oder archivieren (H4)
- [ ] ☐ Klären, ob `jest --coverage` (test:js:coverage) in CI je grün war (Thresholds vs. 0 %-Produktcode-Coverage, H2)

## Artefakte

- `OUT/repo_quality_audit_2026-07-06.md` (dieser Report)
