# Report: Repository-Audit 2026-10-02 — Ergebnis

**Datum:** 2026-10-02
**Fokus:** Audit-Ergebnis und Review-Pakete
**Phase-1-Bericht:** [`repo_audit_2026-10-02.md`](repo_audit_2026-10-02.md)
**Roadmap:** [`../roadmap/forward_architecture_2026-10-02.md`](../roadmap/forward_architecture_2026-10-02.md)

---

## Aktueller Abschlussstand (maßgeblich; ersetzt die Zeitangaben der Abschnitte darunter)

Die Abschnitte ab „Ziel“ dokumentieren den Stand bei Audit-Abschluss (lokal, ungepusht).
Danach hat Kevin/Fleks Push, Draft-PR und mehrere Review-Pakete freigegeben. Stand dieses
Blocks: Korrektur-Commit nach `9da5a57` auf PR #377 (seine eigene ID steht im PR, nicht hier).

| Commit | Inhalt | Freigabe |
|---|---|---|
| `86d8bd6` | WITHDRAW-Gegenfalltests (AUD-02), xfail für AUD-01 | Auftrag (SAFE_LOCAL_PATCH) |
| `abc7ed7` | Audit-, Ergebnis-, Roadmap-Bericht | Auftrag |
| `be7b25e` | R1: WITHDRAW an Stream-Ordnung (AUD-01), Spec §13 | Kevin/Fleks |
| `bc87b67` | R3: Verify-Emitter als Aufruferangabe (AUD-04) | Kevin/Fleks |
| `ccb3581` | ADR-0005 angelegt (AUD-03) | Kevin/Fleks |
| `36c8569` | A2 umgesetzt — lockerere Variante, später korrigiert | Kevin/Fleks (A2) |
| `9da5a57` | R5 teilweise: ADR-0001 *Accepted*, Branch-SHAs | Kevin/Fleks |
| Korrektur-Commit | Review PR #377: A2 in entschiedener Fassung, Apply-Historienscope, State-Digest bindet Entscheidungsreihenfolge, dieser Block | Review PR #377 |

**Geänderte Dateien gesamt:** `src/core/evidence_routing.py`, `tools/erk_verify_emit.py`
(nur Docstring), `tests/unit/test_evidence_routing.py`,
`docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` (§8, §13), `docs/annex/ERK_CONNECTIONS_v0_1.md` (§2),
`docs/decisions/ADR-0001-…` (Status), `docs/decisions/ADR-0005-…` (neu),
drei Audit-/Roadmap-Berichte (neu). Nicht berührt: Workflows, Policies, GOLD, Receipts,
VOIDMAP, `NICHTRAUM/`.

**Tests am Korrekturstand (lokal, isolierte venv):** `make verify` 657 passed, 165 subtests;
ERK-Suiten (unit/ethics/integration) 97 passed; ruff, mypy, black sauber. Gegen den Kernel
von `9da5a57` schlagen genau die sechs neuen Review-Regressionstests fehl. GitHub-CI für den
Korrekturstand: siehe PR.

| Paket | Stand |
|---|---|
| R1 (AUD-01) | umgesetzt |
| R2 (AUD-05, Quellbytes) | offen |
| R3 (AUD-04) | Variante a umgesetzt; S3b (Kopplung an echten Lauf) offen |
| R4 (AUD-03) | ADR-0005 *Accepted* (A2), umgesetzt und per Review korrigiert |
| R5 / AUD-10 | ADR-0001 *Accepted* |
| R5 / AUD-06 | Diffs validiert, **nicht angewendet** (Agent-Berechtigung blockiert Workflow-Änderung) |
| R5 / AUD-07 | 8 gemergte Branches **nicht gelöscht**; Bestätigung offen |
| PR #377 | Draft; Merge nur durch Kevin/Fleks |

Technik, semantische Review und menschliche Freigabe bleiben getrennt: Grüne Tests belegen
das Kernel-Verhalten an synthetischen Streams, keine reale Einwilligung oder authentifizierte
Akteure.

---

## Ziel

Struktur, Branches, Workflows, Doku und Code an fester Revision prüfen; nachweisbare
Schwächen in kleinen, reversiblen Paketen beheben; Zukunftsarchitektur als Vorschlag.

## 1. Baseline, Abschluss, Coverage

