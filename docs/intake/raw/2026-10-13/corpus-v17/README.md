# Korpusnachtrag v17 mit getrenntem v18-Folgestand

**DERIVED / REVIEW-PENDING · Intake raw · keine normative Wirkung**

FOKUS: Korpusnachtrag und Statusabgleich

Dieser Nachtrag ergänzt den [v10-Export](../../2026-10-07/corpus-v10/README.md).
Der Pfad `corpus-v17` benennt den eingefrorenen Vergleichseingang. Die späteren
zwei Teillektüren stehen ausschließlich im getrennten `followup_v17_v18`.
Alle 96 Identitäten werden in der [CSV](corpus-matrix.csv) mit beiden Leseständen geführt.
`READ_COMPLETE` bedeutet historische Lesebehauptung des Index, keine Sachvalidierung.

## Zwei Quellenanker

| Anker | Rolle | SHA-256 |
|---|---|---|
| v17, 1.333.992 Bytes | eingefrorener Eingang vor dem Writeback | `77e4fab4358240a7674943014f9301f1faade50ed0e6072ec10a37d8c6db45e0` |
| v18, 1.379.469 Bytes | bestätigtes materialisiertes Artefakt nach dem Writeback | `66de61ff3fd63fbb478d8feca991ff81d7e36a042228d79da489c7ef3239c01a` |

v18 wurde beim Speichern bestätigt und für diesen Nachtrag erneut materialisiert.
Die eingebetteten Felder `input_library_version: 17` und `observed_version: "17"`
dokumentieren den Eingang des Schreibvorgangs. Sie sind kein aktueller Speicherbeleg.
Die Originalbytes sind privat und nicht im Bundle. Der v17-Hash ist ein im früheren
Lauf beobachteter Anker; die historischen Bytes konnten im Folgelauf nicht erneut
materialisiert werden. Der erhaltene geparste v17-Inhalt und der erneut geladene
v18-Inhalt bilden die beiden strukturellen Vergleichsstände.

## Aus den Einträgen berechnete Zähler

<!-- COUNTS:START -->
| Metric | v10 | v17 | v18 |
|---|---:|---:|---:|
| entries | 63 | 88 | 90 |
| READ_COMPLETE | 56 | 88 | 88 |
| PARTIAL | 7 | 0 | 2 |
| pending_candidates | 11 | 8 | 6 |
| identities | 74 | 96 | 96 |
| points | 192 | 258 | 259 |
| relations | 38 | 66 | 66 |
| conflicts | 5 | 14 | 14 |
| outside_claim_vocabulary | 100 | 93 | 93 |
<!-- COUNTS:END -->

v10→v17: 25 neue erschlossene Einträge, davon 11 vorher als Metadaten bekannt;
7 alte Teillektüren abgeschlossen; 28 Relationen und 9 Konflikte hinzugefügt.
v17→v18: zwei der acht vorgemerkten Quellen partiell gelesen, ein Indexpunkt ergänzt.
Die Identitätsmenge bleibt 96. Der frühere Bericht hatte v17 gezählt und den
Folgelauf separat genannt; die nebeneinanderstehenden Spalten vermeiden diese Mehrdeutigkeit.

## Claim-Vokabular

Referenzmenge aus corpus-gate v0.2: `FAKT`, `MODELL`, `HYPOTHESE`, `METAPHER`, `ANALOGIE`, `UNRESOLVED`.
Andere Quelltags bleiben unverändert erhalten. Vokabularabweichung ist keine
Falschaussage und kein Anlass für automatische Übersetzung oder Promotion.

<!-- TAGS:START -->
| Tag | v10 | v17 | v18 |
|---|---:|---:|---:|
| ARCHITEKTUR | 4 | 4 | 4 |
| AUDIT | 1 | 1 | 1 |
| CLAIM-GUARD | 9 | 8 | 8 |
| FAKT | 19 | 39 | 40 |
| GUARD | 30 | 24 | 24 |
| HYPOTHESE | 2 | 3 | 3 |
| INFERENZ | 1 | 2 | 2 |
| KORPUSBEFUND | 7 | 7 | 7 |
| MODELL | 54 | 101 | 101 |
| POESIE | 1 | 1 | 1 |
| PROVENIENZ | 1 | 1 | 1 |
| REPORTED | 7 | 7 | 7 |
| SPEC | 39 | 38 | 38 |
| UNRESOLVED | 17 | 22 | 22 |
<!-- TAGS:END -->

## Navigation und Prüfung

- [EXPORT.md](EXPORT.md): Felder, Grenzen, getrennte Hashes und EXPORT-04–06.
- [test_verify_counts.py](test_verify_counts.py): automatisierte Fälle zum Verifier.
- [WORKFLOW.md](WORKFLOW.md): Reproduktion und begrenzte Folgearbeiten.
- [corpus-delta.json](corpus-delta.json): v10 als Baseline, v17-Delta, v18-Folgeschritt.
- [Audit](../../../../audit/2026-10-13_corpus_repo_reconciliation.md): C01–C19 und Gegenlesung.
- [Intake-Record](../../../records/INTAKE-2026-10-13-001.md).

Aus dem Repository-Root:

```bash
python3 docs/intake/raw/2026-10-13/corpus-v17/verify_counts.py --export-only
python3 docs/intake/raw/2026-10-13/corpus-v17/verify_counts.py \
  --input-v18 /pfad/zum/privaten/Index.md
python3 docs/intake/raw/2026-10-13/corpus-v17/test_verify_counts.py
```

Der Prüfumfang muss ausdrücklich gewählt werden; es gibt keinen Standardmodus und
keinen stillen Rückfall. Beide erfolgreichen Läufe liefern Exit 0, aber verschiedene
maschinenlesbare Statuswerte:

| Aufruf | Status | Prüft zusätzlich |
|---|---|---|
| `--export-only` | `PASS_EXPORT_ONLY` | nichts über das öffentliche Paket und die v10-Baseline hinaus |
| `--input-v18 PATH` | `PASS_WITH_V18_INPUT` | exakte Originalbytes und direkten Indexvergleich |

Fehlende, doppelte oder unlesbare Moduswahl, ein falscher Originalhash und
abweichender Inhalt scheitern; auf den Exportmodus wird nie zurückgefallen. Jeder
Lauf gibt seine geprüften und ungeprüften Bereiche mit aus.
Geprüft werden Delta, Zähler, Tagverteilung, CSV, Fortsetzungen, Manifest und die
verlinkte Intake-Zeile samt beiden Linkzielen. Kein Statuswert behauptet
wissenschaftliche Gültigkeit, vollständige Originallektüre, grüne Gesamt-CI oder
Mergefreigabe. Der Verifier läuft manuell; dieser Diff richtet keinen CI-Job ein.
Eine grüne allgemeine Repo-CI ersetzt diesen Aufruf nicht.
