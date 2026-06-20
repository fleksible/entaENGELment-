# Report: PR #260 stabilisieren, #259 entschärfen

**Datum:** 2026-06-20
**Fokus:** PR #260 Membran ziehen

## Ziel
Wartungszustand sauber stabilisieren: PR #260 (`fix(ui): VOIDMAP UI-Sync,
SUSPENDED-Status & pnpm-Onboarding`) eng halten und verifizieren, das diff-leere
PR #259 als superseded schließen, Folge-PRs nur schneiden — kein Merge ohne
Human-Go, keine GOLD/IMMUTABLE-Änderung, keine neuen VOIDs.

## Ergebnis (PR #260)
- PR #260 bleibt **eng geschnitten** (10 Dateien, alle innerhalb der 4 Punkte).
- VOIDMAP/UI-**Statusdrift abgesichert** (`tools/voidmap_ui_drift_check.py`,
  in `verify-governance` verdrahtet).
- **SUSPENDED** in UI/Types vollständig unterstützt.
- **pnpm-Onboarding** in README/WELCOME harmonisiert.
- **Keine GOLD/IMMUTABLE-Änderung** (`VOIDMAP.yml` unangetastet).
- **Keine neuen VOIDs, keine VOID-Schließungen** (UI spiegelt nur bestehenden Stand).
- `mergeable_state: clean`, nicht draft. **Kein Merge ausgeführt** (Human-Go ausstehend).

## Aktionen
- [x] PR #260 gegen `main` geprüft — Scope sauber (A1): keine README-Roadmap,
      kein Root `package.json`, kein Mobile-Zoom, kein Legacy `Index.html`,
      kein #240-Nachlauf, kein `make ui-dev`.
- [x] PR-Beschreibung präzisiert (A2): Geltungsbereich des Drift-Guards
      explizit dokumentiert (`id -> status`; Detailfelder handgesynct, nicht
      strukturell validiert).
- [x] Drift-Guard geprüft (A3): vergleicht alle VOID-IDs, meldet fehlende/
      zusätzliche VOIDs + Status-Drift, Exit 0/1/2, dependency-light,
      via `make voidmap-ui-drift-check` und in `verify-governance`.
- [x] SUSPENDED geprüft (A4): Type `OPEN | IN_PROGRESS | SUSPENDED | CLOSED`,
      Filter/Stats/Sort/Farbe (dezentes violet) korrekt, keine TS-Fehler.
- [x] pnpm-Onboarding geprüft (A5): kein `npm ci`/`npm run dev` mehr für die
      aktuelle UI, Repository-Map zeigt auf `pnpm --filter entaengelment-ui dev`.
- [x] .gitignore geprüft (A6): `docs/intake/raw/auto/**` + `!.gitkeep` konsistent
      mit Shadow-Copy-Hook, kuratierte Records bleiben trackbar — behalten.
- [x] PR #259 als superseded kommentiert und **geschlossen** (B1/B2, 0 changed files).

## Verifikation (tatsächlich gelaufen, auf #260-Branch)
| Check | Ergebnis |
|-------|----------|
| `git status` | clean |
| `make voidmap-ui-drift-check` | **OK** — 13 VOIDs in sync |
| `make verify-governance` | **PASS** — 13 Workflows posture-OK, voids-backlog up to date, drift sync |
| `pnpm install --frozen-lockfile` | **OK** (pnpm 10.33.0, node v22) |
| `pnpm turbo run typecheck lint build` | **4/4 successful**, keine TS-Fehler |
| `make verify` (verify-core/pytest) | **FAIL — PR-fremd** (s. Risiken) |

## Bewusst nicht enthalten (→ Folge-PRs)
- README-Roadmap
- Root `package.json` Metadata
- Mobile Zoom
- Legacy `Index.html`
- Issue #240
- `make ui-dev`

## Nicht getan
- Kein Merge von #260 (Human-Go ausstehend).
- Keine Code-Änderung an #260 erzwungen (PR-Body-Präzisierung genügte für A2;
  optionaler Drift-Guard-Kommentar nicht aufgenommen, um #260-Branch nicht zu
  verbreitern).
- Keine Folge-PRs angelegt (nur geplant, s.u.).

## Risiken
- `make verify` (verify-core) bricht in dieser Umgebung beim pytest-Collect ab:
  pytest aus uv-Tool-Env ohne PyYAML → `tools/workflow_posture_check.py`
  `sys.exit(2)` beim Import. **Vorbestehende, PR-fremde Altlast** — keine der
  10 #260-Dateien ist betroffen. `verify-governance` (governance-relevant) ist grün.

## Offene Punkte
- [ ] ☐ Human-Go für Merge von #260 abwarten.
- [ ] ☐ Optional: pytest-Test-Env mit PyYAML ausstatten, damit `make verify`
      lokal/CI nicht am Import scheitert (eigener chore-PR, nicht #260).

## Folge-PRs (nur Schnitt-Vorschlag, nicht umgesetzt)
1. **docs(repo): roadmap and package metadata refresh** — README-Roadmap
   aktualisieren; Root `package.json` Metadata/Lizenz glätten.
2. **fix(ui): mobile zoom and legacy entrypoint marker** — Mobile User-Zoom
   nicht blockieren; Legacy `Index.html` als historischen Prototyp markieren
   oder archivnah verschieben.
3. **chore(voids): stale overdue issue follow-up** — Issue #240 kommentieren
   oder als Watcher bis nach 2026-07-15 umwidmen (nicht schließen ohne Human-Go).

## Artefakte
- `OUT/PR260_stabilization_report.md` (dieser Report)
- PR #260: https://github.com/fleksible/entaENGELment-/pull/260 (Body präzisiert)
- PR #259: https://github.com/fleksible/entaENGELment-/pull/259 (closed, superseded)
