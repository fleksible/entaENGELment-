# PR #475 — ESLint-Abgleich und tatsächlicher Runtime-Scope

Prüfdatum: 2026-11-17 (Europe/Berlin). Technischer Review durch den Coding-Agenten.
Mandat: Prüfung und Ausbesserung dieses Dependency-PRs; Übernahme bei tragfähigen
Nachweisen durch den Auftraggeber ausdrücklich delegiert.

## Gegenstand und Entscheidung

**HOLD: Aktueller High-Audit blockiert den Merge.**
Der geprüfte Dependency-Diff ändert die Lint-Konfiguration und mehrere gemeinsam
verwendete transitive Werkzeuge. Er ist kein zusätzliches Next.js-Runtime-Patch.
Die bereits vorhandenen CI-Läufe decken Lint, Typprüfung, statischen UI-Build,
UI-/Root-JavaScript-Tests und den tatsächlich gestarteten AppImage-Payload ab.

- PR: <https://github.com/fleksible/entaENGELment-/pull/475>
- Geprüfte Basis: `b4ad2a01a87871457d07704bb12d194c784c2bd4`.
- Geprüfter Dependency-Head: `e41e6f4659c007a4e14dabac2bb09a3ab788ba0b`.
- CI-Checkout: synthetischer Merge `5a249e225fa56cb30f87bcdc6c9f6f950bdc3115`.
- Dieser zusätzliche Bericht ändert keine Dependencies oder Produktdateien.

## Exakter Scope

Der ursprüngliche PR ändert ausschließlich `ui-app/package.json` und
`pnpm-lock.yaml`. Einziger direkter Manifest-Pin ist
`eslint-config-next: 16.4.3 -> 16.4.6`. `next` und `@next/env` bleiben auf 16.4.6;
auch die SWC-Paketversionen werden nicht angehoben. Der `next`-Importer erhält
jedoch einen anderen Babel-Peer-Kontext.

Eigenständig ausgeführter struktureller Vergleich:

```sh
python tools/lockfile_scope_diff.py \
  --base b4ad2a01a87871457d07704bb12d194c784c2bd4 \
  --head e41e6f4659c007a4e14dabac2bb09a3ab788ba0b
```

Ergebnis: 28 hinzugefügte und 26 entfernte Paketkennungen, 28 betroffene
Paketnamen; 52 neue und 50 entfernte Snapshot-Kontexte, 466 geänderte
Snapshot-Kanten. Zwei Importer-Kanten ändern sich: `ui-app/dependencies/next`
und `ui-app/devDependencies/eslint-config-next`. Keine Metadatenänderung unter
unveränderten Paketkennungen und keine sonstige Top-Level-Änderung.

| Paketgruppe | Versionsänderung |
| --- | --- |
| `eslint-config-next`, `@next/eslint-plugin-next` | 16.4.3 -> 16.4.6 |
| `typescript-eslint` und zehn `@typescript-eslint/*`-Pakete | 8.72.1 -> 8.72.2 |
| `@babel/core`, `@babel/helper-compilation-targets` | 7.29.7 -> 7.29.13 |
| `@babel/generator`, `@babel/parser`, `@babel/traverse` | 7.29.12 -> 7.29.14 |
| `@babel/helper-module-transforms` | 7.29.7 -> 7.29.14 |
| `@babel/helper-string-parser`, `@babel/types` | 7.29.11 -> 7.29.14 |
| `@babel/helpers` | 7.29.10 -> 7.29.14 |
| `@babel/runtime` | 7.29.13 -> 7.29.14 |
| `@eslint-community/regexpp` | 4.12.3 zusätzlich; 4.12.2 bleibt vorhanden |
| `electron-to-chromium` | 1.5.472 -> 1.5.485 |
| `graceful-fs` | 4.2.12 zusätzlich; 4.2.11 bleibt vorhanden |
| `is-core-module` | 2.17.0 -> 2.18.0 |
| `napi-postinstall` | 0.3.7 -> 0.3.8 |

Damit reicht der Lock-Diff in Jest/Istanbul, React-Hooks-Lint, Resolver und
`fs-extra@7.0.1` hinein. Paketnamen oder eine unveränderte Next-Version allein
wären kein Nachweis unveränderter Teilbäume. Die tatsächlichen Resolution-Kanten
wurden deshalb mitgelesen und gegen die passenden Tests abgeglichen.

Provenienz des Lock-Diffs:

- Basis-Blob: `0db3fce74bc7ff638962dfeee42dc714c3fa9da8`.
- Head-Blob: `6e053d52f1d0d54491598c81fad2898fda5bf9a4`.
- Basis SHA-256: `49a9e20f0160d3b1e93ec66694140582b946a2179af2559848829e294e185a27`.
- Head SHA-256: `851dcc937d26c3f9e8219487514e223044e0134bad58a34d89e7ff455acb4cb6`.
- Raw-Diff SHA-256: `1e56157d23d92d194936a8f56adb7ef7fc01e4cfa866c53fed73ace22eb17e28`.

## Runtime- und Sicherheitsbezug

Statisch gelesen: `ui-app/next.config.js` verwendet `output: 'export'` und
`images.unoptimized: true`. Unter `ui-app/` gibt es keine Route-Handler,
Middleware-/Proxy-Dateien oder Treffer für `use cache`, `unstable_cache`,
`next/cache`, `next/image`, `next/server`, `next/headers`, Edge-Runtime-Auswahl,
`cacheComponents`, `Cache-Control` oder `revalidate`. Der CI-Build bestätigt
statisch vorgerenderte Routen.

