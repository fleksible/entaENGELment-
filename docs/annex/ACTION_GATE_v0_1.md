# ACTION_GATE_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** partial (nur bei explizitem Aufruf)
**Human-Decision-Boundary:** required für jede reale Nebenwirkung
**Datum:** 2026-07-23
**Validation-Refresh:** 2026-07-26
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
| Registry passt nicht zum Ökosystem / unbekanntes Ökosystem | `REGISTRY_UNKNOWN` | HOLD |
| Version für das Ökosystem nicht exakt validierbar | `VERSION_UNVERIFIABLE` | HOLD |
| Quelle nicht `verified` | `SOURCE_UNVERIFIED` | HOLD |
| Netzwerk erforderlich | `NETWORK_REQUIRED` | HOLD + HUMAN_ONLY |
| Dateisystemeffekt | `FILESYSTEM_EFFECT` | HOLD + HUMAN_ONLY |
| Prozesseffekt | `PROCESS_EFFECT` | HOLD + HUMAN_ONLY |
| nicht reversibel | `IRREVERSIBLE_EFFECT` | HOLD + HUMAN_ONLY |
| untrusted Materialquelle | `UNTRUSTED_SOURCE_MATERIAL` | HOLD |

Immer gesetzt: `ACTION_PROPOSAL_ONLY`, `NO_EXECUTION`, `SHELL_FRAGMENT_INERT`.
`HUMAN_APPROVAL_REQUIRED` wird gesetzt, sobald eine reale Nebenwirkung vorliegt
oder der Zustand `HOLD` ist.

Die Allowlist ist nach Ökosystem gekeyt: eine Registry gilt nur als bekannt,
wenn sie zum angegebenen Ökosystem passt (z.B. `npm` + `registry.npmjs.org`).
Eine Fehlzuordnung (`npm` + `pypi.org`) oder ein unbekanntes Ökosystem führt
fail-closed zu `HOLD`. Bekanntheit bedeutet **nicht** Vertrauen zur Ausführung.

Die Exact-Version-Prüfung ist bewusst ökosystemspezifisch und fail-closed:

- `npm` akzeptiert nur vollständiges SemVer 2.0.0 (`Major.Minor.Patch`,
  optionale gültige Prerelease-/Build-Identifier, keine führenden Nullen in
  numerischen Release- oder Prerelease-Komponenten);
- `pypi` akzeptiert nur einen kanonischen öffentlichen PEP-440-Identifier mit
  mindestens drei Release-Komponenten; lokale `+label`-Versionen werden für die
  öffentliche Registry nicht akzeptiert;
- bekannte Registries ohne implementierten lokalen Parser (`cargo`, `go`,
  `maven`, `rubygems`) können `REGISTRY_KNOWN` tragen, bleiben in v0.1 aber
  `VERSION_UNVERIFIABLE`/`HOLD`.

