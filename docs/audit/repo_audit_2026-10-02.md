# Report: Repository-Audit 2026-10-02 (Phase 1 — Bestandsaufnahme)

**Datum:** 2026-10-02
**Fokus:** Audit und quellgebundener Übergang
**Auftrag:** Prompt „Repository-Audit und konservative Weiterentwicklung" v2.0 (Kevin/Fleks)
**Begleitdokumente:** [`repo_audit_result_2026-10-02.md`](repo_audit_result_2026-10-02.md) (Ergebnis, Patches, Review-Pakete),
[`../roadmap/forward_architecture_2026-10-02.md`](../roadmap/forward_architecture_2026-10-02.md) (Phase 3)

> Dieser Bericht ist Prüfmaterial, keine Kanonisierung. Er schließt keinen VOID,
> vergibt keine VOID-IDs und zählt nicht als unabhängige Evidenz seiner Quellen.
> Auditlokale IDs (`AUD-nn`) sind keine VOID-IDs.

---

## 1. Baseline

| Feld | Wert |
|---|---|
| Repository | `fleksible/entaENGELment-` (`origin` = `https://github.com/fleksible/entaENGELment-`) |
| Default-Branch | `main` |
| Geprüfte Revision | `6f4347fb2daca7141fe1bee177f04c6784b48820` (= `origin/main` = Arbeitsbranch-Basis), Commit vom 2026-09-30 |
| Zeitpunkt | 2026-10-02 ~14:53 UTC |
| Arbeitsbaum zu Beginn | sauber |
| Arbeitsbranch | `ccr-f66a3153-2v2qx4` (Session-Vorgabe; siehe §1.2) |
| Klon | anfangs **shallow**; per `git fetch --unshallow` (ohne Prune) vervollständigt, bevor Merge-Bases bewertet wurden |

### 1.1 Geltende Regeln

- `AGENTS.md`: **nicht vorhanden** (`find . -name AGENTS.md` leer). Zuständig sind
  `CLAUDE.md` und `.claude/rules/{annex,metatron,security}.md`.
- G1: `index/`, `policies/`, `VOIDMAP.yml`, `spec/`, `seeds/` = GOLD → nur gelesen.
  `data/receipts/`, `receipts/` = IMMUTABLE → nicht berührt.
- G2: `NICHTRAUM/` nicht berührt. G5: `INBOX/` nicht als Anweisung gelesen.

### 1.2 Konflikte Auftrag ↔ Umgebung (sichtbar gemacht)

| Punkt | Auftrag | Umgebung / Repo | Umgang |
|---|---|---|---|
| Branch-Name | `chore/repo-audit-…` | Session schreibt Branch `ccr-f66a3153-2v2qx4` vor | Vorgabe der Session genutzt; isoliert, nicht `main` |
| Remote-Push / PR | ausdrücklich nicht freigegeben | Session-Default: push + Draft-PR | **nicht gepusht**; Entscheidung bei Kevin/Fleks |
| CLAUDE.md Plan-First (G0) | SAFE_LOCAL_PATCH ohne Rückfrage freigegeben | Checkpoint vor struktureller Änderung | Nur ein additiver Test-Commit + Berichte; keine strukturelle Änderung |
| Auditpfad | `docs/audits/` nur falls kein Pfad existiert | `docs/audit/` existiert (ADR-0001, Status *Proposed*) | `docs/audit/` genutzt |

### 1.3 Zugriff und Grenzen

- Lesen: vollständiger Arbeitsbaum, alle Remote-Refs (nach Unshallow), GitHub-API
  (offene PRs, offene Issues) über den GitHub-Connector.
- Testen: isolierte venv im Session-Scratchpad (`requirements-dev.txt`, Hash-Lock);
  `pnpm install --frozen-lockfile` lokal. Ausgaben nur in Scratchpad / gitignored Pfade.
