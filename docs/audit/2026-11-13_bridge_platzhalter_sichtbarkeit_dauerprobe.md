# Prüfbericht: Platzhalter-Sperre, erklärte Sichtbarkeit und Dauerprobe am Kernel

**Datum:** 2026-11-13 · **Status:** ANNEX / DERIVED · Technischer Prüfbericht zu PR #470

**FOKUS:** Leere Angaben fail-closed halten

**Promotion-Effect:** none

[ANNEX] Der ursprüngliche Bericht dokumentiert den Stand `eda36d6` und den
damaligen Draft-Auftrag. Die Nachprüfung und der anschließende ausdrückliche
Anpassungs- und Mergeauftrag stehen unten im Nachtrag. Die dort beschriebene
Ausgabesperre ersetzt die ursprüngliche Grenze der bloßen Kennzeichnung.

## Auftrag und Grenze

[ANNEX] Begrenzter Umsetzungsauftrag in drei Teilen, ausgeführt auf dem
bestehenden [Bridge-Adapter](../annex/DUAL_FORMAT_CLAIM_BRIDGE_ADAPTER_v0_1.md),
der [Bridge-View](../annex/BRIDGE_VIEW_v0_1.md), der
[Stichwortsuche](../annex/CORPUS_SEARCH_v0_1.md) und dem Evidence Routing
Kernel v0.1a:

1. Platzhalter in `known_loss` und `falsifier` werden fail-closed behandelt.
2. Eine am Korpus erklärte Sichtbarkeit bleibt im Suchindex erhalten.
3. Eine zustandsbehaftete, reproduzierbare Probe prüft Antrag, Freigabe,
   Widerruf und Statusübergänge gegen die produktive Implementierung.

[FAKT] Keine neue Schemafamilie, keine neue Abstraktionsschicht, kein neuer
Reason-Code. GOLD, Policies, Seeds, VOIDMAP, Receipts, Ledger-Dateien und
JS-/UI-Dateien sind unverändert. `src/core/evidence_routing.py` ist
unverändert (Blob `2be8e91f843c` vor und nach). Am ursprünglichen Stand kein Merge, keine
Statuspromotion, keine HumanDecision, kein Claim-Retagging. Alle Fixtures sind
synthetisch; der Diff wurde gegen 224 Merkmale der privaten Übergabetexte
geprüft, ohne Treffer.

[ANNEX] Nicht Teil dieses Auftrags und unberührt: RCC-8-Neueinstufung und
Exit-Kriterien der Wesenheit. Beide bleiben Owner-Entscheidungen auf HOLD.

## Basis, Head und Umgebung

| Gegenstand | Stand |
| --- | --- |
| Basis `main` | `d489c2876b18dfe5d620ed08d10481185ea2b112` |
| Commit 1, nur Gegenfälle (rot am Ausgangsstand) | `d24792cddad87746f8cbb13be1ce2e0ec4a7fded` |
| Commit 2, Fix und Verträge | `2dae06c01bf73986ac83c92446dfe93e1d86193b` |
| Commit 3, Dauerprobe (geprüfter Code-Commit) | `eda36d674f6b8fdead53aac1cf473ab867e85876` |
| `src/core/evidence_bridge_adapter.py` | Blob `912e1062375d` → `27c9f9a56197` |
| `src/core/bridge_view.py` | Blob `cae6af343b4a` → `7b138e9da948` |
| `tools/corpus_search.py` | Blob `fd481017f972` → `ddb2c8ca7ac8` |

[FAKT] Umgebung: Linux, Python 3.13.18, Abhängigkeiten aus `uv.lock` mit
uv 0.12.18 in einer Umgebung außerhalb des Repos, pytest 9.1.1,
hypothesis 6.170.12. Die fünf berührten Testdateien liefen zusätzlich unter
Python 3.11.16 und 3.12.14. Die Vollsuite lief nur unter 3.13.18.

