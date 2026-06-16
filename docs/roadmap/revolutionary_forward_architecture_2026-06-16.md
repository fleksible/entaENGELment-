# Revolutionary Forward Architecture — entaENGELment-

**Datum:** 2026-06-16
**Fokus:** Zukunftsarchitektur (Phase 3 — Plan, nicht Umsetzung)
**Status:** Vorschlag. Nichts hier ist beschlossen; jeder Schritt erfordert
Consent (G0) und ggf. SEMANTIC REVIEW.

> Zielformel: „Revolutionäre Modernisierung durch bessere Membranen, nicht durch
> Austausch des Herzens."

---

## 1. Repository als lebendiges Wissenssystem

**[MODELL]** Das Repo wird als geschichtetes Wissenssystem gedacht, in dem jede
Aussage ihren epistemischen Ort kennt:

```
                 untrusted        markiert / Provenienz        Kanon
   INBOX/  ──▶  exchange_archive/  ──(Review + Consent)──▶  index/ · spec/ · VOIDMAP
                       │                                        │
                       ▼                                        ▼
                 NICHTRAUM/                               receipts/ (IMMUTABLE)
              (maybe · quarantine · archive)              evidence/  (Belegkette)
```

Schichten und ihre Rolle:

| Schicht | Ort (heute) | Rolle | Veränderbarkeit |
|---------|-------------|-------|-----------------|
| Canon | `index/`, `spec/`, `policies/`, `VOIDMAP.yml`, `seeds/` | geltende Wahrheit | GOLD |
| Variants | (noch implizit) | konkurrierende/abgeleitete Lesarten | ANNEX, markiert |
| Schnittraum | (noch nicht angelegt) | Übergangs-/Synthese-Zone | ANNEX |
| Annex | `src/`, `tools/`, `docs/` (meist) | Arbeitsbereich | ANNEX |
| Archive | `NICHTRAUM/archive/` | bewahrt, inaktiv | append/move-only |
| Exchange | `docs/exchange_archive/` | ehemalige Bezüglichkeit | markiert, nicht-Kanon |
| Evidence | `evidence/`, `ark/p4/evidence/`, `docs/release/evidence/` | Belege | IMMUTABLE-nah |
| Receipts | `receipts/`, `data/receipts/`, `ark/p4/receipts/` | Audit-Trail | IMMUTABLE |
| VOIDMAP | `VOIDMAP.yml` | offene Nicht-Auflösungen | GOLD |
| Claim Registry | (noch nicht angelegt) | kanonische Claims + Status | ANNEX |

---

## 2. Vorgeschlagene Zielstruktur

**[MODELL]** Additiv, ohne Bestehendes umzubenennen, solange kein Consent vorliegt.
`(✓)` = existiert, `(+)` = Vorschlag neu.

```
docs/
  canon/        (+)  explizite Kanon-Pointer / Was-gilt-Übersicht
  spec/         (✓)  Spezifikationen (vgl. specs/ → konsolidieren? SEMANTIC REVIEW)
  annex/        (+)  optionaler expliziter ANNEX-Sammelort
  audit/        (✓)  Audit-Reports (ADR-0001: kein paralleles audits/)
  decisions/    (✓)  ADRs (Decision Log)
  exchange_archive/ (✓ neu) ehemalige Bezüglichkeit
  roadmap/      (✓ neu) Zukunftsarchitektur
  voids/        (✓)  VOID-Detaildokumente (+ VOIDMAP.yml als Registry)
  claims/       (+)  Claim Registry
  glossary/     (+)  Term Registry (kanonische Begriffe + Claim-Grenze)
  receipts/     —    (Index-Doc statt Datenduplikat; Daten bleiben in receipts/)
policies/       (✓)
protocols/      (+)  bisher implizit (DeepJump in Makefile/CI) → explizit dokumentieren
scripts/ tests/ tools/ src/  (✓)
.github/workflows/           (✓)
```

**[INFERENZ]** Priorität: zuerst Registries und Glossary (hoher Orientierungswert,
risikoarm), dann optionale Konsolidierungen (`spec/`+`specs/`) nur mit Consent.

---

## 3. Exchange Archive / ehemaliger Austausch

Angelegt in Phase 2 (siehe ADR-0002):

- `docs/exchange_archive/README.md` — Zweck/Abgrenzung.
- `docs/exchange_archive/INDEX.md` — Record-Tabelle.
- `docs/exchange_archive/TEMPLATE_exchange_record.md` — Vorlage.

**[MODELL]** Lebenszyklus eines Records:
`INBOX/ (G5-Prüfung)` → `exchange_record anlegen` → `INDEX.md-Zeile` →
`Review + Consent` → entweder `migrated` (Zielpfad in Kanon) oder `rejected`
(verbleibt als Provenienz) oder `archive` (`NICHTRAUM/archive/`, G3).

