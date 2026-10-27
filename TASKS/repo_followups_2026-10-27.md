---
id: TASK-REPO-FOLLOWUPS-2026-10-27
title: Repo-Struktur und technische Folgeaufgaben
status: ACTIVE
created: 2026-10-27
updated: 2026-10-27
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

## Technische Abnahme / nächste Arbeit

- [x] Korrekturen in die bestehenden PR-Branches bringen; neue Head-CI abgerufen.
- [ ] Aktuelle Head-CI vollständig grün abnehmen; lokale Prüfungen ersetzen sie nicht.
- [ ] Kleine Korrektur-Diffs und diese Karte reviewen; Merge-Entscheidungen
  betreffen den jeweiligen konkreten Umfang.
- [ ] #429/#434 als getrennte Wartungs-Merge-Kandidaten abnehmen.
- [ ] #431/#433 anhand ihrer tatsächlichen Builder-/Parser-Verwendungen prüfen.
- [ ] #432 als gepackte Desktop-App unter aktiver Sandbox starten; UI-Build
  und Glob-Test nicht als Paketstart ausgeben.
- [ ] #435 über #416: kompatible Updates im uv-Lock auflösen, Exporte gemeinsam
  regenerieren; Safety-Konflikte nicht durch manuelle Exportänderungen übergehen.
- [ ] #428 → #426: privates Suchmanifest mit getrennten Original-/Textidentitäten,
  Hashes, Methode, Lesestand und Verlustgrenze erstellen und synthetisch prüfen.

## Begründet offen

- [ ] #418/#423: menschliche Bedeutung der Phase und Sample-/Boundary-Zuordnung.
  Keine automatische Auswahl aus einem bestandenen Toy-Replay.
- [ ] #332: verbleibende Settings und echter privater Empfangstest. Dieser Auftrag
  enthält keinen Versand eines Testberichts an andere Personen.
- [ ] #305: Originalscanner/Rohlisten und operationalisiertes Nullmodell fehlen
  als Grundlage einer neuen Forschungsprüfung; keine Zahlensignatur kanonisieren.

## Grenzen

Keine Umsortierung bestehender Module, keine Löschung, keine Änderungen an GOLD,
Receipts oder vorhandenen versiegelten Save States. Private Korpusdaten, Remotes
und öffentliche Anker sind keine impliziten Nebenprodukte der technischen Arbeit.
