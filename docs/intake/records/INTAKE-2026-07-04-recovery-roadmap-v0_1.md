# INTAKE-2026-07-04-recovery-roadmap-v0_1

**Status:** ROHSEDIMENT / Shadow-Copy / Intake-Kandidat  
**Datum:** 2026-07-04  
**Zweck:** Intake-Record für den Recovery-Zyklus rund um SoT-Spine, Claim-Tags, Breadcrumb-Lint, Runtime Eventlog, Agenten-Penetration, Boden-Test und Rosetta-Annex.

---

## Zugehörige neue PR-Artefakte

- `docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md`
- `policies/claim_tags_v0_2.yaml`
- `docs/governance/CLAIM_LEITER_v0_1.md`
- `docs/governance/BREADCRUMB_LINT_claim_tags_v0_2.md`
- `spec/runtime_eventlog_v0_1.json`
- `docs/governance/RUNTIME_EVENTLOG_SPINE_v0_1.md`
- `docs/governance/GUARD_CHECK_CONTRACT_v0_1.md`
- `docs/runbooks/AGENT_PENETRATION_RUNBOOK_v0_1.md`
- `docs/runbooks/BODENTEST_PROTOCOL_v0_1.md`
- `docs/governance/BRANCH_EXPECTED_STATE.yml`
- `docs/annex/ROSETTA_INTERVALS_v0_1.md`

---

## Kurzbefund

Der Recovery-Zyklus trennt drei Zonen:

1. Bereits vorhandene Repo-Anker wie Privacy Boundary, GitHub Use Policy, VOIDMAP, Intake, Runtime Ledger, F7/QM und Consent-Re-Entry.
2. Neue Governance-Drafts wie SoT-Spine, Claim-Tags, Claim-Leiter, Breadcrumb-Lint und Runtime Eventlog.
3. Rosetta-/Annex-Material, das die Begriffsarbeit erklärt, aber keine Claims beweist.

---

## VOID-016 Check

Frage: Wird rückwirkend Kohärenz in alte Spuren projiziert?

Vorläufige Antwort: Risiko reduziert, aber nicht null. Der Zyklus bleibt deshalb Intake-Kandidat und braucht Review, Claim-Lint und später Boden-Test.

---

## Nächste Gates

- PR-Checks abwarten.
- Keine Zielzustände als already enforced kommunizieren.
- Nach Merge: Folge-PRs für Tooling und eventuelle Linter-Integration planen.