---

## 4. Zukunftsprüfungen (vorgeschlagene CI-Checks)

**[MODELL]** Zunächst **advisory** (warnen), erst nach Stabilisierung blockierend.
Alle read-only, deterministisch, ohne Netzwerk.

| Check | Zweck | Werkzeug-Idee | Start-Modus |
|-------|-------|---------------|-------------|
| Markdown link check | Tote relative Links in `docs/`/Top-Level | lychee oder eigenes Skript | advisory |
| YAML validity | Alle `*.yml`/`*.yaml` parsen (über policy hinaus) | `python -c yaml.safe_load` Sweep | advisory |
| VOIDMAP schema | `VOIDMAP.yml` gegen Schema (Felder, Status-Enum) | jsonschema | advisory → block |
| Receipt format | Receipt-JSON gegen `spec/resonance_receipt_v1_1.schema.json` | vorhandenes `receipt_lint.py` ausweiten | advisory |
| Exchange index consistency | `INDEX.md` ↔ vorhandene Record-Dateien | `exchange_lint.py` (§5) | advisory |
| No forbidden claim collapse | Keine Poesie-als-Beweis-Struktur in Gating-Texten | `claim_lint.py`-Erweiterung | advisory |
| No unmarked metaphysical assertion in spec | Spec-Dateien ohne Claim-Grenze | `claim_lint.py`-Scope auf spec/ | advisory |
| No TODO without VOID reference | Jedes TODO verweist auf eine VOID-ID | grep-basierter Check | advisory |
| No new canonical term without registry entry | Neue Kanon-Begriffe ↔ `docs/glossary/` | `term_lint` (Teil von claim/voidmap-lint) | advisory |

**[FAKT]** Diese Checks sind als **Vorschlag** dokumentiert und in Phase 2 **nicht**
implementiert — neue Workflows mit potenziellen Fehlerquellen werden nicht ohne
Consent und lokale Testmöglichkeit hinzugefügt.

---

## 5. Semantische Wächter (Design, nicht implementiert)

**[MODELL]** Optionale Skripte unter `tools/`. Leitprinzip: **zuerst warnen, nicht
blockieren**; deterministisch; keine semantische Umdeutung, nur Konsistenzprüfung.

| Skript | Aufgabe | Risiko | Empfehlung |
|--------|---------|--------|------------|
| `claim_lint.py` (Erweiterung) | Warnung bei gemischten Sprachvarianten innerhalb einer Datei; Poesie-in-Gating-Text | niedrig | bestehendes Tool erweitern |
| `voidmap_lint.py` | VOIDMAP-Schema, Status-Enum, Datums-Plausibilität, Drift zu `voids_backlog.md` | niedrig | neu, read-only |
| `exchange_lint.py` | `INDEX.md` ↔ Record-Dateien, Pflichtfelder im Template | niedrig | neu, read-only |
| `receipt_lint.py` (Ausbau) | Schema + HMAC-Format über alle Receipt-Pfade | mittel | bestehendes Tool ausweiten |
| `canon_variant_lint.py` | Kanon-Begriff ohne Glossary-Eintrag; Variant ohne Markierung | mittel | erst nach Glossary |
| `semantic_guard_check.py` | Sammel-Runner der obigen Wächter, nur Reporting | niedrig | optional |

**[INFERENZ]** Reihenfolge: `voidmap_lint` und `exchange_lint` zuerst (klar
definierbar, risikoarm), `canon_variant_lint` zuletzt (braucht Glossary + Consent).

---

## 6. Migrationsschema (Vorschlag)

**[MODELL]** Wenn Bestands-Konsolidierungen anstehen (z. B. `specs/`→`spec/`):

1. ADR mit Status `Proposed` + Review-Frage.
2. Querverweis-Scan (Linkcheck) **vor** Verschieben.
3. Verschieben statt Löschen (G3); Redirect-Stub oder Mapping dokumentieren.
4. `verify`/Linkcheck **nach** Migration grün.
5. ADR auf `Accepted`, Receipt/Commit mit Begründung.

---

## 7. Offene Punkte

- [ ] ☐ Registries (Claim/Term/Evidence/Receipt) als REVIEW PATCH umsetzen.
- [ ] ☐ Advisory-CI-Gates einführen (Reihenfolge §4), zunächst nicht-blockierend.
- [ ] ☐ Semantische Wächter implementieren (Reihenfolge §5), warnend.
- [ ] ☐ Konsolidierungs-Entscheidungen (`spec/`/`specs/`, Top-Level `audit/`) — SEMANTIC REVIEW.
- [ ] ☐ Guard-the-guard-Tests für ungetestete Tools (Audit R3).

## 8. Artefakte

- `docs/roadmap/revolutionary_forward_architecture_2026-06-16.md` (dieses Dokument)
