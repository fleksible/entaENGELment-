# ADR-0003: Security Baseline & Code Scanning

- **Status:** Accepted (Baseline-Dokumentation) / Proposed (Code-Scanning-Aktivierung)
- **Datum:** 2026-06-16
- **Kontext-Fokus:** Security-Posture-Baseline (PR #254)

## Context

Nach PR #252 (Audit/Zukunftsarchitektur) und PR #253 (`.gitignore`-Fix) ist der
nächste reife Schritt eine **Security-Posture-Baseline** — nicht ein Feature-Sprung.
Das Repo besitzt bereits Dependency-Audits, SBOM, Bandit, Dependabot-Version-Updates,
SHA-gepinnte Actions und minimale Workflow-Permissions (siehe
`docs/audit/security_posture_baseline_2026-06-16.md`). Es fehlt **Code Scanning
(CodeQL)**. Mehrere Härtungspunkte sind **Repo-Settings**, keine Dateien.

## Decision

1. **Baseline sichtbar machen** statt Sicherheit behaupten: vorhandene Stärken,
   fehlende dateibasierte Bausteine und **offene Settings-Toggles** werden
   explizit als solche markiert (Anti-F7).
2. **Code Scanning:** primär **Default Setup** in den Repo-Settings empfehlen
   (wartungsarm, kein Action-Pinning). **Keine aktive `codeql.yml`** wird in diesem
   PR committet, weil ein aktueller `github/codeql-action`-SHA in der Read-Only-
   Audit-Umgebung **nicht verifizierbar** ist; ein geratener SHA wäre falsche
   Sicherheit. Die Advanced-Variante liegt unten als **Vorlage** (vor Aktivierung
   SHA-pinnen).
3. **Kein Auto-Merge** in diesem PR; `dependabot.yml` bleibt unverändert.
4. **Keine** Framework-Kanon-, Spec-, VOID-, Claim- oder Roadmap-Inhalte berührt.

## Consequences

- (+) Ehrliche Posture: „trägt bereits" vs. „offener Toggle" klar getrennt.
- (+) Kein Workflow mit unverifiziertem SHA; keine falsche Sicherheit.
- (−) Code Scanning ist erst aktiv, wenn du Default Setup togglest **oder** die
  Vorlage SHA-gepinnt aktivierst.
- (−) Settings-Härtung (Branch-Protection etc.) bleibt manuell (außerhalb dieses PRs).

## Alternatives Considered

1. **Aktive `codeql.yml` mit geratenem/Tag-Pin committen** — verworfen: verletzt die
   SHA-Pin-Invariante bzw. riskiert falsche Sicherheit (Anti-F7).
2. **Branch-Protection per PR setzen** — nicht möglich: Rulesets sind Repo-Settings,
   nicht dateibasiert und nicht über die hier verfügbaren Tools schaltbar.
3. **Auto-Merge jetzt aktivieren** — verworfen: erst Baseline, separater späterer
   Entscheid (patch-only, grüne CI).

## Essence Preservation Note

Reine Infrastruktur-/Governance-Entscheidung. Kein Kanon-Begriff, keine symbolische
Architektur, keine Claim-Grenze verändert.

## Linked VOID / Spec / Claim

- Baseline: `docs/audit/security_posture_baseline_2026-06-16.md`
- Kein VOID, keine Spec berührt.

---

## Appendix A — CodeQL Advanced-Setup Vorlage (NICHT aktiv)

> [FAKT] Dies ist eine **Vorlage**, kein aktiver Workflow. Vor Verwendung:
> `github/codeql-action/*` auf einen **aktuellen Release-SHA pinnen** (Kommentar
> mit Versionstag), passend zur Repo-Konvention. Datei dann nach
> `.github/workflows/codeql.yml` legen und committen.

```yaml
name: CodeQL

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  schedule:
    - cron: "0 4 * * 1"   # wöchentlich, Montag
  workflow_dispatch:

# Minimale Permissions: nur was Code Scanning braucht.
permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  analyze:
    name: Analyze (${{ matrix.language }})
    runs-on: ubuntu-latest
    permissions:
      security-events: write   # Upload der Scan-Ergebnisse
      packages: read           # private CodeQL packs
      actions: read            # private repo workflow metadata
      contents: read
    strategy:
      fail-fast: false
      matrix:
        language: ["python", "javascript-typescript"]
    steps:
      - name: Checkout
        # SHA bereits im Repo verwendet (actions/checkout v6.0.3) — wiederverwendbar:
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10  # v6.0.3

      - name: Initialize CodeQL
        # TODO(pin): auf aktuellen github/codeql-action-Release-SHA pinnen.
        uses: github/codeql-action/init@<SHA>  # vX.Y.Z
        with:
          languages: ${{ matrix.language }}

      - name: Autobuild
        uses: github/codeql-action/autobuild@<SHA>  # vX.Y.Z

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@<SHA>  # vX.Y.Z
        with:
          category: "/language:${{ matrix.language }}"
```

> Hinweis: Bei reinem Python/JS/TS ist i. d. R. kein Build nötig; `autobuild` kann
> entfallen. Vor Aktivierung mit `tools/workflow_posture_check.py` und
> `docs/ci/WORKFLOW_MAP.md` abgleichen (neuer Workflow muss dort eingetragen werden,
> da `security-events: write` über `contents: read` hinausgeht).
