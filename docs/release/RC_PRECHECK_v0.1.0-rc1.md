# RC Preflight — v0.1.0-rc1

Status: Gate-Checks abgeschlossen (2026-04-06). Offene Punkte: A1, A3, C3.  
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
- [x] `README.md` verweist auf den Release-Prozess bzw. dieses RC-Preflight-Dokument.
- [ ] Offene Risiken/Unsicherheiten für den RC sind benannt (keine impliziten Annahmen).

### B) Technische Release-Gates (lokal prüfbar)
- [x] `python3 tools/verify_pointers.py --strict`
  - Ergebnis (2026-04-06): ✅ All core pointers valid. 5 optional paths missing (out/status, out/badges, out/verify, out/snapshot_manifest, docs/voids_backlog.md) — erwartet in lokalem Checkout.
- [x] `python3 tools/claim_lint.py --scope index,spec,receipts,tools`
  - Ergebnis (2026-04-06): ✅ No untagged claims found in scope.
- [x] `python3 tools/port_lint.py`
  - Ergebnis (2026-04-06): ✅ Port-Lint: OK (no errors).
- [x] `for f in receipts/*.json; do python3 tools/receipt_lint.py "$f"; done`
  - Ergebnis (2026-04-06): ✅ 4/4 receipts: PASS.
- [x] `pytest tests/ -x --tb=short`
  - Ergebnis (2026-04-06): ✅ 160 passed in 1.48s (0 failures, 0 errors).
- [x] `grep -r "return 0.5" src/core/` liefert keine Stub-Metriken.
  - Ergebnis (2026-04-06): ✅ No stub metrics found.
- [x] `VOIDMAP.yml` enthält keine ownerlosen `OPEN`/`IN_PROGRESS`-VOIDs.
  - Ergebnis (2026-04-06): ✅ All active VOIDs have owners (VOID-010: fleks, VOID-011: fleks).

### C) Workflow-Readiness
- [x] `.github/workflows/release.yml` bleibt tag-getrieben (`v*.*.*`) und unverändert bzgl. RC-Logik.
- [x] RC-Tag-Konvention bestätigt: `v0.1.0-rc1` (führt zu `prerelease=true` wegen `-rc` im Tag).
- [ ] Keine lokalen Änderungen mehr offen, die nicht in den RC sollen.
  - Ausstehend: Branch `claude/repo-audit-analysis-oiW6K` (CI-Fixes + Audit-Report) muss vor RC-Tag auf `main` gemergt sein.

## Offene Blocker vor echtem RC-Tag

1. **CHANGELOG.md**: `[Unreleased]` Sektion um klare `v0.1.0-rc1`-Markierung erweitern.
2. **Risikodokumentation**: Bekannte Risiken explizit nennen (VOID-010/VOID-011 IN_PROGRESS, UI static-only).
3. **Branch merge**: `claude/repo-audit-analysis-oiW6K` → `main` (CI-Fixes, Audit-Befunde).

## Explizite Nicht-Ziele in diesem Schritt

- Kein `git tag ...`
- Kein `git push --tags`
- Keine GitHub Release-Erstellung
- Kein Eingriff in Gate- oder Release-Workflow-Logik

## Gate-Lauf-Protokoll (2026-04-06)

```
Gate 1 — verify_pointers --strict:  PASS (core valid, 5 optional missing)
Gate 2 — claim_lint:                PASS (no untagged claims)
Gate 3 — port_lint:                 PASS (no errors)
Gate 4 — receipt_lint (4 receipts): PASS
Gate 5 — ownerless VOIDs:           PASS
Gate 6 — pytest tests/ (160 tests): PASS (1.48s)
Gate 7 — no stub metrics:           PASS
```