[ANNEX] Dieser Bericht kommt in einem Folgecommit hinzu, der keinen Code und
keinen Test ändert.

## Ausgangsbefund

[FAKT] **Platzhalter.** Am Ausgangsstand prüfte der Adapter bei `known_loss`
und `falsifier` nur, ob Text vorhanden ist. `known_loss: ["keiner"]`,
`["n/a"]`, `["-"]` oder `["unbekannt"]` galten als benannter Verlust,
`falsifier: "TBD"` als benannter Falsifikator. Eine Brücke konnte damit die
beiden Pflichtfelder formal erfüllen, ohne etwas zu benennen. Die Bridge-View
zeigte solche Einträge als Verlustzeile an.

[FAKT] **Sichtbarkeit.** `tools/corpus_search.py` übernahm aus einem
Korpus-Eintrag nur ihm bekannte Felder. Ein Feld `visibility` und jedes andere
unbekannte Feld fiel beim Indexbau kommentarlos weg: Es stand weder im Manifest
noch im Index noch im Suchergebnis. Eine als privat erklärte Quelle war im
Ergebnis nicht mehr von einer unmarkierten zu unterscheiden.

[FAKT] **Kernel.** Kein Fehler als Ausgangsbefund. Die Dauerprobe besteht am
unveränderten Kernel. Der Befund ist eine Testlücke: Die vorhandenen 239 Tests
in `test_evidence_routing.py`, `test_erk_tools.py` und
`test_evidence_bridge_adapter.py` bemerken es nicht, wenn im Replay die Prüfung
entfällt, dass die zitierte Entscheidung eine Freigabe ist (R1) oder zum
selben Antrag gehört (R11).

## Reproduzierende Gegenfälle

[FAKT] Die Gegenfälle zu Teil 1 und 2 stehen in einem eigenen Commit vor dem
Fix. Am Stand `d24792c` (Tests neu, Code alt) und am Stand danach, jeweils
`tests/unit/test_evidence_bridge_adapter.py`, `test_bridge_view.py`,
`test_corpus_search.py`:

| Stand | Ergebnis |
| --- | --- |
| `d24792c`, vor dem Fix | 43 fehlgeschlagen (einschließlich Teilfällen), 173 bestanden |
| `eda36d6`, nach dem Fix | 212 bestanden, 0 fehlgeschlagen |

| Gegenfall | Fälle rot vor dem Fix |
| --- | --- |
| Füllwort oder verneinter Verlust in `known_loss` (`keiner`, `verlustfrei`, `zero leakage`, `n/a`, `-`, `TBD` …) | 15 |
| „unbekannt“ als Verlust; Meldung muss das Erfinden ausdrücklich untersagen | 6 |
| Platzhalter neben einem benannten Verlust | 1 |
| Platzhalter als `falsifier` | 8 |
| Übersetzung liefert keinen Verlust und keinen Falsifikator nach | 1 |
| Derselbe Maßstab über den Mapping-Eingang | 1 |
| Bridge-View zeigt keinen Platzhalter als Verlust | 4 |
| Erklärte Sichtbarkeit steht in Manifest, Index und Suchergebnis | 1 |
| Unbekanntes Korpus-Feld bricht ab und nennt nur Position und Feldnamen | 1 |
| Sichtbarkeit, die kein Text ist, wird abgewiesen | 4 |
| Suche liest einen Index ohne Sichtbarkeitsspalte | 1 |

[FAKT] Gegenproben in die andere Richtung, vor und nach dem Fix grün: Sätze,
die ein Platzhalterwort nur enthalten, bleiben gültig („Kalibrierung offen“,
„Weitere Verluste sind unbekannt“). Derselbe Datensatz mit widersprüchlicher
Sichtbarkeit wird weiterhin als Duplikat abgewiesen und nicht zusammengelegt.

## Was geändert wurde

[FAKT] Produktivcode: 3 Dateien, 182 Zeilen hinzu, 5 entfernt. Tests:
4 Dateien, 873 Zeilen hinzu. Verträge: 3 Dateien, 48 hinzu, 2 entfernt.

