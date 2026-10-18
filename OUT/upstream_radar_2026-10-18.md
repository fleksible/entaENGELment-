# Report: Upstream-Radar

**Datum:** 2026-10-18
**Fokus:** Upstream-Änderungen mit Repo-Einfluss

## Ziel
Ermitteln, welche Änderungen bei den Quellen, von denen das Repo abhängt, einen
wesentlichen Einfluss haben. Die Quellen sind:
- Laufzeit- und Toolchain-Pakete
- CI-Plattform
- Agenten-Tooling
- Standards

Nur Treffer mit konkreter Wirkung auf dieses Repo, nach Dringlichkeit sortiert.

FOKUS-SWITCH: Merge-Stand und Repo-Pflege -> Upstream-Radar
Grund: ausdrücklicher Auftrag des Owners am 2026-10-18.

## Aktionen
- [x] Inventur, was das Repo tatsächlich nutzt:
  - `package.json`, `ui-app/package.json`
  - `pyproject.toml`, `uv.lock`
  - 16 Workflows
  - `.claude/`
- [x] Aktuelle Versionen direkt aus der npm-Registry und PyPI abgefragt
- [x] Primärquellen gelesen: Next.js-Blog, GitHub Security Advisories, eslint.org, pnpm.io, GitHub Changelog, Claude-Code-Doku
- [x] Node-Runtime aller SHA-gepinnten Actions aus deren `action.yml` geprüft
- [x] Peer-Ranges für TypeScript 7 und ESLint 10 gegen die Registry geprüft

## Befunde

### 1. Hoch: Next.js 16.3.8 ist von den Advisories vom 14.10. betroffen
- GHSA-673q-mjm6-r5xr (critical, RCE in `use cache`) und GHSA-p3m5-59mp-jv5r (high, DoS über Server Actions) [FACT]:
  - betroffen: `>=16.0.0 <=16.4.0`
  - gepatcht: `16.4.1`
- Für 16.3.x gibt es keinen Patch. Gepatcht werden nur 16.4.x (Active LTS) und 15.5.x [FACT].
- **Das Audit-Gate ist dafür blind.** Die npm-Advisory-DB liefert für `next@16.3.8` keinen Treffer, also bleibt `pnpm audit` grün [FACT].
- **Reale Ausnutzbarkeit hier gering.** Die UI ist `output: 'export'` ohne `use cache`, ohne Server Actions und ohne `next/image` [FACT]. Auf `sharp` ≥ 0.35.5 zwingt bereits ein Override [FACT].
- Maßnahme:
  - `next` und `eslint-config-next` → `16.4.x`
  - `react` und `react-dom` → `^19.3.1` (Hinweis aus der Advisory-Begleitung)

### 2. Hoch: Python-Untergrenze liegt hinter dem Upstream
- Python 3.9 ist seit Oktober 2025 EOL. Für Python 3.10 ist das Support-Ende laut PEP 619 für Oktober 2026 geplant, also diesen Monat. Python 3.15.0 ist seit dem 09.10.2026 erschienen [FACT].
- Im Repo:
  - `requires-python = ">=3.9"`
  - die CI-Matrizen testen 3.9–3.12
  - 3.13, 3.14 und 3.15 werden nicht getestet [FACT]
- Upstream: black 26, mypy 2, pytest 9, pip-audit und setuptools 84 verlangen bereits ≥ 3.10. numpy 2.5 und scipy ≥ 1.17 verlangen ≥ 3.12 [FACT, PyPI]. Der uv-Lock hält deshalb parallele Alt-Stände, z. B. numpy 2.0.2 und scipy 1.13.1.
- Lokal unter 3.13 laufen alle 665 Tests grün [FACT, diese Session].
- Maßnahme: Untergrenze auf 3.11 oder mindestens 3.10 anheben und 3.13/3.14 in die Matrix aufnehmen.
  - Betrifft: `pyproject.toml`, `uv.lock`, die Exporte und 2 Workflows.
  - `pyproject.toml` ist ANNEX, aber die Änderung ist strukturell → Plan-First.

