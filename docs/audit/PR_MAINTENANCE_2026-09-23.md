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

## Integration der JS-Updates

[FACT] #351 (Next 16.3.3), #349 (PostCSS 8.5.23), #347 (Tailwind 4.3.3)
und #348 (Turbo 2.10.7) werden gemeinsam integriert. Überlappende Manifest-
und Lockfile-Änderungen werden durch Beibehaltung aller vier Zielversionen und
Regeneration mit dem Repo-Pin `pnpm@10.33.0` aufgelöst.
[MODEL] #346 (Next 16.2.12) und #350 (identisches Next-Update ohne Lockfile)
sind nach erfolgreicher Integration durch #351 ersetzt; Historie bleibt erhalten.

[FACT] Der frische lokale Audit weist zusätzlich zu den September-11-Funden
kritisches Next <16.3.3 und hohes Sharp <0.35.4 aus. Die Security-Floors werden
für PostCSS, Undici 6/7, fast-uri, brace-expansion, nanoid, browserslist,
@xmldom/xmldom, baseline-browser-mapping und sharp aktualisiert.
Die vorhandene CJS-/ESM-Kompatibilitätsanpassung wird für brace-expansion 5.0.9
übernommen; die alte Patchdatei bleibt als Provenienz erhalten.

## Workflow-Korrekturen

- [FACT] Security Audit berücksichtigt nun `pnpm-workspace.yaml`, `patches/**`
  und `pyproject.toml`; vorher konnten diese Dependency-Eingaben den Pfadfilter
  umgehen. JS-Workspace prüft ebenfalls Patchänderungen.
- [FACT] `All Tests Pass` läuft mit `always()` und akzeptiert ausschließlich
  erfolgreiche Ergebnisse aller drei Vorgänger. Bash-Prüfung aller 64
  Kombinationen aus success/failure/skipped/cancelled: genau eine erfolgreich.
- [FACT] SoT-Dokumentpointer und veröffentlichte Checknamen in den Governance-
  Entwürfen korrigiert. Settings-Enforcement bleibt UNVERIFIED.

## Lokale Prüfung

- [FACT] `make verify`: 626 Tests und 165 Subtests erfolgreich; Ports, Pointer
  und Claims bestanden (Python 3.12). Bestehende Warnungen bleiben sichtbar.
- [FACT] `make verify-governance`: 14 Workflows erfüllen den Posture-Vertrag,
  Backlog und 22 VOID-Einträge sind synchron.
- [FACT] Node der lokalen Umgebung: 24.19.0; GitHub prüft weiterhin Node 22.
  Der initial im PATH verfügbare pnpm war 11; die finale Lockdatei wird explizit
  mit `corepack pnpm` (Repo-Pin 10.33.0) regeneriert und frozen installiert.
- [FACT] Der lokale S4-Kontrolllauf enumeriert 24 Knoten, drei Nachbarn pro
  Knoten und den Eigenwert -1 im ungewichteten Kern. Das stützt den in
  `ISSUE_APPROACHES_2026-09-23.md` dokumentierten Periodizitäts-Prüfpunkt.

Weitere JS-/Security-Ergebnisse werden nach Abschluss ergänzt; aus diesem
Zwischenstand folgt noch keine Merge-Freigabe der JS-Integration.

[FACT] Finale Lock-Auflösung mit pnpm 10.33.0 abgeschlossen. Anschließendes
`corepack pnpm audit --json`: 867 Dependencies, keine gemeldeten Advisories
(0 critical/high/moderate/low/info, keine muted Advisories). Dies ist ein
zeitgebundener Registry-Befund, keine allgemeine Sicherheitsgarantie.