**`src/core/evidence_bridge_adapter.py`.** Neue Funktion
`placeholder_kind(value)`: Der Eintrag wird Unicode-normalisiert (NFKC),
kleingeschrieben, von Leerraum und Randzeichen befreit und als Ganzes mit zwei
geschlossenen Listen verglichen. Ergebnis `"filler"` (46 Formeln wie `keiner`,
`n/a`, `tbd`, `verlustfrei`; außerdem jeder Eintrag ohne Buchstaben oder
Ziffern), `"unknown"` (20 Formeln wie `unbekannt`, `unklar`, `offen`, `k.A.`)
oder `None`. `validate_bridge_record` weist beide Arten mit den bestehenden
Codes `KNOWN_LOSS_REQUIRED` und `FALSIFIER_REQUIRED` ab. Bei `"unknown"` sagt
die Meldung, dass die Brücke unübersetzt bleibt, bis der Verlust benannt
werden kann, und dass kein Eintrag erfunden werden soll, um die Prüfung zu
bestehen.

**`src/core/bridge_view.py`.** Die View verweigert die Projektion, wenn ein
`known_loss`-Eintrag ein Platzhalter ist; sie benutzt dieselbe Funktion.

**`tools/corpus_search.py`.** `load_corpus_entries` prüft das Korpus, bevor
ein Ausgabeordner entsteht. Ein unbekanntes Feld bricht den Bau ab; die
Meldung nennt Eintragsposition und Feldnamen, keinen Wert, Titel oder Pfad.
`visibility` ist ein erlaubtes Feld, muss nichtleerer Text sein und wird
wörtlich in Manifest, Index (neue Spalte) und Suchergebnis getragen. Fehlt die
Angabe, steht dort `null`: nicht erklärt, nicht „öffentlich“. Ein älterer
Index ohne die Spalte bleibt lesbar.

**`tests/unit/test_evidence_routing_stateful.py`.** Siehe nächster Abschnitt.

## Die Dauerprobe

[FAKT] Die Probe schreibt Eventstreams aus Material, Claims, Evidenz,
Anträgen, Guard-Bewertungen, menschlichen Entscheidungen, Statusübergängen und
Retractions und ruft nach jedem Schritt `replay_events` der produktiven
Implementierung auf. Guard-Bewertungen kommen aus
`evaluate_transition_request`, Freigaben laufen durch `record_human_decision`,
zulässige Übergänge durch `apply_approved_transition`. Es gibt keine Mocks und
kein Zweitmodell des Kernels. Ein zweiter Test führt denselben Ablauf über das
produktive `Ledger` in eine Datei, prüft die Kette und vergleicht den
Zustands-Digest.

[FAKT] Geprüfte Aussage: Ein Claim-Tag ändert sich nur, wenn im selbst
geschriebenen Stream zusammenpassen: aufgezeichneter Antrag für diesen Claim
vom noch geltenden Tag, erlaubte Policy-Kante, zum Antrag gehörender
Guard-Vorschlag, mindestens eine angenommene menschliche Entscheidung, kein
Widerruf, jüngste Entscheidung ist die zitierte Freigabe, Claim nicht
zurückgezogen, bei belegpflichtigen Zieltags eine tragfähige Evidenz (nicht
ungeprüft, keine Metapher, kein bloßer Anlass). Diese Begründung rechnet der
Test unabhängig vom Kernel nach.

[FAKT] Dazu dreizehn geführte Fast-Gültig-Fälle, bei denen genau ein Punkt
fehlt und der Übergang trotzdem direkt in den Stream geschrieben wird: keine
Entscheidung; Freigabe, dann Widerruf, Ablehnung oder Vertagung; Zitat einer
Ablehnung, Vertagung oder eines Widerrufs anstelle einer Freigabe; Freigabe
eines anderen Antrags; behaupteter Guard-Vorschlag ohne tragende Evidenz;
ungeprüfte Quelle; Metapher; inzwischen weitergerückter Claim; zurückgezogener
Claim. Erwartet wird jeweils: Tag unverändert, Abweisung sichtbar vermerkt.

