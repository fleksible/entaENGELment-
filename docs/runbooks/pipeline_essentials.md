# Pipeline Essentials — Ausbau-Runbook

[FACT] Dieses Runbook bündelt weitere Möglichkeiten, die DeepJump-Pipeline für essenzielle Handhabung zu erweitern, ohne die bestehenden Gates zu überladen.

## Zielbild

Die Pipeline bleibt dreistufig: **Verify → Status → Snapshot**. Neue Checks werden zuerst als beobachtende Essentials sichtbar gemacht, danach mit klarer Scope-Definition in `make verify` oder CI gehärtet.

Der Scanner ist bewusst beobachtend. Er dokumentiert Ausbauoptionen, verändert aber keine bestehenden Gates.

Die aktuelle Workflow-/Rechtekarte steht in [`docs/ci/WORKFLOW_MAP.md`](../ci/WORKFLOW_MAP.md).

## Schneller Lage-Scan

```bash
make pipeline-essentials
```

Der Befehl ruft `tools/pipeline_essentials.py` auf und erzeugt einen statischen Markdown-Report zu vorhandenen Essentials und nächsten Ausbauoptionen.

## Workflow-Posture-Drift prüfen

```bash
make workflow-posture-check
```

Der Befehl ruft `tools/workflow_posture_check.py` auf und prüft read-only, ob jede Datei unter `.github/workflows/` einen expliziten `permissions`-Block sowie einen `concurrency`-Block mit `cancel-in-progress: true` deklariert. Berechtigungen, die breiter als `contents: read` sind, müssen in [`docs/ci/WORKFLOW_MAP.md`](../ci/WORKFLOW_MAP.md) als Ausnahme dokumentiert sein (der Workflow-Dateiname muss dort genannt werden). Der Check verändert keine Dateien, braucht kein Netzwerk und endet bei Drift mit Exit-Code 1.

## Lokale Verifier-Membranen

```bash
make verify
make verify-governance
make verify-js
make verify-all
```

[FACT] `make verify` bleibt der stabile Core-Entry-Point für Ports, Tests, Pointer und Claim-Lint. Governance- und JS/TS-Workspace-Checks sind eigene Membranen, damit kleine lokale Änderungen bedienbar bleiben und UI-/Dependency-PRs nicht versehentlich durch einen Python-only-Run als geprüft gelten.

[FACT] `make verify-js` erzwingt `pnpm install --frozen-lockfile` und danach `pnpm turbo run typecheck lint build`. Damit werden UI-App- und Package-Änderungen an die gleiche Lockfile-/Workspace-Disziplin gebunden wie die PR-CI.

[FACT] `make verify-governance` bündelt Workflow-Posture-Check und VOID-Backlog-Drift-Check. Es prüft keine inhaltliche VOID-Schließung, sondern ob die Repo-Artefakte synchron und posture-stabil bleiben.

## Dependency-PR-Leseregel

[FACT] Bei `ui-app/**`, `packages/**`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `package.json`, `turbo.json` oder `tsconfig.base.json` ist ein grüner Core-Verify allein nicht ausreichend. Vor Merge braucht es die JS/TS-Workspace-Membran: frozen lockfile install, typecheck, lint und build.

[MODEL] Für das Repository ist das die F7-kompatible Lesart: kein `False OK` aus einem falschen Prüfraum. Ein Dependency-PR darf nicht durch Claims-/Pointer-/Python-Checks als ausreichend validiert erscheinen, wenn seine eigentliche Wirkung im UI-/Workspace-Membranraum liegt.

## Konkrete Ausbau-Möglichkeiten

| ID | Möglichkeit | Nutzen | Nächster Schritt |
|----|-------------|--------|------------------|
| ESS-001 | `make verify` als lokaler Core-Entry-Point | Weniger Bedienfehler vor PRs | Im Contributor-Flow weiter als Pflichtschritt kommunizieren |
| ESS-002 | Receipt-Lint früher laufen lassen | Audit-Drift wird vor Release sichtbar | Scope für `receipts/` und `ark/p4/receipts/` festlegen |
| ESS-003 | VOID-Backlog-Drift in PR-CI prüfen | Governance-Doku bleibt synchron zur `VOIDMAP.yml` | `make voids-backlog-check` in eine PR-Workflow-Stufe aufnehmen |
| ESS-004 | Frame-Lint kanonisch scopen | Operative Frames werden maschinell konsistent | `FRAME_LINT_PATHS` verbindlich festlegen |
| ESS-005 | HMAC-Status-Verifikation bewusst trennen | Fork-PRs ohne Secrets bleiben prüfbar | Signierte Runs nur in trusted CI/Schedule erzwingen |
| ESS-006 | Snapshot-Artefakte konsequent hochladen | Reproduzierbarkeit wird leichter auditierbar | Manifest-Upload für geplante Runs prüfen |
| ESS-007 | Lokale Dependency-Audit-Vorstufe | Release-Prep erkennt Risiko früher | Optionales Make-Target für leichte Audits ergänzen |
| ESS-008 | Gepinnte Actions rotieren | Supply-Chain-Risiko bleibt reviewbar | SHA-Rotation über dedizierte Dependency-PRs planen |
| ESS-009 | Lokaler JS/TS-Workspace-Verifier | UI-/Package-Änderungen werden im richtigen Prüfraum validiert | `make verify-js` bei Dependency-/UI-PRs verpflichtend lesen |
| ESS-010 | Blocking JS/TS Workspace PR Gate | Dependabot-PRs laufen gegen frozen Lockfile + Turbo | CI-Ergebnisse vor Merge prüfen; kein Merge bei Package-/Lockfile-Drift |
| ESS-011 | Workflow Map synchron halten | Verifier-Membranen bleiben auditierbar | Neue Workflows sofort in `docs/ci/WORKFLOW_MAP.md` eintragen |
| ESS-012 | Einheitliche Node-Major-Version | Verhindert split-brain zwischen UI-Build und Workspace-CI | JS-Testworkflow und Workspace-CI auf dieselbe Node-Major-Version halten |

## Härtungsregel

[FACT] Ein Essential wird erst dann blocking, wenn drei Bedingungen erfüllt sind:

1. Scope ist eindeutig dokumentiert.
2. Lokaler Befehl existiert und ist reproduzierbar.
3. CI-Ausführung hat einen klaren Secret-/Fork-Fallback.

So bleibt die Pipeline bedienbar und gewinnt trotzdem zusätzliche Kontrollpunkte.