| Feld | Wert |
|---|---|
| Baseline | `6f4347fb2daca7141fe1bee177f04c6784b48820` (`origin/main`, 2026-09-30) |
| Arbeitsbranch | `ccr-f66a3153-2v2qx4` (lokal; **nicht gepusht**, siehe §9) |
| Getesteter Code-Stand | `86d8bd6` (= Baseline + Testdatei-Erweiterung; `src/` unverändert) |
| Abschluss | Berichts-Commit auf `86d8bd6` (nur `docs/`; ändert keinen getesteten Code — seine eigene ID wird hier bewusst nicht genannt) |
| Coverage | siehe Phase-1-Bericht §2 (READ_COMPLETE / READ_PARTIAL / INVENTORIED / UNOBSERVED) |

## 2. Prüfungen

Umgebung: Python 3.11.15 in isolierter venv (Scratchpad, `requirements-dev.txt` mit Hashes),
Node 22.22.0, pnpm 10.33.0. Keine Secrets, keine Netz-Nebenwirkungen außer Paket-Downloads
und `git fetch --unshallow`.

| Prüfung | Befehl | Stand | Exit | Ergebnis |
|---|---|---|---|---|
| Kern-Verify | `make verify PY=<venv>/python` | `6f4347f` | 0 | PASSED — 634 passed, 165 subtests |
| Kern-Verify | dto. | `86d8bd6` | 0 | PASSED — 637 passed, 1 xfailed, 165 subtests |
| Governance | `make verify-governance` | `6f4347f` | 0 | PASSED — Posture 15/15, Backlog aktuell, 22 VOIDs synchron |
| Lint | `make lint` (ruff) | beide | 0 | PASSED |
| Typen | `make type-check` (mypy, 48 Dateien) | `6f4347f` | 0 | PASSED |
| Format | `black --check src tools tests` | `6f4347f` | 0 | PASSED (99 Dateien) |
| Fractalsense | `cd Fractalsense && python -m pytest` | `6f4347f` | 0 | PASSED — 184 |
| JS-Workspace | `pnpm install --frozen-lockfile && pnpm turbo run typecheck lint build test` | `6f4347f` | 0 | PASSED — 5/5 Tasks |
| Jest | `npx jest` | `6f4347f` | 0 | PASSED — 66/66 |
| Relative MD-Links | Scratchpad-Skript über 234 getrackte `.md` | `6f4347f` | — | PASSED — 0 kaputt (1 Fehltreffer in Inline-Code) |
| ERK-Probe Withdraw | `probe_withdraw.py` (Scratchpad) | `6f4347f` | — | FAILED-Fall belegt (AUD-01) |
| ERK-Probe Reject/Defer/Replay | `probe2.py` (Scratchpad) | `6f4347f` | — | Verhalten dokumentiert (AUD-03) |
| Mutationsprobe P1 | WITHDRAW-Prüfungen in Scratch-Kopie entfernt | — | 1 | erwartetes Rot: 3 failed |
| Fix-Probe R1 | Fix in Scratch-Kopie, ERK-Suiten | — | 1 | 77 passed, xfail → XPASS(strict) (gewollt) |
| `make status` / `make snapshot` | — | — | — | NOT_RUN (kein Secret; nicht nötig für Befunde) |
| GitHub-CI-Läufe | — | — | — | NOT_RUN (nicht abgefragt) |
| Branch-Schutz / Security-Settings | — | — | — | BLOCKED (kein Settings-Zugriff) |

Ein grüner Lauf belegt nur seine geprüften Bedingungen; synthetische ERK-Tests ersetzen
weder authentifizierte Zustimmung noch einen Nachweis menschlicher Wirksamkeit.

## 3. Geänderte Dateien und Commits

| Commit | Datei | Diff | Klasse |
|---|---|---|---|
| `86d8bd6` | `tests/unit/test_evidence_routing.py` | +77 (Klasse `TestWithdrawalBoundary`) | SAFE_LOCAL_PATCH |
| Berichts-Commit | `docs/audit/repo_audit_2026-10-02.md`, `docs/audit/repo_audit_result_2026-10-02.md`, `docs/roadmap/forward_architecture_2026-10-02.md` | neu | Berichts-Ausnahme |