Folgerung für diesen Repository-Stand: Die in den gemeinsamen Next-Release-Notes
genannten Cache-, Edge-Cookie- und Bildoptimierungsfehler sind kein belegter
aktiver Nutzungspfad dieser UI. Dieser PR darf deshalb weder als Beleg einer
neuen Runtime-Sicherheitsreparatur noch als umfassender Sicherheitsnachweis
geführt werden. Externe Deployments oder abweichende Betriebskonfigurationen
wurden nicht geprüft.

## Direkt gelesene CI- und Review-Belege

API-Stand des Dependency-Heads: 34 Check-Runs = 25 erfolgreich, 8 übersprungen,
1 neutral; keine fehlgeschlagene Prüfung. Keine eingereichte menschliche
GitHub-Review und keine Inline-Review-Threads vorhanden. Eine angeforderte Review
ist keine Freigabe; dieser Bericht ist ebenfalls keine unabhängige Zweitreview.

| Beleg | Tatsächlich gelesener Umfang |
| --- | --- |
| [Workspace-Job](https://github.com/fleksible/entaENGELment-/actions/runs/43796606267/job/133066723146) | Frozen Install, fünf Turbo-Aufgaben erfolgreich, keine Cache-Treffer; Typprüfung, ESLint, Next-Build, 58 Node-Tests und 6 UI-Jest-Tests bestanden |
| [Separater UI-Build](https://github.com/fleksible/entaENGELment-/actions/runs/43796605980/job/133066722399) | Next 16.4.6 kompiliert; statischer Export erfolgreich |
| [Root-JavaScript](https://github.com/fleksible/entaENGELment-/actions/runs/43796605980/job/133066722471) | Je 71 Tests in sechs Suites, mit und ohne Coverage, bestanden |
| [Desktop](https://github.com/fleksible/entaENGELment-/actions/runs/43796606009/job/133066723023) | 7 Packaging-/Sandbox-Tests, AppImage-Bau und Start des tatsächlichen Payloads mit aktiver Sandbox bestanden |
| [JS-Audit](https://github.com/fleksible/entaENGELment-/actions/runs/43796606129/job/133066723082) | Vollständiger Audit meldet fünf Befunde: 1 niedrig, 4 moderat; nur das High-Gate ist erfolgreich |

Das JS-Audit nennt `glob` (GHSA-3g3m-2fjr-6pw4), `minimatch`
(GHSA-g3hv-75wg-m249) und `deepmerge` (GHSA-gcqx-w48m-w2h4) in Test-/Packaging-
Werkzeugen. Die betreffenden Paketversionen werden durch diesen PR nicht
geändert. Das vollständige `pnpm audit` beendet sich mit Exit 1; der Workflow
erlaubt diesen Schritt und blockiert erst bei `--audit-level=high`.
**Grüner Job bedeutet hier keine Befundfreiheit.** Diese verbleibenden Findings
werden nicht stillschweigend behoben oder als durch diesen PR erledigt markiert.

CodeQL ist neutral: Vier Konfigurationen fehlen für den PR-Vergleich. Die
Legacy-Build-/Security-Jobs und der signierte DeepJump-Pfad sind übersprungen;
ihnen wird keine Prüfleistung zugeschrieben. Die dedizierten Jobs liefern die
oben benannten konkreten Belege.

## Erneuter Audit: früheres Grün ist überholt

Nach Aufnahme dieses Berichts wurde die CI am Head
`9292851344b41ac9f6f2073a267d90f5df2c2293` erneut gestartet.
Der [aktuelle JS-Audit-Job](https://github.com/fleksible/entaENGELment-/actions/runs/44144870580/job/134257148477)
scheitert jetzt auch im verbindlichen `pnpm audit --audit-level=high` mit Exit 1:
sechs Befunde, davon vier moderat und zwei hoch. Die früheren fünf Befunde sind
ein zeitlich gebundener Nachweisstand; ihre Zahl darf nicht fortgeschrieben werden.

Die beiden hohen Befunde betreffen `picomatch` über
`electron-builder > app-builder-lib > @electron/rebuild > node-gyp > tinyglobby`
und `jest > @jest/core > jest-haste-map > anymatch`.
[GHSA-fc5q-39xc-vjpf / CVE-2026-112366](https://github.com/advisories/GHSA-fc5q-39xc-vjpf)
wurde am 17. November 2026 überprüft/aktualisiert, betrifft laut Advisory
Versionen bis einschließlich 4.0.7 und nennt keine gepatchte Version.
Diese Dependency war bereits in der Basis enthalten und wird durch #475 nicht
angehoben. Das ist ein konkreter aktueller Gate-Befund, kein Nachweis eines
erreichbaren Angriffs auf die statisch exportierte UI.

Das Python-Audit desselben Laufs ist erfolgreich. Weitere erfolgreiche
Funktionsprüfungen ersetzen das fehlgeschlagene High-Gate nicht. Eine
Ausnahmeregel oder Herabstufung des Gates ist nicht Teil dieses Dependency-PRs.

## Kleinste belastbare Handlung

Den Versionsabgleich vorbereitet offen halten. Vor einer Übernahme müssen die
hohen `picomatch`-Befunde durch eine verfügbare Reparatur beseitigt werden oder
eine eigenständig begründete, ausdrücklich autorisierte Risikoausnahme vorliegen.
Ein separater Cache-/Edge-Integrationstest
ist für die hier fehlenden Nutzungspfade nicht erforderlich. Bei zukünftigem
Serverbetrieb, Cache Components oder aktivierter Bildoptimierung muss die
Erreichbarkeit neu bewertet werden. Governance-Regeln und menschliche
Commit-Zuständigkeit ändern sich durch diese Versionspflege nicht.