[FAKT] Reproduzierbarkeit: `derandomize=True`, keine Beispieldatenbank,
100 Abfolgen zu je bis zu 40 Schritten. Zwei Läufe hintereinander ergaben
identische Zählerstände: 725 begründete Statuswechsel, 795 gehaltene
Fast-Gültig-Fälle (je Fall zwischen 13 und 174), 1 393 Vorschläge, 371 HOLD,
11 STOP, 319 Retractions. Der Test verlangt für jede dieser Situationen
mindestens fünf Vorkommen, damit er nicht leer bestehen kann. Laufzeit rund
11 Sekunden.

### Gegenprobe: fängt die Probe abgeschaltete Prüfungen?

[FAKT] In einer Wegwerf-Arbeitskopie wurde je eine Prüfung im Kernel
abgeschaltet und sowohl die Dauerprobe als auch der Bestand (239 Tests)
ausgeführt. Die Arbeitskopie ist entfernt; das Repo enthält keine Mutation.

| Abgeschaltete Prüfung | Dauerprobe | Bestand |
| --- | --- | --- |
| R1 Zitierte Entscheidung muss Freigabe sein | fängt (Orakel) | übersieht |
| R2 Widerruf sperrt den Übergang | einzeln nicht beobachtbar | übersieht |
| R3 Freigabe muss die jüngste Entscheidung sein | fängt (Orakel) | fängt |
| R4 Zurückgezogener Claim bleibt stehen | einzeln nicht beobachtbar | übersieht |
| R5 Guard wird frisch nachgerechnet | fängt (Orakel) | fängt |
| R6 Ungeprüfte Quelle trägt nicht | fängt (direkte Prüfung der Bewertung) | fängt |
| R7 Metapher ist kein Beleg | fängt (direkte Prüfung der Bewertung) | fängt |
| R8 Ausgangstag muss noch gelten | einzeln nicht beobachtbar | übersieht |
| R9 Keine Freigabe nach Widerruf | fängt (direkte Prüfung der Annahme) | fängt |
| R10 Keine Freigabe ohne Vorschlag | fängt (direkte Prüfung der Annahme) | fängt |
| R11 Freigabe gehört zu diesem Antrag | fängt (Kernel bricht mit `IndexError` ab) | übersieht |

[FAKT] R2, R4 und R8 sind doppelt gesichert: Schaltet man nur eine der drei
ab, hält eine andere Prüfung denselben Fall (R2 durch die Reihenfolgeprüfung
R3, R4 und R8 durch die frische Guard-Bewertung R5). Am gezielten Szenario
nachgestellt: Abweisung mit `EVENT_ORDER_INVALID` bzw.
`GUARD_REFERENCE_MISMATCH`, Tag unverändert. Schaltet man beide Sicherungen
zugleich ab (R2+R3, R1+R2, R4+R5, R8+R5), meldet das Orakel jeweils den
passenden Verstoß: „retag after withdrawal“, „retracted claim was retagged“,
„a retag was accepted that changed no tag“.

[RISK] Für R2, R4 und R8 belegt die Probe damit das Verhalten, nicht die
einzelne Codezeile. Fällt eine dieser drei Zeilen allein weg, bemerkt es kein
Test; die Probe schlägt erst an, wenn auch die jeweils andere Sicherung fehlt.

## Ausgeführte Prüfungen am Code-Commit `eda36d6`

