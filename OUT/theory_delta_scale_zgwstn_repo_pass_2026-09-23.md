# Report: Theorie-Delta Scale Scanner + zGWSTN

**Datum:** 2026-09-23  
**Fokus:** provenance-first theory delta  
**Authority:** DERIVED  
**Branch:** `agent/theory-delta-scale-zgwstn-20260923`  
**Base:** `main@17fd78e2d71e4b314c54051a0922a7aa0b82c03e`

## Ziel

[FAKT] Dieser Pass prüft, ob der heutige Theorie-Delta bereits durch vorhandene
Repo-Strukturen getragen wird und ergänzt nur nachgewiesene Lücken.

[FAKT] Keine GOLD-Datei, kein Receipt und keine VOIDMAP-ID wird verändert.

## Gap-Befund: Sphärenlogik

[FAKT] `ui-app/lib/tesser3takt-bridge.ts` definiert bereits
`ResolutionScale = MICRO | MESO | MACRO`.

[FAKT] Derselbe Runtime-Knoten implementiert aktuell nur
`MicroToMesoBridgeRequest` mit MICRO→MESO.

[FAKT] `ui-app/lib/tesser3takt-hud.ts` definiert
`ObserverMode = OUTER | INNER | INVERSE`.

[FAKT] Im geprüften Repo existieren keine Treffer für die verlangten
`BOTTOM_UP`, `TOP_DOWN`, `SPECTATOR_READ_ONLY`-Contracts als zusammenhängenden
Scale-Scanner.

[INFERENZ] Es besteht damit eine echte, aber schmale Dokumentationslücke:
Skala, Richtung und Observer-Rolle sind vorhandene oder anschlussfähige Achsen,
aber noch nicht gemeinsam als anti-overclaim Scan-Contract beschrieben.

[FAKT] Die Lücke wird ausschließlich durch
`docs/annex/SPHAERENLOGIK_SCALE_SCANNER_v0_1.md` als ANNEX/[SPEC-WIP] ergänzt.

[FAKT] Der Sidecar enthält vier negative Fixtures:
Formähnlichkeit bei Mechanismusdivergenz, projektive Linienkreuzung,
Makro-Fit bei Mikro-Konflikt und unzureichende Evidenz mit offenem Kenogramm.

## Gap-Befund: zGWSTN

[FAKT] `WELCOME.md` beschreibt die Gläserne Agora als user-sovereign claim space
mit Fork-, Revision- und Withdrawal-Pfaden.

[FAKT] `PRIVACY_BOUNDARY.md` hält private User-Claims, persönliche symbolische
Profile und inferierte psychologische/behaviorale Profile standardmäßig privat.

[FAKT] `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` trennt
GuardDecision, HumanDecision und Claim-Retagging.

[FAKT] Im geprüften Repo existiert kein `zGWSTN`-, `sharedNow`-,
`ACCEPT_AS_SHARED`- oder `KEEP_INDIVIDUAL`-Contract.

[INFERENZ] Der fehlende Teil ist eine read-only Schnittmengenprojektion des
explizit Geteilten, nicht eine neue Claim-Policy oder kollektive Ontologie.

[FAKT] Wegen Intake-First wurde der Prototyp unter
`docs/intake/raw/ZGWSTN_READ_ONLY_FRAME_v0_1.md` abgelegt und nicht in Runtime,
Spec-GOLD oder VOIDMAP geschrieben.

[FAKT] Die Pflicht-Counterfixture A={X,Y,Z}, B={X,Q,R}, C={X,Y,R} ergibt
`sharedNow={X}` und verbietet die Ableitung einer kollektiven Aussage über X,Y,R.

## Guards

[FAKT] Beide Artefakte halten folgende Trennungen explizit:

```text
scale_shift != mechanism_identity
perspective_shift != ontic_change
overlap != collision
resonance != authority
observer != sovereign
```

[FAKT] Der Scale-Scanner führt PASS/HOLD nur als lokalen Kandidatengate:
PASS benötigt B1 Resonanz, B2 Persistenz, B3 topologische Distinktheit und
B4 Stabilität nach Reentry; jede fehlende Bedingung ergibt HOLD.

[FAKT] Auch PASS erzeugt keine Claim-, CANON-, GOLD-, Runtime- oder VOID-Promotion.

[FAKT] zGWSTN ist `authorityStatus: DERIVED`, `readOnly: true`,
`persistence: NONE`, `humanCommitRequired: true`.

## Bewusst nicht verändert

[FAKT] `VOIDMAP.yml` bleibt unverändert.

[FAKT] `WELCOME.md` bleibt unverändert.

[FAKT] `docs/annex/MICRO_MESO_BRIDGE_v0_1.md` bleibt unverändert.

[FAKT] `docs/spec/tesser3takt_hud_v0_2.md` bleibt unverändert.

[FAKT] `docs/decisions/TRAVERSAL_GRAMMAR_v0_1.md` bleibt unverändert.

[FAKT] `docs/narratives/grimm2/GRIMM_IR_MEREOTOPOLOGY_INTAKE_v0_1.md` bleibt unverändert.

[FAKT] `docs/spec/ruecknahme_operator.md` bleibt unverändert.

[FAKT] Kein Runtime-Typ und keine Persistenzlogik wurden implementiert.

## Unresolved / Kenogramme

[FAKT] Relation zwischen neuem `ScanObserver` und bestehendem
`ObserverMode = OUTER | INNER | INVERSE` bleibt ungebunden.

[FAKT] TOP_DOWN- und BIDIRECTIONAL-Runtime-Semantik bleibt offen.

[FAKT] Authentisierung/Teilnehmeridentität für zGWSTN bleibt offen.

[FAKT] Persistenzsemantik der Reader-Aktionen bleibt offen.

[FAKT] Konfliktauflösung jenseits von `CONTEST`/Kenogramm bleibt offen.

[FAKT] Keine dieser offenen Stellen erhält in diesem Pass eine neue VOID-ID.

## Reentry

[INFERENZ] Der kleinste nächste Reentry ist nicht "mehr Theorie", sondern ein
konkreter UI-/Reader-Test: Kann ein Mensch Scale/Direction/Observer bzw. sharedNow
lesen, ohne Mechanismusidentität oder Kollektivautorität hineinzulesen?

[FAKT] Bis zu diesem Test bleiben beide Artefakte HOLD und human-commit-required.
