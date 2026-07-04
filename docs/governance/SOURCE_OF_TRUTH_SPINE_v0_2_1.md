# SOURCE_OF_TRUTH_SPINE_v0_2_1

**Status:** Draft / Intake-Kandidat  
**Datum:** 2026-07-04  
**Claim-Status:** [SPEC-WIP]  
**Geltungsbereich:** Governance-Architektur und Source-of-Truth-Membranen  
**Nicht-Ziel:** Dieses Dokument macht keine Claims wahr. Es beschreibt, wie Claim-Status nachvollziehbar wird.

---

## 1. Kernprinzip

SoT ist kein einzelner Thron und keine statische Datei. SoT entsteht durch kontrollierte Kopplung zwischen vier Schichten:

| Schicht | Hält | Hält nicht |
|---|---|---|
| Repo | Regeln, Policies, Specs, Guard-Definitionen | menschliche Bedeutung |
| Backend / Runtime | Ereignisse, Claim-States, Hash-Chain, Snapshots | Interpretation oder Zustimmung |
| Externe Quellen | Fakten, Messungen, Simulationen, Material Pointers | Geltung oder Sinn |
| Mensch | Bedeutung, Consent, Rücknahme | maschinell erzwingbare Wahrheit |

GitHub ist Witness/Kristall: Es dokumentiert reduced Anchors und Integritätshinweise. GitHub beweist nicht die Wahrheit von Claims.

UI- und Agentenoutput sind Vorschläge und Projektionen, niemals Source of Truth.

---

## 2. Resonance-Glue

„Resonance“ meint hier operative Kopplung und Rückkopplung zwischen Schichten, nicht einen Wahrheitsanspruch.

Vier Glue-Arten:

1. **Cryptographic Glue:** Hash, HMAC, `prev_hash`, `replay_hash`, `snapshotRootHash`; macht Veränderungen prüfbar und tamper-evident innerhalb dokumentierter Annahmen.
2. **Semantic Glue:** Claim-Tags, VOID-Bezug, MaterialPointer-Rollen, Transitionen.
3. **Procedural Glue:** Calm Intake, Sprechakt-Runbook, Claim-Lint, Agenten-Penetration, Guard-Drills, Review.
4. **Human Glue:** Consent, Bedeutung, Rücknahme, Kontextfreigabe.

Glue darf nie dazu führen, dass nicht freigegebene Bedeutung in öffentliche Artefakte diffundiert.

---

## 3. A/B-Trennung

- **B-Schicht:** private Generatoren, innere Symbolik, kreative Experimente, Rosetta-Bilder.
- **A-Schicht:** fremdfähige Policies, Specs, Runbooks, reduzierte Anchors und überprüfbare Prozessregeln.

B kann A erzeugen. A muss allein verständlich bleiben. Rosetta-/Annex-Sprache darf erklären, aber keine Claim-Hochstufung begründen.

---

## 4. Intake-first

Jeder neue Claim, Chat-Treffer oder Artefakt beginnt als ROHSEDIMENT im Calm Intake. Kanonisierung erfolgt nur nach Review, Claim-Status, Geltungsbereich, Evidence- oder VOID-Pfad und Rücknahme-Bedingung.

**VOID-016 Recovery Gate:**

> Ist dieser Treffer wirklich eine frühere Lösung, oder projizieren wir rückwirkend Kohärenz hinein?

Wenn dieser Check nicht bestanden wird, bleibt der Treffer Intake-Sediment oder wird als VOID markiert.

---

## 5. SoT is not a truth-maker

Eine Source of Truth macht Claims nicht wahr. Sie macht ihren Status nachvollziehbar:

- behauptet
- getaggt
- belegt
- offen
- widerlegt
- zurückgenommen
- als VOID akzeptiert

Wahrheit bleibt abhängig von Evidenz, Quelle, Messung, Modellgrenzen und menschlicher Interpretation.

---

## 6. Enforcement-Status

**Already enforced / partially enforced:** bestehender Claim-Lint, Verify-Pointers, DeepJump Verify, Receipt-Lint in vorhandenen Scopes, Intake-Pattern.

**Target enforcement:** Guard-Drill-Lint, Branch-Protection Drift-Check, Runtime Eventlog Claim-Transition Enforcement, vollständige Provenienz-Inversion-Erkennung.

Nur bereits implementierte Checks dürfen als live kommuniziert werden.

---

## 7. Nachgelagerte Artefakte

- `policies/claim_tags_v0_2.yaml`
- `docs/governance/CLAIM_LEITER_v0_1.md`
- `docs/governance/ANTI_CAPTURE_BREADCRUMB_LINT_claim_tags_v0_2.md`
- `docs/governance/GUARD_DRILL_CONTRACT_v0_1.md`
- `spec/runtime_eventlog_v0_1.json`
- `docs/runbooks/AGENT_PENETRATION_RUNBOOK_v0_1.md`
- `docs/runbooks/BODENTEST_PROTOCOL_v0_1.md`
- `docs/governance/BRANCH_PROTECTION_EXPECTED_STATE.yml`
- `docs/annex/RESONANCE_WITHOUT_CAPTURE_zN_SATURN_HEXAGON_v0_1.md`

---

## 8. Motto

> SoT macht Claims nicht wahr. SoT macht ihren Status nachvollziehbar.
