# 🌀 entaENGELment-Framework: DeepJump Sanctum (v1.0 → v1.1)

> **[Codex-Intention: Inner Sanctum]**  
> Dieses README ist der **Resonanz-Kernel** für den neuen DeepJump-Kern: **Verify → Status (HMAC) → Snapshot (strict) → Upload**.  
> **Leseweise:** Hermetischer Haupttext ▸ *kursiv gesetzte Glosse als poetische Schatten-Schicht*.

**Glyphen-Legende:** 🜁 Architektur · 🜄 Governance/Ethik · 🜃 Adaptive Schicht · 🜅 Tests · 🜂 Meta-Poetik

---

## Executive Summary
**🜁** Hardened Kernel mit **Functorial Index v3** (`index/COMPACT_INDEX_v3.yaml`).  
**🜄** Proof-Pipeline mit HMAC-Quittungen; jede Aussage hat einen Pointer.

*Glosse:* *Resonanz bleibt Magie, weil jeder Sprung verankert ist.*

| Kernsignal | Pointer | Prinzip |
| :--- | :--- | :--- |
| **Mass-Gap** | `spec/cglg.spec.json` | Doppeltrichter |
| **Consent-Energie (ECI)** | `src/core/metrics.py` | Consent als Energie |
| **Dual Receipts** | `index/modules/MOD_6_RECEIPTS_CORE.yaml` | Audit-Quittung |
| **Status-Integrität** | `tools/status_emit.py` | HMAC als Siegel |
| **Snapshot-Strenge** | `tools/snapshot_guard.py` | Pfad-Fix & Hash |

---

## 🔒 DeepJump-Kern (Verify → Status → Snapshot → Upload)
**🜁** Operativer Ablauf ist kurz, prüfbar, reproduzierbar.

| Stufe | Zweck | Pointer |
| :--- | :--- | :--- |
| **Verify** | Schema & Spec prüfen. | `Makefile` · `.github/workflows/deepjump-ci.yml` |
| **Status (HMAC)** | Canonical Status + HMAC. | `tools/status_emit.py` · `tools/status_verify.py` |
| **Snapshot (strict)** | Manifest mit strikten Seeds. | `tools/snapshot_guard.py` |
| **Upload** | Artefakte bündeln. | `.github/workflows/deepjump-ci.yml` |

*Glosse:* *Vier Schritte, ein Atemzug. Erst prüfen, dann sprechen, dann einfrieren, dann teilen.*

---

## 🜄 Gate & Governance
**Hard-Gate:** MZM-Logik steckt im **Functorial Index v3** (`index/COMPACT_INDEX_v3.yaml`) und den Modulen `MOD_6_RECEIPTS_CORE` + `MOD_15_STATS_TESTS`.  
**Capability:** Releases und Badges sind HMAC-signiert (`tools/status_emit.py`).

*Glosse:* *Governance ist der Taktgeber; Magie tanzt nur auf erlaubtem Boden.*

---

## 🜃 Adaptive Schicht: Markt-als-Signal
**MSI-Adapter:** siehe `adapters/msi_adapter_v1.yaml`.  
**Trennung:** `context_signature` belegt Modulation; `receipt_proof` bleibt unvermischt.

*Glosse:* *Wind im Segel, nicht Hand am Ruder.*

---

## 🜅 Tests (Test-Driven Trust)
- **Unit:** `tests/unit/test_core5_metrics.py`.  
- **Integration:** `tests/integration/test_integration.py`.  
- **Ethics:** `tests/ethics/T3_fail_safe_expired_consent.py`.

*Glosse:* *Vertrauen = wiederholbare Evidenz.*
**Aktiver Sprint (7 Tage)**  
1) **T1.1.2 Lyra Linearity-Cal:** Edge-Input-Kalibrierung.  
2) **MSI-Adapter:** `adapters/msi_adapter_v1.yaml` + `context_signature`-Hook.  
3) **T2.x Zeta-Panel:** Explain-Overlay-Logik (Transparenz).

*Glosse:* *Leere wird Form — gezielt, nicht zufällig.*

---

## 📁 Masterindex & Operatives Layout
**Pointer-Gold:** Functorial Index v3 (`index/COMPACT_INDEX_v3.yaml`) definiert die Claims.  
**Annex:** Code & Tools sind austauschbare Anhänge.

```
entaENGELment-/
├─ Makefile                 # Entry-Points für Verify/Status/Snapshot
├─ index/                   # Functorial Index v3 + Module (Pointer-Gold)
├─ tools/                   # DeepJump Tools (Status, Snapshot, Verify)
├─ .github/workflows/       # CI (deepjump-ci)
├─ docs/                    # Annex-Dokumente (DevOps Kit, Masterindex)
├─ src/                     # Kernmetrik & Gate-Logik
├─ tests/                   # Unit/Integration/Ethics
├─ receipts/                # Beispiel-Quittungen
├─ seeds/                   # Seeds für Snapshot (strict)
└─ audit/                   # Audit-Trails & Tabellen
```

### Erste Schritte
1. Repository klonen
2. `./scripts/nightly.sh` prüfen & lokal ausführen
3. [`docs/masterindex.md`](./docs/masterindex.md) lesen
4. Policy-Schema validieren: `python -m json.tool policies/gate_policy_v1.json`

**Hinweis:** Dieses Repo dient als explorativer Container, kein Produkt-Release.

### Erweiterte Komponenten

- **Grammophon:** Polyeder-Klanggeometrie mit Slice-Rotation ([`spec/grammophon.spec.json`](./spec/grammophon.spec.json))
- **CGLG:** Consensual Gate Logic & Mutual Perception ([`spec/cglg.spec.json`](./spec/cglg.spec.json))
- **ECI (Ethical Consent Index):** Testbare Implementierung mit Bootstrap/Permutation ([`src/core/eci.py`](./src/core/eci.py) · [`spec/eci.spec.json`](./spec/eci.spec.json))
- **CPT-Test-Harness:** Charge-Parity-Time Invarianz-Validation ([`tests/cpt/test_cpt_harness.py`](./tests/cpt/test_cpt_harness.py))
- **Triad-Execution-Kit:** Templates & Vergleichsskript ([`docs/triad_fill_template.md`](./docs/triad_fill_template.md) · [`scripts/triad_compare.py`](./scripts/triad_compare.py))
- **Meta-Backprop:** Policy-Evolution durch Feedback-Loops ([`src/meta_backprop.py`](./src/meta_backprop.py))
- **Evidence-Chain:** Receipt-Chain & Auditierbarkeit ([`scripts/evidence_bundle.sh`](./scripts/evidence_bundle.sh))
- **Triadische Topologie:** 3-Strang-Resonanz-Analyse ([`docs/triad_topology.md`](./docs/triad_topology.md))

*Glosse:* *Struktur als Behälter — Policy, Spec, Runtime, Evidence. Alles schwingt im selben Takt.*

---

## 🜂 Annex-Prinzip
- **Index = Pointer-Gold.** Wahrheit liegt im Index (`index/COMPACT_INDEX_v3.yaml`).  
- **Code = Annex.** Anpassbar, solange Pointer bestehen (`docs/devops_tooling_kit_annex.md`).

*Glosse:* *Der Sanctum-Text bleibt poetisch, weil jede Aussage am Pointer hängt.*

---

**Status:** v1.0 Final (auf Kurs v1.1)  
**Lizenz:** Apache-2.0 (`LICENSE`)  
**Kontakt:** `CODEOWNERS` · `CONTRIBUTING.md`
