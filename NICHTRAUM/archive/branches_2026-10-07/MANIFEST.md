# Branch-Archiv 2026-10-07

Per **G3**: Die folgenden 16 Remote-Branches wurden zur Entfernung freigegeben (User-OK 2026-10-07).
Diese Liste hält den letzten Commit jedes Branches fest, damit jeder Branch reversibel bleibt.

**Grund:** Alle Branches sind entweder vollständig in `main` enthalten (A) oder veraltet (B,
200–350 Commits hinter `main`; ihre Inhalte sind in neuerer Form bereits in `main`).

**Wiederherstellen:** `git push origin <sha>:refs/heads/<branch>`

| Branch | Gruppe | Letzter Commit (SHA) | Datum | Commits nicht in main |
|---|---|---|---|---|
| `claude/analyze-repo-essence-LKgK4` | A | `dd28e79ef64deabddbafad69540f742b5050b992` | 2026-01-03 | 0 |
| `claude/refactor-codebase-011CV4t3cQACpBAxqgu1MX1D` | A | `9fbf1de83a49f49a84a7b76e2a6b2089223ca235` | 2026-01-03 | 0 |
| `claude/repo-maintenance-consolidation-LA2ek` | A | `315e8dc9646a69d87e761c2515d95f94d316175c` | 2026-01-04 | 0 |
| `claude/align-coverage-policy` | A | `fb471aa683775ad8bb5f8ef4c64230692d5529ca` | 2026-04-04 | 0 |
| `codex/update-markdown-file-in-repository` | A | `68395d792e7d949f7da2904781e1f03b4c49865f` | 2025-12-29 | 0 |
| `codex/update-readme-for-deepjump-integration` | A | `723f8bc1b5ca860e803d153f09081dfbf194d771` | 2025-12-29 | 0 |
| `phase0/foundation-pack` | A | `b808c507c26a73ede7c78a6752ea1c100d62114b` | 2026-01-18 | 0 |
| `dependabot/github_actions/actions/setup-node-6.4.0` | A | `5a6f000245cb89e0ccbabe11383ad11adc69c782` | 2026-05-11 | 0 |
| `claude/sleepy-dirac-sgsjk0` | A | `0ed4ed79144b23aaebe33dc9ece5e106658cc8f1` | 2026-06-20 | 3 |
| `claude/repo-audit-analysis-oiW6K` | B | `0ac6599ea699e806e1375c5016f59814971e17ea` | 2026-04-06 | 4 |
| `claude/repo-maintenance-audit-mnZVm` | B | `5a9136425c3cc66a2a82875307d58b764019b2f9` | 2026-05-20 | 2 |
| `claude/ui-lint-flat-config` | B | `47069a86505009b9aa81f62d460e5a41ecc94288` | 2026-06-16 | 1 |
| `codex/beheben-von-fehlern-beim-mergen` | B | `e42aefb9b492693904efb189a812127c0a800b81` | 2026-05-31 | 3 |
| `codex/find-more-ways-to-enhance-pipeline-management` | B | `f5eeff860fe34f0ea0ebddc9ba2fba759cf84eb2` | 2026-05-30 | 2 |
| `codex/review-open-prs-and-issues-for-merge` | B | `8a462301dfb5b5ffda6ce9452c63dc262fda4b03` | 2026-06-11 | 1 |
| `fix/ci-security-pip-audit-171` | B | `57ac842435311a1eb04480f4c0f9028cdf042e0c` | 2026-05-11 | 1 |

## Gerettete Inhalte

- `repo_audit_2026-04-06.md` — war `OUT/repo_audit_2026-04-06.md` auf `claude/repo-audit-analysis-oiW6K`
  (einziger inhaltlich neuer Bestandteil aus Gruppe B; nie in `main` gelandet).
- Nicht übernommen: `ui-app/package-lock.json` aus `codex/beheben-von-fehlern-beim-mergen`
  — npm-Lockfile, obsolet seit pnpm (siehe `../README.md`).
