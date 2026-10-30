# Gezielter Pilot: Arbeitsstatus, Abschluss und Architekturentscheid

**Datum:** 2026-10-30  
**Fokus:** Drei unterschiedliche Entscheidungsarten  
**Status:** DERIVED / REVIEW-PENDING; keine Statusänderung und keine Kanonpromotion

## Maßstab und Kontaktstand

Es gelten die [Pilotkriterien](2026-10-30_pilot_criteria.md). Deren SHA-256 wurde
vor den neuen fachlichen Läufen festgehalten:
`50270199ec13142923acfceb6b24b02fa96c064a4b32d56a5b77d4a2c8fd4528`.
Die Fälle und Teile ihrer Begründungen waren bereits bekannt. Das ist kein
Blindtest, keine statistische Stichprobe und keine neue Grundgesamtheit.

Die folgenden Ergebnisse sind Teilurteile. Reproduzierbarkeit, Angemessenheit
eines Closing Path, Autorisierung und menschliche Beobachtung werden getrennt.

## VOID-027: OPEN → IN_PROGRESS

- **Ursprüngliche Aussage:** partielle HUD-Implementierung rechtfertigt
  IN_PROGRESS; CLOSED bleibt ausdrücklich ausgeschlossen.
- **Direkter Anker:** `VOIDMAP.yml` am Integrationscommit
  `2163a8bd1bfc7270b797bfb202414c8ad0ccc8da`, PR #320. Alle sechs dort genannten
  Quell-, Fixture-, Test- und README-Pfade existieren an dieser Revision.
- **Gegenbeobachtung/Scope:** Der Closing Path verlangt zusätzlich unter anderem
  1xn-Slice, Apex, kalibrierte Achse, Entscheidungsleiste und Receipt-Link. Die
  Registry und der PR weisen diese Komponenten als offen aus.
- **Teilurteil:** NACHVOLLZIEHBAR als begrenzte Arbeitsstatusaussage. Eine
  vollständige Umsetzung oder ihre Runtime-Qualität ist damit nicht validiert.
  Die historischen UI-Tests wurden in diesem Piloten nicht erneut ausgeführt.
- **Menschlicher Entscheid:** Die ursprüngliche Freigabe ist hier nicht als
  menschlicher Originalturn gelesen worden; diese Teilfrage bleibt LÜCKENHAFT.
  Der PR-Account oder der Merge allein ergänzt diesen Nachweis nicht.

## VOID-011: IN_PROGRESS → CLOSED

### Was neu ausgeführt wurde

| Stand | Export `--check` | Export-/Core-5-Tests | Bedeutung |
|---|---|---:|---|
| Schließung `e74cd6f956959f62c3147cf4f210783bb29a5511` | Exit 0, Up to date | 25 bestanden | damalige Exportbytes aus damaligem Code in der lokalen Python-Umgebung reproduzierbar |
| main `3b72b9db7da703e2f3c90bd3d69c4cdfb5e37bec` | Exit 0, Up to date | 27 bestanden | heutiger Export einschließlich späterer Ergänzungen reproduzierbar |

Die 37 gemeinsam ausgeführten gezielten Tests am Arbeitsstand enthalten diese
27 Metriktests plus zehn neue Lockfile-Diff-Tests. Sie sind keine 37 unabhängigen
Evidenzkanäle. Laufumgebung: CPython 3.12.14, pytest 9.2.0. Es wird weder eine
vollständig lock-identische CI-Umgebung noch Plattformunabhängigkeit behauptet.

Der Export am Schließungsstand enthält 30 SIMULATION_PROXY-Zeilen, festen Seed,
Konfiguration, Claim-Grenze und CSV-Hash. `source_sha256`, MI_BASELINE und MI_EXCESS
kamen später hinzu. Die heutige Ausgabe darf nicht rückwirkend als damalige
Abnahmegrundlage ausgegeben werden.

### Was Issue #311 tatsächlich belegt

Der direkt gelesene Issue-Body ist ein automatisch erzeugter Overdue-Hinweis.
Die vollständige abgerufene Kommentarseite enthält zwei Kommentare:

- 2026-07-29 12:39:18Z: IN_PROGRESS, keine Entscheidung und keine Schließung.
- 2026-09-30 07:36:18Z: bestehende Toy-Metriken reichen noch nicht für den
  deterministischen SIMULATION_PROXY-Nachweis.

Ein Owner-OK vom 18. Oktober steht dort nicht. Der Issue wurde am 18. Oktober
04:11:49Z automatisch durch PR #407 geschlossen. Der Commit, die PR-Beschreibung
und der Auditbericht berichten eine Ownerauswahl, sind aber nicht der gesuchte
menschliche Originalturn. Damit ist weder das Fehlen jeglicher Freigabe bewiesen
noch geklärt, ob eine Freigabe die fertige Erfüllung oder deren Ankündigung sah.
Diese Teilfrage bleibt **LÜCKENHAFT**.