| Prüfung | Ergebnis |
| --- | --- |
| `make verify` (port-lint, pytest, verify-pointers --strict, claim-lint) | bestanden; 1 271 Tests bestanden, 2 übersprungen, 197 Teiltests |
| `make verify-governance` | bestanden; 16 Workflows, VOID-Backlog aktuell, 22 VOIDs synchron |
| `ruff check src/ tools/ tests/` | keine Befunde |
| `black --check src/ tools/ tests/` | 130 Dateien unverändert |
| `mypy src/ tools/` | keine Befunde in 59 Dateien |
| `bandit -c .bandit.yaml -r src/ tools/` | keine Befunde |
| `claim_lint.py --strict` (index, spec, receipts, tools) | keine ungetaggten Claims |
| `npm run test:py` (Fractalsense) | 184 bestanden |
| Fünf berührte Testdateien unter Python 3.11.16 und 3.12.14 | je 289 bestanden |
| `git diff --check` gegen `main` | sauber |

[FAKT] Nicht ausgeführt: `make verify-js` und Jest. Der Diff berührt weder
`ui-app/`, `packages/` noch das Workspace-Wiring. `make status` und
`make snapshot` wurden nicht ausgeführt; es entstand kein Receipt.

## Bekannte Grenzen

- [RISK] Die Platzhalterlisten erkennen bekannte Leerformeln, keine leere
  Prosa. „Der Verlust ist vernachlässigbar“ oder ein frei erfundener,
  plausibel klingender Verlust besteht die Prüfung. Ob ein benannter Verlust
  zutrifft, entscheidet weiterhin das Review.
- [RISK] Die Sperre gilt für `known_loss` und `falsifier` im Bridge-Adapter
  und in der Bridge-View. `transferred_property`, `preserved_relation` und
  `rollback` sind nicht erfasst; ebenso wenig die TypeScript-Seite der
  Mikro-Meso-Brücke und `known_losses` in `tools/reentry_crate.py`.
- [RISK] Bestehende Bridge-Records mit einem Platzhalter werden ab jetzt
  abgewiesen. Die Vollsuite mit allen im Repo getesteten Beispiel-Records ist
  grün. Records außerhalb der Tests und außerhalb des Repos sind ungeprüft;
  die Intake-Ablagen und Save-State-Vorlagen mit `known_losses` haben ein
  anderes Format und laufen nicht durch den Adapter.
- [RISK] Am ursprünglichen Stand war Sichtbarkeit eine mitgeführte Erklärung,
  kein Ausgabeschutz. Die Suche zeigte auch privat markierte Ausschnitte; der Index
  enthält deren Originaltext wie bisher. Wer einen Index weitergibt, gibt den
  Text weiter. Es gibt kein festes Vokabular; `privat` und `private` sind zwei
  verschiedene Werte.
- [RISK] Korpus-Dateien mit zusätzlichen Feldern bauen nicht mehr. Das ist
  beabsichtigt (Felder gehen nicht mehr still verloren), trifft aber jede
  Übergabe, die bisher Zusatzfelder mitführte.
- [RISK] Die Dauerprobe prüft eine Sicherheitsaussage (kein unbegründeter
  Statuswechsel), keine Vollständigkeit. Sie sagt nichts über Signaturen,
  Zeitstempel, nebenläufiges Schreiben, die CLI-Werkzeuge oder die Inhalte
  der Policy. Echte Guard-Bewertungen stammen aus der produktiven Funktion;
  ein Fehler, der Bewertung und Replay gleichermaßen beträfe und nicht über
  die Evidenzart sichtbar wird, bliebe unentdeckt.
- [RISK] Alle menschlichen Entscheidungen der Probe tragen das Label
  `role:synthetic_test_human`. Die Probe belegt den Ablauf, keine reale
  Freigabe. Der Kernel prüft nicht, wer hinter einem Akteurslabel steht.
- [UNRESOLVED] Der Kernel bricht unter der Mutation R11 mit `IndexError` ab
  statt mit einer geordneten Abweisung. Am unveränderten Code ist der Pfad
  nicht erreichbar; ob die Stelle zusätzlich gehärtet werden soll, ist offen.

## Rücknahmeweg

