# CONSENT_RECORD_MAPPING_v0_1

**Status:** Mapping-Entwurf
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Datum:** 2026-10-28
**Anlass:** Vorschlag V4 (Checkup 2026-10-28)
**Bezug:** `src/core/evidence_routing.py`, `spec/eci.spec.json`,
`docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` § 9.1 und § 13–14

Nur ein Mapping vorhandener Felder. Kein neues Consent-Protokoll, keine
Schemaänderung.

---

## 1. Quellenlage

- **ISO/IEC TS 27560:2023** (Consent record information structure): Volltext
  kostenpflichtig, **nicht gelesen**. Feldnamen unten stammen aus dem DPV-Guide,
  der den Standard abbildet.
- **DPV-Guide „Consent Records and Receipts as per ISO/IEC TS 27560:2023 using
  DPV“**: Final Community Group Report (15.02.2026). Ausdrücklich „not a W3C
  Standard nor … on the W3C Standards Track“.
- **DPV 2.1**: Final Community Group Report (16.03.2025, als veraltet markiert).
  Begriffe nur aus dem Index übernommen; Definitionen wurden nicht gelesen.

## 2. Vorhandene Consent-bezogene Felder im Repo

| Repo-Feld / -Wert | Ort | Bedeutung im Repo |
|---|---|---|
| `CONSENT_MISSING` | ERK Claim-Status, `ReasonCode` | erforderlicher Consent fehlt → HOLD/STOP (Invariante 9) |
| `CONSENT_REVOKED` | ERK Claim-Status | Consent widerrufen → blockiert |
| `HumanDecision` `APPROVE`/`REJECT`/`DEFER`/`WITHDRAW` | ERK | menschliche Entscheidung zu einem Request; letzter Stand zählt (ADR-0005) |
| `human_actor` | ERK | **nicht authentifiziertes** Rollen-Label |
| `decided_at`, `requested_at`, `retracted_at` | ERK | vom Aufrufer behauptete Zeitpunkte; Reihenfolge im Stream entscheidet |
| `likert_norm`, `behavior_proxy`, `physio_proxy`, `eci_value` | `spec/eci.spec.json` (GOLD) | Proxy-Metrik, **kein** Consent-Nachweis |

## 3. Mapping

| ISO 27560 / DPV (laut Guide) | nächstes Repo-Gegenstück | Abdeckung |
|---|---|---|
| schema version | `schema_version` der ERK-Records | teilweise (eigenes Schema, keine 27560-Konformität) |
| record id | `request_id` / `decision_id` | teilweise |
| pii principal id (→ data subject) | — | **fehlt**: Das Repo modelliert keine betroffene Person |
| purpose, lawful basis, processing | — | **fehlt** |
| pii controllers | — | **fehlt** |
| event time | `decided_at` (behauptet, nicht autoritativ) | teilweise |
| event type / event state (→ ConsentStatus) | `HumanDecision`, `CONSENT_MISSING`/`CONSENT_REVOKED` | teilweise, siehe § 4 |
| validity duration | — | **fehlt** (kein Ablauf modelliert) |
| entity id | `human_actor` (nicht authentifiziert) | nur als Label |
| `dpv:ConsentRecord` / `dpv:ConsentReceipt` | ERK-Ledger-Events / Status-Receipts | nicht gleichbedeutend: Receipts im Repo belegen Gate-/Status-Läufe, keine Einwilligung |

## 4. Consent-Status und -Typen

| DPV-Begriff (Name laut DPV-2.1-Index bzw. DPV-Guide) | Repo | Regel |
|---|---|---|
| Consent Given | `HumanDecision(APPROVE)` für genau einen Request | nur für diesen Request, nicht übertragbar |
| Consent Refused | `HumanDecision(REJECT)` | blockiert |
| Consent Withdrawn / Consent Revoked | `HumanDecision(WITHDRAW)` vor Anwendung; `CONSENT_REVOKED`; `Retraction` nach Anwendung | blockiert; append-only |
| Consent Requested | offener Request ohne Entscheidung | blockiert |
| Consent Unknown | fehlende Entscheidung, unbekannter Status | → `CONSENT_MISSING` (fail-closed) |
| Consent Expired / Consent Invalidated | — | nicht modelliert; bei Bedarf → `CONSENT_MISSING` |
| **Implied Consent** | — | **für explizit freigabepflichtige Übergänge in diesem Projekt nicht ausreichend → `CONSENT_MISSING`** |
| Expressed / Explicitly Expressed Consent | `HumanDecision(APPROVE)` | nur explizite Entscheidung zählt |

Die Aufnahme eines DPV-Begriffs ins Vokabular erzeugt **keine** neue Erlaubnis im
Repo. Insbesondere öffnet Implied Consent keinen Übergang, der heute eine explizite
`HumanDecision(APPROVE)` verlangt.

## 5. Grenzen

- Keine betroffene Person, kein Zweck, kein Verantwortlicher, keine Gültigkeitsdauer:
  Das Repo ist kein Consent-Management-System (ERK § 14).
- `human_actor` ist nicht authentifiziert (ERK § 9.1).
- ECI ist eine Proxy-Metrik und kein Consent-Record.

## 6. Quellen

- DPV-Guide (CG Report, 15.02.2026): https://w3c-cg.github.io/dpv/guides/consent-27560
- DPV 2.1 (CG Report, 16.03.2025): https://w3c-cg.github.io/dpv/2.1/dpv/ — nur Index gelesen
- ISO/IEC TS 27560:2023 — nicht gelesen (kostenpflichtig)
