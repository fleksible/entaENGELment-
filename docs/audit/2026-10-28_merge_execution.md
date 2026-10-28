# Merge-Abnahme der vier geprüften Pakete · 28.10.2026

**FOKUS:** Begrenzte Fixes nach Gegenprüfung übernehmen
**Status:** DERIVED / MERGE-REVIEW; generated_review
**Authority-Status:** ANNEX
**Scope:** PRs #438, #439, #440 und #441 in fleksible/entaENGELment-.

## Freigabe und Bedeutung

[FAKT] Der Nutzer hat nach dem konkreten Review-Vorschlag die Bereinigung und
Übernahme „wie besprochen“ ausdrücklich beauftragt. Das umfasst die vier
benannten Pakete, ihre dokumentierten Verhaltensänderungen, die dafür nötige
Branch-Integration, CI-Prüfung und diesen Audit-Nachweis.

[FAKT] Die Freigabe übernimmt keine neuen GOLD-Regeln, Standards oder
Consent-Protokolle. Die Konzeptnotizen bleiben ANNEX-Entwürfe. Ein Code-Merge
erzeugt keinen empirischen Nachweis der Projektmodelle und keine Kanonisierung.

## Eingänge und bisherige Merges

Die ursprüngliche geprüfte main-Basis ist
`e8bea51be1e1787e6cb654d666e7231512cf2f1d`.

| Paket / PR | geprüfter veröffentlichter Eingang | übernommener Head | Merge nach main |
|---|---|---|---|
| Paket 1 / #438 | `89bc3da960b422fb7c28a777ade140e5b2020850` | identisch | `c021ac60066394191ede66ca9b76ce212b09ea24` |
| Paket 2 / #439 | `f1bd24ea8dffdc25c2d3ae6e5620a0d5465e1cde` | identisch | `518a781eed6235aeab12d49409cfaf70507f91b6` |
| Paket 4 / #440 | `b9d1a66bbe4eba6b79099f55245b0a2d4ac57f59` | `e62600b916ab1ff92308ecf5dbe9bfcdca65d344` | `7abef87625abe4e228fe8a6ab30583af111af8ba` |
| Paket 3 / #441 | `7962f48b57b7e8ea24f35e154826c76a85acacd8` | Integration der ursprünglichen Änderungen und dieses Nachweises | folgt erst nach neuer grüner CI; endgültige SHA im PR-Merge-Ereignis |

[FAKT] #439 und #440 enthalten den nachgeprüften P1-Head. Beim Merge von #439
gegen main nach #438 entstand exakt dessen bereits geprüfter Tree
`ed3cb332c85f48c24e11df6f8e6a1f2f2aa2123a`.

[FAKT] #440 wurde ohne Force-Update mit main nach #439 integriert. Gegen diese
Basis blieben genau die fünf ursprünglichen P4-Dateien. Der neue Tree
`0814a5a8bcf90b8c1438a2119dabcc70ffeae9ca` ist identisch mit dem lokal
berechneten Merge-Tree; alle fünf erforderlichen Checks des neuen Heads waren
vor dem Merge erfolgreich, kein Job war mehr laufend oder fehlgeschlagen.
Es gab keine neue Lock-Auflösung.

[FAKT] Reihenfolge: #438 → #439 → #440 → #441, jeweils mit Merge-Commit.
Die letzten beiden Paketnummern sind absichtlich 4 und 3.

## Frische gemeinsame Gegenprüfung

[FAKT] Die vier ursprünglichen PR-Inhalte wurden lokal konfliktfrei auf
`2f5016bc629d5ad9ac584a4c874c2b7412eb7574`, Tree
`0bba9db433430f7a99d6d9b753e93cf7f97a142d`, zusammengeführt und frisch geprüft.
Dies ist ein lokaler Prüf-Commit, keine veröffentlichte Produktversion.
Dieser Audit-Nachweis kommt als einzige weitere Datei hinzu.

Die Umgebung wurde über `python tools/python_lock.py sync --group dev` mit
exakt uv 0.12.18 aufgebaut: Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1,
Hypothesis 6.170.12, pytest 9.1.1.

