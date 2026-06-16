# Calm Intake Layer — Result Report (PR #255)

**Datum:** 2026-06-16
**Fokus:** Intake-/Flow-Fänger einziehen (additiv)
**Branch:** `chore/intake-layer`
**Basis-HEAD:** `2ec5f3f` (main nach #252, #253, #254)

> Zielsatz: *Intake heißt — nichts Wertvolles muss sofort wahr werden, um nicht
> verloren zu gehen.*

---

## 1. Was wurde angelegt?

- `docs/intake/` — semipermeabler Vorraum (Capture→Triage-Trichter):
  - `README.md`, `INDEX.md`, `TEMPLATE_intake_record.md`
  - Unterordner `raw/`, `triaged/`, `parked/`, `rejected/`, `records/` (je `.gitkeep`)
- `tools/intake_add.py` — lokaler Helper (kopiert, indexiert, optional Record)
- Makefile-Target `make intake FILE=… TITLE=… SOURCE=…` (Wrapper um den Helper)
- `CLAUDE.md` — neue „Pattern F: Intake-First für unverortete Artefakte"
- Dieser Bericht.

## 2. Geänderte / neue Dateien

| Datei | Art |
|-------|-----|
| `docs/intake/README.md` · `INDEX.md` · `TEMPLATE_intake_record.md` | neu |
| `docs/intake/{raw,triaged,parked,rejected,records}/.gitkeep` | neu |
| `tools/intake_add.py` | neu |
| `Makefile` | geändert (+`intake`-Target, Help, .PHONY) |
| `CLAUDE.md` | geändert (+Pattern F) |
| `docs/audit/intake_layer_result_2026-06-16.md` | neu |

**[FAKT]** Keine Bestandsinhalte umgedeutet; Änderungen an `Makefile`/`CLAUDE.md`
sind rein additive Ergänzungen.

## 3. Wie funktioniert der Intake-Flow?

```
created document
  → make intake / python tools/intake_add.py
  → Kopie nach docs/intake/raw/<YYYY-MM-DD>/<slug>
  → Zeile in docs/intake/INDEX.md (Status: raw)
  → optional Record in docs/intake/records/INTAKE-<date>-NNN.md
  → später menschliche Triage:
       parked | migration-candidate | rejected | migrated
```

Der Helper **kopiert** (nie verschieben/löschen, G3), vergibt eine Tages-ID
`INTAKE-YYYY-MM-DD-NNN`, und schreibt **ausschließlich** unter `docs/intake/`.

## 4. Bewusst gesetzte Grenzen

- **Capture erlaubt, Kanonisierung verboten.** Kein automatisches Migrieren nach
  `canon`/`spec`/`VOIDMAP`/`glossary`/`roadmap`.
- **Zwei Schutzwälle im Helper:** `_assert_inside_intake` (Ziel muss unter
  `docs/intake/` liegen) und `_assert_not_forbidden` (explizite Sperrliste für
  index/spec/policies/seeds/docs-spec/docs-specs/docs-glossary/docs-roadmap/
  docs-canon + `VOIDMAP.*`).
- **Anti-Duplikation:** `docs/intake/` dupliziert nicht `INBOX/`,
  `docs/exchange_archive/` oder `NICHTRAUM/`, sondern ist der *Verb*-Raum dazwischen
  (auffangen→sichten). Abgrenzung in `README.md` §4 dokumentiert.
- **Unangetastet:** VOIDMAP, Canon, Spec, Roadmap-Inhalte, Security-Workflows,
  `dependabot.yml`, README-Hauptdatei, Framework-Begriffe.

## 5. Ausgeführte Checks

| Check | Ergebnis |
|-------|----------|
| `python3 -m py_compile tools/intake_add.py` | ok |
| `claim_lint --scope index,spec,receipts,tools --strict` | exit 0 |
| `verify_pointers --strict` | exit 0 |
| `workflow_posture_check` | exit 0 |
| `make intake` ohne Args | Usage + exit 2 (erwartet) |
| `make intake` realer Lauf (Temp-Datei) | kopiert/indexiert/Record ✓ |
| Schreibgrenze | nur `docs/intake/` berührt; Quelle unangetastet ✓ |
| Testresiduen | restlos entfernt; INDEX auf Platzhalter zurück ✓ |

**Limitierung:** `pytest`/`ruff` sind in dieser Umgebung nicht installiert; die
Python-Testsuite und Ruff-Lint liefen **nicht** lokal (Anti-F7). Die CI deckt beides
ab; der Helper wurde funktional manuell getestet.

## 6. Offene Risiken

- **[INFERENZ]** `INDEX.md` wird per Append gepflegt; bei manueller Bearbeitung
  parallel zum Helper sind Merge-Konflikte möglich (gewollt schlank, kein DB-Lock).
- **[HYPOTHESE]** Begriffliche Nähe zu `INBOX/`/`exchange_archive/` könnte verwirren;
  mit `README.md` §4 adressiert, aber Praxis muss es bestätigen.
- **[FAKT]** Kein Lint erzwingt bisher Intake-Index-Konsistenz (Status-Enum,
  Record↔Index). Optionaler `intake_lint.py` wäre ein späterer Schritt.

## 7. Mögliche, aber NICHT getane nächste Schritte

- Advisory `intake_lint.py` (Status-Enum + Record/Index-Konsistenz) — analog zum
  Roadmap-Vorschlag für `exchange_lint`.
- Triage-Helper (`intake_triage.py`) zum kontrollierten Verschieben raw→triaged/parked.
- Dependabot-Advisory-Triage auf `main` (separater, vorrangiger Security-Vorgang).

## 8. Essenz-Bestätigung

**[FAKT]** Kein Kanon-, Spec-, VOID-, Claim- oder Roadmap-Inhalt verändert. Keine
Löschung, kein Force-Push, kein Merge, kein Auto-Merge, keine Dependabot-/
Security-Workflow-Änderung. Rein additive, reversible Intake-Membran.
