# Report: Repo-Checkup Funktion, Korrektheit, Anschluss, Form

**Datum:** 2026-10-28
**Fokus:** Repo-Checkup ohne Änderungen
**Stand:** `e8bea51` (Merge #432)
**Modus:** Witness. Der Code bleibt unverändert, einziges Artefakt ist dieser Report.

## Ziel

Das Repo auf Funktion und Korrektheit prüfen, und zwar in der Essenz (tut der Kern,
was er verspricht?), im Anschluss (passen Teile und Doku zusammen?) und in der Form.
Ohne Befund wäre das auch ein Ergebnis gewesen.

## Ergebnis in einem Satz

Alle Gates sind grün. Die Lücken liegen dort, wo Tests nicht hinschauen: Das
MZM-Hard-Gate öffnet bei `NaN`, der Core-Stability-Guard lässt einen degenerierten
Sattel mit Consent passieren, und `permutation_test` ist statistisch leer.

## Gates (alle grün)

| Gate | Ergebnis |
|------|----------|
| `make verify` (port-lint, pytest, verify-pointers --strict, claim-lint) | 857 passed, 2 skipped (DataLad nicht installiert) |
| `make verify-governance` | 16 Workflows PASS, Backlog aktuell, 22 VOIDs in sync |
| `ruff` / `black --check` / `mypy` / `bandit` | sauber (117 Files, 58 Source-Files) |
| `claim_lint --strict`, `receipt_lint --strict ark/p4/receipts`, `receipt_lint receipts/*.json` | PASS |
| `void011_metrics_export --check`, `spectra_table_lint`, `verify_cards`, Grimm-Fixtures | PASS |
| `make snapshot` / `demo` / `gate-test` / `benchmark-replay` / `erk-drill` | PASS (`out/` in Scratchpad umgeleitet) |
| Fractalsense-pytest | 184 passed |
| Jest (root) | 68 passed |
| `pnpm install --frozen-lockfile` + `turbo typecheck lint build test` | 5/5 Tasks, ui-app 58 Tests, Next-Build 9 Routen |

Umgebung: Python 3.13, Node 22.22, pnpm 10.33.0; Python-Deps aus `requirements-dev.txt`
(hash-gepinnt) in einer venv außerhalb des Repos.

## Befunde

### B1 · HOCH · MZM-Hard-Gate öffnet bei `NaN` (Essenz)

`tools/mzm/gate_toggle.py:80` und `:89`: Jeder Vergleich mit `NaN` ergibt `False`.
Damit greift weder `phi < phi_min` noch `abs(m_norm_l2 - 1.0) >= 1e-9`, und `float("nan")`
wird vom CLI ohne Fehler geparst.

```
$ python tools/mzm/gate_toggle.py nan true true nan true
GateOpen=true
$ ENTA_GATE_STRICT=1 python tools/mzm/gate_toggle.py nan true true nan true
GateOpen=true      (exit 0)
```

Das widerspricht dem Modulvertrag „Gate opens only when all constraints are satisfied“.
Weil `Ledger.metric()` `NaN` annimmt (siehe B5), steht der Durchlass außerdem als
gültiges `passed: true` in einer Chain, die `verify_chain_from_file` als intakt meldet.
Im Repo gibt es das richtige Muster schon: `tools/spectra_table_lint.py:_number`
filtert mit `math.isfinite`.

**Fix-Vorschlag:** `math.isfinite` vor beide Vergleiche setzen und auf die vorhandenen
Codes `BLOCK_PHI_BELOW_MIN` bzw. `BLOCK_M_NORM_INVALID` abbilden. So braucht es keine
GOLD-Änderung am Enum in `spec/runtime_event.schema.json`. Dazu Ethics-Tests für
`nan`/`inf`/`-inf`.

### B2 · MITTEL · Core-Stability-Guard lässt degenerierten Sattel mit Consent durch (Essenz/Anschluss)

`src/stability/hessian_void.py:60-65` prüft „irgendein |λ| < thr“ **vor** „irgendein λ < 0“.
Eine Hessian mit `λ = (-5, 0)` wird deshalb als `FLAT` eingestuft, und
`src/core/stability_guard.stability_gate(..., consent_available=True)` liefert `ALLOW`.
Der parallele MOD_18-Pfad blockiert denselben Zustand:

```
core  : FLAT  -> (True, 'FLAT: Proceeding with explicit consent (VOID acknowledged)')
MOD18 : DEGENERATE_SADDLE -> ('BLOCK', 'BLOCK_UNSTABLE_DEGENERATE')
```

Damit sagen zwei Guards zum selben Zustand Gegensätzliches, und der Core-Guard verletzt
seinen eigenen Docstring („UNSTABLE: λ < 0 … blockieren“). Derzeit ruft kein Laufzeitpfad
`stability_gate` auf, getroffen ist also die Bibliotheks-API. Ein Test für den gemischten
Fall fehlt.

**Fix-Vorschlag:** In `classify_stability` erst auf negative Eigenwerte prüfen
(→ `UNSTABLE`), dann auf flache. Dazu ein Test `(-5, 0)` → BLOCK auch mit Consent.

### B3 · MITTEL · `eci.permutation_test` ist statistisch leer (Essenz)

`src/core/eci.py:79-87` permutiert eine einzelne Stichprobe und vergleicht ihren
Mittelwert. Eine Permutation ändert den Mittelwert aber nicht. Das Ergebnis ist eine
Stufenfunktion mit p ≈ 0,001 für `observed > mean(samples)` und p = 1 sonst:

```
observed 0.49 -> 1.0 · 0.5000001 -> 0.001 · 0.51 -> 0.001
```

Wer die Funktion als „validation helper“ nutzt, bekommt Scheinsignifikanz. Sie wird
nirgends aufgerufen und ist nicht getestet (laut Coverage-Analyse 2026-07-30 bereits
„vollständig unabgedeckt“).

**Fix-Vorschlag:** Entweder als echter Zwei-Stichproben-Test neu bauen (Labels
permutieren) oder als `[TODO]` markieren und nach `NICHTRAUM/maybe/` verschieben.
Dafür ist ein User-Entscheid nötig.

### B4 · NIEDRIG · `Ledger.verify_chain()` meldet nach Reopen fälschlich `False` (Essenz)

`src/core/ledger.py:345`: Die In-Memory-Prüfung startet mit `prev_hash = None`.
`_load_last_hash()` (`:166`) knüpft beim Öffnen einer bestehenden Datei aber an deren
letzten Hash an. Ab dem ersten neuen Event sagt `verify_chain()` deshalb `False`,
`verify_chain_from_file()` dagegen korrekt `True`. Genau so arbeitet das Gate-CLI mit
`ENTA_LEDGER_PATH`. Das ist ein Fehlalarm und kein Fail-open.

**Fix-Vorschlag:** Den geladenen Start-Hash merken und als Anker in `verify_chain` nutzen.

### B5 · NIEDRIG · `Ledger.metric()` schreibt Nicht-Standard-JSON `NaN` (Form/Anschluss)

`Ledger.event()` lehnt `NaN` ab (`allow_nan=False`, `:242`), `metric()` und `gate()`
dagegen nicht. In der JSONL landet dann `"value":NaN`, was nicht RFC-8259-konform ist
(`jq`, `JSON.parse` brechen ab). Das verstärkt B1.

### B6 · FORM · `src/README.md` taggt Stubs und Falschbeschreibungen als `[FAKT]` (Anschluss)

| Zeile | README sagt | Code ist |
|-------|-------------|----------|
| `core/eci.py` | „Elliptic Cumulative Integral coherence metric“ [FAKT] | Ethical Consent Index |
| `cglg/gate_logic.py` | [FAKT] | Modul selbst: `[HYP]` Stub |
| `tools/throat_vector.py` | „Throat-vector topology computation“ [FAKT] | Einzeiler `sqrt(x²+y²)/(z+1e-6)` |
| `cglg/mutual_perception.py` | [FAKT] | Einzeiler `(a+b)/2`, ohne Docstring/Tag |

Das verletzt die Regel aus `EPISTEMIC_HYGIENE.md` („never let a [HYPOTHESIS] … masquerade
as a [FACT]“). `claim_lint` erfasst `src/README.md` nicht (Scope `index,spec,receipts,tools`),
deshalb fällt es nicht auf. Ähnlich nennt die Modultabelle in `CLAUDE.md`
`cauchy_detector.py` (`max−min`), `throat_vector.py` und `mutual_perception.py` als
„Einstiegspunkte“. Das ist seit der Coverage-Analyse 2026-07-30 bekannt und noch offen.

### B7 · FORM · Setup-Doku verschweigt den harten `uv`-Pin (Anschluss)

`make install-dev` ruft `tools/python_lock.py sync` auf, und das bricht ohne **exakt**
`uv 0.12.18` ab (`FAIL: uv 0.12.18 is required`, hier mit uv 0.11.32 reproduziert).
README („3-Befehls-Setup“) und CONTRIBUTING erwähnen `uv` nicht. `CLAUDE.md` beschreibt
`install-dev` noch als „pip install -r requirements-dev.txt + editable install“. Der Pin
steht nur in Audit-Reports. Ein frischer Clone scheitert also schon an Schritt 1 des
dokumentierten Setups.

### B8 · FORM · `make demo` meldet „verified“, obwohl nicht verifiziert wurde

Ohne `ENTA_HMAC_SECRET` emittiert `status_emit` `UNSIGNED`, und `status_verify` überspringt
mit Exit 0. Das Makefile druckt trotzdem „=== Demo PASS: Receipt emitted and verified ===“.
Lokal ist das gewollt (Fail-closed nur in CI), die Erfolgszeile behauptet aber mehr, als
passiert ist.

### Rauschen (kein Handlungsbedarf, nur notiert)

- Fractalsense-Tests: 235 `UserWarning: Overwriting the cmap …` (Re-Registrierung pro Test).
- ui-app-Tests: `MODULE_TYPELESS_PACKAGE_JSON`-Warnungen von Node beim Laden der `.ts`-Libs.

## Was trägt (Essenz geprüft, ohne Befund)

- `metrics.plv` / `mi` / `fd`: PLV als |mean e^{iθ}|, Histogramm-MI und Higuchi-Normierung
  (`(N−1)/(⌊(N−m)/k⌋·k)/k`) sind formal korrekt. Den MI-Bias kennt der Gesamtcheck
  2026-10-18 bereits, VOID-011 trägt eine Baseline.
- `eci.compute_eci`: Gewichtsnormierung und Umverteilung bei fehlendem Physio-Kanal stimmen.
- `spectral_void` (MOD_18) und `stability/stability_guard`: Die Taxonomie ist vollständig
  und fail-closed (`UNDEFINED` → BLOCK).
- `status_emit` / `status_verify`: Die Kanonisierung beim Signieren und Prüfen ist identisch,
  `compare_digest` wird genutzt, ohne Secret in CI gilt Fail-closed.
- `ledger.verify_chain_from_file`: strikt, mit geschlossenem Schema und Fail-closed.
- `action_gate`: kennt nur PROPOSE/HOLD, nutzt eine read-only Registry-Allowlist und
  importiert keine ausführenden Libraries.
- Electron: `nodeIntegration:false`, `contextIsolation:true`, `sandbox:true`,
  Navigation/Window-Open laufen über eine Protokoll-Allowlist (`http(s)`).

## Aktionen

- [x] Kanonische Gates und Layer (Python, Governance, JS/TS, Fractalsense, Jest) ausgeführt
- [x] Kern-Gates und Guards gelesen und auf Edge-Cases geprobt (NaN, gemischte Eigenwerte, Reopen)
- [x] Doku ↔ Code abgeglichen (`src/README.md`, `CLAUDE.md`, README-Setup)
- [x] Mit früheren Audits abgeglichen (2026-07-06, 2026-07-30, 2026-10-18), damit nur Neues oder
      weiterhin Offenes gemeldet wird

## Nicht getan

- Keine Fixes. Plan-First (G0): Die Fix-Vorschläge oben warten auf OK.
- Kein Deep-Review von `evidence_routing.py` (1701 Zeilen) über die Numerik-Stichprobe
  hinaus. Die Timestamps (`*_at`) fließen nicht in Entscheidungen ein.
- Electron-Packaging/AppImage-Smoke nicht lokal ausgeführt (läuft in `ci-desktop.yml`).
- GitHub-Actions-Status von `main` nicht abgefragt, nur lokal reproduziert.

## Risiken

- B1 ist das einzige Fail-open in einem Gate, das sich selbst „Hard-Gate“ nennt. Die
  Eintrittsschwelle ist niedrig (ein einziges `nan` als Argument oder `NaN` aus einer
  vorgelagerten Berechnung).
- B2 und B3 sind latent: kein Laufzeit-Aufrufer, aber öffentliche API mit falscher Semantik.

## Offene Punkte

- [ ] ☐ B1: NaN/inf-Guard in `gate_toggle` + Ethics-Tests (ANNEX, ohne GOLD)
- [ ] ☐ B2: Prüfreihenfolge in `classify_stability` + Test für gemischte Eigenwerte
- [ ] ☐ B3: `permutation_test` reparieren oder parken (User-Entscheid)
- [ ] ☐ B4/B5: Ledger-Anker beim Reopen; `allow_nan=False` auch in `metric`/`gate`
- [ ] ☐ B6: `src/README.md`-Tags an Modul-Docstrings angleichen; ggf. claim_lint-Scope prüfen
- [ ] ☐ B7: `uv 0.12.18` in README/CONTRIBUTING/CLAUDE.md-Setup nennen
- [ ] ☐ B8: Demo-Erfolgszeile an Signed/Unsigned koppeln

## Artefakte

- `docs/audit/2026-10-28_repo_checkup.md`
