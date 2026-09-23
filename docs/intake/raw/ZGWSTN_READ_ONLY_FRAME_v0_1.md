# ZGWSTN_READ_ONLY_FRAME_v0_1

**Status:** INTAKE · [SPEC-WIP]  
**Authority-Status:** DERIVED  
**Runtime:** none  
**Persistence:** none  
**Writeback:** forbidden  
**Human-Commit:** required

## 0. Zweck

[HYPOTHESE] `zGWSTN` ("wir sind hier") kann als rein projektiver Gegenwartsrahmen
nützlich sein, wenn er ausschließlich sichtbar macht, welche bereits explizit
freigegebenen Claim-Referenzen in einem aktuellen Leseframe tatsächlich geteilt sind.

[FAKT] Dieser Prototyp erzeugt keine kollektive Identität, keine Mehrheitswahrheit,
keinen Gruppenwillen und keine psychologische Profilierung.

[FAKT] Der Prototyp ist ein Intake-Artefakt und kein kanonischer Gläserne-Agora-Vertrag.

## 1. Minimaler Typ

```ts
type ClaimRef = string & { readonly __claimRef: unique symbol };
type KenogramRef = string & { readonly __kenogramRef: unique symbol };
type ProvenanceRef = string & { readonly __provenanceRef: unique symbol };
type TraversalOffer = string & { readonly __traversalOffer: unique symbol };

type AgoraAction =
  | 'ACCEPT_AS_SHARED'
  | 'KEEP_INDIVIDUAL'
  | 'CONTEST'
  | 'FORK'
  | 'SILENCE'
  | 'WITHDRAW';

type ZGwstnFrame = {
  frameId: string;
  sharedNow: readonly ClaimRef[];
  individualOnly: readonly ClaimRef[];
  contested: readonly KenogramRef[];
  availableSteps: readonly TraversalOffer[];
  provenance: readonly ProvenanceRef[];
  actions: readonly AgoraAction[];
  humanCommitRequired: true;
  authorityStatus: 'DERIVED';
  readOnly: true;
  persistence: 'NONE';
};
```

[FAKT] Die Typen sind absichtlich opaque Referenzen; der öffentliche Prototyp speichert
keine privaten Claim-Texte, Nutzerprofile oder biographischen Rekonstruktionsdaten.

[FAKT] `sharedNow` ist eine Projektion explizit geteilter Referenzen im aktuellen Frame.

[FAKT] `individualOnly` bezeichnet Referenzen, die im aktuellen Frame nicht als
gemeinsam geteilt markiert sind; daraus folgt keine Bewertung ihres Wahrheitsstatus.

[FAKT] `contested` hält offene oder widersprochene Relationen als Kenogramm-Referenzen
sichtbar.

[FAKT] `availableSteps` enthält Traversal-Angebote und keine Handlungsautorität.

## 2. Unverhandelbare Guards

```text
sharedNow != collective_identity
sharedNow != majority_truth
availableSteps != recommendation_authority
resonance != authority
observer != sovereign
```

[FAKT] Keine Aktion dieses Frames darf automatisch einen Claim promoten.

[FAKT] Keine Aktion dieses Frames darf psychologische oder verhaltensbezogene Profile
ableiten.

[FAKT] Keine Aktion dieses Frames darf einen versteckten Writeback in Ledger,
Registry, VOIDMAP, Profiling-State oder Remote-Telemetrie auslösen.

[FAKT] Private User-Lore darf nicht in diesen öffentlichen Repo-Prototyp geschrieben
werden.

[FAKT] Die Gläserne Agora macht in dieser Lesart Relationen revisierbar; sie erzeugt
keine kollektive Souveränität.

## 3. Ableitung von `sharedNow`

[FAKT] `sharedNow` darf nur aus Claim-Referenzen gebildet werden, die jeder am Frame
beteiligte Eingang explizit als aktuell teilbar markiert hat.

[INFERENZ] Eine sichere Minimaloperation ist die Mengen-Schnittmenge dieser expliziten
Freigaben:

```text
sharedNow = intersection(explicitSharedRefs(participantFrame_i))
```

[FAKT] Fehlende Zustimmung wird nicht als Zustimmung interpretiert.

