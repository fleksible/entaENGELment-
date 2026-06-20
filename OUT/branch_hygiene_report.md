# Report: Branch Hygiene — entaENGELment-

**Datum:** 2026-06-20
**Fokus:** Branch-Inventar / 17 Branches einordnen

## Ziel
Die vorhandenen Remote-Branches (außer `main`) inventarisieren, gegen `origin/main`
einordnen und einen Entscheidungsbericht erzeugen (keep / merge / close / rebase /
archive / delete-vorschlag). **Keine** Löschung, kein Force-Push, kein Merge, kein
Close ohne Human-Go.

---

## Base
- `origin/main` @ `158712d` — "docs(out): PR #260 stabilization report (#261)" (2026-06-20)
- Working tree: clean ✓
- Default branch: `main` ✓
- Remote erreichbar, `--prune` ausgeführt ✓

## Summary
- Total remote branches excluding main: **17**
- Active PR branches (open PR): **1** (`#245`)
- Merge-ready PR branches: **0**
- Redundant / empty PR branches (offen): **0** — es gibt aktuell nur **einen** offenen PR
- Superseded / fully-absorbed branches (0 net diff vs. main): **11**
- Unmerged content branches (need review): **4**
- Align-with-main candidates: **0** (keine aktiv-zu-haltenden Branches hinter main mit eigenem Wert außer #245)
- Unknown/protected / GOLD-berührend: **1** (`codex/review-open-prs-and-issues-for-merge` ändert `VOIDMAP.yml` = GOLD)

> **Wichtiger Hinweis zur Task-Annahme:** Die ursprüngliche Aufgabe nahm an, dass
> **PR #260** ein aktiver Wartungs-PR und **PR #259** ein diff-leerer Redundanz-PR sei.
> Stand jetzt sind **beide geschlossen**: #260 wurde via #261 **gemerged**
> (2026-06-20), #259 wurde **ohne Merge geschlossen**. Es existiert nur **noch ein
> einziger offener PR: #245** (Dependabot eslint). Es ist also **kein** PR-Close
> (Option 1) mehr nötig oder möglich.

> **Methodik-Hinweis (ahead/behind vs. Inhalt):** Git meldet **keinen** Branch als
> `--merged` und alle Branches mit `ahead > 0`. Grund: Squash-/Merge-Commits in der
> Historie. Maßgeblich für „enthält der Branch noch eigenes Material?" ist daher der
> **Drei-Punkt-Inhaltsdiff** `git diff origin/main...<branch>`: Zeigt er **0 Dateien**,
> ist der Netto-Inhalt des Branches bereits in `main` (oder leer) → nichts zu retten.

---

## Branch Table

| Branch | PR(s) | Ahead | Behind | Net diff vs main | Last Commit | Class | Empfehlung |
|--------|-------|-------|--------|------------------|-------------|-------|------------|
| `dependabot/npm_and_yarn/ui-app/eslint-10.5.0` | #245 **open** | 2 | 44 | 1 file (package.json) | 2026-06-16 | KEEP_ACTIVE_PR | Behalten; aktiver Dependabot-PR. Mergen ist Maintainer-Entscheid. |
| `codex/review-open-prs-and-issues-for-merge` | #241 merged, #242 closed | 1 | 53 | 21 files **incl. VOIDMAP.yml (GOLD)** | 2026-06-11 | UNKNOWN_PROTECTED | **STOP** — berührt GOLD. Human-Review nötig, **nicht** löschen, **nicht** mergen. |
| `claude/repo-maintenance-audit-mnZVm` | #213 closed, #251 closed | 2 | 126 | 3 files (Makefile, voids_backlog, voids_backlog_gen.py) | 2026-05-20 | UNMERGED_STALE | Review: enthält neues Tool `tools/voids_backlog_gen.py`. PRs zu, Inhalt nicht in main. Archivieren oder neuen PR. |
| `codex/beheben-von-fehlern-beim-mergen` | #214 closed | 3 | 101 | 7 files (ui-app) | 2026-05-31 | UNMERGED_STALE | Review: ui-app Guard/Focus-Stabilisierung + Deps. PR zu, nicht gemerged. Archivieren oder neuen PR. |
| `codex/find-more-ways-to-enhance-pipeline-management` | #215 closed | 2 | 100 | 4 files (pipeline_essentials) | 2026-05-30 | UNMERGED_STALE | Review: neues Tool `tools/pipeline_essentials.py` + Test + Runbook. Archivieren oder neuen PR. |
| `claude/ui-lint-flat-config` | #222 closed **MERGED** | 1 | 73 | 1 file (tsconfig.json) | 2026-06-16 | MERGED_STALE_LEFTOVER | PR gemerged; Branch trägt nur noch tsconfig-Delta (wahrsch. durch #223/#224 abgelöst). Vermutl. löschbar nach Review. |
| `claude/align-coverage-policy` | — keiner — | 373 | 132 | **0 files** | 2026-04-04 | SUPERSEDED_NO_DIFF | Netto-Inhalt in main / leer. Kein PR. Löschen-Vorschlag nach Human-Go. |
| `claude/analyze-repo-essence-LKgK4` | — keiner — | 63 | 132 | **0 files** | 2026-01-03 | SUPERSEDED_NO_DIFF | Wie oben. Löschen-Vorschlag nach Human-Go. |
| `claude/refactor-codebase-011CV4t3cQACpBAxqgu1MX1D` | — keiner — | 62 | 132 | **0 files** | 2026-01-03 | SUPERSEDED_NO_DIFF | Wie oben. Löschen-Vorschlag nach Human-Go. |
| `claude/repo-audit-analysis-oiW6K` | — keiner — | 388 | 132 | **0 files** | 2026-04-06 | SUPERSEDED_NO_DIFF | Wie oben. Löschen-Vorschlag nach Human-Go. |
| `claude/repo-maintenance-consolidation-LA2ek` | — keiner — | 70 | 132 | **0 files** | 2026-01-04 | SUPERSEDED_NO_DIFF | Wie oben. Löschen-Vorschlag nach Human-Go. |
| `claude/sleepy-dirac-sgsjk0` | #259 closed (unmerged) | 3 | 8 | **0 files** | 2026-06-20 | SUPERSEDED_NO_DIFF | PR #259 bereits geschlossen; Netto-Inhalt in main. Löschen-Vorschlag nach Human-Go. |
| `codex/update-markdown-file-in-repository` | — keiner — | 53 | 132 | **0 files** | 2025-12-29 | SUPERSEDED_NO_DIFF | Wie oben. Löschen-Vorschlag nach Human-Go. |
| `codex/update-readme-for-deepjump-integration` | — keiner — | 57 | 132 | **0 files** | 2025-12-29 | SUPERSEDED_NO_DIFF | Wie oben. Löschen-Vorschlag nach Human-Go. |
| `dependabot/github_actions/actions/setup-node-6.4.0` | — keiner — | 9 | 132 | **0 files** | 2026-05-11 | SUPERSEDED_NO_DIFF | setup-node Bump bereits anderweitig in main (#232). Löschen-Vorschlag nach Human-Go. |
| `fix/ci-security-pip-audit-171` | — keiner — | 5 | 132 | **0 files** | 2026-05-11 | SUPERSEDED_NO_DIFF | pip-audit-Umstellung bereits in main. Löschen-Vorschlag nach Human-Go. |
| `phase0/foundation-pack` | — keiner — | 190 | 132 | **0 files** | 2026-01-18 | SUPERSEDED_NO_DIFF | Netto-Inhalt in main. Name klingt „foundational" → vor Löschung kurz bestätigen. |

---

## Safe Actions Proposed

### Can close PR, no code loss expected
- **Keine.** Es gibt nur einen offenen PR (#245), und der ist ein gültiger,
  nicht-redundanter Dependabot-PR. (Der ursprünglich genannte #259 ist bereits
  geschlossen.)

### Can delete branch after Human-Go (kein Code-Verlust — 0 net diff vs. main)
- `claude/align-coverage-policy`
- `claude/analyze-repo-essence-LKgK4`
- `claude/refactor-codebase-011CV4t3cQACpBAxqgu1MX1D`
- `claude/repo-audit-analysis-oiW6K`
- `claude/repo-maintenance-consolidation-LA2ek`
- `claude/sleepy-dirac-sgsjk0`
- `codex/update-markdown-file-in-repository`
- `codex/update-readme-for-deepjump-integration`
- `dependabot/github_actions/actions/setup-node-6.4.0`
- `fix/ci-security-pip-audit-171`
- `phase0/foundation-pack` *(Name beachten — kurz bestätigen)*

### Needs review before action (enthält eigenes, nicht in main vorhandenes Material)
- `claude/repo-maintenance-audit-mnZVm` — neues Tool `tools/voids_backlog_gen.py` (+248 Z.)
- `codex/beheben-von-fehlern-beim-mergen` — ui-app Guard/Focus + Deps (7 Dateien)
- `codex/find-more-ways-to-enhance-pipeline-management` — neues Tool `tools/pipeline_essentials.py` + Test + Runbook
- `claude/ui-lint-flat-config` — PR #222 gemerged, nur tsconfig-Rest übrig (vermutl. abgelöst)

### Keep / Do-not-touch
- `dependabot/npm_and_yarn/ui-app/eslint-10.5.0` — aktiver offener PR #245
- `codex/review-open-prs-and-issues-for-merge` — **GOLD-berührend (VOIDMAP.yml)**, Human-Review

---

## Nicht getan (bewusst ausgelassen)
- Keine Branches gelöscht.
- Keine Branches force-gepusht.
- Keine PRs gemerged.
- Keine PRs geschlossen.
- Keine Branches rebased oder mit main angeglichen.
- GOLD/IMMUTABLE unangetastet.

## Risiken / Notes
- **GOLD-Berührung:** `codex/review-open-prs-and-issues-for-merge` ändert `VOIDMAP.yml`.
  Jede Aktion mit diesem Branch (Merge, neuer PR) ist eine GOLD-Change und erfordert
  explizite Anweisung + Begründung.
- **„0 net diff" ≠ „identische Historie":** Die 11 superseded Branches haben divergente
  Historie (ahead-Commits), aber identischen Netto-Baum-Stand gegenüber dem Merge-Base.
  Löschung verliert nur die (redundante) Historie, keinen Inhalt. Reversibel über Reflog/PR-Refs
  nur begrenzt — daher Human-Go.
- **Stale-Material:** Die 3 „needs review"-codex/claude-Branches enthalten potenziell
  wertvolle, nie gemergte Tools/Fixes. Vor Löschung: Inhalt sichten.

## Offene Punkte (Human-Entscheid nötig)
- [ ] ☐ 11 superseded Branches löschen? (Batch nach Human-Go)
- [ ] ☐ `phase0/foundation-pack` trotz „foundational"-Name löschbar?
- [ ] ☐ 3 unmerged-content Branches: archivieren, neuen Draft-PR, oder verwerfen?
- [ ] ☐ `claude/ui-lint-flat-config` Rest-tsconfig-Delta: löschen oder übernehmen?
- [ ] ☐ `codex/review-open-prs-and-issues-for-merge` (GOLD/VOIDMAP): wie verfahren?

## No-Action Guard
No branches were deleted. No branches were force-pushed. No PRs were merged.
No PRs were closed. Only read-only inventory + this report were produced.

---

## Addendum — Go B: Sichtung der 4 Review-Branches (2026-06-20, read-only)

Tiefenprüfung der als „needs-review" markierten Branches. Methodik: Zwei-Punkt-Tip-Diff
(`main..branch`) + Existenz-/Identitätsprüfung der Signatur-Dateien in `main`.

**Kernbefund:** Alle 4 Branch-Tips liegen **−13.000 bis −15.000 Zeilen hinter main**
(Stand vor dem Monorepo/pnpm-Umbau). Ihr jeweiliger Drei-Punkt-„Eigenanteil" (ein Tool /
Fix) ist in `main` **bereits vorhanden, in neuerer Form**. `DIFFERENT` = Branch ist die
ältere Variante, nicht „Branch hat Material, das main fehlt".

| Branch | Signatur | In main? | Verdikt |
|--------|----------|----------|---------|
| `claude/repo-maintenance-audit-mnZVm` | `voids_backlog_gen.py` + Make-Targets + doc | Ja (Make-Targets present, Tool+Doc existieren) | superseded |
| `codex/find-more-...-pipeline-management` | `tools/pipeline_essentials.py` + Test + Runbook | Ja (neuere Variante) | superseded |
| `codex/beheben-von-fehlern-beim-mergen` | ui-app Guard/Focus | Ja (`FocusIndicator.tsx` absorbiert) | superseded |
| `claude/ui-lint-flat-config` | `ui-app/tsconfig.json` flat-config | PR #222 **merged**; main neuer (#223/#224) | superseded (merged) |

**Folge für die Klassifikation:** Diese 4 rücken von „needs-review" → „superseded,
kein Verlust bei Löschung". Damit wären nach Human-Go bis zu **15** Branches gefahrlos
löschbar. `codex/review-open-...` (GOLD/VOIDMAP) und `#245` (Dependabot) bleiben **separat**.

**Kein Schnitt ausgeführt** — reine Sichtung. Löschung weiterhin nur nach explizitem Go.

## Artefakte
- `OUT/branch_hygiene_report.md`