Nicht geändert: `src/`, `tools/`, Workflows, Policies, GOLD, Receipts, `NICHTRAUM/`, VOIDMAP.
Geprüfter Unterschied der Teständerung: rein additiv, keine bestehende Assertion geändert,
keine Fixture verändert (die Tests konstruieren Zusatz-Events in-memory).

## 4. Technik / semantische Review / menschliche Freigabe — getrennt

- **Technik (belegt):** Kern-, Governance-, Python-, Fractalsense- und JS-Gates lokal grün.
  ERK hält im Vertrag: Request-/Guard-/Human-Bindung, Policy-Drift, Replay, Export.
  Abweichung: AUD-01 (Rücknahme-Zeitstempel).
- **Semantische Review (offen):** AUD-01 Rücknahmeregel, AUD-03 Mehr-Akteur-Regel,
  AUD-04 Evidenzformulierung des Verify-Emitters, AUD-10 ADR-0001.
- **Menschliche Freigabe (ausstehend):** Push/PR dieses Branches, AUD-06 (Release-/VOID-Workflow-Lock),
  AUD-07 Branch-Löschungen, Issue-/PR-Entscheidungen (#298, #365, #333, #332, #311).

## 5. Bewusst erhaltene Auffälligkeiten

| Auffälligkeit | Grund |
|---|---|
| Kernel-Verhalten AUD-01 | Consent-/Rücknahme-Semantik; nur als xfail markiert, Fix als Paket R1 |
| REJECT/DEFER nach APPROVE (AUD-03) | vertragskonform; kein Test, der es festschreibt |
| `release.yml`/`void-sync.yml` ungelockt (AUD-06) | in #373 ausdrücklich auf Freigabe zurückgestellt |
| 8 gemergte Remote-Branches | Löschung = HUMAN_AUTHORIZATION_REQUIRED |
| Claim-Lint- vs. Register-Vokabular (AUD-09) | bekannt, dokumentiert; Angleichung wäre globale Normalisierung |
| Neue VOIDs | keine angelegt; Vorschlag nur in R1/R4 |

## 6. Review-Pakete

### R1 — Rücknahme an Stream-Ordnung binden (AUD-01)

> **Status-Nachtrag 2026-10-02:** Entscheidung Kevin/Fleks „Stream-Ordnung ist maßgeblich".
> Umgesetzt im Folge-Commit dieses Branches (Replay-Pfad wie unten; `apply_approved_transition`
> nach Variante a: jedes übergebene `WITHDRAW` des Requests blockiert). xfail-Marker entfernt,
> Spec §13 ergänzt. Der folgende Text beschreibt den Stand vor der Umsetzung.

- **Klasse:** SEMANTIC_REVIEW_REQUIRED + TECHNICAL_REVIEW_REQUIRED
- **Vorschlag (Replay-Pfad), im Scratch geprüft:**

```diff
--- a/src/core/evidence_routing.py
+++ b/src/core/evidence_routing.py
@@ -1421,11 +1421,10 @@ def _apply_retag_event(...)
-    approved_at = approval.get("decided_at", 0.0)
     for record in _human_decisions_for_request(state, request_id):
-        if record.get("decision") == HUMAN_WITHDRAW and record.get("decided_at", 0.0) >= float(
-            approved_at
-        ):
+        # Stream order is authoritative: every WITHDRAW already replayed for
+        # this request precedes the retag, whatever its asserted decided_at.
+        if record.get("decision") == HUMAN_WITHDRAW:
             raise EvidenceRoutingError(
```

- **Plus:** `xfail`-Marker in `TestWithdrawalBoundary` entfernen (strict erzwingt das).
- **Offen:** `apply_approved_transition(human_decisions=...)` erhält eine ungeordnete Liste;
  Alternative a) jedes WITHDRAW blockiert, b) Zeitstempel beibehalten und Parameter-Doku schärfen.
- **Nutzen:** Rücknahme fail-closed, symmetrisch zu „APPROVE nach WITHDRAW".
- **Risiko:** Streams, die WITHDRAW mit älterem `decided_at` als „historisch überholt" meinen, würden
  nun blockieren — im Repo nicht gefunden.
- **Validierung:** 77 ERK-Tests grün, xfail → XPASS(strict), ruff sauber (Scratch).
- **Rollback:** Revert des Fix-Commits.
- **VOID:** kein passender VOID gefunden; neuer Eintrag nur als Vorschlag, falls gewünscht.

