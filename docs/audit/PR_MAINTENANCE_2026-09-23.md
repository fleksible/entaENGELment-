# PR maintenance — 2026-09-23

**FOKUS:** offene Dependency-PRs prüfen und Integrationsblocker beheben.
**Status:** Arbeitsprotokoll; Befunde gelten nur für die genannten Revisionen.
**Baseline:** `0aa93c5351164b86fc0bcdc1b72b5d5db8e4cb9f`.

## Maßstab

[MODEL] Consent, Provenienz, Revisionsfähigkeit und Verify-before-merge aus
README/CLAUDE bestimmen diesen Wartungslauf. Ein grüner Check belegt seinen
Scope, keine allgemeine Sicherheit. Private Quellen werden nicht exportiert.

## Codecov #352

[FACT] Diff: ausschließlich der SHA-Pin in `.github/workflows/ci.yml`,
`fb8b3582...` → `303a32d7...` (7.1.1). Token-Scope und Fehlerbehandlung bleiben
unverändert. Der Branch lässt sich konfliktfrei mit der Baseline verbinden.
[FACT] Sieben PR-Workflows auf `f0c15aae` waren erfolgreich, darunter DeepJump,
Python Quality und Tests. Codecov selbst läuft nur nach Push, nicht im PR-Gate;
dieser Upload ist weiterhin optional. Kein Nachweis eines erfolgreichen Uploads.

## Initiale Blocker

- [FACT] #351: Workspace-Build grün, Security Audit rot. Job `103164476341`
  meldet 18 hohe und 11 moderate JS-Advisories; kein Anlass zur Gate-Abschwächung.
- [FACT] #350 ändert nur das UI-Manifest, #351 auch den Workspace-Lockfile.
- [FACT] #298 und #339 haben fehlgeschlagene Toolchain-Gates und dokumentierte
  Parser-/React-Plugin-Inkompatibilitäten. Major-Migration bleibt separat.
- [FACT] Fünf offene Issues: #278, #305, #311, #332, #333.