[FAKT] Schweigen erzeugt keine Zugehörigkeit zu `sharedNow`.

[FAKT] Ein Widerspruch bleibt als `contested`/Kenogramm sichtbar und wird nicht durch
Mehrheit entfernt.

## 4. Reader-/Agora-Aktionen

[FAKT] Der Prototyp bietet genau diese reversiblen Intent-Typen an:

- [FAKT] `ACCEPT_AS_SHARED` — eine Referenz für den aktuellen Frame als teilbar markieren.
- [FAKT] `KEEP_INDIVIDUAL` — eine Referenz ausdrücklich außerhalb von `sharedNow` halten.
- [FAKT] `CONTEST` — eine Relation als strittig/ungeklärt markieren.
- [FAKT] `FORK` — eine alternative Lesespur anbieten, ohne den Ursprung zu überschreiben.
- [FAKT] `SILENCE` — keine Festlegung erzwingen.
- [FAKT] `WITHDRAW` — eine frühere Freigabe für zukünftige Frames zurückziehen.

[FAKT] In diesem READ-ONLY-Prototyp sind diese Aktionen nur `TraversalOffer`-artige
Intents; sie führen selbst keinen State-Write aus.

[INFERENZ] Eine spätere Implementierung müsste jeden Write in einen bestehenden,
expliziten HumanDecision-/Consent-Fluss übergeben, statt die Aktion lokal als
Autorität zu behandeln.

## 5. Pflicht-Counterfixture

[FAKT] Eingaben:

```text
A: X, Y, Z
B: X, Q, R
C: X, Y, R
```

[FAKT] Ergebnis:

```text
sharedNow = X
```

[FAKT] Nicht zulässige Ableitung:

```text
"Das Kollektiv glaubt X, Y, R"
```

[FAKT] `Y` ist nicht geteilt, weil B es nicht freigegeben hat.

[FAKT] `R` ist nicht geteilt, weil A es nicht freigegeben hat.

[FAKT] Häufigkeit 2/3 ist keine Mehrheitswahrheit und kein Ersatz für explizite
Schnittmengen-Semantik.

## 6. Verhältnis zu bestehenden Repo-Knoten

[FAKT] `WELCOME.md` beschreibt die Gläserne Agora bereits als user-sovereign claim
space mit Fork-/Revision-/Withdrawal-Pfaden.

[FAKT] `PRIVACY_BOUNDARY.md` hält rohe User-Claims, persönliche symbolische Profile
und inferierte psychologische/behaviorale Profile standardmäßig privat.

[FAKT] `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md` trennt
`GuardDecision`, `HumanDecision` und Claim-Retagging und erlaubt Retagging nur nach
explizitem HumanDecision plus erneuter Guard-Validierung.

[INFERENZ] `zGWSTN` ergänzt diese Strukturen nur um eine lesbare Momentaufnahme der
expliziten Schnittmenge; es braucht dafür keine neue Claim-Policy.

## 7. Known Loss / Unresolved

[FAKT] Dieser Prototyp definiert keine Teilnehmeridentität und keine Authentisierung.

[FAKT] Dieser Prototyp definiert keine Persistenzsemantik für Aktionen.

[FAKT] Dieser Prototyp definiert keine Konfliktauflösung jenseits des Offenhaltens.

[FAKT] Dieser Prototyp definiert keine Gewichtung von Claims, Teilnehmern oder
Provenienzquellen.

[FAKT] Dieser Prototyp erzeugt keine neue VOID-ID.

[HYPOTHESE] Falls ein späterer UI-Prototyp sinnvoll wird, sollte er zuerst nur eine
lokale, flüchtige Projektion mit `readOnly: true` rendern und jede schreibende Aktion
an einen getrennten HumanDecision-Flow delegieren.

## 8. Reentry

[FAKT] Reentry-Frage: Reicht die explizite Schnittmenge als Orientierung, ohne dass
Nicht-Geteiltes in eine imaginierte Kollektivposition zurückgeschrieben wird?

[FAKT] Bis diese Frage in einem konkreten UI-/Reader-Kontext geprüft wurde, bleibt der
Status `HOLD`.

[FAKT] `humanCommitRequired=true`.
