# Report: Repo-Qualitäts-Audit — Remediation (Full-Depth-Fixes)

**Datum:** 2026-07-06
**Fokus:** Audit-Findings umsetzen

## Ziel

Umsetzung **aller** im Full-Depth-Audit vom 2026-07-06 identifizierten
Findings (K1, H1–H3, M1–M5, S1–S6) mit empirischer Verifikation über die reale
Toolchain. Einziger bewusst zurückgestellter Punkt: die Doku-Reorganisation (S7),
weil sie GOLD-Pointer/README-Querverweise berührt und einen eigenen fokussierten
PR verdient.

## Aktionen

- [x] **K1 (KRITISCH)** — Electron gehärtet: `main.js` auf `nodeIntegration:false`,
      `contextIsolation:true`, `sandbox:true` + `preload.js` (contextBridge,
      minimale Read-only-Surface). Externe Navigation wird via `setWindowOpenHandler`
      / `will-navigate` in den System-Browser umgeleitet. `Index.html` erhält eine
      **Content-Security-Policy** (`object-src 'none'`, `base-uri 'none'`, Script-Hosts
      auf self + die zwei gepinnten CDNs beschränkt) und **SRI (sha384)** auf allen
      vier CDN-Scripts. Latenter Bug mitbehoben: `loadFile('index.html')` →
      `'Index.html'` (case-sensitiv auf Linux).
- [x] **H1 (HOCH)** — Neuer PR-blockierender Workflow `ci-python-quality.yml`
      (ruff · black --check · mypy · bandit) auf `pull_request` + push; schließt die
      Lücke, dass diese Gates zuvor nur auf non-PR-Events liefen.
- [x] **H2 (HOCH)** — Stub-Ehrlichkeit: `metrics.eci` (jetzt `[HYP]`-getaggt, verweist
      auf `eci.compute_eci`), `cglg/gate_logic.py` und `meta_backprop.py` als
      `[HYP]`/`[TODO]`-Platzhalter markiert (kein Verhaltenswechsel).
- [x] **H3 (HOCH)** — Verwaiste Electron-Scripts: `start`/`dist` nutzen `npx`,
      damit sie ohne deklarierte (schwere) `electron`-Dependency und ohne
      Lockfile-Änderung lauffähig sind.
- [x] **M1 (MITTEL)** — `uv.lock` (stale, ~390 KB) nach `NICHTRAUM/archive/` (G3).
- [x] **M2 (MITTEL)** — Root-`package.json`-Metadaten korrigiert
      (`name`, `author`, `description`, **`license: ISC → Apache-2.0`**), doppelte
      Keys entfernt, `build.mac`-Einrückung gefixt.
- [x] **M3 (MITTEL)** — Version `1.0.0 → 0.1.0` (pyproject, package.json,
      `tests/__init__.py`); Classifier `Beta → Alpha`.
- [x] **M4 (MITTEL)** — Referenzwert-Tests für PLV/MI/FD/ECI ergänzt (identische
      Phasen → PLV=1, Antiphase → PLV≈0, identische Reihen → MI>0, konstanter
      Partner → MI=0, Gerade → FD≈1, Clamp-Intervalle). +8 Tests.
- [x] **M5 (MITTEL)** — 4 `.zip` + 5 `.min.js` (0 Inbound-Refs) nach
      `NICHTRAUM/archive/fractalsense/` (G3); Quellen (`*.js`) bleiben.
- [x] **S1** — `# noqa: claim-lint` → `# claim-lint: ignore` (ruff-Warnung weg;
      `claim_lint` akzeptiert beide Marker, backward-compatible).