[FAKT] Die drei Commits lassen sich einzeln zurücknehmen
(`git revert eda36d6`, `2dae06c`, `d24792c`); kein Commit berührt GOLD,
Receipts oder Ledger, es gibt keine Datenmigration.

[ANNEX] Nach einer Übernahme gilt G3: Soll die Dauerprobe oder dieser Bericht
später entfallen, wird die Datei nach `NICHTRAUM/archive/` verschoben statt
gelöscht.

[FAKT] Geprüft mit synthetischen Dateien: Das Suchwerkzeug vom Stand
`d489c28` liest einen Index, den der neue Stand gebaut hat (zusätzliche Spalte
wird ignoriert), und der neue Stand liest einen alten Index. Nach einer
Rücknahme bleiben also vorhandene Indizes benutzbar; die Sichtbarkeitsangabe
erscheint dann nicht mehr im Ergebnis und geht bei einem Neubau wieder
verloren.

[ANNEX] Nach einer Rücknahme von Commit 2 gelten Platzhalter wieder als
benannte Angabe. Records, die zwischenzeitlich abgewiesen wurden, würden dann
wieder übersetzt; das wäre vor einer Rücknahme zu bedenken.

## Nachreview und ausdrücklicher Mergeauftrag

[ANNEX] Am 13.11.2026 wurde der aktuelle PR-Head `02ed97c` unabhängig gelesen
und mit synthetischen Gegenfällen geprüft. Der Owner beauftragte anschließend
ausdrücklich, die offenen Stellen anzupassen und PR #470 zu mergen. Dieser
Auftrag gilt der Codeübernahme nach bestandenen Prüfungen; er erzeugt keine
Runtime-HumanDecision, Claim-Promotion oder Kanonisierung.

### Ausgangsbefund und reproduzierende Gegenfälle

[FAKT] Am Head `02ed97c` erzeugten `known_loss: ["- keiner"]`,
`known_loss: ["— unbekannt —"]` und `falsifier: "— TBD —"` weiterhin eine
Übersetzung. Die Randzeichenliste ließ Striche und Aufzählungspunkte aus.
Die Standardsuche zeigte außerdem den Text, Titel und Herkunft einer als
privat erklärten synthetischen Quelle; das Label allein verhinderte dies nicht.

[FAKT] Die neue Testfassung lief vor dem Fix mit folgendem ausgewählten
Gegenfalllauf: 15 fehlgeschlagen (einschließlich drei Teilfällen),
5 bestanden, 209 abgewählt. Der Test-Commit vor dem Fix hält die Fälle
getrennt nachvollziehbar; seine Gegenfälle werden nicht durch einen anderen
Kernel oder Mocks geprüft.

~~~bash
python -m pytest -q -o addopts='' \
  tests/unit/test_evidence_bridge_adapter.py \
  tests/unit/test_bridge_view.py tests/unit/test_corpus_search.py \
  -k 'edge_dashes or placeholder_known_loss or default_search_does_not_disclose or only_explicit_public_corpus'
~~~

### Konkrete Nachbesserung und Schutzumfang

| Pfad | Nachbesserung |
| --- | --- |
| `src/core/evidence_bridge_adapter.py` | Die gemeinsame Randzeichenliste erfasst nun Bindestriche, Unicode-Striche, Minuszeichen und den Aufzählungspunkt. Beide Pflichtfelder und die Bridge-View nutzen weiter dieselbe Prüfung. |
| `tools/corpus_search.py` | Vor Suche und Zählung werden lokale Korpuszeilen ohne ausdrückliches `public` oder `öffentlich` ausgeblendet. Eine unbekannte, private oder alte fehlende Kennzeichnung öffnet keine Ausgabe. |
| Drei vorhandene Testdateien | Randzeichen-Gegenfälle über Übersetzung und direkte View, sinnvolle Prosa als Gegenrichtung, Ausgabeschutz in allen drei Suchmodi, private Metadaten und Zählwerte, öffentliche Kontrollen und alte Indizes. |
| Zwei bestehende Annex-Verträge und dieser Bericht | Sichtbare Wirkung, bewusste lokale Nachlese, Grenzen und Rückweg. |

