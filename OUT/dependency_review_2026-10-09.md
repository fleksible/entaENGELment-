# Report: Abhängigkeiten und automatische Agent-Anweisungen

**Datum:** 2026-10-09
**Nachprüfung:** 2026-10-10
**Fokus:** Dependency-Restpunkte bearbeiten
**Authority:** DERIVED / REVIEW-PENDING
**Basis:** main `a7773db68d97dbd8271b0921d011934d2e921170`.

## Ziel
Den heutigen Auditstand prüfen, gepatchte Next.js-Befunde beseitigen und Turbos
automatische Änderungen an Agent-Anweisungen explizit deaktivieren.

## Aktionen
- [x] Audit neu ausgeführt. Abweichung vom Bericht des 7. Oktober: jetzt acht
  Befunde (1 low, 5 moderate, 2 high; davon ein High ignoriert).
- [x] Next.js und eslint-config-next auf 16.3.8 angehoben, Lockfile aktualisiert.
  Dies adressiert die sechs neuen Next.js-Advisories ohne zusätzliche Ausnahme.
- [x] `agentGuidance: false` in `turbo.json`: Turbo soll keine eigenen Blöcke
  mehr in der Root-AGENTS.md erzeugen/aktualisieren. Das installierte Schema von
  Turbo 2.11.7 unterstützt diese Option. Vorhandene Anweisungen werden nicht gelöscht.
- [x] `braces`-Ausnahme erneut überprüft und Prüfnachweis an der Ausnahme verlinkt.
- [x] Lockfile mit der Repo-Version pnpm 10.33.0 erzeugt; der Diff enthält nur
  Next.js-bezogene Einträge. Keine Lockformat-Migration.
- [x] `pnpm turbo run typecheck lint build test`: 5/5 Tasks erfolgreich,
  einschließlich 23 UI-Tests und statischem Produktions-Build.
- [x] Audit nach dem Versionsupdate: wieder zwei Befunde (1 moderate, 1 high
  ignoriert); `pnpm audit --audit-level=high` besteht.
- [x] Am 10. Oktober erneut bestätigt: Frozen-Lock-Prüfung mit pnpm 10.33.0
  und High-Audit-Gate erfolgreich; main weiterhin auf dem oben genannten Commit.

## Security-Befunde und Grenzen

| Paket | Befund | Ergebnis der Prüfung |
|---|---|---|
| next 16.3.6 | GHSA-cjq9-62q9-8jv4 (high) sowie fünf weitere Advisories | Update auf 16.3.8; keine neue Ignore-Regel. |
| braces 3.0.3 | GHSA-vfj7-8cjw-p6xm (high) | Weiterhin keine gepatchte Version laut Advisory. Bestehende Ausnahme bleibt unverändert. |
| sprintf-js 1.1.3 | GHSA-hp3w-g68c-fv3c (moderate) | Weiterhin keine gepatchte Version laut Advisory. Sichtbar im Audit; keine Ausnahme ergänzt. |

[FACT] Der installierte braces-Pfad ist `ui-app → eslint-config-next →
@next/eslint-plugin-next → fast-glob → micromatch → braces`. Er ist eine
Entwicklungsabhängigkeit. Die Ausnahme ist durch diese begrenzte Nutzung
begründet, nicht durch eine Reparatur des verwundbaren Pakets. Repo-/CI-Eingaben
bleiben eine Vertrauensannahme; „dev dependency“ allein beweist keine Sicherheit.
Bei neuem Datenpfad oder Upstream-Patch ist die Ausnahme erneut zu bewerten.

[FACT] sprintf-js liegt im optionalen Entwicklungsweg `electron-builder →
app-builder-lib → @electron/get → global-agent → roarr → sprintf-js`.
Keine Aussage über generelle Unausnutzbarkeit.

[FACT] Die derzeitige Next-Konfiguration exportiert statisch und setzt
`images.unoptimized: true`. Das begrenzt die konkrete Laufzeitexposition des
Image-Optimizer-Fundes, ersetzt aber das Versionsupdate nicht.

## Privater Meldeweg: vorbereiteter Empfangstest
Der externe Ende-zu-Ende-Empfang ist **UNOBSERVED**. Die verfügbare Verbindung ist
ein Maintainer-Zugang; ein selbst angelegter Draft-Advisory würde den Meldeweg
für außenstehende Personen nicht prüfen. Kein Testbericht wurde versandt.

Konkreter harmloser Test für ein autorisiertes Konto ohne Repo-Adminrechte:

1. Unter `https://github.com/fleksible/entaENGELment-/security/advisories`
   „Report a vulnerability“ öffnen.
2. Titel: `[TEST – keine Schwachstelle] Privater Meldeweg 2026-10-09`.
3. Inhalt: „Abgestimmter Funktionstest. Keine Schwachstelle, keine Secrets,
   keine Exploitdaten. Bitte nur den privaten Empfang bestätigen.
   Testkennung: ENTA-PRIVATE-ROUTE-20261009.“
4. Maintainer bestätigt den Empfang privat. Nur Datum, erfolgreiche Zustellung
   und diese harmlose Testkennung dürfen als Ergebnis dokumentiert werden.
5. Den Test anschließend privat als Test schließen; nichts veröffentlichen.

## Nicht getan
- Keine neuen Advisory-Ausnahmen, kein Release, kein Merge.
- Kein Patch des Upstream-Pakets braces oder sprintf-js behauptet.
- Kein vorhandenes AGENTS.md gelöscht oder automatisch kanonisiert.

## Risiken
- Security-Grün bleibt mit der bestehenden High-Ausnahme vereinbar.
- Die Deaktivierung von Agent-Guidance ist eine reversible Konfigurationsentscheidung
  in diesem Review-Kandidaten; die House Rules bleiben maßgeblich.

## Offene Punkte
- [ ] CODEOWNERS-/Claude-/Diogenes-Review vor Integration.
- [ ] Externer privater Empfangstest mit getrenntem Melder- und Empfängerkonto.
- [ ] Upstream-Patches für braces/sprintf-js weiter beobachten.

## Artefakte
- `ui-app/package.json`
- `pnpm-lock.yaml`
- `pnpm-workspace.yaml`
- `turbo.json`

## Quellen
- [braces-Advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm)
- [sprintf-js-Advisory](https://github.com/advisories/GHSA-hp3w-g68c-fv3c)
- [Next.js-SSRF-Advisory](https://github.com/vercel/next.js/security/advisories/GHSA-cjq9-62q9-8jv4)
- [Turbo agentGuidance](https://turborepo.dev/docs/reference/configuration#agentguidance)