### R2 — Quellbytes-Bindung (AUD-05)

- **Klasse:** TECHNICAL_REVIEW_REQUIRED. Lesender Prüfer in `tools/`, Kernel bleibt dateifrei.
  Alternative: Status quo + Spec-Hinweis. Details Roadmap S2.

### R3 — Evidenzformulierung Verify-Emitter (AUD-04)

> **Status-Nachtrag 2026-10-02:** Formulierung von Kevin/Fleks übernommen; umgesetzt in
> `docs/annex/ERK_CONNECTIONS_v0_1.md` §2 und im Modul-Docstring von `tools/erk_verify_emit.py`.
> Kein Verhaltenswechsel; die Kopplung an einen echten Lauf (Roadmap S3b) bleibt offen.

- **Klasse:** SEMANTIC_REVIEW_REQUIRED.
- **Vorschlag** (`docs/annex/ERK_CONNECTIONS_v0_1.md` §2 und Docstring `tools/erk_verify_emit.py`):

```diff
-- Das Event dokumentiert, dass ein Lauf stattfand — es macht kein Ergebnis wahr.
+- Das Event dokumentiert die Angabe des Aufrufers, dass ein Lauf stattfand. Der
+  Emitter führt selbst keinen Verify-Lauf aus und prüft keinen Exitcode — es
+  macht kein Ergebnis wahr.
```

- **Alternative:** Kopplung an echten Lauf (`--run`), Roadmap S3b.
- **Nutzen:** Anti-F7 — Doku trägt nicht mehr als die Herkunft. **Risiko:** gering. **Rollback:** Revert.

### R4 — Mehr-Akteur-Regel (AUD-03)

> **Status-Nachtrag 2026-10-02:** angelegt als `docs/decisions/ADR-0005-erk-human-decision-precedence.md`; Kevin/Fleks hat A2 entschieden, umgesetzt im Folge-Commit (`TestDecisionPrecedence`).

- **Klasse:** SEMANTIC_REVIEW_REQUIRED. ADR-0005 mit drei Alternativen (Roadmap S4). Kein Code vorab.

### R5 — Hygiene (AUD-06, AUD-07, AUD-10)

> **Status-Nachtrag 2026-10-02 („R5 umsetzen“):**
> - **AUD-10:** ADR-0001 auf *Accepted* gesetzt.
> - **AUD-06:** Die in `docs/ci/PYTHON_LOCK.md` vorbereiteten Diffs für `release.yml` und
>   `void-sync.yml` wurden lokal validiert: Release-Gates G1–G7 liefen im gelockten
>   `dev`-Environment grün (647 passed), der VOID-Monitor im `runtime`-Environment mit
>   Exit 0 (Scratch-Kopie, ohne Issue-Schreiben). Das Anwenden wurde von der
>   Berechtigungsprüfung der Agent-Session blockiert (Workflows mit `contents: write` /
>   `issues: write`). **Nicht angewendet**; bleibt manuell oder nach Freigabe in der Session.
> - **AUD-07:** Keine Löschung ohne ausdrückliche Bestätigung. Tip-SHAs zur Wiederherstellung
>   (alle Ancestors von `origin/main`, geprüft 2026-10-02):
>
> | Branch | Tip-SHA |
> |---|---|
> | `claude/align-coverage-policy` | `fb471aa683775ad8bb5f8ef4c64230692d5529ca` |
> | `claude/analyze-repo-essence-LKgK4` | `dd28e79ef64deabddbafad69540f742b5050b992` |
> | `claude/refactor-codebase-011CV4t3cQACpBAxqgu1MX1D` | `9fbf1de83a49f49a84a7b76e2a6b2089223ca235` |
> | `claude/repo-maintenance-consolidation-LA2ek` | `315e8dc9646a69d87e761c2515d95f94d316175c` |
> | `codex/update-markdown-file-in-repository` | `68395d792e7d949f7da2904781e1f03b4c49865f` |
> | `codex/update-readme-for-deepjump-integration` | `723f8bc1b5ca860e803d153f09081dfbf194d771` |
> | `dependabot/github_actions/actions/setup-node-6.4.0` | `5a6f000245cb89e0ccbabe11383ad11adc69c782` |
> | `phase0/foundation-pack` | `b808c507c26a73ede7c78a6752ea1c100d62114b` |
>
> Wiederherstellung: `git push origin <SHA>:refs/heads/<branch>`.