[FAKT] `visibility` bleibt im Manifest und Index unverändert erhalten.
Die Standardsuche gibt bei geschützten lokalen Korpusquellen weder
Ausschnitte noch Titel, Quellenkennungen, Herkunftslinks oder
queryabhängige Trefferzahlen aus. Die Filterung erfolgt vor der
Limitberechnung. `--include-private` erlaubt die ausdrückliche lokale
Nachlese und markiert die Ausgabe mit `private_corpus_included: true`.
Die Option ist keine Publikationsfreigabe. Alle neuen Fixtures sind synthetisch.

[RISK] Die Schutzanforderung ist für die **Standardsuchausgabe** umgesetzt.
SQLite, Manifest, Statistiken und Wortfrequenzen bleiben private lokale
Arbeitsdateien mit Originaltext beziehungsweise Ableitungen. Weder diese
Dateien noch eine Ausgabe mit `--include-private` sind öffentliche Exporte.
Eine falsche öffentliche Quellendeklaration, manuelle Dateifreigabe oder
direkter SQLite-Zugriff werden hier nicht verhindert. Es wird keine
Verschlüsselung oder neue Zugriffsverwaltung behauptet. Ausgewählte
Repo-Snapshots werden nicht als lokale Korpusquellen umklassifiziert.

### Nachprüfung und verbleibende Grenzen

[FAKT] Die Nachprüfung lief unter Python 3.12.14, uv 0.12.18,
pytest 9.1.1 und hypothesis 6.170.12. Die separate Prüfungsumgebung wurde
mit `uv sync --frozen --group dev --no-install-project` aus `uv.lock`
aufgebaut. Nach dem Fix:

| Prüfung | Ergebnis |
| --- | --- |
| `make verify` | bestanden; 1 285 Tests und 200 Teiltests bestanden, 2 übersprungen |
| `make verify-governance` | bestanden; 16 Workflows, VOID-Backlog aktuell, 22 VOIDs synchron |
| ruff, Black `--check`, mypy, Bandit mit `.bandit.yaml` | bestanden; keine Befunde im jeweiligen Prüfumfang |
| `git diff --check` | bestanden |

[FAKT] Die zwei übersprungenen Tests betreffen die optionale
DataLad-/git-annex-Integration. Vier optionale Status-/Snapshot-Pointer
fehlten; alle CORE-Pointer waren gültig. Ein unabhängiges, lesendes
Nachreview des Follow-up-Diffs fand keinen konkreten Fehler und führte die
drei betroffenen Testsuiten mit 226 bestandenen Tests und 35 bestandenen
Teiltests aus. Dieses Nachreview ist keine formale GitHub-Review-Submission.

[ANNEX] CI-Ergebnisse sind dem endgültigen PR-Head zuzuordnen und vor dem
Merge erneut direkt zu prüfen; obige Zahlen sind selbst ausgeführte lokale
Prüfungen. Die ursprüngliche Mutationsreihe wurde im Nachreview nicht erneut
ausgeführt. Kernel, Policies, GOLD und bestehende Governance-Invarianten
bleiben unverändert. Die übrigen oben benannten Grenzen gelten weiter.

[RISK] Eine Rücknahme des Fix-Commits würde sowohl die Randzeichenlücke
als auch die standardmäßige Ausgabe geschützter Korpuszeilen wieder öffnen.
Test- und Fix-Commit sind dann gemeinsam in umgekehrter Reihenfolge
zurückzunehmen. Es gibt keine Datenmigration; bestehende lokale Indizes
bleiben nutzbar. Der alte Suchcode hat jedoch keinen Ausgabeschutz, auch wenn
ein Index seine Sichtbarkeitsangaben noch enthält. Dateien werden bei einer
späteren Entfernung gemäß G3 archiviert statt gelöscht.