### 3. Mittel: Lieferkette, Cooldown für npm fehlt
- pnpm ≥ 10.16 kennt `minimumReleaseAge`. Seit pnpm 11 ist der Default 1440 Minuten (1 Tag); das Repo nutzt pnpm 10.33, dort ist er 0 [FACT].
- Dependabot wartet seit 14.07.2026 standardmäßig 3 Tage bei Version-Updates. Security-Updates kommen weiter sofort [FACT].
- Lokale und manuelle Installs, etwa Sammel-Updates wie in #404, haben damit keinen Cooldown.
- Maßnahme: `minimumReleaseAge: 1440` in `pnpm-workspace.yaml`. Eine Zeile, passt zur Security-Floor-Logik dort.

### 4. Mittel: Guards wirken nur auf Claude, und nur als Bitte
- Die Claude-Code-Doku sagt: CLAUDE.md wird als Kontext gelesen, „not enforced configuration“. Blockieren geht nur per PreToolUse-Hook oder Permission-Regeln [FACT].
  - Im Repo erzwingt nur der Pre-Commit-Hook etwas (`receipt-lint`).
  - G1 (GOLD), G2 (NICHTRAUM) und G3 (nicht löschen) sind für Agenten nicht technisch abgesichert [FACT].
- Das Repo wird auch mit Codex bearbeitet: `codex/*`-Branches, #389–#391. Es gibt aber kein `AGENTS.md` [FACT].
  - AGENTS.md ist der offene Standard unter der Agentic AI Foundation (Linux Foundation).
  - Codex-Sessions sehen die Guards G0–G6 damit nicht [HYP: Codex liest CLAUDE.md nicht].
- `.claude/skills/witness_mode.md` liegt flach. Claude Code lädt Skills nur als `.claude/skills/<name>/SKILL.md`, der Witness-Mode wird also nicht als Skill gefunden [FACT].
- CLAUDE.md hat 408 Zeilen; die Doku empfiehlt unter 200 [FACT].
- Maßnahmen:
  - a. `AGENTS.md` mit den Guards anlegen; `CLAUDE.md` importiert es (`@AGENTS.md`)
  - b. Deny-Regeln oder ein PreToolUse-Hook für `index/`, `policies/`, `VOIDMAP.yml`, `data/receipts/`, `receipts/` und `NICHTRAUM/`
  - c. Skill nach `.claude/skills/witness_mode/SKILL.md` verschieben (G3: verschieben, nicht löschen)

### 5. Mittel: Signierte Evidence ohne Secret möglich
- Das Repo ist öffentlich. GitHub-Artifact-Attestations (`actions/attest`) signieren ohne Schlüssel über OIDC und Sigstore und schreiben ins Transparency-Log. Für öffentliche Repos ist das in allen Plänen kostenlos [FACT, GitHub-Doku].
- Heute: Ohne `ENTA_HMAC_SECRET` überspringt CI die Signatur (`signed:false`) [FACT, CLAUDE.md]. In keinem Workflow gibt es eine Attestation [FACT].
- Maßnahme: Snapshot- und Status-Artefakte in `deepjump-ci` bzw. `release.yml` attestieren.
  - Das ergänzt HMAC, ersetzt es aber nicht.
  - Neue Permissions `id-token: write` und `attestations: write` → Workflow-Posture-Check beachten.

### 6. Beobachten, nicht sofort handeln
- **TypeScript 7.0** (Go-Compiler, GA seit Juli 2026): `typescript-eslint` 8.71 erlaubt nur TypeScript `<6.1.0` [FACT]. `eslint-config-next` hängt daran.
  - Ein Dependabot-Major auf TS 7 würde den Lint brechen.
  - Maßnahme: `ignore` für typescript semver-major in `dependabot.yml`, bis typescript-eslint TS 7 unterstützt.
- **ESLint 9 ist seit 06.08.2026 EOL** [FACT]. ESLint 10 wird aber von `eslint-plugin-react`, `-import` und `-jsx-a11y` (Peer `^9`) noch nicht unterstützt [FACT].
  - Nur Dev-Tooling, kein Laufzeitrisiko. Wechsel, wenn `eslint-config-next` nachzieht.
- **pnpm 11/12:** pnpm 12 (Rust-Rewrite) ist `latest`. pnpm 10 wird laut Drittquellen noch gepflegt [HYP, keine offizielle EOL-Angabe].
  - pnpm 11 verlangt Node ≥ 22 (erfüllt) und ersetzt `onlyBuiltDependencies` durch `allowBuilds`.
  - Wechsel als eigener Scope.

