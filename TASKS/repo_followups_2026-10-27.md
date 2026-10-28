---
id: TASK-REPO-FOLLOWUPS-2026-10-27
title: Repo-Struktur und technische Folgeaufgaben
status: ACTIVE
created: 2026-10-27
updated: 2026-10-28
assignee: Codex
priority: high
---

# Repo-Struktur und technische Folgeaufgaben

FOKUS: Struktur und bestehende Folgekorrekturen

Diese Arbeitsliste referenziert bestehende PRs/Issues. Sie ersetzt weder VOIDMAP
noch deren Statusregister und autorisiert keine Kanonpromotion. Ein Haken unter
"lokal erledigt" bedeutet keinen bereits ausgeführten Merge.

## Lokal erledigt

- [x] Öffentliche Basis und alle zwölf offenen PR-Heads auflösen; vier offene
  Issues und die vorhandenen Review-Ergebnisse als Eingänge erfassen.
- [x] Strukturelle Lesekarte als DERIVED / REVIEW-PENDING im Intake ablegen.
- [x] #427: externe gleiche Dateinamen über Quellen-ID trennen, vier Regressionen.
- [x] #428: Dotdatei-/Ankerumfang explizit machen und im echten DataLad-Lauf
  gefundenen Abbruch vor der Missing-Protokollierung beheben.
- [x] #430: Node-Vertrag und veralteten ESLint-Pin-Kommentar korrigieren;
  komplette lokale JS/TS-Pipeline besteht.
- [x] Gemeinsamer synthetischer DataLad-/Reentry-Lauf: Klon, Import, Extraktion,
  Inventar, signierter Save, Verifikation, rerun, fsck und fehlende Eingabe.
- [x] Claudes späteren #427-Folgestand `373ac6e` mitgelesen und nachgetestet:
  69 Reentry-Tests; gemeinsame Integration 839 Tests und 165 Subtests bestanden.

## Technische Abnahme / nächste Arbeit

- [x] Korrekturen in die bestehenden PR-Branches bringen; neue Head-CI abgerufen.
- [x] Aktuelle Code-PR-Heads vollständig grün abnehmen; lokale Prüfungen ersetzen sie nicht.
- [x] Korrektur-Diffs und Karte technisch reviewen; Owner-Freigabe für die
  geprüften grünen Merges liegt vor. Dies ist keine Claim-Promotion.
- [x] #429/#434 getrennt abnehmen und mergen.
- [x] #433 nach Bot-Aktualisierung erneut prüfen und mergen.
- [x] #425/#426/#427/#428/#430 übernehmen; kombinierter Stand besteht 859 Tests
  und 169 Subtests sowie die relevanten JS-/Governance-Gates.
- [x] #431: reales AppImage mit Builder 26.18.0 gebaut; implizites
  `--no-sandbox` im Launcher behoben. Gepackter 44.9.1-Start unter aktiver
  Sandbox in CI belegt und als `5ee665a` gemergt.
- [x] #432: gepackter Electron-45.0.0-Start separat mit aktivem Renderer-Seccomp,
  NoNewPrivs und Isolation in Job 122754144129 belegt. Endgültige Head-CI und
  Merge-Status stehen im [PR-Journal](https://github.com/fleksible/entaENGELment-/pull/432).
- [x] #435: vier kompatible Updates im uv-Lock aufgelöst, Exporte regeneriert,
  aktuelle CI grün; als `e0c3781` gemergt. Drei inkompatible Ziele bleiben HOLD.
- [ ] #428 → #426: privates Suchmanifest mit getrennten Original-/Textidentitäten,
  Hashes, Methode, Lesestand und Verlustgrenze erstellen und synthetisch prüfen.

## Begründet offen

- [ ] #416: dauerhafter konsistenter Dependabot-/Export-Pfad; die erfolgreichen
  manuellen Korrekturen beweisen keine reparierte Updater-Automation.
- [ ] Safety-Kompatibilität: filelock 4.1.0, safety-schemas 0.0.21 und
  typer 0.27.3 bleiben aufgrund belegter Resolver-Konflikte HOLD.
- [ ] #418/#423: menschliche Bedeutung der Phase und Sample-/Boundary-Zuordnung.
  Keine automatische Auswahl aus einem bestandenen Toy-Replay.
- [ ] #332: verbleibende Settings und echter privater Empfangstest. Dieser Auftrag
  enthält keinen Versand eines Testberichts an andere Personen.
- [ ] #305: Originalscanner/Rohlisten und operationalisiertes Nullmodell fehlen
  als Grundlage einer neuen Forschungsprüfung; keine Zahlensignatur kanonisieren.

## Grenzen

Die ausgeführten Code-/Wartungs-Merges und ihre tatsächlichen Commit-IDs stehen
in [der Merge-Abnahme](../docs/audit/2026-10-27_merge_session.md). Die Übernahme
dieses Dokumentationsabschlusses ist im Journal von PR #436 nachvollziehbar.

Der technische Nachlauf vom 28.10. ist in den Audits zu
[#435](../docs/audit/2026-10-28_pr435_python_lock_repair.md),
[#431](../docs/audit/2026-10-28_pr431_desktop_package.md) und
[#432](../docs/audit/2026-10-28_pr432_electron45.md) belegt. Die Paketabnahme
betrifft Linux-Payload unter Xvfb; sie ist keine vollständige Plattform- oder
WebGL-/Audio-/CDN-Abnahme.

Keine Umsortierung bestehender Module, keine Löschung, keine Änderungen an GOLD,
Receipts oder vorhandenen versiegelten Save States. Private Korpusdaten, Remotes
und öffentliche Anker sind keine impliziten Nebenprodukte der technischen Arbeit.
