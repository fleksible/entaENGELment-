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
- [ ] `CHANGELOG.md` unter `Unreleased` enthält einen klaren RC-Hinweis und die erwarteten Punkte für `v0.1.0-rc1`.
- [ ] `README.md` verweist auf den Release-Prozess bzw. dieses RC-Preflight-Dokument.
- [ ] Offene Risiken/Unsicherheiten für den RC sind benannt (keine impliziten Annahmen).

### B) Technische Release-Gates (lokal prüfbar)
- [ ] `python3 tools/verify_pointers.py --strict`
- [ ] `python3 tools/claim_lint.py --scope index,spec,receipts,tools`
- [ ] `python3 tools/port_lint.py`
- [ ] `for f in receipts/*.json; do python3 tools/receipt_lint.py "$f"; done`
- [ ] `pytest tests/ -x --tb=short`
- [ ] `grep -r "return 0.5" src/core/` liefert keine Stub-Metriken.
- [ ] `VOIDMAP.yml` enthält keine ownerlosen `OPEN`/`IN_PROGRESS`-VOIDs.

### C) Workflow-Readiness
- [ ] `.github/workflows/release.yml` bleibt tag-getrieben (`v*.*.*`) und unverändert bzgl. RC-Logik.
- [ ] RC-Tag-Konvention bestätigt: `v0.1.0-rc1` (führt zu `prerelease=true` wegen `-rc` im Tag).
- [ ] Keine lokalen Änderungen mehr offen, die nicht in den RC sollen.

## Explizite Nicht-Ziele in diesem Schritt

- Kein `git tag ...`
- Kein `git push --tags`
- Keine GitHub Release-Erstellung
- Kein Eingriff in Gate- oder Release-Workflow-Logik

## Mögliche Blocker vor echtem RC-Tag

- Fehlende oder unvollständige Changelog-Einträge für RC-relevante Änderungen.
- Nicht-grüne Gate-Checks (lokal oder CI).
- Unklare Scope-Abgrenzung zwischen bestätigter Baseline und `v0.1.0-rc1`.
