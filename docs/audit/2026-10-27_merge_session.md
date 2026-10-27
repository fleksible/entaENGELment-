# Merge-Abnahme 27. Oktober 2026

Status: DERIVED / technischer Abschluss vor Übernahme von PR #436.
Ausgangsbasis: `main@83caf03d6e8039637f147f1313238ca5cab611f6`.
Abgenommene Codebasis vor dem Dokumentationsabschluss:
`main@ff340de9d5746af594e51c478e7b762a506550a4`.

## Autorisierter Umfang und Verfahren

Der Owner hat die geprüften, grünen Änderungen im bestehenden Projektumfang zur
Übernahme beauftragt. Offene Bedeutungsentscheidungen und noch nicht ausgeführte
Desktop-Abnahmen bleiben getrennt. Es wurden reguläre Merge-Commits verwendet;
die Herkunftshistorie bleibt erhalten. Jeder Merge war an eine konkret gelesene
Head-SHA gebunden. Keine erzwungenen Ref-Updates oder überschriebenen Statuschecks.

Die fünf geschützten Pflichtkontexte wurden an den betreffenden Heads gelesen:
Pointer-/Lint-Gate, DeepJump-Audit, All Tests Pass, Python Quality und PR-Fokus.
Weitere tatsächlich angelegte Analyse-/Testchecks mussten abgeschlossen sein.
Ausgelassene Signing-/Legacy-Jobs zählen nicht als ausgeführte Prüfungen.

## Ausgeführte Merges

| PR | Tatsächlich übernommener Head | Bestätigter Merge-Commit |
|---|---|---|
| [#429](https://github.com/fleksible/entaENGELment-/pull/429) | `de11de19a6fdd77e447816161c841d98f3b6093e` | `9ab3eb78058e9296b4eb2c1d8068b6f2c4dc2ecf` |
| [#434](https://github.com/fleksible/entaENGELment-/pull/434) | `be93ef7d085715557020de37e0f7899b6b129bf1` | `f3af15638b1b4916e18dc08d20d4f60ddcff4d03` |
| [#425](https://github.com/fleksible/entaENGELment-/pull/425) | `673cbbfbfbf46377af6932daa242f3742378979c` | `e74722673037413378d1ff32a1d3caad1068decf` |
| [#426](https://github.com/fleksible/entaENGELment-/pull/426) | `2e82ff8f3ea552dbd473fe512eedc031b168226b` | `3aa984f637e4022e5f0cc43955cfaded18942d5a` |
| [#427](https://github.com/fleksible/entaENGELment-/pull/427) | `373ac6e230014f32fb3baee0f542c96268212960` | `75e30e6042ca6b068922df3f08aad308c84915b2` |
| [#428](https://github.com/fleksible/entaENGELment-/pull/428) | `46c4c5c2159de95c628106960dd303b4d21d407f` | `af69e360f249817ecc302c3678b4ee13c1bd6096` |
| [#433](https://github.com/fleksible/entaENGELment-/pull/433) | `22727713609563836bf53ab6e03137eba0b98616` | `b72cfd94b6e47da559104c986bce9358e0604c41` |
| [#430](https://github.com/fleksible/entaENGELment-/pull/430) | `d9302f8d1c28a91231c12be10220454948ee7bcc` | `ff340de9d5746af594e51c478e7b762a506550a4` |

#433 wurde zwischen Prüfung und Merge vom Bot auf einen neueren main-Stand
aktualisiert. Der neue Diff blieb bei zwei Dateien und ausschließlich YAML
2.9.0 → 2.9.1; der neue Head wurde nochmals geprüft. Im versionierten eigenen
JS-/TS-Code wurde keine direkte Verwendung der npm-yaml-API gefunden.

## Lockfile-Konflikt von #430

Nach #434 entstand ein tatsächlicher Konflikt zwischen den bisherigen
React-Query-Peerschlüsseln und dem neuen ESLint-Graphen. Die Auflösung erfolgte
mit pnpm 10.33.0. Ein strukturierter Vergleich mit dem bereits geprüften
ESLint-Stand zeigte ausschließlich die inzwischen gemergten Zielversionen
React Query/query-core 5.104.5 und YAML 2.9.1 als zusätzliche Paketwechsel.
Übrige gemeinsame Paketmetadaten, Overrides und Patch-Zuordnungen blieben gleich.

Der neue Head wurde gegen main zusammengeführt und erneut vollständig geprüft.
Vor dem Merge waren auch die zuvor noch laufenden CodeQL-Einzelprüfungen
Python, JavaScript/TypeScript, C/C++ und Actions erfolgreich abgeschlossen.
Es wurde kein laufender Analysejob durch einen administrativen Merge übergangen.

## Gemeinsame Validierung

- Lokales `make verify`: **859 Tests und 169 Subtests bestanden**, einschließlich
  der Suchsuite und echter DataLad-/Annex-End-to-End-Fälle.
- `make verify-governance` und strenger Claim-Lint bestanden.
- Eingefrorene pnpm-Installation und vollständige Turbo-Pipeline bestanden:
  vier Tasks ausgeführt, ein unveränderter Shared-Typecheck aus dem Cache.
- Root-Jest: vier Suites, 66 Tests bestanden.
- DataLad-/Reentry-Proben schließen Import in Klon, inerte Git-Steuerdateien,
  Annex-README, gleichnamige Quellen, Hashabweichung, Missing-/Stale-Fälle,
  signiertes Speichern/Verifizieren, rerun und fsck ein.
- Python 3.12.14, pytest 9.1.1, DataLad 1.7.1, git-annex 10.20261026,
  pdftotext 24.02.0; JS lokal mit Node 24.22.1 und pnpm 10.33.0.
  Dies ist kein behaupteter bytegleicher Nachbau sämtlicher CI-Umgebungen.

Die CI am neuen Dokumentations-Head wird zusätzlich vor dessen Merge geprüft.
Der Merge-Commit von #436 ist im GitHub-PR-Journal belegt; dieser Bericht
enthält absichtlich keinen erfundenen eigenen künftigen Merge-Hash.

## Schutzgrenzen und verbleibende Arbeit

Der vollständige Pfadvergleich gegen die Ausgangsbasis zeigt keine Änderung an
`index/`, `spec/`, `policies/`, `seeds/`, `VOIDMAP.yml` oder den vorhandenen
Receipt-Bereichen. Der öffentliche versiegelte Reentry-Erststand ist bytegleich
zum geprüften #427-Eingang erhalten. Private Originale, Einzelhash-Inventare,
Remotes und öffentliche Anker wurden nicht durch den Merge angelegt.

| Offen | Konkreter Grund |
|---|---|
| #423 / #418 | Phasenbedeutung und Sample-/Boundary-Zuordnung bleiben eine menschliche Entscheidung; grüne Replay-Tests wählen das Modell nicht. |
| #431 | Packaging-/Collector-Pfade des Builder-Updates benötigen einen konkreten Paketnachweis. Allgemeine grüne CI ersetzt diesen Nachweis nicht. |
| #432 | Echter Start des gepackten Electron-45-Artefakts unter aktiver Sandbox fehlt. |
| #435 / #416 | Aktuelle Pflichtchecks rot; Export-/Lock-Drift und Safety-Abhängigkeitskonflikte. Kein Bypass des Drift-Gates. |

Der Korpus-Suchadapter, Account-/Empfangstest #332 und Forschungsgrundlagen #305
bleiben weitere eigene Arbeitspakete der Aufgabenliste. Die technischen Merges
erzeugen keinen empirischen Befund, keine Phasenwahl und keinen Kanonstatus.
