# Report: Branch-Aufräumen

**Datum:** 2026-10-07
**Fokus:** Branches aufräumen, main aktuell

## Ziel
Alle Branches gegen `main` prüfen; sicherstellen, dass `main` aktuell ist; veraltete Branches
reversibel entfernen (G3); offene Dependabot-PRs abarbeiten.

## Befund
- `main` ist aktuell — kein Branch enthält Arbeit, die in `main` fehlt und benötigt wird.
- 21 Branches neben `main`:
  - **A (9):** vollständig in `main` enthalten (0 eigene Änderungen netto).
  - **B (7):** 200–350 Commits hinter `main`; Inhalte (z. B. `voids_backlog_gen.py`,
    `pipeline_essentials.py`, ESLint-Flat-Config, `pip-audit`) sind in neuerer Form in `main`.
  - **C (5):** offene Dependabot-PRs #298, #365, #374, #375, #376.
- Details + SHAs: `NICHTRAUM/archive/branches_2026-10-07/MANIFEST.md`

## Aktionen
- [x] Volle Git-Historie geholt, alle Branches verglichen (Commits, Patch-Äquivalenz, Netto-Diff)
- [x] Einzigen nicht in `main` vorhandenen Inhalt (Audit-Bericht 2026-04-06) nach `NICHTRAUM/archive/` gerettet
- [x] Manifest mit letztem Commit je Branch angelegt
- [ ] ☐ Archiv-Tags pushen + Branches entfernen — **in der Cloud-Session gesperrt (HTTP 403)**, manuell (s. u.)

## Manuell ausführen (lokal, im Repo-Klon)

```bash
git fetch origin --prune
BRANCHES="
claude/analyze-repo-essence-LKgK4
claude/refactor-codebase-011CV4t3cQACpBAxqgu1MX1D
claude/repo-maintenance-consolidation-LA2ek
claude/align-coverage-policy
codex/update-markdown-file-in-repository
codex/update-readme-for-deepjump-integration
phase0/foundation-pack
dependabot/github_actions/actions/setup-node-6.4.0
claude/sleepy-dirac-sgsjk0
claude/repo-audit-analysis-oiW6K
claude/repo-maintenance-audit-mnZVm
claude/ui-lint-flat-config
codex/beheben-von-fehlern-beim-mergen
codex/find-more-ways-to-enhance-pipeline-management
codex/review-open-prs-and-issues-for-merge
fix/ci-security-pip-audit-171
"
# 1) Sichern: jeder Branch bekommt einen Tag archive/<branch> (bleibt dauerhaft wiederherstellbar)
for b in $BRANCHES; do git tag "archive/$b" "origin/$b"; done
git push origin 'refs/tags/archive/*:refs/tags/archive/*'
# 2) Erst danach Branches entfernen
git push origin --delete $BRANCHES
```

Wiederherstellen eines Branches: `git push origin archive/<branch>:refs/heads/<branch>`

Alternative ohne Terminal: GitHub → Repo → *Branches* → Mülleimer-Symbol je Branch
(GitHub bietet kurz danach „Restore“ an; die SHAs im Manifest sind die dauerhafte Referenz —
für echte Dauer-Sicherung aber bitte den Tag-Weg nutzen).

## Nicht getan
- Keine Branches entfernt, keine Tags gepusht (Session-Push auf eigenen Branch beschränkt).
- `ui-app/package-lock.json` aus Gruppe B nicht übernommen (npm-Lockfile, obsolet seit pnpm).

## Risiken
- Branch-Löschung ohne vorherige Tags: Commits werden auf GitHub irgendwann unerreichbar. → Tags zuerst.
- Dependabot #298 (TypeScript 7) und #365 (ESLint 10) sind Major-Sprünge mit Bruchrisiko.

## Offene Punkte
- [ ] ☐ Tags pushen + 16 Branches entfernen (Befehle oben)
- [ ] ☐ Dependabot-PRs: Rebase angefordert; Merge nach grünem CI

## Artefakte
- `NICHTRAUM/archive/branches_2026-10-07/MANIFEST.md`
- `NICHTRAUM/archive/branches_2026-10-07/repo_audit_2026-04-06.md`
- `NICHTRAUM/archive/README.md` (Eintrag ergänzt)
- `OUT/branch_cleanup_2026-10-07.md`
