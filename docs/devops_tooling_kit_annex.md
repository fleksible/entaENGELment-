# DeepJump DevOps Tooling Kit — Annex (Functorial Index v3)

> **Annex-Prinzip:** Index = Pointer-Gold (`index/COMPACT_INDEX_v3.yaml`). Code & Tooling = Annex. Jeder operative Satz hängt an einem Pfad.

## Entry Points (kurz)
| Zweck | Pointer | Call |
| :--- | :--- | :--- |
| Verify (Schemas/Specs) | `Makefile` | `make verify-json` |
| Status (HMAC) | `tools/status_emit.py` | `make status` |
| Status-Check | `tools/status_verify.py` | `make status-verify` |
| Snapshot (strict) | `tools/snapshot_guard.py` | `make snapshot` |
| CI-Pipeline | `.github/workflows/deepjump-ci.yml` | GitHub Actions |
| Pointer-Gold | `index/modules/MOD_6_RECEIPTS_CORE.yaml` · `index/modules/MOD_15_STATS_TESTS.yaml` | Functorial Index |

*Glosse:* *Vier Schritte, ein Atemzug. Erst prüfen, dann sprechen, dann einfrieren, dann teilen.*

## Ablauf: Verify → Status (HMAC) → Snapshot (strict) → Upload
1. **Verify** — Policies/Specs prüfen.  
   `make verify-json`
2. **Status (HMAC)** — Canonical JSON + HMAC.  
   `make status STATUS=PASS H=0.85 DMI=4.8 PHI=0.75 REFRACTORY=120`
3. **Status-Check** — HMAC gegenprüfen.  
   `make status-verify RECEIPT=receipts/arc_sample.json`
4. **Snapshot (strict)** — Seeds/Audit einfrieren. Abbruch, wenn Seeds fehlen.  
   `make snapshot SNAPSHOT_INPUTS='"seeds/*.yaml" "audit/*.yaml"'`
5. **Upload** — CI bündelt Artefakte nur bei Erfolg.  
   `.github/workflows/deepjump-ci.yml`

## HMAC-Disziplin
- Secret aus `CI_SECRET` oder `ENTA_HMAC_SECRET`.  
- Payload canonicalisieren, Signatur als eigener Knoten.  
- Badge + JSON landen unter `out/status/` und `out/badges/`.

## Snapshot-Strenge
- Relativ zum Repo-Root hashen (`tools/snapshot_guard.py`).  
- `--strict` erzwingt Seeds im Manifest.  
- Pfad-Drift wird geblockt (Common-Path-Check).

## Artefakte & Annex-Fächer
- **Receipts:** `receipts/*.json` (Beispielquittungen).  
- **Seeds:** `seeds/*.yaml` (müssen im Snapshot stehen).  
- **Audit:** `audit/` (Tabellen, Logs).  
- **Docs:** dieses Annex-Dokument + `docs/masterindex.md`.  
- **CI:** `.github/workflows/deepjump-ci.yml` führt Verify/Status/Snapshot/Upload als Kette.

*Glosse:* *Magie bleibt, weil jeder Sprung an ein Siegel gebunden ist.*
