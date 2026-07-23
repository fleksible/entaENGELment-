# ACTION_GATE_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** partial (nur bei explizitem Aufruf)
**Human-Decision-Boundary:** required für jede reale Nebenwirkung
**Datum:** 2026-07-23
**Modul:** `src/core/action_gate.py`
**Ergänzt:** `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` §2, §14 („Kein Action-Gate in dieser Phase")

---

## 1. Zweck

Die Action-Gate-Schnittstelle v0.1 schließt die in der ERK-Spec dokumentierte
Grenze („kein Action-Gate") mit dem **kleinsten sicheren, nicht ausführenden**
Delta. Sie übersetzt eine extern gefundene Handlungsanweisung — etwa eine
Install-Zeile aus einer README, einem Makefile oder einer requirements-Datei —
in ein strukturiertes, inertes `ActionProposal`-Manifest.

Sie ist **kein Paket-Sicherheitsprodukt** und **kein Installer**. Sie berechnet
nur ein Manifest und deterministische lokale Checks.

## 2. Nicht-Ziele

- keine automatische Installation, kein Paketmanagement,
- keine Netzwerkabfrage (das Repo besitzt keine kontrollierte Netz-Abstraktion),
- keine Shell-, Subprozess- oder Dateisystem-Ausführung,
- kein Parsen von `proposed_command` in ausführbare Tokens,
- keine Claim-Promotion und kein zweites Governance-System,
- keine Reputations- oder Signaturprüfung von Paketen (v0.1),
- keine Kopplung an GOLD, Policies, Receipts oder VOIDMAP.

## 3. Manifest-Felder

`build_action_proposal(...) → ActionProposal` erzeugt genau dieses Manifest:

| Feld | Rolle | Herkunft |
|---|---|---|
| `action_id` | stabile ID | Aufrufer |
| `schema_version` | `action_gate.v0.1` | Modul |
| `source_material_ref` | Verweis auf `MaterialRef.material_id` | Aufrufer |
| `proposed_command` | **reiner String**, nie ausgeführt | Aufrufer |
| `ecosystem` | z.B. `pypi`, `npm`, `shell` | Aufrufer |
| `package_or_resource` | Ziel | Aufrufer |
| `requested_version` | angeforderte Version | Aufrufer |
| `registry_or_origin` | Herkunft/Registry | Aufrufer |
| `network_required` | bool | Aufrufer |
| `filesystem_effects` | Liste beschriebener Effekte | Aufrufer |
| `process_effects` | Liste beschriebener Effekte | Aufrufer |
| `reversibility` | `reversible` \| sonst | Aufrufer |
| `verification_status` | `verified` \| sonst | Aufrufer |
| `guard_state` | **berechnet**: `PROPOSE` \| `HOLD` | Gate |
| `responsibility_class` | **berechnet**: `COMPUTATIONAL` \| `IN_BETWEEN` \| `HUMAN_ONLY` | Gate |
| `human_approval_required` | **berechnet** | Gate |
| `reason_codes` | **berechnet**, geschlossenes Vokabular | Gate |
| `visibility` | Sichtbarkeitsklasse | Aufrufer |

Die deskriptiven Felder beschreiben die *gefundene* Anweisung; das Extrahieren
ist Aufgabe des Aufrufers. Das Gate führt nichts davon aus.

## 4. Verantwortungsklassen

Die *Manifest-Berechnung selbst* ist immer COMPUTATIONAL. `responsibility_class`
beschreibt die **vorgeschlagene Handlung**:

- **COMPUTATIONAL** — deterministisch, ohne externe Nebenwirkung, vollständig
  überprüft (bekannte Registry, gepinnte Version, verifizierte Quelle,
  reversibel, trusted/reviewed Material). Nur diese Klasse erreicht `PROPOSE`
  ohne erzwungene menschliche Freigabe.
- **IN_BETWEEN** — effektfrei, aber unaufgelöst (unbekannte Registry, nicht
  gepinnte Version, unverifizierte oder untrusted Quelle). Review-Kandidat,
  niemals stiller Durchlass.
- **HUMAN_ONLY** — reale externe Nebenwirkung (Netzwerk, Dateisystem, Prozess,
  Installation) oder Irreversibilität. Erfordert eine explizite, widerrufbare
  menschliche Entscheidung; niemals durch einen Agenten substituierbar.

## 5. Fail-closed Regeln

Der Gate-Zustand startet optimistisch bei `PROPOSE` und sinkt bei jeder
Verletzung fail-closed auf `HOLD`:

| Bedingung | Reason-Code | Wirkung |
|---|---|---|
| Registry/Herkunft nicht in Allowlist | `REGISTRY_UNKNOWN` | HOLD |
| Version nicht gepinnt/überprüfbar | `VERSION_UNVERIFIABLE` | HOLD |
| Quelle nicht `verified` | `SOURCE_UNVERIFIED` | HOLD |
| Netzwerk erforderlich | `NETWORK_REQUIRED` | HOLD + HUMAN_ONLY |
| Dateisystemeffekt | `FILESYSTEM_EFFECT` | HOLD + HUMAN_ONLY |
| Prozesseffekt | `PROCESS_EFFECT` | HOLD + HUMAN_ONLY |
| nicht reversibel | `IRREVERSIBLE_EFFECT` | HOLD |
| untrusted Materialquelle | `UNTRUSTED_SOURCE_MATERIAL` | HOLD |

Immer gesetzt: `ACTION_PROPOSAL_ONLY`, `NO_EXECUTION`, `SHELL_FRAGMENT_INERT`.
`HUMAN_APPROVAL_REQUIRED` wird gesetzt, sobald eine reale Nebenwirkung vorliegt
oder der Zustand `HOLD` ist.

Die Allowlist-Bekanntheit einer Registry bedeutet **nicht** Vertrauen zur
Ausführung; sie unterscheidet nur eine benannte Ökosystem-Registry von
unbekannter Herkunft.

## 6. Invarianten (getestet)

`tests/ethics/test_action_gate_no_execution.py` und
`tests/unit/test_action_gate.py`:

1. **No execution** — das Modul importiert keine ausführende/netzwerkfähige
   Bibliothek (AST-Import-Check) und ruft `eval/exec/os.system/subprocess.*`
   nicht auf (AST-Call-Check).
2. **Command stays inert** — `proposed_command` (auch `curl … | bash`) bleibt
   wortgleich erhalten und wird nie tokenisiert.
3. **Setup-Doku ist Daten** — README-/Makefile-/requirements-Zeilen erzeugen nur
   ein zurückgehaltenes Proposal; ein monkeypatchter Subprozess/`os.system`
   wird während des Baus nie berührt.
4. **Fail-closed** — unbekannte Registry und nicht überprüfbare Version führen
   zu `HOLD`.
5. **HUMAN_ONLY** — jede reale Nebenwirkung erfordert `human_approval_required`.
6. **Deterministisch** — identische Eingabe ergibt identisches Manifest und
   identischen `manifest_digest`; Reason-Code-Reihenfolge ist stabil.

## 7. Abgrenzung

`guard_state` (`PROPOSE`/`HOLD`) ist ein lokales Durchlass-Signal, **kein**
Claim-Status und **kein** menschlicher Entscheid. Das Action-Gate ist ein
eigenes Übergangssystem neben Claim-Tag-Transition, tesser3TAKT-Review und UI
BoundaryTransition (ERK-Spec §11) und teilt weder Typen noch Vokabular mit ihnen.
Das eigene `ActionReasonCode`-Enum ist bewusst getrennt vom `ReasonCode` des
Claim-Kernels.

## 8. Bekannte Grenzen & Phase-2-Kandidaten

- Keine kryptografische Registry-/Signaturprüfung; `verification_status` ist
  eine Zusicherung des Aufrufers, keine authentifizierte Prüfung.
- Keine Ledger-Emission des Manifests in v0.1 (bewusst: das Gate erzeugt nur ein
  Manifest). Eine spätere Anbindung als `MATERIAL_REGISTERED` +
  `EvidenceRelation(PROVENANCE_ONLY)` ist ein separater, zu genehmigender Adapter.
- **Phase-2-Kandidat (dokumentiert, nicht implementiert):** ein deterministischer
  Kontext-Rot-/Drift-Check zwischen `CLAUDE.md`, Claim-Tag-Policy,
  Runtime-Eventlog-Draft, Python-Typen und Tests. Er wird hier bewusst **nicht**
  gebaut und erzeugt **kein** neues Backlog-System und keine `VOIDMAP.yml`-Mutation.

## 9. Rücknahme

Das Modul ist ANNEX: Es kann durch Entfernen der Aufrufe deaktiviert werden,
ohne GOLD, Policies oder Receipts zu berühren. Es schreibt nichts persistent.
