# Report: Gesamtcheck nach #407

**Datum:** 2026-10-18
**Fokus:** Gesamtcheck nach GOLD-Merge

## Ziel

Nach dem Merge von #407 prüfen, ob alles läuft, ob etwas vergessen oder falsch
angebunden ist, und was erst jetzt auffällt.

## Befund: läuft

- `main` nach #407 (`e74cd6f`): alle 12 ausgelösten Workflows grün.
- Lokal auf dem Branch: `make verify` (702 Tests, `-W error::DeprecationWarning`),
  `make verify-governance`, `make verify-js` (frozen lockfile), ruff, black, mypy,
  Fractalsense (184), `python tools/python_lock.py check`, Export-Drift-Check.
- Deny-Regel `Edit(/data/receipts/**)` aus `.claude/settings.json` per Probe bestätigt:
  der Schreibversuch wird abgewiesen.

## Befund: falsch angebunden oder vergessen

| # | Befund | Folge | Behebung |
|---|--------|-------|----------|
| 1 | Codex-Review zu #407: 6 Threads (2×P1, 4×P2) | s. u. | `c35d11b`, `d100dc3`, `798d542` |
| 2 | Bericht lag in `OUT/`, G6 verlangt `docs/audit/` | Audit-Trail unvollständig | verschoben (`c35d11b`) |
| 3 | „ERK-Fixtures konform“ galt nur für `CLAIM_CREATED`; `CLAIM_RETAGGED` nutzt `reason_codes`, die Spec verlangte `reason` | Aussage im #407-Bericht zu weit | GOLD-CHANGE `798d542` (`reason` oder `reason_codes`), Test über alle Fixture-Events |
| 4 | `eventlog_spec_check`: Leerzeichen-Strings galten als vorhanden | leerer Beleg passiert | `c35d11b` |
| 5 | `spectra_table_lint`: `nan`/`inf` und überzählige Zellen passierten | verunreinigte Tabelle möglich | `c35d11b` |
| 6 | VOID-011-Meta nannte Quellen nur als Pfade | Export nicht an Implementierung gebunden | `source_sha256` (`d100dc3`) |
| 7 | AGENTS.md G1 ohne `spec/`, `seeds/` (annex.md, CLAUDE.md, settings.json führen beide als GOLD) | Codex liest unvollständige GOLD-Liste | `4ebca5e` |
| 8 | Dependabot-uv (#406) auf allen Python-Jobs rot: Updater schreibt die Exporte anders als `tools/python_lock.py export` | jeder uv-PR scheitert am Drift-Check | gleiche Versionen im Repo-Weg (`2799b76`); Verfahren als Kommentar in `.github/dependabot.yml` |
| 9 | Dependabot-npm scheitert mit `ERR_PNPM_NO_MATURE_MATCHING_VERSION` (Run 39095081707) | Cooldown 4320 min über den ganzen Lockfile, `next 16.4.2` war 2 Tage alt | selbstheilend; Kommentar in `pnpm-workspace.yaml` (`4ebca5e`) |

## Befund: erst jetzt aufgefallen

- **MI-Schätzer-Bias.** `mi()` (Histogramm, √n Bins je Achse) liefert bei unabhängigen
  Signalen ~0,5 nats (n=256), unabhängig von n. Im VOID-011-Export war MI bei schwacher
  Kopplung damit fast nur Bias (S7-C0.1: 0,52 nats). Entscheid: `mi()` bleibt, der Export
  führt `MI_BASELINE` (8 feste Permutationen) und `MI_EXCESS`. Ergebnis je Seed 7/42:
  0,01/0,12 → 0,19/0,22 → 1,36/1,32 nats, monoton in der Kopplung.
- **Higuchi-FD** (bereits in #407 behoben): Normierung 1/k statt 1/k² klemmte FD auf 1,0.
  PLV und PF stimmen mit analytischen Werten überein.

## Aktionen

- [x] #407 gemergt, `main` grün gelesen
- [x] Codex-Befunde behoben, Threads beantwortet
- [x] GOLD-CHANGE Spec `CLAIM_RETAGGED` (User-Entscheid: `reason` oder `reason_codes`)
- [x] MI-Baseline im VOID-011-Export (User-Entscheid), VOID-011-Doku ergänzt
- [x] Tooling-Update aus #406 im Repo-Weg; Ersatzverfahren dokumentiert (User-Entscheid: manuell, kein Workflow)
- [x] Überholte Dependabot-PRs mit Verweis geschlossen (User-Entscheid)

## Nicht getan

- `mi()` selbst nicht geändert (kein Bias-korrigierter Schätzer im Kern).
- Kein Workflow, der Dependabot-uv-PRs automatisch nachrechnet.
- `policies/` unverändert: die ERK-Policy ist per `policy_digest` gebunden.

## Risiken

- Jeder künftige Dependabot-uv-PR bleibt rot, bis er manuell ersetzt wird.
- `MI_EXCESS` ist bei schwacher Kopplung klein gegen die Streuung der Baseline;
  die Werte bleiben `SIMULATION_PROXY`.

## Offene Punkte

- [ ] ☐ #333: Punkt „Dependabot so ausrichten, dass Lock-Updates nicht widersprüchlich sind“ nur
      verfahrensseitig gelöst; Checkbox „Python 3.9–3.12 validieren“ ist durch die Untergrenze
      3.10 (Matrix 3.10–3.14) überholt.
- [ ] ☐ #332: Empfangstest des privaten Meldewegs (Owner-Aktion).
- [ ] ☐ #305: Annex F v0.3, unverändert offen.
- [ ] ☐ VOID-028 (high, OPEN) hat kein `target_date`; VOID-011 verweist darauf.
- [ ] ☐ Radar: Build-Attestations, ESLint 10, pnpm 11/12 (je eigener PR).
- [ ] ☐ Remote-Branches gemergter PRs; Aufräumen nur nach OK (G3).

## Artefakte

- `docs/audit/2026-10-18_gesamtcheck.md`
- `docs/audit/2026-10-18_gold_changes.md`
- `spec/runtime_eventlog_v0_1.json`
- `tools/eventlog_spec_check.py`, `tools/spectra_table_lint.py`, `tools/void011_metrics_export.py`
- `data/metrics/void011_resonance_metrics.csv`, `.meta.json`
- `docs/voids/VOID-011_resonance_metrics.md`
- `.github/dependabot.yml`, `pnpm-workspace.yaml`, `AGENTS.md`, `CLAUDE.md`
