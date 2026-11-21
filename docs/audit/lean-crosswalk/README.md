# Evidence-Index: Lean-Crosswalk v0.1

**Status:** ANNEX / SPEC-WIP · **Promotion-Effect:** none

**Nachweisstatus (2026-11-21):** `REAL_LEAN_RUN_VERIFIED_FOR_FIXTURES_A_E`

[ANNEX] Der Marker dokumentiert einen Nachweis. Er ist kein Laufzeitstatus des
Crosswalks, keine Claim-Promotion und keine semantische Bestätigung. Er gilt nur für
die fünf konstruierten Testdeklarationen A–E unter Lean 4.35.0. Die frühere
Kennzeichnung `Lean: NOT_RUN` in den Prüfberichten vom 2026-11-21 beschreibt den
damaligen Stand und bleibt unverändert.

## Inhalt dieses Ordners

| Datei | Herkunft | SHA-256 |
| --- | --- | --- |
| [`Lean4-PR478-Evidence.zip`](Lean4-PR478-Evidence.zip) | Lean-Lauf in einer externen Linux-Umgebung, Originalbytes unverändert | `ef036331329250a57d65b115ec9f0ca474afda50138f2ad360c59b2ac265ee68` |
| [`PR478_unabhaengige_Evidence_Gegenpruefung.md`](PR478_unabhaengige_Evidence_Gegenpruefung.md) | unabhängige Gegenprüfung des Archivs, Originalbytes unverändert | `14fe373bd7557426ed9c1f5cd819150687e96c9d3f33a382e867071715159119` |
| [`2026-11-21_evidence_uebernahme.md`](2026-11-21_evidence_uebernahme.md) | Übernahmeprüfung beim Einchecken (dieser PR) | – |

Im Archiv (65 Einträge, `SHA256SUMS` deckt 64 Dateien ab):

| Pfad im Archiv | Inhalt | SHA-256 |
| --- | --- | --- |
| `Lean4-PR478-Pruefbericht.md` | Bericht des ausführenden Laufs | `67387d405a00f0748bb873f1334e326493f5256ffc966b7b78bd5043e4f8d54e` |
| `raw/audit_stdout.txt` | Originalausgabe von `lake env lean CrosswalkProbe/Audit.lean`, 413 Bytes | `fc5aca573ccae3550757c266e7ba25a48137c5e5bb783ecb0c7fbcd21c0ab7e1` |
| `results/audit_raw.json` | Rückgabe von `audit_raw()` auf diese Bytes | `1bb01819c9ac6ff2a85b758ebe0ea8404fd0e50b5d7de373f8951767dd546ab7` |
| `sources/` | die sechs geprüften Dateien vom PR-Head `0b50c4d` | siehe `meta/sources.sha256` |
| `meta/`, `tools/` | Umgebung, Prozessprotokoll, Toolchain-Prüfsummen, Aufzeichnungs- und Leseskript | siehe `SHA256SUMS` |
| `build-products/` | Lake-Manifest und Build-Dateien (u. a. `Basic.olean`) | siehe `meta/build-products.json` |

## Befund

| Fall | Deklaration (`CrosswalkProbe.Basic.…`) | Axiome laut Lean | `audit_raw()` |
| --- | --- | --- | --- |
| A | `thm_direct_gap` | `sorryAx` | `OPEN_OBLIGATION` |
| B | `thm_transitive_gap` | `sorryAx` | `OPEN_OBLIGATION` |
| C | `thm_closed_formal` | keine | `FORMAL_CLOSED` |
| D | `thm_custom_axiom` | `externalAssumption` | `HOLD_TRUST_BOUNDARY` |
| E | `thm_mixed` | `sorryAx`, `externalAssumption` | `OPEN_OBLIGATION`, Fremdaxiom in `foreign_axioms` erhalten |

[ANNEX] Das `FORMAL_CLOSED` von C betrifft nur die Testaussage `True` und wird auf
keine Projektbehauptung übertragen.

## Selbst nachprüfen

```bash
cd docs/audit/lean-crosswalk
sha256sum Lean4-PR478-Evidence.zip          # ef0363…ee68
mkdir /tmp/ev && unzip -q Lean4-PR478-Evidence.zip -d /tmp/ev
(cd /tmp/ev && sha256sum -c SHA256SUMS)     # 64 × OK
```

Python-Replay ohne Lean (Leser vom PR-Head `0b50c4d`, Originalbytes aus dem Archiv),
Ergebnis muss bytegleich zu `results/audit_raw.json` sein:

```bash
git worktree add /tmp/head 0b50c4d6e284aa06cf43a03aec98ace616d1ce65
python3 -I -B /tmp/ev/tools/read-audit.py /tmp/head /tmp/ev/raw/audit.exit /tmp/ev/raw/audit_stdout.txt \
  | cmp - /tmp/ev/results/audit_raw.json
```

## Weiterhin offen

- [ANNEX] HOLD: Ende-zu-Ende-Provenienz zwischen erzeugten Karten und tatsächlichen Lean-Rohdaten.
- [ANNEX] HOLD: semantische Zuordnung zwischen mathematischer Formalisierung und menschlicher Aussage.
- [ANNEX] HOLD: Verständlichkeitstest mit Menschen.
- [ANNEX] HOLD: allgemeine Gültigkeit des Lesers außerhalb der fünf geprüften Deklarationen.
- [ANNEX] Die Ausführung selbst ist nur durch das Archiv belegt; weder die Gegenprüfung
  noch die Übernahmeprüfung haben Lean erneut gestartet.

Vertrag: [LEAN_CROSSWALK_v0_1](../../annex/LEAN_CROSSWALK_v0_1.md)