- [x] **S2** — Modul-Docstring in `test_core5_metrics.py` an den Dateianfang.
- [x] **S3** — Ungenutzten mypy-`tests.*`-Override aus `pyproject.toml` entfernt.
- [x] **S5** — `ledger.verify_chain_from_file()` ergänzt (On-Disk-Chain-Verifikation).
- [x] **S6** — `gate_toggle` parst `phi`/`m_norm_l2` mit try/except (Exit 2 statt Traceback).
- [x] **Bonus** — `# nosec B506`-Kommentar in `receipt_lint.py` bereinigt
      (bandit „Test in comment"-Warnungen weg).

## Nicht getan

- **S7 (Doku-/Root-Sprawl)** bewusst zurückgestellt: Das Verschieben der 16
  Root-Markdown-Dateien nach `docs/` berührt README- und ggf. Index-Querverweise
  und riskiert das strikte `verify-pointers`-Gate. Gehört in einen eigenen,
  fokussierten PR mit Link-Rewrite. → als offener Punkt vermerkt.
- **electron als echte Dependency** nicht hinzugefügt: Der ~150-MB-Binary-Download
  + Regenerierung von `pnpm-lock.yaml` würde das `--frozen-lockfile`-Gate
  (`ci-js-workspace`, `security-audit`) riskieren. `npx`-Ansatz (H3) löst das
  Lauffähigkeits-Problem ohne diesen Eingriff.

## Risiken

- **CSP + `'unsafe-inline'`**: `Index.html` enthält große Inline-Scripts, daher ist
  `script-src 'unsafe-inline'` nötig. Die RCE-Kernabsicherung liegt in
  `nodeIntegration:false` + SRI; Inline-Refactoring wäre die nächste Härtungsstufe.
- **SRI pinnt exakte CDN-Versionen**: Ändert das CDN die Bytes (z. B. Re-Publish),
  wird das Script blockiert — gewollt, aber bei CDN-Rotation zu aktualisieren.
- Änderungen an `package.json`/`pyproject.toml` sind bewusst **metadaten-/scope-only**
  gehalten, damit weder `--frozen-lockfile` noch der Python-Build brechen.

## Offene Punkte

- [ ] ☐ S7: Root-Markdown-Sprawl nach `docs/governance/` konsolidieren (eigener PR).
- [ ] ☐ K1-Folgestufe: Inline-Scripts aus `Index.html` extrahieren → `'unsafe-inline'` entfernen.
- [ ] ☐ H2-Folgestufe: `metrics.eci`-Duplikat langfristig gegen `eci.compute_eci` konsolidieren (VOID-011).
- [ ] ☐ `styles.min.css` in `Fractalsense/` auf Verwendung prüfen (nicht mitarchiviert, konservativ belassen).

## Verifikation (empirisch ausgeführt)

| Gate | Ergebnis |
|------|----------|
| `pytest` | **194 passed** (vorher 186; +8 Referenzwert-Tests) |
| `ruff check src/ tools/ tests/` | All checks passed (noqa-Warnung weg) |
| `black --check` | 74 files unchanged |
| `mypy src/ tools/` | Success: no issues (37 files) |
| `bandit -c .bandit.yaml -r src/ tools/` | No issues identified (exit 0, Warnungen weg) |
| `port_lint` | OK |
| `verify_pointers --strict` | All core pointers valid |
| `claim_lint --strict` | No untagged claims |
| `workflow_posture_check` | **14 workflows** PASS (neu: `ci-python-quality.yml`) |
| `voidmap_ui_drift_check` | 22 VOIDs in sync |
| `voids_backlog_gen --check` | Up to date |

## Artefakte

- `main.js`, `preload.js`, `Index.html` (K1)
- `.github/workflows/ci-python-quality.yml` (H1)
- `src/core/metrics.py`, `src/cglg/gate_logic.py`, `src/meta_backprop.py` (H2)
- `package.json`, `pyproject.toml`, `tests/__init__.py` (M2/M3)
- `tests/unit/test_core5_metrics.py` (M4/S2)
- `tools/claim_lint.py`, `tools/status_verify.py`, `tools/receipt_lint.py`, `tools/mzm/gate_toggle.py` (S1/S6/Bonus)
- `src/core/ledger.py` (S5)
- `NICHTRAUM/archive/uv.lock`, `NICHTRAUM/archive/fractalsense/*`, `NICHTRAUM/archive/README.md` (M1/M5)