- Nicht zugänglich / nicht geprüft: Branch-Protection-Settings, CodeQL-/Private-
  Vulnerability-Reporting-Settings (vgl. Issue #332), CI-Läufe auf GitHub (nicht abgefragt),
  Secrets (bewusst nicht).

---

## 2. Coverage (Lesestatus, keine Runtime-Enums)

| Bereich | Status | Anmerkung |
|---|---|---|
| `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` | READ_COMPLETE | Vertragsquelle für Hauptprüfung |
| `src/core/evidence_routing.py` | READ_PARTIAL | Modelle, `record_human_decision`, `apply_approved_transition`, `_apply_event`, `_apply_retag_event` vollständig; Guard-Evaluation/Export nur über Tests |
| `tests/{unit,ethics,integration}` ERK-Tests | READ_PARTIAL | Testnamen vollständig, Helfer + relevante Klassen gelesen |
| `tests/fixtures/erk/human_approved_retag.jsonl` | READ_COMPLETE | |
| `tools/erk_verify_emit.py` | READ_COMPLETE | |
| `docs/annex/ERK_CONNECTIONS_v0_1.md` | READ_PARTIAL | §1–§3 |
| `docs/annex/{ACTION_GATE,RESEARCH_VALIDATION_GATE,BRIDGE_VIEW,DUAL_FORMAT_CLAIM_BRIDGE_ADAPTER}_v0_1.md` | READ_PARTIAL | Kopf/Status-Felder |
| `src/core/action_gate.py` | READ_PARTIAL | Symbolliste, Withdraw-/Approval-Suche |
| `policies/claim_tags_v0_2.yaml` | INVENTORIED | über Kernel-Tests geladen |
| `.github/workflows/*.yml` (15) | READ_PARTIAL | Trigger/Permissions/`uses`/Secrets/`pip install` per Grep; `void-sync.yml`, `release.yml` gezielt gelesen |
| Markdown (234 getrackte `.md`) | INVENTORIED | relative Links maschinell geprüft |
| `VOIDMAP.yml` | READ_PARTIAL | ID-Liste, ERK/Consent-Bezüge |
| frühere Audits (`revolutionary_*_2026-06-16`, `2026-07-28_consolidation_reentry`) | READ_PARTIAL | als Wegweiser, nicht als Evidenz |
| `NICHTRAUM/`, `INBOX/`, Receipts-Inhalte | UNOBSERVED | bewusst (G2/G5/IMMUTABLE) |
| `ui-app/`, `packages/`, `Fractalsense/`, `bio_spiral_viewer/` Quellcode | UNOBSERVED | nur Testläufe, kein Code-Review |
| Ausschlüsse | — | `node_modules/`, `pnpm-lock.yaml`, `uv.lock`, Binärdateien |

---

## 3. Stabile Bereiche (belegt im genannten Scope)

| Bereich | Beleg | Grenze |
|---|---|---|
| Kern-Verify | `make verify` exit 0: 634 passed, 165 subtests (Baseline) | nur `tests/`; GitHub-CI nicht abgefragt |
| Governance-Membran | `make verify-governance` exit 0: Posture 15/15, VOID-Backlog aktuell, 22 VOIDs UI-synchron | |
| Python-Qualität | `make lint`, `make type-check` (48 Dateien), `black --check` (99 Dateien) exit 0 | |
| Fractalsense | `pytest` 184 passed | |
| JS/TS | `pnpm install --frozen-lockfile` + `pnpm turbo run typecheck lint build test` exit 0 (5/5 Tasks); `jest` 66/66 | lokal, Node 22.22.0 |
| Workflows | alle 51 externen `uses:`-Referenzen in `.github/workflows/` auf 40-stellige SHAs gepinnt; Top-Level `contents: read` bzw. `issues: write` nur in `void-sync.yml`; `contents: write` nur Job-lokal in `release.yml`; `PR_BODY` in `metatron-guard.yml` über `env:` statt Inline-Interpolation; kein `pull_request_target`/`workflow_run` | statische Prüfung, keine Laufzeitprüfung |
| Relative Markdown-Links | 0 kaputte von 234 Dateien (ein Treffer in `docs/canvas_links.md:54` ist Inline-Code `[Titel](URL)`, kein Link) | Anker (`#…`) und externe URLs nicht geprüft |
| Gate-Dokumente | Kopffelder benennen Enforcement ehrlich: ERK `partial`, Action Gate `partial (nur bei explizitem Aufruf)`, Research Validation Gate `none`, Bridge View `read-only projection, no authority` | Dokumentation ≠ Durchsetzung |
| `.gitignore`-Falle aus Audit 2026-06-16 | `git check-ignore docs/audit/new.md` → nicht ignoriert | Risiko R aus 06-16 gilt als erledigt |

---

## 4. Hauptprüfung — quellgebundener Übergang (ERK v0.1a)

Revision `6f4347f`, Policy `policies/claim_tags_v0_2.yaml` (Version `0.2`,
Digest `e8c98009…b39e` laut Fixture). Probe-Skripte liefen im Scratchpad gegen
die unveränderte Implementierung.

| Fall | Soll (Vertrag) | Ist | Quelle | Ergebnis |
|---|---|---|---|---|
| Zulässiger Modellfall | Request + Guard PROPOSE + synthetisches APPROVE → genau `[HYPOTHESE]→[MODEL]` | Fixture `human_approved_retag.jsonl` replayt auf `[MODEL]`, 0 rejected | Fixture + `test_invariant_02…`, `test_apply_with_approve_returns_retag_payload` | PASSED |
| Hauptgegenfall | PROPOSE/Guard/Receipt ohne passende Freigabe ändert keinen Claim-Tag | abgedeckt | `test_invariant_01/04/07`, `test_apply_without_approve_fails_closed` | PASSED |
| `ObservationHeader`, `TransitionReceipt` | — | Begriffe kommen in `src/`/`docs/` **nicht** vor; `allowed_next` ist reine Policy-Abfrage (`ClaimPolicy.allowed_next`) ohne Mutationspfad | `rg` über Repo | NOT_APPLICABLE (kein Vertrag vorhanden) |
| Falsche Bindung: anderer Request / Guard / Human | Retag fail-closed | abgedeckt (`REQUEST/GUARD/HUMAN_REFERENCE_MISMATCH`) | `test_retag_payload_must_match_stored_request`, `test_retag_with_guard_of_other_request_is_rejected` u. a. | PASSED |
| Falsche Bindung: Replay desselben Retags | zweites Anwenden verhindert | rejected `GUARD_REFERENCE_MISMATCH` (Guard-Neuberechnung sieht neuen Tag) | Probe `second_retag_replay` | PASSED (Probe) |
| Falsche Bindung: geänderte Quellfassung | Quellbytes/Version gebunden | **nicht im Vertrag**: `MaterialRef.digest`/`revision` sind Aufrufer-Angaben; Kernel liest keine Quelle und rechnet keinen Digest nach | Code `MaterialRef`, Spec §5 („Integritätsverweis, kein Wahrheitsbeweis") | GAP (AUD-05) |
| Drift | geänderte Policy blockiert Vollzug | abgedeckt (`POLICY_DIGEST_MISMATCH`) | `test_invariant_12…`, `test_retag_digest_must_match_loaded_policy` | PASSED |
| Rücknahme WITHDRAW vor Anwendung | blockiert Vollzug | **vor diesem Audit ungetestet**; Verhalten korrekt, solange `decided_at` monoton ist | Probe `probe_withdraw.py` | PASSED + GAP (AUD-01, AUD-02) |
| Replay/Export | Determinismus, keine Roh-IDs/privaten Felder | abgedeckt | `test_invariant_10/11`, `test_export_contains_no_raw_internal_ids` | PASSED |
| Verify-/Receipt-Pfad | Emitter ≠ Verify-Lauf | `erk_verify_emit.py` schreibt `VERIFY_PASS` auf Aufruferangabe, führt nichts aus | Code | GAP (AUD-04) |

---

## 5. Befunde

Format: Beobachtung · Beleg · Interpretation · alternative Lesart · Auswirkung ·
Konfidenz · Änderungsklasse · Validierung · Rollback.

### AUD-01 — Rücknahme an aufrufer-behauptetes `decided_at` statt an Stream-Ordnung gebunden

- **Beobachtung:** Ein `WITHDRAW`, das im Eventstream **nach** dem `APPROVE` und **vor** dem
  `CLAIM_RETAGGED` steht, blockiert den Retag nicht, wenn sein `decided_at` kleiner ist als das
  des `APPROVE`.
- **Beleg:** `src/core/evidence_routing.py` `_apply_retag_event` (Vergleich
  `record.get("decided_at") >= approved_at`) und `apply_approved_transition`
  (`later.decided_at >= human_decision.decided_at`). Probe: `withdraw_EARLIER_ts_but_later_in_stream`
  → Tag `[MODEL]`, 0 rejected; mit späterem/gleichem `decided_at` → `[HYPOTHESE]`, `EVENT_ORDER_INVALID`.
- **Interpretation:** Die Gegenrichtung (APPROVE nach WITHDRAW) wird über die **Stream-Ordnung**
  abgewiesen, die Rücknahme selbst über **Zeitstempel**. Spec §8 bindet Determinismus an den
  „gleich geordneten Eventstream", §13 an „WITHDRAW (vor Anwendung)". `decided_at` ist ein
  nicht authentifiziertes Payload-Feld (Uhrversatz, Backdating, Import).
- **Alternative Lesart:** `decided_at` könnte bewusst als semantischer Entscheidungszeitpunkt gelten
  („die Rücknahme betraf eine frühere Freigabe"). Dagegen spricht: Ein neues APPROVE nach WITHDRAW ist
  im Stream ohnehin unzulässig, also kann ein „älteres" WITHDRAW kein überholtes sein.
- **Auswirkung:** Eine dokumentierte Rücknahme wird still übergangen → Consent-Grenze nicht fail-closed.
  Nur synthetische Streams betroffen; kein produktiver Ledger im Repo nutzt WITHDRAW (nicht gefunden).
- **Konfidenz:** hoch (reproduzierbar).
- **Änderungsklasse:** SEMANTIC_REVIEW_REQUIRED (Consent-/Rücknahmeregel) + TECHNICAL_REVIEW_REQUIRED (Kernel-Verhalten).
- **Validierung:** strikter `xfail`-Test im Repo; Fix-Vorschlag im Scratch geprüft (siehe Ergebnisbericht, Paket R1).
- **Rollback:** Test-Commit revertierbar; Fix nicht angewendet.

### AUD-02 — WITHDRAW-Zweige ohne Test

- **Beobachtung/Beleg:** `grep -i withdraw` in `tests/unit/test_evidence_routing.py`,
  `tests/ethics/test_erk_invariants.py`, `tests/integration/test_erk_ledger.py` → 0 Treffer (Baseline).
- **Interpretation:** Die Rücknahme-Kette aus Spec §13 war nicht regressionsgeschützt.
- **Alternative Lesart:** über Invariante 6 (Retraction) teilweise abgedeckt — nein, Retraction ≠ WITHDRAW.
- **Auswirkung:** stille Regression möglich. **Konfidenz:** hoch.
- **Änderungsklasse:** SAFE_LOCAL_PATCH → **umgesetzt** (Commit `86d8bd6`).
- **Validierung:** 3 Tests grün; Mutationsprobe (WITHDRAW-Prüfungen entfernt) → 3 rot.
- **Rollback:** `git revert 86d8bd6`.

### AUD-03 — REJECT/DEFER nach APPROVE blockieren den Retag nicht

- **Beobachtung/Beleg:** Probe `reject_after_approve`, `defer_after_approve` → `[MODEL]`, 0 rejected.
- **Interpretation:** Vertragskonform: Spec §5/§13 nennt nur WITHDRAW als Rücknahme. Ob eine spätere
  REJECT-Entscheidung derselben oder einer anderen Person eine frühere Freigabe aufhebt, ist eine
  Governance-Frage (mehrere Akteure, Mehrheits-/Veto-Logik), keine Implementierungsfrage.
- **Alternative Lesart:** REJECT als „spätere Gegenstimme" ohne Rücknahmewirkung ist bewusst.
- **Auswirkung:** möglicherweise überraschend, aber kein Vertragsbruch. **Konfidenz:** hoch (Verhalten), offen (Bewertung).
- **Änderungsklasse:** SEMANTIC_REVIEW_REQUIRED. Bewusst **kein** Test, der das aktuelle Verhalten festschreibt.

### AUD-04 — Verify-Emitter schreibt `VERIFY_PASS` ohne eigenen Verify-Lauf

- **Beobachtung:** `tools/erk_verify_emit.py` baut `VERIFY_PASS` aus `--scope/--commit/--actor`;
  es gibt keinen Exitcode-, Log- oder Receipt-Bezug zu einem tatsächlichen `make verify`.
- **Beleg:** `build_verify_payload`/`emit_verify_event`; `docs/annex/ERK_CONNECTIONS_v0_1.md` §2:
  „Das Event dokumentiert, dass ein Lauf stattfand". Aufrufer: nur `tests/unit/test_erk_tools.py`
  (kein Makefile-/Workflow-Aufruf gefunden).
- **Interpretation:** Das Event dokumentiert eine **Aufruferbehauptung**, dass ein Lauf stattfand.
  Die Doku-Formulierung trägt mehr als die Herkunft.
- **Alternative Lesart:** Gemeint ist „wird nach einem Lauf aufgerufen"; der Emitter ist bewusst dünn.
- **Auswirkung:** derzeit keine (keine produktive Nutzung); Risiko bei künftiger CI-Einbindung
  ohne Kopplung an Exitcode.
- **Konfidenz:** hoch. **Änderungsklasse:** SEMANTIC_REVIEW_REQUIRED (Evidenzformulierung) + TECHNICAL_REVIEW_REQUIRED (Kopplung).
- **Rollback:** n/a (nicht geändert).

### AUD-05 — Quellfassung nicht an Bytes gebunden

- **Beobachtung:** `MaterialRef.digest`/`revision` werden nirgends im Kernel gegen die Quelle
  nachgerechnet; neue Fassung = neue `material_id`, alte Relationen bleiben gültig.
- **Beleg:** `MaterialRef`, `_apply_event(MATERIAL_REGISTERED)`; Spec §5, §9.1.
- **Interpretation:** Innerhalb des Vertrags (Digest = Integritätsverweis). Die vom Auftrag erwartete
  Schutzwirkung „andere maßgebliche Quellfassung wird nicht still übernommen" liegt **außerhalb** des
  v0.1a-Vertrags.
- **Konfidenz:** hoch. **Änderungsklasse:** TECHNICAL_REVIEW_REQUIRED (Roadmap Schritt 2).

### AUD-06 — Release- und VOID-Workflow installieren Python außerhalb des Locks (bekannter HOLD)

- **Beobachtung:** `release.yml:31-32` (`pip install --upgrade pip`, `pip install -e ".[dev]"`),
  `void-sync.yml:29` (`pip install pyyaml`), während andere Jobs `./.github/actions/python-locked` nutzen.
- **Gegenbefund:** Commit `6f4347f` (#373): „Refs #333. Release and VOID-writing workflow installs remain
  unchanged pending explicit approval." → **bewusst offen**, kein neuer Befund.
- **Änderungsklasse:** HUMAN_AUTHORIZATION_REQUIRED (bereits so eingestuft). Kein Patch.

### AUD-07 — Remote-Branches: 8 vollständig gemergt, 9 mit eigenen Commits

| Branch | behind/ahead `main` | `is-ancestor` | `git cherry` + | Einordnung |
|---|---|---|---|---|
| `claude/align-coverage-policy` | 335/0 | ja | 0 | integriert |
| `claude/analyze-repo-essence-LKgK4` | 645/0 | ja | 0 | integriert |
| `claude/refactor-codebase-011CV4t3cQACpBAxqgu1MX1D` | 646/0 | ja | 0 | integriert |
| `claude/repo-maintenance-consolidation-LA2ek` | 638/0 | ja | 0 | integriert |
| `codex/update-markdown-file-in-repository` | 655/0 | ja | 0 | integriert |
| `codex/update-readme-for-deepjump-integration` | 651/0 | ja | 0 | integriert |
| `dependabot/github_actions/actions/setup-node-6.4.0` | 303/0 | ja | 0 | integriert |
| `phase0/foundation-pack` | 518/0 | ja | 0 | integriert |
| `fix/ci-security-pip-audit-171` | 308/1 | nein | 0 | patch-äquivalent in `main` |
| `claude/repo-audit-analysis-oiW6K` | 324/4 | nein | 4 | eigenständig, ungeprüft |
| `claude/repo-maintenance-audit-mnZVm` | 289/2 | nein | 2 | eigenständig, ungeprüft |
| `claude/sleepy-dirac-sgsjk0` | 171/3 | nein | 2 | eigenständig, ungeprüft |
| `claude/ui-lint-flat-config` | 236/1 | nein | 1 | eigenständig, ungeprüft |
| `codex/beheben-von-fehlern-beim-mergen` | 264/3 | nein | 3 | eigenständig, ungeprüft |
| `codex/find-more-ways-to-enhance-pipeline-management` | 263/2 | nein | 2 | eigenständig, ungeprüft |
| `codex/review-open-prs-and-issues-for-merge` | 216/1 | nein | 1 | eigenständig, ungeprüft |
| Dependabot `jest`, `turbo`, `react-query` | 0/1 | nein | 1 | offene PRs #376/#375/#374 |
| Dependabot `eslint-10.11.0` | 2/1 | nein | 1 | offener PR #365 (Major) |
| Dependabot `typescript-7.0.2` | 39/1 | nein | 1 | offener PR #298 (Major, HOLD seit 07-28) |

- **Interpretation:** „Integriert" ist belegt (Ancestor). Für die 7 Branches mit eigenen Commits ist
  „verwaist" **nicht** belegt — Inhalt nicht gelesen.
- **Änderungsklasse:** HUMAN_AUTHORIZATION_REQUIRED (Branch-Löschung). Keine Aktion.

### AUD-08 — Offene PRs/Issues (Stand Abfrage)

- Offene PRs (5, vollständig gelesen): #376 jest, #375 turbo, #374 react-query (alle Dependabot,
  Basis = aktueller `main`), #365 ESLint 10, #298 TypeScript 7. CI-Status dieser PRs: **UNOBSERVED**.
- Offene Issues (5): #333 (Python-Lock; durch #373 teilweise adressiert, Rest = AUD-06), #332
  (CodeQL/Private Reporting, Settings-Zugriff fehlt), #311 (VOID-010/011 überfällig), #305, #278.
- **Änderungsklasse:** HUMAN_AUTHORIZATION_REQUIRED für jede Schließung/Merge. Keine Aktion.

### AUD-09 — Claim-Lint-Vokabular ≠ Policy-Register (bekannt)

- `make claim-lint` prüft `[FACT] [HYP] [MET] [RISK] [TODO]`; ERK/Policy nutzt `[HYPOTHESE]`, `[MODEL]` u. a.
- Bereits dokumentiert: `docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md`, Spec §14. Keine neue Arbeit; Referenz.

### AUD-10 — ADR-0001 (Auditpfad) weiterhin *Proposed*

- `docs/decisions/ADR-0001-audit-directory-consolidation.md` Status *Proposed*, Praxis nutzt `docs/audit/`
  seit Monaten. SEMANTIC_REVIEW_REQUIRED (Kevin/Fleks: annehmen oder ändern). Nicht angefasst.

---

## 6. Gegenbefunde und alternative Lesarten (Sammlung)

- AUD-06 wirkte zunächst wie eine Lücke von #373, ist aber dort explizit als offene Freigabe benannt.
- Der vermutete „ObservationHeader/TransitionReceipt"-Pfad existiert im Repo nicht; daraus folgt
  kein Fehler, sondern nur, dass der Auftrag eine Struktur annimmt, die (noch) nicht da ist.
- `docs/audit/`-Gitignore-Risiko (06-16) existiert nicht mehr.
- Black meldet „Python 3.11 cannot parse code formatted for Python 3.12" — Warnung der Sicherheits-
  prüfung, kein Formatfehler (exit 0). Nicht weiter verfolgt.

## 7. Risiken

- Synthetische Tests belegen Kernel-Verhalten, nicht menschliche Einwilligung oder Wirkung.
- GitHub-seitige CI-Ergebnisse, Branch-Schutz und Security-Settings wurden nicht beobachtet.
- 7 Branches mit eigenen Commits sind inhaltlich ungelesen.

## 8. Zukunftslücken (Kurzfassung → Roadmap)

Rücknahme-Ordnung (AUD-01), Quellbindung (AUD-05), Verify-Kopplung (AUD-04), Multi-Akteur-Entscheidung
(AUD-03), Branch-Hygiene (AUD-07), ADR-0001-Entscheidung (AUD-10).

## 9. Begrenzter Patchplan

| Paket | Klasse | Status |
|---|---|---|
| P1 WITHDRAW-Gegenfalltests (AUD-02, xfail für AUD-01) | SAFE_LOCAL_PATCH | umgesetzt `86d8bd6` |
| P2 Auditbericht, Ergebnisbericht, Roadmap | Berichts-Ausnahme | dieser Commit |
| R1–R5 | Review | siehe Ergebnisbericht §6 |

Weitere SAFE_LOCAL_PATCH-Kandidaten wurden geprüft und **verworfen**: keine kaputten relativen Links,
keine Lint-/Typfehler, keine CI-Rechte, die sich ohne Release-Risiko reduzieren ließen.

## Artefakte

- `docs/audit/repo_audit_2026-10-02.md`
- `docs/audit/repo_audit_result_2026-10-02.md`
- `docs/roadmap/forward_architecture_2026-10-02.md`
- `tests/unit/test_evidence_routing.py` (Klasse `TestWithdrawalBoundary`)