### Geprüft, kein Handlungsbedarf
- GitHub hat Node 20 für Actions entfernt (Sept. 2026). Alle 5 gepinnten Actions laufen bereits auf `node24` [FACT].
- Electron 44 ist aktueller Stable-Major (45 in Beta); 44.9.0 kommt über Dependabot.
- Die CI nutzt Node 22: im LTS, kompatibel mit pnpm 11 und Next 16.

## Nicht getan
- Keine Änderung am Code; reine Recherche.
- Keine Prüfung inhaltlicher Fach-Quellen (Resonanz/Mereotopologie). Gesucht war nach Tooling- und Plattform-Einfluss.
- EU AI Act und MCP nicht vertieft: Das Repo ist Forschung ohne Produktivbetrieb und nutzt kein MCP.

## Risiken
- [RISK] Befund 1 bleibt im Audit unsichtbar, bis die npm-Advisory-DB nachzieht. Grünes Audit heißt hier nicht befundfrei.
- [RISK] Ein Teil der Daten stammt aus Sekundärquellen, markiert als [HYP]. Termine wie das genaue EOL-Datum von Python 3.10 können sich verschieben.

## Umsetzung (Owner-OK 2026-10-18, PR #404)
- [x] Befund 1: `next`/`eslint-config-next` 16.4.2, `react`/`react-dom` 19.3.1.
  Geprüft: `verify-js` 5/5, Jest 66/66, Playwright 7 Routen.
- [x] Befund 2: `requires-python >=3.10`, Matrix 3.10–3.14.
  - Lock entfernt nur 13 reine 3.9-Stände.
  - Locked-Install unter 3.10 und 3.14 je 665/665.
- [x] Befund 3: `minimumReleaseAge: 1440`. Lokal nachgewiesen: Eine 1 Tag junge Version wird abgelehnt.
- [x] Befund 4:
  - Guards und Stop Conditions nach `AGENTS.md` verschoben, `CLAUDE.md` importiert sie.
  - Regeln in `.claude/settings.json`: `deny` für Receipts; `ask` für GOLD, `docs/negations.md` und `NICHTRAUM/archive/`.
  - Skill nach `.claude/skills/witness_mode/SKILL.md` verschoben, danach sofort als Skill erkannt.
  - Abweichung vom Wortlaut „Deny“: GOLD und NICHTRAUM/archive bekommen `ask` statt `deny`, weil G1/G3 Änderungen mit OK erlauben. `deny` würde auch eine freigegebene GOLD-CHANGE blockieren.
- [x] Befund 6: Dependabot-`ignore` für typescript semver-major.

## Offene Punkte
- [ ] ☐ Artifact-Attestations (Befund 5), eigener Scope wegen neuer Workflow-Permissions
- [ ] ☐ ESLint 10, sobald `eslint-config-next` und seine Plugins es unterstützen (Befund 6)
- [ ] ☐ pnpm 11/12 als eigener Scope (Befund 6)
- [ ] ☐ Deny-/Ask-Regeln greifen nur für Claude Code. Eine tool-neutrale Absicherung, etwa ein `commit-msg`-Hook, der GOLD-Änderungen ohne `GOLD-CHANGE:` ablehnt, steht noch aus.

## Quellen
- Next.js Security Update 14.10.2026: https://nextjs.org/blog/nextjs-security-update-october-14-2026
- GHSA-673q-mjm6-r5xr: https://github.com/vercel/next.js/security/advisories/GHSA-673q-mjm6-r5xr
- GHSA-p3m5-59mp-jv5r: https://github.com/vercel/next.js/security/advisories/GHSA-p3m5-59mp-jv5r
- PEP 790 (Python 3.15): https://peps.python.org/pep-0790/
- Python-Releases: https://www.python.org/downloads/
- pnpm Dependency-Resolution-Settings: https://pnpm.io/settings/dependency-resolution
- pnpm 11 Release: https://pnpm.io/blog/releases/11.0
- Dependabot Default-Cooldown: https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/
- ESLint Version Support: https://eslint.org/version-support/
- ESLint v10 Migration: https://eslint.org/docs/latest/use/migrate-to-10.0.0
- GitHub Node-20-Deprecation: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
- Artifact Attestations: https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds
- Claude Code Memory/Rules/AGENTS.md: https://code.claude.com/docs/en/memory
- Claude Code Skills: https://code.claude.com/docs/en/skills
- AGENTS.md / Agentic AI Foundation: https://openai.com/index/agentic-ai-foundation/

## Artefakte
- `OUT/upstream_radar_2026-10-18.md`