| Prüfung | Ergebnis |
|---|---|
| `make verify` | **1126 passed, 2 skipped, 169 subtests passed**; Ports, Pointer und Claims bestanden |
| `make verify-governance` | 16 Workflows bestanden; 22 VOIDs synchron |
| `ruff check src/ tools/ tests/` | bestanden |
| `black --check src/ tools/ tests/` | bestanden; 125 Dateien unverändert |
| `mypy src/ tools/` | bestanden; 58 Quelldateien |
| `bandit -c .bandit.yaml -r src/ tools/` | keine Findings in der konfigurierten Prüfung |
| `python tools/python_lock.py check` | bestanden |
| `make demo` ohne Secret | PASS (UNSIGNED), signature not verified |
| `make demo` mit ausschließlich lokalem Testschlüssel | Signatur erfolgreich geprüft |
| sechs Python-/JavaScript-Byte-Vektoren | alle dokumentierten Hash-Paare erneut reproduziert; Node v24.22.1 |

[FAKT] In den lokalen zwei Skips fehlen DataLad/git-annex. In den zuvor gelesenen
GitHub-Runtime-Jobs gab es einen weiteren Skip wegen fehlendem pdftotext.
Lokaler Gesamtlauf und GitHub-Einzelläufe werden nicht als derselbe Lauf gezählt.
Die sechs Byte-Vektoren sind ein gezielter Abgleich, kein allgemeiner
Interoperabilitäts- oder Standardkonformitätsnachweis.

## Abschlusskriterium für #441

[FAKT] Gegen main nach #440 bleiben die ursprünglichen 13 Doku-/Test-Dateien von
#441 einschließlich der korrigierten Demo-Ausgabe sowie diese Audit-Datei.
Die Zusammenführung in CHANGELOG.md erhält beide bestehenden Ergänzungen.

Vor dem letzten Merge müssen auf dem veröffentlichten Integrations-Head
DeepJump-Audit, Pointer/Lint, All Tests Pass, Python-Qualität und FOKUS-Guard
erfolgreich sein. Zusätzlich werden laufende und fehlgeschlagene Jobs geprüft.
Danach wird der erreichte main-Tree mit diesem freigegebenen Tree abgeglichen;
die main-CI wird gesondert kontrolliert. Dieser vor dem letzten Merge verfasste
Nachweis behauptet dessen späteres Ergebnis nicht vorab.

## Erhaltene Restgrenzen

- [UNRESOLVED] B9 bleibt für explizite Matrix-only-Zugänge, extern geschätzte
  Matrizen und falsche deklarierte Fehler-/Funktionsannahmen offen.
  Der Snapshot ist ein Konsistenzcheck, keine Grenze gegen Code im selben Prozess.
- [FAKT] Core behält 1e-6, MOD_18 1e-8. Übereinstimmende Blockierentscheidungen
  sind nur bei gleicher Toleranz geprüft.
- [FAKT] B3 bleibt mit NotImplementedError vorläufig stillgelegt.
  Ein Ersatz braucht Zielgröße, Beobachtungseinheit, H0 und Austauschbarkeit.
- [FAKT] Bei einem IO-Abbruch kann eine Ledger-Teilzeile bleiben; der
  In-Memory-Zustand bleibt unverändert, die Dateiprüfung erkennt den Defekt.
- [FAKT] Properties prüfen ihre formulierten Invarianten. Die vorliegenden
  Testläufe sind kein allgemeiner Sicherheitsbeweis.
- [FAKT] Signatur-, Consent-, Trust-Ableitungs-, Scope- und Widerrufsnotizen
  implementieren keine neuen Protokolle. Offene Empfänger-/Ressourcenbindung und
  Trust-Ableitung bleiben offen; geometrisches STABLE ist keine Einwilligung.
- [FAKT] Kein GOLD-, Receipt-, NICHTRAUM- oder negations.md-Pfad ist im
  übernommenen kombinierten Diff geändert; keine Dateien oder Branches gelöscht.

## Herkunft

- [Gegenprüfung am gepinnten Audit-Stand](https://github.com/fleksible/entaENGELment-/blob/2e66db7a6e3f1c13760a34a174f9d046a4c77372/docs/audit/2026-10-28_followup_review.md).
  Der historische Audit-PR #437 wird durch diese vier Merges nicht automatisch
  mit übernommen; der gepinnte Nachweis bleibt getrennt referenziert.
- [#438](https://github.com/fleksible/entaENGELment-/pull/438),
  [#439](https://github.com/fleksible/entaENGELment-/pull/439),
  [#440](https://github.com/fleksible/entaENGELment-/pull/440),
  [#441](https://github.com/fleksible/entaENGELment-/pull/441):
  Original-Diffs, veröffentlichte Git-Objekte und GitHub-Checks gelesen.
- Die technischen Ergebnisse dieses Nachweises wurden im aktuellen Merge-Lauf
  selbst geprüft. Historische Messungen und ihre Gegenproben bleiben an die
  jeweils dort benannten Stände gebunden.
