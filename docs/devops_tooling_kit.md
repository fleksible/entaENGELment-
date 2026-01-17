# EntaENGELment DevOps Tooling Kit

Dieses Dokument beschreibt das vollständige DevOps‑Kit für das EntaENGELment‑Projekt. Es ergänzt den Kernindex durch eine technische Annex‑Ebene: der Code und die Konfigurationen werden ausgelagert, während der Index nur auf diese Dateien verweist. Das Kit gewährleistet Reproduzierbarkeit, Governance und kryptographische Integrität.

## Repository‑Layout

Die folgende Baumstruktur spiegelt den Standardaufbau wider und definiert, wo sich die relevanten Artefakte befinden. Sie dient als Referenz für die Module innerhalb des Kernindex.

```
entaENGELment-/
├── index/                       # Kernindex (Tier‑0/1/2) und Modul‑Metadaten
│   ├── COMPACT_INDEX_v3.yaml
│   └── modules/
│       ├── MOD_6_RECEIPTS_CORE.yaml
│       └── MOD_15_STATS_TESTS.yaml
├── docs/                        # Annex‑Dokumente
│   └── devops_tooling_kit.md    # dieses Dokument
├── tools/                       # operative Skripte
│   ├── snapshot_guard.py        # Manifest‑Generator mit relativen Pfaden
│   ├── status_emit.py           # Status‑Emitter mit HMAC‑Signierung
│   └── status_verify.py         # Verifikationswerkzeug für den Status
├── tests/                       # Verifikations‑Skripte (Beispiele)
│   ├── test_snapshot_guard.py   # Testet Portabilität und Determinismus
│   ├── test_status_emit.py      # Testet HMAC‑Einbindung
│   └── verify_deep_jump.py      # P9‑Runbook‑Logik (Referenz)
├── receipts/                    # Beispiel‑Quittungen (JSON)
├── seeds/                       # Konfigurations‑Seeds (müssen ins Manifest)
├── audit/                       # Audit‑Logs und Governance‑Tabellen
├── .github/workflows/           # CI‑Konfigurationen
│   └── deepjump-ci.yml
└── Makefile                     # zentraler Entry‑Point für Tasks
```

## Snapshot Guard

`tools/snapshot_guard.py` erstellt ein JSON‑Manifest mit SHA‑256‑Hashes aller vom Benutzer angegebenen Eingabedateien. Um Portabilität zu garantieren, werden Pfade relativ zum Repository‑Root angegeben; Dateien außerhalb des Repos werden übersprungen. Über die Option `--strict` kann der Vorgang abbrechen, wenn keine Seed‑Dateien im Manifest auftauchen. Dies erfüllt die Anforderungen aus `MOD_6_RECEIPTS_CORE` (`FIX_PATH_DRIFT` und `FREEZE_SEEDS`).

```python
#!/usr/bin/env python3
"""EntaENGELment Snapshot Guard (Final Hardened)
Zweck: Erstellt Manifest mit SHA‑256 Hashes.
Härtung: commonpath‑Check, Root‑Globbing, Strict‑Mode."""
```

### Nutzung

```bash
# Erstellung eines Manifests für Seeds und Audit‑Konfigurationen
python tools/snapshot_guard.py out/snapshot_manifest.json "seeds/*.yaml" "audit/*.yaml" --strict
```

## Status Emit

`tools/status_emit.py` erzeugt eine Statusdatei (`deepjump_status.json`) sowie ein visuelles Badge (`deepjump.svg`). Die Nutzdaten (Status, Metriken, Zeitstempel) werden canonicalisiert und mittels HMAC‑SHA256 signiert. Das Geheimnis wird vorzugsweise aus der Umgebungsvariable `CI_SECRET` (oder `ENTA_HMAC_SECRET`) gelesen; eine CLI‑Option existiert für Fallback‑Szenarien. Dies entspricht der Spezifikation `FIX_STATUS_INTEGRITY` aus `MOD_15_STATS_TESTS`.

```python
#!/usr/bin/env python3
"""EntaENGELment Status Emitter (Final Hardened)
Zweck: Erzeugt status.json mit HMAC‑Signatur.
Härtung: ENV‑Secrets, Canonical JSON."""
```

### Nutzung

```bash
CI_SECRET="my-secret" python tools/status_emit.py --outdir out --status PASS --H 0.85 --dmi 4.8 --phi 0.75 --refractory 120
```

## Status Verify

Um sicherzustellen, dass die HMAC‑Signatur korrekt ist, bietet `tools/status_verify.py` ein Prüfwerkzeug. Es entfernt die Signatur aus der Datei, canonicalisiert den Rest und berechnet den erwarteten HMAC. Stimmen Werte nicht überein, liefert das Tool einen Fehlercode ungleich 0.

```python
#!/usr/bin/env python3
"""EntaENGELment Status Verifier
Zweck: Prüft HMAC‑SHA256 Signatur eines status.json."""
```

## Makefile

Die Makefile definiert die zentralen Aufgaben: Verifikation, Status‑Emit, HMAC‑Verifikation und Snapshot. Pattern‑Globbing wird in Anführungszeichen übergeben, sodass Python die Muster verarbeitet und nicht die Shell. Ein integriertes `status-verify`‑Target führt den Self‑Check direkt aus.

```Makefile
PY ?= python3
OUT ?= out
RECEIPT ?= receipts/arc_sample.json
SNAPSHOT_INPUTS ?= "seeds/*.yaml" "audit/*.yaml"
STATUS ?= PASS
H ?= 0.84
DMI ?= 4.7
PHI ?= 0.72
REFRACTORY ?= 120
```

## CI‑Workflow

Das GitHub‑Workflow `deepjump-ci.yml` automatisiert die Abfolge aus Verifikation, Status‑Emission, HMAC‑Überprüfung, Snapshot und Artefakt‑Upload. Durch die Bedingung `if: ${{ success() }}` wird ein Upload nur durchgeführt, wenn alle vorherigen Schritte fehlerfrei abgeschlossen wurden.

```yaml
name: DeepJump CI
on:
  push:
    branches: [ main, master ]
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * *'
jobs:
  deepjump-audit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Verify Logic (P9 Check)
        run: make verify-json
      - name: Emit & Verify Status Integrity
        env:
          CI_SECRET: ${{ secrets.CI_SECRET }}
        run: make status-verify STATUS=PASS H=0.85 DMI=4.8 PHI=0.75
      - name: Generate Snapshot Manifest
        run: make snapshot SNAPSHOT_INPUTS='"seeds/*.yaml" "audit/*.yaml"'
      - name: Upload Audit Artifacts
        if: ${{ success() }}
        uses: actions/upload-artifact@v4
        with:
          name: deepjump-audit-trail
          path: |
            out/status/deepjump_status.json
            out/badges/deepjump.svg
            out/verify.json
            out/snapshot_manifest.json
```

Dieses DevOps‑Kit bildet die operative Grundlage für das EntaENGELment‑Projekt. Es trennt den Kernindex von der technischen Implementierung und stellt sicher, dass jede Aussage oder Metrik durch entsprechende Tests und Quittungen abgesichert ist. Die Härtungsspezifikationen aus den Modul‑Metadaten sind vollständig implementiert und werden sowohl lokal als auch in der CI durchgesetzt.
