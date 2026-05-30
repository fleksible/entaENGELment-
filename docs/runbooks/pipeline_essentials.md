# Pipeline Essentials — Ausbau-Runbook

[FACT] Dieses Runbook bündelt weitere Möglichkeiten, die DeepJump-Pipeline für essenzielle Handhabung zu erweitern, ohne die bestehenden Gates zu überladen.

## Zielbild

Die Pipeline bleibt dreistufig: **Verify → Status → Snapshot**. Neue Checks werden zuerst als beobachtende Essentials sichtbar gemacht, danach mit klarer Scope-Definition in `make verify` oder CI gehärtet.

Der Scanner ist bewusst beobachtend. Er dokumentiert Ausbauoptionen, verändert aber keine bestehenden Gates.

## Schneller Lage-Scan

```bash
make pipeline-essentials
```

Der Befehl ruft `tools/pipeline_essentials.py` auf und erzeugt einen statischen Markdown-Report zu vorhandenen Essentials und nächsten Ausbauoptionen.

## Konkrete Ausbau-Möglichkeiten

| ID | Möglichkeit | Nutzen | Nächster Schritt |
|----|-------------|--------|------------------|
| ESS-001 | `make verify` als lokaler Single-Entry-Point | Weniger Bedienfehler vor PRs | Im Contributor-Flow weiter als Pflichtschritt kommunizieren |
| ESS-002 | Receipt-Lint früher laufen lassen | Audit-Drift wird vor Release sichtbar | Scope für `receipts/` und `ark/p4/receipts/` festlegen |
| ESS-003 | VOID-Backlog-Drift in PR-CI prüfen | Governance-Doku bleibt synchron zur `VOIDMAP.yml` | `make voids-backlog-check` in eine PR-Workflow-Stufe aufnehmen |
| ESS-004 | Frame-Lint kanonisch scopen | Operative Frames werden maschinell konsistent | `FRAME_LINT_PATHS` verbindlich festlegen |
| ESS-005 | HMAC-Status-Verifikation bewusst trennen | Fork-PRs ohne Secrets bleiben prüfbar | Signierte Runs nur in trusted CI/Schedule erzwingen |
| ESS-006 | Snapshot-Artefakte konsequent hochladen | Reproduzierbarkeit wird leichter auditierbar | Manifest-Upload für geplante Runs prüfen |
| ESS-007 | Lokale Dependency-Audit-Vorstufe | Release-Prep erkennt Risiko früher | Optionales Make-Target für leichte Audits ergänzen |
| ESS-008 | Gepinnte Actions rotieren | Supply-Chain-Risiko bleibt reviewbar | SHA-Rotation über dedizierte Dependency-PRs planen |

## Härtungsregel

[FACT] Ein Essential wird erst dann blocking, wenn drei Bedingungen erfüllt sind:

1. Scope ist eindeutig dokumentiert.
2. Lokaler Befehl existiert und ist reproduzierbar.
3. CI-Ausführung hat einen klaren Secret-/Fork-Fallback.

So bleibt die Pipeline bedienbar und gewinnt trotzdem zusätzliche Kontrollpunkte.
