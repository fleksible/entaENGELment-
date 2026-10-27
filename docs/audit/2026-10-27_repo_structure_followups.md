# Repo-Struktur und Folgekorrekturen

Stand: 27. Oktober 2026 · DERIVED / REVIEW-PENDING.
FOKUS: Repo-Struktur und bestehende Folgeaufgaben

## Umfang

Die strukturelle Lesekarte liegt als Intake-Entwurf unter
`docs/intake/raw/2026-10-27/repo-struktur-und-technische-folgeaufgaben.md`.
Die administrative Arbeitsliste liegt unter `TASKS/repo_followups_2026-10-27.md`.
Beide referenzieren die bestehende öffentliche Basis und offene Arbeit; sie ändern
keinen VOID-, Claim-, Phasen-, Receipt- oder Kanonstatus.

Die Basis `main@83caf03d6e8039637f147f1313238ca5cab611f6` enthält 727 getrackte
Dateien. Zum Eingang wurden zwölf offene PRs und vier offene Issues direkt
abgerufen. Alle zwölf PR-Heads wurden aufgelöst. Die vertiefte technische Arbeit
bezieht sich auf #427/#428/#430; weitere Wartungs- und Forschungsarbeiten bleiben
mit konkretem Abschlusskriterium in der Lesekarte verzeichnet.

## Umgesetzte Folgekorrekturen

| PR | Bereitgestellter Head | Geänderter Vertrag / Nachweis |
|---|---|---|
| [#427](https://github.com/fleksible/entaENGELment-/pull/427) | `e28c1a5a38f13b56f9c115e4f09a6bcc6a4e0d44` | Externe gleiche Basenames erhalten eine Quellen-ID im Payload-Pfad. 67 Reentry-Tests; insgesamt 808 Tests + 165 Subtests. |
| [#428](https://github.com/fleksible/entaENGELment-/pull/428) | `46c4c5c2159de95c628106960dd303b4d21d407f` | Anker-Auswahl benannt; fehlende lokale Inputs erreichen die Skripte ohne vorgeschaltetes get. 29 Korpus-Tests einschließlich echter DataLad-E2E-Läufe; insgesamt 770 Tests + 165 Subtests. |
| [#430](https://github.com/fleksible/entaENGELment-/pull/430) | `6ed3efdec04e18b19615859df5bb0b2b30ace0b0` | Node-Bereich und alter ESLint-Kommentar korrigiert. Fünf erfolgreiche Workspace-Tasks ohne Task-Cache, Root-Jest 66 Tests; Kern 741 Tests + 165 Subtests. |

Die von GitHub erzeugten Git-Trees wurden vollständig mit den lokal getesteten
Trees verglichen, nicht nur einzelne Dateianfänge oder Testzahlen. Die Branches
wurden mit erwarteter alter Head-SHA aktualisiert, ohne Force-Update. Die
PR-Beschreibungen benennen die datierten Nachträge und trennen frühere Testangaben
von den neuen lokalen Ergebnissen.

## Gemeinsame Integrationsprobe

Die vier PR-Stände #427/#428/#429/#430 wurden zusätzlich ausschließlich lokal auf
der genannten main-Basis zusammengeführt. Die Merge-Schritte liefen ohne Konflikt.
Der lokale Integrations-Tree ist
`69866c01199c9e06b4f3706e26887fa5ed01b618`.

- `make verify`: 837 Tests und 165 Subtests bestanden.
- `make verify-governance` und strenger Claim-Lint bestanden.
- Echte DataLad-Probe mit synthetischen Quellen: Klon-Import, README im Annex,
  inerte Git-Steuerdatei, drei gleichnamige externe Quellen, signierter Reentry,
  Verifikation, rerun ohne neuen Commit, fsck und fehlender Inhalt bestanden.
- Python 3.12.14, pytest 9.1.1, DataLad 1.7.1, git-annex 10.20261026,
  pdftotext 24.02.0; für die separate JS-Prüfung Node 24.22.1 und pnpm 10.33.0.

Die lokale Integration ist kein bereits ausgeführter Merge nach main. Die
Head-CI auf GitHub wird gesondert beobachtet; ausgelassene Signing-/Legacy-Jobs
werden nicht aus einem grünen Workflow pauschal als ausgeführt ausgegeben.

## Abgrenzung und offene Abnahme

### Während der Abnahme hinzugekommener Folgestand

Claude ergänzte #427 um
`373ac6e230014f32fb3baee0f542c96268212960`, direkt auf dem oben bereitgestellten
`e28c1a5`. Die Quellen-ID-Zuordnung bleibt erhalten. Neu werden Notiz-Symlinks
ohne Dateiinhalt schon vor der Zielanlage abgewiesen; zwei Regressionen ergänzen
den Stand. Der vollständige kleine Diff wurde gelesen und die Reentry-Suite
erneut ausgeführt: 69 bestanden. Die GitHub-CI dieses Folgestands ist grün.

Die lokale gemeinsame Integration wurde um diesen Commit fortgesetzt:
839 Tests und 165 Subtests sowie Governance bestanden. Der frühere 837er-Lauf
oben bleibt als eigener, zuvor geprüfter Stand erhalten. Der Quellenpfad-Fix
wurde durch den parallelen Folgestand nicht ersetzt.

GOLD, vorhandene Receipts, versiegelte Erststände, private Korpusoriginale und
Remote-/Ankerfreigaben wurden nicht geändert. Die Lesekarte ist keine vollständige
semantische Lektüre aller Dateien und kein universeller Security-Audit.

Der Suchadapter #428 → #426, Desktop-Smoke-Test #432, gezielte Reviews #431/#433,
der konsistente Python-Update-Pfad #435/#416 sowie die menschlichen oder
Account-bezogenen Reste #418/#423, #332 und #305 behalten eigene Abschlusskriterien.

## Anschließende technische Merge-Freigabe

Nach diesem datierten Prüfstand wurde die Übernahme der geprüften grünen PRs
beauftragt. Die acht ausgeführten Code-/Wartungs-Merges, die erneute
Lockfile-Abnahme und die weiterhin offenen Grenzen stehen gesondert in
[2026-10-27_merge_session.md](2026-10-27_merge_session.md). Der kombinierte
Codebestand besteht 859 Tests und 169 Subtests; die frühere Integrationshistorie
oben wird dadurch nicht rückwirkend als derselbe Lauf ausgegeben.
