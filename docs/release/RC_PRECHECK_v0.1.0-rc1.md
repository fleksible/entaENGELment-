# RC Preflight — v0.1.0-rc1

Status: Draft checklist for first reproducible release candidate path.  
Scope: Preparation only (no tag creation, no release trigger).

## Ziel

Einen klar nachvollziehbaren `v0.1.0-rc1`-Kandidaten vorbereiten, sodass ein späteres Tagging (`v0.1.0-rc1`) deterministisch durch die vorhandene Release-Pipeline läuft.

## RC-Scope (konservativ)

- Nur bereits integrierte, verifizierte Änderungen aus `main` seit dem zuletzt bestätigten Release-Tag (falls vorhanden).
- Keine neue Release-Automatisierung.
- Keine Verhaltensänderung im Release-Workflow.
- Dokumentations- und Nachvollziehbarkeits-Verbesserungen sind erlaubt.

## Preflight-Checkliste

### A) Inhalt & Dokumentation
- [x] `CHANGELOG.md` unter `Unreleased` enthält einen klaren RC-Hinweis und die erwarteten Punkte für `v0.1.0-rc1`.
- [ ] `README.md` verweist auf den Release-Prozess bzw. dieses RC-Preflight-Dokument.
- [x] Offene Risiken/Unsicherheiten für den RC sind benannt (keine impliziten Annahmen).

### B) Technische Release-Gates (lokal prüfbar)
- [x] `python3 tools/verify_pointers.py --strict` — WARN: core pointers valid; 4 optional `out/*` artifacts missing.
- [x] `python3 tools/claim_lint.py --scope index,spec,receipts,tools`
- [x] `python3 tools/port_lint.py`
- [x] `for f in receipts/*.json; do python3 tools/receipt_lint.py "$f"; done`
- [x] `pytest tests/ -x --tb=short`
- [x] `grep -r "return 0.5" src/core/` liefert keine Stub-Metriken.
- [x] `VOIDMAP.yml` enthält keine ownerlosen `OPEN`/`IN_PROGRESS`-VOIDs.

### C) Workflow-Readiness
- [x] `.github/workflows/release.yml` bleibt tag-getrieben (`v*.*.*`) und unverändert bzgl. RC-Logik.
- [x] RC-Tag-Konvention bestätigt: `v0.1.0-rc1` (führt zu `prerelease=true` wegen `-rc` im Tag).
- [ ] Keine lokalen Änderungen mehr offen, die nicht in den RC sollen.

## Evidence Snapshot — 2026-05-18

Evidence file: [`docs/release/evidence/RC_PREFLIGHT_v0.1.0-rc1_2026-05-18.md`](evidence/RC_PREFLIGHT_v0.1.0-rc1_2026-05-18.md)

Summary:

- Technical gates completed with PASS except `verify_pointers --strict`, which is PASS/WARN: all core pointers are valid, but 4 optional `out/*` artifacts are missing.
- `CHANGELOG.md` already contains an `Unreleased` / `Release Prep` entry for this RC preflight path.
- Release workflow remains tag-triggered and treats `-rc` tags as prereleases.
- No tag, release trigger, workflow edit, UI/dependency edit, or `data/receipts/` change is part of this evidence pass.

Open items before an actual RC tag:

- README does not yet explicitly link the release process or this RC preflight document.
- `git status --short` was not captured as a dedicated evidence gate, so local clean-state remains unchecked in this snapshot.
- The pointer WARN should remain visible unless the optional `out/*` artifacts are generated or deliberately accepted as non-blocking for RC.

## Explizite Nicht-Ziele in diesem Schritt

- Kein `git tag ...`
- Kein `git push --tags`
- Keine GitHub Release-Erstellung
- Kein Eingriff in Gate- oder Release-Workflow-Logik

## Mögliche Blocker vor echtem RC-Tag

- Fehlende oder unvollständige Changelog-Einträge für RC-relevante Änderungen.
- Nicht-grüne Gate-Checks (lokal oder CI).
- Unklare Scope-Abgrenzung zwischen bestätigter Baseline und `v0.1.0-rc1`.