Damit führen insbesondere npm-Werte wie `1.2.3evil`, `1.2.3.4`,
`1.2.3+a+b`, numerische Komponenten mit führenden Nullen, Ranges und
Whitespace nicht zu `VERSION_PINNED`. Die Prüfung folgt der
[SemVer-2.0.0-Grammatik](https://semver.org/spec/v2.0.0.html) und der
[kanonischen PEP-440-Grammatik](https://packaging.python.org/en/latest/specifications/version-specifiers/#appendix-parsing-version-strings-with-regular-expressions),
ohne neue Runtime-Abhängigkeit.

`visibility` wird nie über die Sichtbarkeit der Materialquelle hinaus eskaliert:
ohne Angabe erbt das Proposal die Quell-Sichtbarkeit, sonst wird auf das
Restriktivere von Wunsch und Quelle geklemmt (unbekannte Quell-Sichtbarkeit →
`private`). So diffundiert kein privater `proposed_command` über ein
`reduced`/`public`-Label.

Die Default-Registry-Allowlist ist unveränderlich (`MappingProxyType`), damit
kein Consumer sie prozessweit aufweiten kann.

`ActionProposal` ist öffentlich lesbar, aber **builder-sealed**. Der Builder
übergibt intern ein prozesslokales, nicht serialisierbares Konstruktionstoken;
`ActionProposal(**manifest)` und `dataclasses.replace(...)` können die
berechneten Felder deshalb nicht selbst wählen. Das Token erscheint weder in
`to_manifest()` noch im Digest. Ein aus JSON gelesener Datensatz ist nur inertes
Material und muss mit der aktuellen `MaterialRef`-Quelle und Registry-Policy
erneut durch `build_action_proposal(...)` laufen.

Das Konstruktionstoken ist ausdrücklich **kein Geheimnis, keine Signatur und
keine Sandbox** gegen bösartigen Python-Code im selben Prozess. Es versiegelt
die normale API-/Deserialisierungsgrenze und verhindert versehentliche oder
datengetriebene Rekonstruktion berechneter Felder. Autorisierung muss außerhalb
dieses Moduls stattfinden.

Der interne `__post_init__` prüft zusätzlich die vollständige Kohärenz des
Builder-Ergebnisses: obligatorische Inert-Codes, genau eine
Registry-Entscheidung, paarige Version-/Quell-Codes, exakte
Effekt-/Irreversibilitäts-Codes, `guard_state`,
`human_approval_required` und `responsibility_class`. Reason-Codes sind
duplikatfrei und geschlossen. So kann auch ein späterer interner Refactor keine
widersprüchlichen berechneten Felder emittieren.

Semantische Steuerfelder und Identifikatoren dürfen keinen führenden oder
nachlaufenden Whitespace tragen. Registry-Policies werden nur als eingebaute
`dict`-Container bzw. als die unveränderliche Default-Policy akzeptiert;
beliebige Python-`Mapping`-Implementierungen (auch hinter einem Mapping-Proxy)
werden nicht aufgerufen.

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
4. **Fail-closed** — nicht zum Ökosystem passende Registry, nicht implementierte
   Versionsgrammatik und ungültige npm-/PyPI-Exact-Versionen führen zu `HOLD`.
5. **HUMAN_ONLY** — jede reale Nebenwirkung **und Irreversibilität** erfordert
   `human_approval_required`.
6. **Deterministisch** — identische Eingabe ergibt identisches Manifest und
   identischen `manifest_digest`; Reason-Code-Reihenfolge ist stabil.
7. **Builder-sealed** — rohe/deserialisierte Manifeste können keine berechneten
   Gate-Felder konstruieren; intern werden alle Feld-/Code-Ableitungen
   gegengeprüft.

## 7. Abgrenzung

`guard_state` (`PROPOSE`/`HOLD`) ist ein lokales Durchlass-Signal, **kein**
Claim-Status und **kein** menschlicher Entscheid. Das Action-Gate ist ein
eigenes Übergangssystem neben Claim-Tag-Transition, tesser3TAKT-Review und UI
BoundaryTransition (ERK-Spec §11) und teilt weder Typen noch Vokabular mit ihnen.
Das eigene `ActionReasonCode`-Enum ist bewusst getrennt vom `ReasonCode` des
Claim-Kernels.

Die beiden unverhandelbaren Grenzen lauten:

```text
PROPOSE != AUTHORIZE
PROPOSE != EXECUTE
```

Alle folgenden Re-entry-Punkte bleiben bis zu einer getrennten Prüfung und
ausdrücklichen Autorisierung geschlossen:

| Re-entry-Punkt | Status | Grenze |
|---|---|---|
| Payload-Limits | `HOLD` | keine belastbare Größen-/Komplexitätsgrenze in v0.1 |
| Registry-Signaturprüfung | `HOLD` | keine kryptografische Registry-Authentisierung |
| Consumer-Authentizität | `HOLD` | kein authentifizierter Consumer-Witness |
| Ausführende Runtime-Grenze | `HOLD` | kein ausführender Consumer wird implementiert |
| Ledger- oder UI-Kopplung | `HOLD` | nur über separat genehmigte Adapter |
| Installations- oder Deploymentpfad | `HOLD` | kein Pfad in v0.1 |

Insbesondere ist `PROPOSE` **keine Ausführungsautorisierung**. Paketname,
Effektdeklarationen, `verification_status` und der inerte Command-Text bleiben
Beschreibungen des Aufrufers; v0.1 vergleicht den Command nicht semantisch mit
diesen Deklarationen. Kein Runtime-Consumer darf aus dem Manifest direkt eine
Installation oder andere Nebenwirkung ableiten.

## 8. Bekannte Grenzen & Phase-2-Kandidaten

- Keine kryptografische Registry-/Signaturprüfung; `verification_status` ist
  eine Zusicherung des Aufrufers, keine authentifizierte Prüfung.
- Deskriptive Metadaten (Paket/Ziel, Effekte, Reversibilität) sind
  Aufruferangaben und werden nicht gegen den inerten Command geparst. Die
  Builder-Versiegelung schützt die Manifest-Kohärenz, nicht die Wahrheit dieser
  Angaben.
- Keine Ledger-Emission des Manifests in v0.1 (bewusst: das Gate erzeugt nur ein
  Manifest). Eine spätere Anbindung als `MATERIAL_REGISTERED` +
  `EvidenceRelation(PROVENANCE_ONLY)` ist ein separater, zu genehmigender Adapter.
- **Phase-2-Kandidat (dokumentiert, nicht implementiert):** ein deterministischer
  Kontext-Rot-/Drift-Check zwischen `CLAUDE.md`, Claim-Tag-Policy,
  Runtime-Eventlog-Draft, Python-Typen und Tests. Er wird hier bewusst **nicht**
  gebaut und erzeugt **kein** neues Backlog-System und keine `VOIDMAP.yml`-Mutation.
- **Phase-2-Kandidat — weitere Exact-Version-Grammatiken:** v0.1 implementiert
  nur npm SemVer 2.0.0 und einen konservativen kanonischen PyPI/PEP-440-Pfad.
  Cargo-, Go-, Maven- und RubyGems-Versionen bleiben bis zu einem jeweils
  getesteten lokalen Parser `VERSION_UNVERIFIABLE`/`HOLD`. Die Erweiterung ist
  ein separater, zu genehmigender Adapter; kein gemeinsamer Näherungsparser darf
  mehrere inkompatible Ökosysteme still freigeben.
- Ein serialisiertes Manifest ist weder signiert noch autorisiert und kann in
  v0.1 nicht als `PROPOSE` rehydriert werden. Eine spätere Replay-/Ledger-Grenze
  benötigt einen authentifizierten Policy-/Material-Witness und ein eigenes
  Schema.

## 9. Rücknahme

Das Modul ist ANNEX: Es kann durch Entfernen der Aufrufe deaktiviert werden,
ohne GOLD, Policies oder Receipts zu berühren. Es schreibt nichts persistent.
