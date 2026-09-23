# ROSETTA_MEMBRANE_TRANSLATION_FRAME_v0_1

**Status:** INTAKE · [SPEC-WIP] · [ROSETTA]  
**Authority-Status:** DERIVED  
**Runtime:** none  
**Persistence:** none  
**Promotion-Effect:** none  
**Human-Commit:** required

## 0. Zweck

[FACT] Dieser Intake beschreibt keinen universalen Bedeutungsraum und keine gemeinsame
Ontologie.

[INFERENZ] Er präzisiert die bereits vorhandene Rosetta-/Bridge-Linie als
**kontextabhängige semipermeable Übersetzungsrelation** zwischen getrennten
Lore-/Vokabularräumen.

[FACT] Der Rahmen darf Übersetzung anbieten, ohne Identität, Evidenz, Authority oder
vollständige Übersetzbarkeit zu behaupten.

## 1. Minimaler Contract

```ts
type QuestionProvenance = {
  questionId: string;
  askedByRef: string;
  questionTextRef: string;
  contextRef?: string;
};

type TranslationEdge = {
  sourceRef: string;
  targetRef: string;
  preservedRelation: string;
  knownLoss: readonly string[];
  provenance: readonly string[];
  reversibilityStatus:
    | 'UNTESTED'
    | 'LOSSY'
    | 'PARTIAL'
    | 'REVERSIBLE_WITHIN_SCOPE';
};

type RosettaMembraneFrame = {
  frameId: string;
  questionProvenance: QuestionProvenance;
  sourceLoreRef: string;
  targetLoreRef: string;
  translationCandidates: readonly TranslationEdge[];
  untranslatedSource: readonly string[];
  untranslatedTarget: readonly string[];
  consentState: 'UNREVIEWED' | 'ACCEPTED' | 'REVISED' | 'REJECTED' | 'SILENCE';
  protectedOrigin: boolean;
  authorityStatus: 'DERIVED';
  humanCommitRequired: true;
};
```

[FACT] `questionProvenance` gehört zur Übersetzungsrelation selbst. Dieselben beiden
Lore-Räume dürfen unter verschiedenen Fragen unterschiedliche Kanten besitzen.

[FACT] `untranslatedSource` und `untranslatedTarget` sind keine Fehlerlisten. Sie
halten den nicht übertragenen Rest explizit sichtbar.

## 2. Harte Guards

```text
translation != identity
translation != evidence
translation != authority
similarity != equivalence
universal_procedure != universal_translatability
reverse_relation != lossless_inverse
untranslated_remainder != failure
silence != consent
```

[FACT] Eine Übersetzung darf many-to-many sein. Sie muss keine Funktion sein.

[FACT] Rückübersetzung darf verlustbehaftet sein. Ein Round-trip darf daher einen
anderen Repräsentanten ergeben, ohne dass dieser Unterschied verborgen wird.

[FACT] Private oder geschützte Herkunft darf die öffentliche, reduzierte Relation
motivieren, ohne öffentlich rekonstruierbar zu werden.

## 3. Verhältnis zu bestehenden Repo-Knoten

[FACT] `docs/annex/ROSETTA_INTERVALS_v0_1.md` behandelt Rosetta als erklärende,
nicht evidenzgebende Beziehungssprache.

[FACT] `docs/narratives/grimm2/fixtures/mereotopology_edge_fixtures_v0_1.json`
enthält bereits eine partielle Übersetzungszone mit getrennten Resten.

[FACT] `src/core/evidence_bridge_adapter.py` modelliert bereits
`preserved_relation`, `known_loss`, `falsifier`, `rollback` und
`protected_origin` und erzeugt Vorschläge statt Vollzug.

[INFERENZ] Dieser Intake erzeugt deshalb keinen zweiten Translation-Stack. Er
beschreibt die noch fehlenden Kandidaten `questionProvenance`,
zweiseitige Lore-Referenzen und explizite unübersetzte Reste für einen späteren
Crosswalk.

## 4. PASS/HOLD

[FACT] Die sieben Counterfixtures unter
`docs/narratives/grimm2/fixtures/rosetta_membrane_translation_fixtures_v0_1.json`
prüfen ausschließlich Guard-Verhalten.

[FACT] Kein erfolgreiches Fixture erzeugt CANON-, GOLD-, Runtime-, Claim- oder
VOID-Promotion.

[FACT] Bis ein fremder Reader die Darstellung ohne Gleichsetzungs- oder
Authority-Fehllesung reentert, bleibt dieser Contract: **HOLD**.
