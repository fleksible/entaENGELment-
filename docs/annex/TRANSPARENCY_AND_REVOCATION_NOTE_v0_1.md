# TRANSPARENCY_AND_REVOCATION_NOTE_v0_1

**Status:** Konzeptnotiz
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Datum:** 2026-10-28
**Anlass:** Vorschläge V3 (SCITT/VC) und V5 (Widerruf laufender Arbeit)
**Bezug:** `src/core/ledger.py`, `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` § 13,
`docs/annex/SIGNED_BYTES_DECISION_NOTE_v0_1.md`

Keine Implementierung, keine vorweggenommene Ablösung der Ledger-Hash-Kette,
kein Rollback-Versprechen.

---

## Teil A · SCITT und VC als kombinierbare Schichten (V3)

| Schicht | Standard | Rolle | Verhältnis |
|---|---|---|---|
| Aussage | W3C Verifiable Credentials 2.0 (Recommendation 2025) | Datenmodell für eine signierte Aussage („Issuer sagt X über Y“) | kann Payload einer SCITT-Aussage sein |
| Transparenz | IETF SCITT, RFC 9943 (Proposed Standard, Juni 2026) | Architektur: Issuer reicht *Signed Statements* bei einem *Transparency Service* ein, Prüfende erhalten *Receipts* | nimmt beliebige Payloads auf, auch JSON |
| Receipt-Format | RFC 9942, COSE Receipts | Beweisformat für die Aufnahme in eine prüfbare Datenstruktur | gehört zu SCITT |
| Repo heute | `ledger.py` (SHA-256-Hash-Kette, lokal) | Manipulationserkennung einer lokalen Ereignisfolge | bleibt; ein Transparency Service wäre eine zusätzliche, externe Schicht |

Folgerungen:
- VC und SCITT sind kein Entweder-oder: VC beschreibt *was* gesagt wird, SCITT
  *wie* die Aussage öffentlich nachvollziehbar wird.
- JSON-Payloads sind mit SCITT vereinbar; die Wahl der signierten Bytes regelt
  die Entscheidungsnotiz zu V2/V1.
- Die lokale Hash-Kette wird dadurch nicht ersetzt. Ob und wann ein externer
  Transparency Service sinnvoll ist, ist eine eigene Entscheidung (Kosten,
  Öffentlichkeit, Datenschutz: private Inhalte dürfen nicht in ein öffentliches Log).

## Teil B · Widerruf laufender, delegierter Arbeit (V5)

### B.1 Wann relevant

Erst dann, wenn das Repo tatsächlich **laufende, delegierte Arbeit** hat: Jobs,
Agenten oder Callbacks, die mit einer Freigabe weiterarbeiten. Heute gibt es das
nicht. Das Action-Gate führt nichts aus, und der ERK widerruft append-only über
`WITHDRAW` und `Retraction` (§ 13).

### B.2 Problem

Ein Widerruf beendet nicht automatisch Arbeit, die bereits unterwegs ist
(Warteschlangen, Callbacks, Operationen beim Anbieter). Unbekannte Nachläufer
können nach dem Widerruf noch mit alter Autorität wirken.

### B.3 Konzept (angelehnt an „root-scoped quiescence“)

Nach Zhu und Wang, arXiv 2609.21284 (Preprint, 18.09.2026; Abstract gelesen):

1. **Cut:** Die widerrufene Autorität erhält einen Schnittpunkt; neue Arbeit darf
   unter ihr nicht mehr entstehen.
2. **Fence:** Geschützte Endpunkte nehmen nach dem Fence nichts mehr unter der
   alten Autorität an.
3. **Nachweis je Endpunkt:** Alle Annahmen vor dem Fence werden verbucht, und es
   wird bestätigt, dass danach keine mehr erfolgten.
4. **Unbekannt bleibt unbekannt:** Fehlende oder widersprüchliche Evidenz gilt als
   *unbestimmt*, nicht als Erfolg. Das entspricht der Fail-closed-Haltung des Repos.

### B.4 Grenzen, die jede Übernahme mitführen muss

- Der Nachweis gilt **nur innerhalb des definierten Manifests** (der bekannten
  Endpunkte und Konfiguration). Er belegt keinen globalen Stillstand.
- **Kein Rollback:** Bereits eingetretene Wirkungen werden nicht rückgängig gemacht.
- Nachläufer außerhalb des Manifests bleiben möglich und sind als offenes Risiko
  auszuweisen.
- Die Ergebnisse des Preprints (dort 17/17 auf einer anbieterfreien Testsuite)
  sind nicht unabhängig geprüft.

### B.5 Anschluss im Repo (nur Vorschlag)

- Ein späterer ausführender Consumer müsste vor jeder Wirkung den aktuellen
  Consent-Stand prüfen und `CONSENT_REVOKED` als Fence behandeln.
- Ein „Widerrufs-Receipt“ wäre ein neues Ereignis (append-only) mit
  Manifest-Bezug und dem Ergebnis *bestätigt / unbestimmt* je Endpunkt.

## Quellen

- RFC 9943, An Architecture for Trustworthy and Transparent Digital Supply Chains
  (Proposed Standard, 06/2026), https://datatracker.ietf.org/doc/rfc9943/ —
  Datatracker-Eintrag gelesen (Status, Datum, Bezug auf RFC 9942).
- RFC 9942, COSE Receipts — nur über RFC 9943 referenziert, nicht selbst gelesen.
- W3C: „The Verifiable Credentials 2.0 family of specifications is now a W3C
  Recommendation“, https://www.w3.org/news/2025/the-verifiable-credentials-2-0-family-of-specifications-is-now-a-w3c-recommendation
  — Ankündigung gelesen, Spezifikationen nicht im Detail.
- Zhu, Wang: Authorization Revocation for Long-Running AI Agents, arXiv 2609.21284,
  https://arxiv.org/abs/2609.21284 — nur Abstract.