- **Klasse:** HUMAN_AUTHORIZATION_REQUIRED / SEMANTIC_REVIEW_REQUIRED.
  AUD-06: `release.yml` Gate-Job und `void-sync.yml` auf `./.github/actions/python-locked` umstellen
  (Release-Lauf lokal nicht testbar → nur mit Tag-Probe auf Fork/Test-Tag).
  AUD-07: 8 gemergte Branches (Liste Phase-1 §5) löschen oder behalten.
  AUD-10: ADR-0001 *Accepted* setzen oder ändern.

## 7. Verbleibende Unsicherheiten

- CI-Ergebnisse auf GitHub für `main` und offene PRs nicht beobachtet.
- 7 Branches mit eigenen Commits inhaltlich ungelesen; „verwaist" nicht behauptet.
- `src/core/evidence_routing.py` Guard-Evaluation und Export nur über Tests, nicht Zeile für Zeile gelesen.
- Keine Aussage über Settings (Branch-Schutz, CodeQL, Private Reporting).

## 8. Ausgeführte Befehle (Auszug, ohne Secrets)

```
git status -sb; git rev-parse HEAD; git fetch origin; git fetch --unshallow origin
git rev-list --left-right --count origin/main...<branch>; git merge-base --is-ancestor; git cherry
python3 -m venv <scratch>/venv; pip install -r requirements-dev.txt; pip install -e . --no-deps
make verify PY=<venv>/python; make verify-governance; make lint; make type-check; black --check
cd Fractalsense && python -m pytest
pnpm install --frozen-lockfile; pnpm turbo run typecheck lint build test; npx jest
python <scratch>/linkcheck.py; python <scratch>/probe_withdraw.py; python <scratch>/probe2.py
pytest tests/unit/test_evidence_routing.py -k Withdrawal (Repo, Mutations- und Fix-Kopie)
GitHub-Connector: list_pull_requests(state=open), list_issues(state=OPEN)
```

Nebenwirkungen im Arbeitsbaum: `node_modules/`, `*.egg-info`, `.turbo/`, `.next/` — alle gitignored.

## 9. Nicht getan

- Kein Push, kein PR, kein Merge, keine Issue-/Branch-Aktion (Auftrag §6).
- Keine Änderung an `src/`, Policies, Workflows, GOLD, Receipts, VOIDMAP.
- Kein Exchange-Record, kein ADR, kein neuer Validator (kein belegter Bedarf).

## 10. Genau ein nächster Schritt für Kevin/Fleks

- **Anlass:** AUD-01 — eine dokumentierte Rücknahme kann still übergangen werden.
- **Vorarbeit:** Paket R1 (Diff oben), xfail-Test im Branch, Fix im Scratch validiert.
- **Entscheidung:** „Stream-Ordnung ist für WITHDRAW maßgeblich" — ja/nein; dazu a/b für
  `apply_approved_transition`.
- **Fertig-Kriterium:** Fix-Commit, xfail-Marker entfernt, `make verify` grün, Spec §13 um einen
  Satz zur Ordnung ergänzt.
- **Kleiner Fallback:** Nur Spec §13 präzisieren („Rücknahme gilt bei `decided_at ≥` Freigabe")
  und den xfail-Test als dokumentierte Grenze stehen lassen.

Vorab außerdem nötig: Freigabe, ob dieser lokale Branch gepusht und als Draft-PR geöffnet werden soll.

## Offene Punkte

- [ ] ☐ Push/Draft-PR dieses Branches freigeben?
- [ ] ☐ R1 entscheiden (nächster Schritt)
- [ ] ☐ R3 Formulierung übernehmen?
- [ ] ☐ R4/R5 terminieren

## Artefakte

- `tests/unit/test_evidence_routing.py`
- `docs/audit/repo_audit_2026-10-02.md`
- `docs/audit/repo_audit_result_2026-10-02.md`
- `docs/roadmap/forward_architecture_2026-10-02.md`

*Resonanz ohne Verschmelzung. Kopplung ohne illegitimen Writeback. Ein Git-Commit verleiht
diesem Bericht keine zusätzliche Authority.*
