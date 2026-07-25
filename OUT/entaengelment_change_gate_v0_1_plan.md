# Report: EntaENGELment Change-Gate Skill v0.1 — Planbericht (Phase 2)

**Datum:** 2026-07-24
**Fokus:** Change-Gate Skill v0.1
**Modus:** Phase 1 read-only abgeschlossen → Phase-2-Scope-Entscheidung
**Claim-Status:** [SPEC-WIP] (Planbericht, keine Kanonisierung)

## Ziel

Ein operativer Claude-Skill unter `.claude/skills/entaengelment-change-gate/`,
der vor nichttrivialen Änderungen **bereits vorhandene** Repo-Regeln
operationalisiert. Kein neuer Source of Truth, keine Governance-Instanz, keine
semantische Autorität, kein Ersatz für menschliche Entscheidungen.

---

## 1. Befund (Phase 1, read-only)

### 1.1 Source-of-Truth-Tabelle

| Regel / Begriff | Bestehender Repo-Pfad | Verbindlichkeit | Im Skill nur referenzierbar? |
|---|---|---|---|
| G0–G6 Guards | `CLAUDE.md` | Projektregel (House Rules) | ja — nur zitieren/auslösen |
| GOLD / ANNEX / IMMUTABLE / Semi-GOLD + Pfadlisten | `.claude/rules/annex.md` | Projektregel | ja |
| NICHTRAUM-Schutz (G2), Deletion-Verbot (G3) | `CLAUDE.md`, `.claude/rules/annex.md` | Projektregel | ja |
| Fokus / Aufmerksamkeit / Fokus-Switch (G4) | `.claude/rules/metatron.md`, `docs/guards/metatron_rule.md`, `tools/metatron_check.py` | Projektregel + CI-Check | ja |
| untrusted Inhalte, Injection-Pattern, Quarantine (G5) | `.claude/rules/security.md` | Projektregel | ja |
| Read-only-Modus | `.claude/skills/witness_mode.md` | vorhandener Skill | ja — **wird nicht angefasst** |
| Claim-Tags (Register v0.2) | `policies/claim_tags_v0_2.yaml` (**GOLD**) | Draft-Register `[SPEC-WIP]` | ja — nur lesen/referenzieren |
| Claim-Leiter, Anti-Capture, Provenienz-Schutz | `docs/governance/CLAIM_LEITER_v0_1.md` | Draft `[SPEC-WIP]` | ja |
| Claim-Lint (enforced Tag-Set) | `tools/claim_lint.py` | blockierend in `make verify` | ja |
| „SoT is not a truth-maker", Schichtenmodell, A/B-Trennung | `docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md` | Draft `[SPEC-WIP]` | ja |
| „Guard ohne Check bleibt Zielzustand" | `docs/governance/GUARD_CHECK_CONTRACT_v0_1.md` | Draft `[SPEC-WIP]` | ja |
| HumanDecision `APPROVE\|REJECT\|DEFER\|WITHDRAW` | `src/core/evidence_routing.py`, `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` §5 | implementiert (partial enforcement) | ja — **nicht importieren** |
| GuardDecision `PROPOSE\|HOLD\|STOP` (bewusst **kein** PASS) | `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` §5 | implementiert | ja |
| 12 ERK-Invarianten (u. a. „Policy is not truth", „Provenance is not evidence", „Consent fails closed") | `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` §7, `tests/ethics/test_erk_invariants.py` | implementiert + getestet | ja |
| Geschlossenes Reason-Code-Vokabular, fail-closed Schema | `src/core/evidence_routing.py` (`ReasonCode`) | implementiert | ja — **Muster**, keine Wiederverwendung der Codes |
| `authority_effect`, `Authority-Status`, `Promotion-Effect`, `Human-Decision-Boundary`, `Runtime-Enforcement` | `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md`, `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` (Kopfblöcke) | ANNEX-Konvention | ja |
| `known_loss` / `known_loss_required` (deklarierte Verluste) | `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §12 + `source_relation`-Block | ANNEX-Konvention | ja |
| Falsifikator, Rücknahmepfad, „Falsifikation vor Verstärkung" | `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §3.1–3.6, §7, §8 | ANNEX-Konvention | ja |
| `CLASSIFICATION_UNDETERMINED` (keine automatische Wahl der stärkeren Klasse) | `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §2 | ANNEX-Konvention | ja |
| Exit-Semantik: verbotene Endzustände + `ELIGIBLE_FOR_EXTERNAL_REVIEW` | `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md` §11 | ANNEX-Konvention | ja |
| `PASS \| HOLD \| LOOP \| STOP` (Assembly-Navi-Navigationsentscheidung) | `docs/tesser3takt/TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md` §9 | ANNEX-Modell | ja — **anderes System** |
| Intake-First / Calm Intake (Pattern F) | `docs/intake/README.md`, `tools/intake_add.py`, `CLAUDE.md` | Projektregel | ja |
| Report-Schema für `OUT/` | `CLAUDE.md` | Projektregel | ja |
| Verify-Membran (`make verify`, `verify-governance`, `verify-js`) | `Makefile`, `CLAUDE.md` | blockierend vor Merge (G6) | ja |
| Anti-Overclaim-Sprache | `ANTI_CAPTURE_POLICY.md` | Governance-Draft | ja |
| Claim-Tagging & Safe Extension | `EPISTEMIC_HYGIENE.md` | ANNEX, Guards gewinnen | ja |
| VOID-Backlog (offene Grenzen) | `VOIDMAP.yml` (**GOLD**), `docs/voids_backlog.md` | GOLD + generiert | ja — nur lesen |

### 1.2 Begriffliche Mehrdeutigkeiten (Befund)

1. **`PASS_CANDIDATE` existiert im Repository nicht.** Volltextsuche über
   `*.md/*.py/*.yaml/*.yml/*.json`: 0 Treffer. Die im Auftrag vorgeschlagene
   Bezeichnung wäre ein **neuer Statuswert**.
2. **`HOLD` ist mehrfach belegt** und ausdrücklich nicht übersetzbar:
   Research-HOLD (`RESEARCH_VALIDATION_GATE_v0_1.md` §9), ERK-Guard-HOLD
   (`EVIDENCE_ROUTING_KERNEL_v0_1.md` §5), tesser3TAKT-Navigations-HOLD
   (`TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md` §9). Der ERK-Text nennt explizit drei
   **nicht gleichzusetzende** Übergangssysteme (§11).
3. **`PASS` ist im Maschinenpfad bewusst ausgeschlossen**: „Bewusst kein `PASS`:
   Guard-State und menschliche Claim-Entscheidung dürfen nicht zusammenfallen"
   (ERK §5). `RESEARCH_VALIDATION_GATE` §11 verbietet zusätzlich `PASS`,
   `VALIDATED`, `PROVEN`, `SAFE`, `CLINICALLY_READY`, `ETHICALLY_APPROVED` ohne
   externe zuständige Entscheidung.
4. **`REJECT` ist ein HumanDecision-Wert** (ERK §5), kein Agenten-Erwartungswert.
5. **`LOOP` gehört zur tesser3TAKT-Navigation**, nicht zu Change-Gating.
6. **Claim-Lint-Vokabular ≠ Register-Vokabular**: `tools/claim_lint.py` erzwingt
   `[FACT] [HYP] [MET] [TODO] [RISK]`; `policies/claim_tags_v0_2.yaml` führt ein
   breiteres Register. Der Unterschied ist in `tools/README.md` und
   `EVIDENCE_ROUTING_KERNEL_v0_1.md` §14 als bekannt dokumentiert.
7. **`.claude/` ist in `annex.md` nicht klassifiziert** — weder GOLD noch ANNEX
   noch IMMUTABLE noch NICHTRAUM (siehe §1.4).

### 1.3 Erkannte Überschneidungen / Risiko eines parallelen Systems

| Risiko | Bestehende Struktur | Vermeidung im Skill |
|---|---|---|
| Neue Statusleiter | Claim-Register, GuardDecision, HumanDecision, Assembly-Navi | Skill führt **keine** eigene Leiter ein; nur zwei bereits belegte, ausdrücklich als „kein Status" markierte Endwörter (§2.3) |
| Neue Reason-Code-Autorität | ERK `ReasonCode` (geschlossen, im Eventstream) | Skill-Codes sind **lokal**, gehen nie in Ledger/Receipts/Events; Nicht-Äquivalenz explizit dokumentiert |
| Zweiter Guard-Katalog | G0–G6 in `CLAUDE.md` | Skill **zitiert** G0–G6, definiert keinen eigenen Guard |
| Zweite GOLD-Definition | `.claude/rules/annex.md` | Pfadliste im Validator trägt Quellverweis; ein Test prüft, dass jedes Präfix wörtlich in `annex.md` vorkommt |
| Zweite Verify-Membran | `make verify` | Skill ist **nicht** in `make verify` verdrahtet; nur seine Tests laufen dort mit |
| Guard ohne Check | `GUARD_CHECK_CONTRACT_v0_1.md` | Skill behauptet keine Live-Enforcement; Validator ist advisory und wird als solcher benannt |

### 1.4 Grenzbefund `.claude/`

`.claude/rules/annex.md` listet `.claude/` in keiner der vier Kategorien.
Behandlung in diesem Patch: **additiv-ANNEX**, begründet durch
(a) ausdrückliche Nutzeranweisung auf genau diesen Pfad,
(b) rein additive Neuanlage eines Unterverzeichnisses,
(c) `.claude/` ist in keiner GOLD-/IMMUTABLE-/NICHTRAUM-Liste enthalten,
(d) `.claude/skills/witness_mode.md` bleibt unverändert.

Die **Klassifikation von `.claude/` in `annex.md`** bleibt eine menschliche
Entscheidung und wird in diesem Patch **nicht** vorgenommen (das wäre eine
Änderung an einer Regeldatei außerhalb des Auftragsscopes).

---

## 2. Geplanter Scope

### 2.1 Neu anzulegende Dateien

| Pfad | Inhalt |
|---|---|
| `.claude/skills/entaengelment-change-gate/SKILL.md` | Skill-Definition: Aktivierungsbereich, Ablauf, Guard-Semantik, Quellenbindung |
| `.claude/skills/entaengelment-change-gate/references/change-manifest-schema.md` | Feldschema, Reason-Codes, Nicht-Äquivalenztabelle, Abgrenzungen |
| `.claude/skills/entaengelment-change-gate/templates/change-manifest.yaml` | Leeres Arbeits-Template mit Kommentaren |
| `.claude/skills/entaengelment-change-gate/scripts/validate_change_manifest.py` | Deterministischer, offline, seiteneffektfreier Validator |
| `tests/unit/test_change_gate_manifest.py` | Pytest-Suite (12 geforderte Fälle) |
| `OUT/entaengelment_change_gate_v0_1_plan.md` | dieser Bericht |
| `OUT/entaengelment_change_gate_v0_1_audit.md` | Abschlussbericht (Phase 4) |

### 2.2 Zu ändernde bestehende Dateien

**Keine.** Der Patch ist vollständig additiv.

### 2.3 Bewusste Abweichungen von der Auftragsvorlage (mit Quellenbegründung)

| Vorschlag im Auftrag | Umsetzung | Quelle der Abweichung |
|---|---|---|
| `expected_reentry_state: PASS_CANDIDATE\|HOLD\|LOOP\|REJECT` | `expected_gate_outcome: HOLD \| ELIGIBLE_FOR_EXTERNAL_REVIEW` | `PASS_CANDIDATE` hat 0 Repo-Treffer → wäre neuer Statuswert. `RESEARCH_VALIDATION_GATE_v0_1.md` §11 liefert bereits die kanonische Nicht-PASS-Formulierung `ELIGIBLE_FOR_EXTERNAL_REVIEW` ausdrücklich „nicht als Runtime-Status und nicht als Claim-Tag" |
| `LOOP` als Erwartungswert | entfällt | gehört zu `TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md` §9; ERK §11 verbietet Gleichsetzung der Übergangssysteme |
| `REJECT` als Erwartungswert | entfällt | `REJECT` ist ein `HumanDecision`-Wert (ERK §5); ein Agent darf ihn nicht vorwegnehmen |
| `HOLD` | bleibt, **gate-lokal gescoped** | `RESEARCH_VALIDATION_GATE_v0_1.md` §9: „Das Wort HOLD besitzt verschiedene lokale Rollen … Keine automatische Übersetzung" |
| `change_class: … UNDETERMINED` | `CLASSIFICATION_UNDETERMINED` | wörtlicher Repo-Begriff, `RESEARCH_VALIDATION_GATE_v0_1.md` §2 |
| `declared_losses` | `known_loss` | wörtlicher Repo-Begriff (`known_loss_required`, §12 ebd.) |
| `reversibility.rollback_path` | bleibt, dokumentiert als „Rücknahmepfad" | Repo-Begriff „Rücknahmepfad" ebd. §3.1–3.6 |
| `authority_effect.value: NONE` | `none \| requested` | Repo kennt attestiert nur `authority_effect: none`; `requested` drückt den Antrag aus, nicht die Gewährung |
| Validator unter `.claude/skills/.../scripts/` | **beibehalten** (nicht `tools/`) | `tools/README.md`: „These tools enforce the project's governance membrane" — eine Ablage dort würde den Skill als Governance-Membran ausweisen und genau das parallele System erzeugen, das vermieden werden soll |
| Tests | `tests/unit/test_change_gate_manifest.py` | Repo-Konvention (`pyproject.toml` → `testpaths=["tests"]`); Import des Skript-Pfads über `importlib`, da `.claude/` kein Python-Paket ist |

### 2.4 Ausdrücklich nicht berührte Dateien

`.claude/skills/witness_mode.md` · `.claude/rules/*` · `CLAUDE.md` ·
`index/**` · `policies/**` · `spec/**` · `seeds/**` · `VOIDMAP.yml` ·
`data/receipts/**` · `receipts/**` · `ark/**` · `NICHTRAUM/**` · `INBOX/**` ·
`docs/negations.md` · alle bestehenden Tests · alle Workflows · `Makefile` ·
`tools/**` · `src/**` · JS/TS-Workspace (`ui-app/`, `packages/`, Lockfiles).

### 2.5 Vorgesehene Tests

`tests/unit/test_change_gate_manifest.py` mit den zwölf geforderten Fällen:
minimal valides ANNEX-Manifest · fehlendes Pflichtfeld · unbekannter Enum-Wert ·
GOLD-Pfad ohne HumanDecision · HumanDecision ohne konkrete Frage · endgültige
Selbstattestierung · endgültiger `PASS` · mögliches paralleles Statussystem ·
widersprüchliche Pfadfreigaben · Determinismus (identische Eingabe → identische
Ausgabe) · keine Netzwerk-/Prozess-/Write-Nebenwirkungen · GOLD-Präfixe des
Validators sind in `.claude/rules/annex.md` belegt.

### 2.6 Verifikation

`make verify` · `make verify-governance` · zusätzlich fokussiert
`pytest tests/unit/test_change_gate_manifest.py -v`.
`make verify-js` ist **nicht** erforderlich: der Patch berührt keinen der Pfade
aus dem `ci-js-workspace.yml`-Filter.

### 2.7 Mögliche menschliche Entscheidungen (nicht vom Agenten getroffen)

- [ ] ☐ Soll `.claude/` in `.claude/rules/annex.md` explizit klassifiziert werden?
- [ ] ☐ Soll `ELIGIBLE_FOR_EXTERNAL_REVIEW` als gate-lokale Formulierung
      bestätigt oder durch einen anderen bestehenden Begriff ersetzt werden?
- [ ] ☐ Soll der Validator später advisory in eine Make-/CI-Stufe wandern
      (dann greift `GUARD_CHECK_CONTRACT_v0_1.md`)?
- [ ] ☐ Soll `witness_mode.md` perspektivisch in die Verzeichnisform migrieren?
      (**Folgearbeit**, nicht Teil dieses Patches)
- [ ] ☐ Soll der Skill in `docs/masterindex.md` o. ä. verlinkt werden?

---

## 3. Nicht getan (bewusst)

- Keine Migration von `.claude/skills/witness_mode.md`.
- Keine Verdrahtung in `Makefile`, `.github/workflows/` oder `make verify`.
- Keine neuen VOID-Einträge, keine `VOIDMAP.yml`-Änderung.
- Keine neuen Claim-Tags, Statuswerte oder Authority-Klassen.
- Keine Änderung an `tools/README.md` (der Validator ist keine `tools/`-Membran).
- Keine Löschung, keine Verschiebung, keine stille Migration.

## 4. Risiken

- **[RISK]** Der Validator liegt außerhalb von `ruff`/`black`/`mypy`-Scope
  (`src/ tools/ tests/`). Er wird dennoch nach denselben Konventionen
  geschrieben; die Tests laufen in der Verify-Membran mit.
- **[RISK]** Die GOLD-Pfadliste im Validator ist eine **Kopie** der Angaben aus
  `annex.md`. Gegenmaßnahme: Test auf wörtliche Belegbarkeit; Drift wird
  sichtbar, statt still zu bleiben.
- **[RISK]** `ELIGIBLE_FOR_EXTERNAL_REVIEW` wird aus dem Forschungs-Gate in einen
  Change-Gate-Kontext übernommen. Gegenmaßnahme: ausdrückliche Scoping-Notiz
  („gate-lokal, keine automatische Übersetzung"), analog zur HOLD-Regel dort.

---

## 5. Entscheidung

**PROCEED_ANNEX_ONLY**

Bedingungsprüfung:

| Bedingung | Status |
|---|---|
| Änderungen vollständig additiv im ANNEX-/nicht-klassifizierten `.claude/`-Bereich | erfüllt (§1.4, §2.2) |
| Keine GOLD-/IMMUTABLE-/Receipt-/Policy-/VOIDMAP-/NICHTRAUM-Änderung | erfüllt (§2.4) |
| Keine Löschung, keine Verschiebung | erfüllt |
| Keine neue Runtime-Abhängigkeit | erfüllt (`pyyaml` ist Kern-Dependency in `requirements.txt`/`pyproject.toml`) |
| Keine neuen Claim-Tags, Statuswerte, Authority-Klassen | erfüllt (§2.3) |
| Additiv und reversibel | erfüllt (Rücknahme = Verzeichnis nach `NICHTRAUM/archive/` verschieben, G3) |
| Repo-Terminologie eindeutig genug | erfüllt nach Auflösung in §1.2/§2.3 |
| Tests mit vorhandener Toolchain ausführbar | erfüllt (pytest, Baseline `make verify` und `make verify-governance` grün) |

> `PROCEED_ANNEX_ONLY` ist ein lokales Arbeitssignal dieses Berichts. Es ist
> kein Claim-Status, kein Governance-Status und keine Validierung.

---

## Artefakte

- `OUT/entaengelment_change_gate_v0_1_plan.md` (dieser Bericht)
- geplant: `.claude/skills/entaengelment-change-gate/**`, `tests/unit/test_change_gate_manifest.py`
