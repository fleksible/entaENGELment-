# Report: Rot gemergte Stände korrigieren, offene PRs mergen

**Datum:** 2026-10-07
**Fokus:** Rote CI korrigieren, PRs mergen

## Ziel
Auftrag des Owners: Dinge korrigieren, die trotz roter CI gemergt wurden, und alle übrigen PRs mergen. Gemergt wird nur bei grüner CI (G6).

## Befund
- **Rot gemergt (30.09.):** #369, #370 und #371 gingen mit rotem `CI Pipeline` auf `main` [FACT].
  - Ursache war `black==26.5.1` aus #363: unter Python 3.9 nicht installierbar.
  - #369 hatte zusätzlich einen roten Security-Audit.
  - Behoben bereits durch #372 (Python-3.9-Trennung) und #370 (Audit). Seit `26d8111` ist die Push-CI auf `main` grün [FACT].
  - Alle späteren Merges (#372–#380) waren beim Merge grün.
- **Am 07.10. rot auf `main`:** der wöchentliche Security-Audit (Lauf vom 05.10.) [FACT].
  - Ursache waren neue Advisories nach dem letzten Merge, kein Merge-Fehler.
  - Betroffen: 4 high (`sharp`, `source-map-js`, `http-cache-semantics`, `braces`) und 4 moderate.
- **Dependabot-uv-Jobs** schlagen seit #373 fehl [FACT].
  - Fehlerbild: `unknown url type: '/pypi/…'` beim Hash-Update der exportierten requirements.
  - Kein CI-Gate, nicht Teil dieses Auftrags.

## Aktionen
- [x] #383: Audit-Floors per pnpm-Override angehoben
  - high: `sharp` 0.35.5, `source-map-js` 1.2.2, `http-cache-semantics` 4.3.0
  - moderate: `js-yaml` 5.4.3, `fast-uri` 3.1.8, `brace-expansion` 5.0.12
  - Kompatibilitäts-Patch für brace-expansion auf 5.0.12 portiert
  - GHSA-vfj7-8cjw-p6xm (`braces`) per `auditConfig.ignoreGhsas` ausgenommen: kein Upstream-Fix, nur Dev-Lint-Pfad. Die Ausnahme hat der Owner freigegeben.
  - Gemergt; Security-Audit auf `main` danach grün.
- [x] #381 (SECURITY.md, privater Meldeweg): auf Ready gesetzt, gemergt (CI grün)
- [x] #382 (Eval-Freeze Phase 1a): auf Ready gesetzt, gemergt (CI grün)
- [x] #374 (react-query) und #375 (turbo): rebased und gemergt (parallel, nicht durch diese Session); Security-Audit danach grün
- [x] #386 ersetzt #376 (jest 30.5.2): gemergt; Dependabot konnte #376 zweimal nicht neu aufbauen, #376 mit Verweis geschlossen
- [x] Lokal verifiziert:
  - `pnpm audit --audit-level=high`
  - Jest 66/66
  - `pnpm turbo run typecheck lint build test`
  - `make verify` mit gelocktem Dev-Env (uv 0.12.18, Python 3.12)

## Nicht getan
- #298 (TypeScript 7) und #365 (ESLint 10) nicht gemergt. Der Owner hatte HOLD entschieden; inzwischen sind beide mit Begründung geschlossen (Inkompatibilität mit Next.js 16 bzw. eslint-plugin-react 7.37.5).
- Issues nicht geschlossen: Issues lassen sich nicht mergen. Bei #332 und #333 sind laut Owner-Kommentaren noch Restpunkte offen.
- Dependabot-uv-Fehler nicht angefasst (eigener Scope).

## Risiken
- [RISK] Die `braces`-Ausnahme schwächt das Audit-Gate für genau eine GHSA. Entfernen, sobald `braces` oder `fast-glob` einen Fix ausliefert.
- [RISK] `sprintf-js` (moderate, kein Fix) bleibt im Audit-Report sichtbar. Es ist nicht gate-relevant.
- [RISK] Ohne funktionierende uv-Updates kommen keine automatischen Python-Bump-PRs.

## Offene Punkte
- [ ] ☐ Dependabot-uv-Updater reparieren (Hash-Update der exportierten requirements*.txt)
- [ ] ☐ `braces`-Ausnahme beim nächsten wöchentlichen Audit erneut prüfen
- [ ] ☐ #332 und #333: Restpunkte laut Issue-Kommentaren
- [ ] ☐ turbo ≥ 2.11 (seit #375) erzeugt bei Agent-Läufen automatisch eine Root-`AGENTS.md` mit Agent-Anweisungen. Entscheiden: committen oder in `turbo.json` `"agentGuidance": false` setzen. Bisher nicht committet (G5).

## Artefakte
- `pnpm-workspace.yaml`
- `pnpm-lock.yaml`
- `patches/brace-expansion@5.0.12.patch`
- `package.json`
- `OUT/red_merge_cleanup_2026-10-07.md`