Quellen: [Issue #311](https://github.com/fleksible/entaENGELment-/issues/311),
[PR #407](https://github.com/fleksible/entaENGELment-/pull/407).
Der GitHub-Accountname belegt keine menschliche Direktbeobachtung; mehrere
Antworten dieses Accounts weisen sich ausdrücklich als Claude-Code-generiert aus.

### Closing Path und bereits vorhandene Gegenlese

Die historische VOID-Doku verlangt stabilen Toy-Export, SIMULATION_PROXY und
deterministische Tests. Diese schmale technische Aussage ist durch die neuen
Läufe NACHVOLLZIEHBAR. Der weitergehende Plan in
`docs/audit/ISSUE_APPROACHES_2026-09-23.md` fordert zusätzlich eine Code-Revision;
er ist dort als MODEL-Vorschlag markiert. Seine normative Übernahme wird hier
nicht still unterstellt. Am Schließungsstand fehlte die stabile Codebindung;
PR #408 ergänzt sie. Der entsprechende
[Reviewbefund](https://github.com/fleksible/entaENGELment-/pull/407#discussion_r4305679175)
und die spätere Antwort sind direkt gelesen worden.

Die vorhandene [Gegenlese vom 23. Oktober](2026-10-23_gold_pr407_408_gegenlese.md)
§4.1 und §5 behandelt bereits FD-Referenz, MI-Bias, fehlende unabhängige
Ownerquelle und weitere Grenzen. Sie wird als berichteter früherer Prüflauf
verwendet; ihre Resultate werden nicht pauschal als hier erneut ausgeführt
ausgegeben. Sie ist kein unabhängiger menschlicher Readback. Die neue
Neuberechnung bestätigt Reproduzierbarkeit, nicht allgemeine Metrikvalidität.

### FD-Beifang: enger Such- und Reproduktionsbefund

Der FD-Fix ist Commit `80372e56a00e5b4bfa50515dafd28f77f2b46573`.
Die alte Funktion aus dessen Elternstand und die heutige Funktion wurden auf
gleichen Eingaben ausgeführt:

| Eingabe | vor Fix | nach Fix |
|---|---:|---:|
| weißes Rauschen, Python-Random-Seed 42, n=512 | 1.0 | 1.9981721359 |
| Random Walk, gleicher Seed, n=512 | 1.0 | 1.5145631457 |
| Toy-Signal a, Seed 7, n=256, Kopplung 0.1 | 1.0 | 1.0086202072 |
| Toy-Signal a, Seed 42, n=256, Kopplung 0.1 | 1.0 | 1.0064356906 |

Die historischen Tests prüfen float, Gerade nahe 1 und den geklemmten
Wertebereich. Diese Prüfungen unterscheiden den alten Fehler nicht zuverlässig
von der korrigierten Funktion. Der Funktionsverlauf nennt die Implementierung
bereits im Commit `d213e97` vom 13. März; die Registry-Notiz vom 4. April ist
kein Beleg für einen erst dort beginnenden Implementierungszeitraum.

Die begrenzte Repo-Suche umfasste FD/Higuchi-Nennungen im aktuellen getrackten
`src`, `tools`, `tests`, `docs`, `OUT` und `VOIDMAP.yml` (ohne importierte
Korpus-Rohkopien), die fd-Aufrufstellen im Elternstand des Fixes sowie die
Funktionshistorie. Dort ist der Toy-Generator der einzige direkte
Produktivcode-Aufrufer der alten fd-Funktion. Reexports und Tests sind getrennt.

Damit ist eine echte Schwäche der damaligen Testabdeckung reproduziert. Ein
Statusentscheid oder ein empirischer Claim, der auf den falschen FD-Zahlen
beruhte, ist durch diese Suchabdeckung **nicht nachgewiesen**. Private Chats,
externe Ausführungen, dynamische Aufrufe und alle historischen Textfassungen
sind damit nicht vollständig abgedeckt. Ein solcher Durchrutsch-Fall bleibt ein
gezielter Suchauftrag; die Implementierungsdauer allein schließt ihn nicht.

## ADR-0001: Proposed → Accepted

- **Direkter Anker:** Änderung in `1c2852d8685deb99e3e57d52868f7c7e0300f069`,
  PR #377 und die ADR selbst. Sie schreiben die Annahme „R5 umsetzen“ Kevin/Fleks
  zu. Der PR weist sich als Claude-Code-generiert aus.
- **Gegenstand:** bestehendes `docs/audit/` beibehalten, kein zweites
  `docs/audits/` anlegen. Die Entscheidung beansprucht keine wissenschaftliche
  Wahrheits- oder VOID-Promotion.
- **Technischer Teil:** NACHVOLLZIEHBAR als vorhandene Ablagekonvention;
  `git check-ignore docs/audit/new.md` gibt Exit 1, der Pfad ist nicht ignoriert.
- **Autorisierung:** LÜCKENHAFT im direkt gelesenen Material. Der ursprüngliche
  menschliche R5-Turn wurde hier nicht gelesen. Eine berichtete Annahme und das
  Accepted-Feld dürfen nicht gegenseitig ihre einzige Beglaubigung sein.

## Ergebnis und Grenzen

Es wurden weder VOID-Status noch ADR, Policy, GOLD oder Receipts geändert.
Insbesondere erzeugt diese Prüfung keinen nachträglichen human_witness und
keine rückdatierte Freigabe. Ein heutiger menschlicher Readback könnte den
heutigen Entscheid dokumentieren; er würde nicht beweisen, was am 18. Oktober
bereits vorlag oder gesehen wurde.

Die Arbeit liefert drei unterschiedlich begrenzte Fallprüfungen und den
separaten [Lockfile-Granularitätsvektor](2026-10-30_lockfile_scope_erratum.md).
Sie ist keine Häufigkeitsmessung von Fehlpromotionen und kein Wirksamkeitsbeweis
für eine ganze Governance-Architektur.
