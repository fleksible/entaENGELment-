# Methodenfall: gültiges Paar und fehlende Phase

**Status:** ANNEX · DERIVED · [SPEC-WIP]

**Gelesene Basis:** `fc35b35a63091383249bc3448d3ae3119f1f5570`

**Beobachtet:** 2026-10-23

## 1. Auswahl und vorab benannte Prüfung

[ANNEX] Als erster Methodenfall wird ein öffentlicher technischer Vertrag gewählt.
Die Auswahl repräsentiert keine persönliche Erfahrung. Geprüft wird die
[registergetreue Claim-Methode](REGISTERGETREUE_CLAIM_PRUEFUNG_v0_1.md):
Ausgangsaussage, zusätzliche Deutung und ausgeführter Beleg müssen unterscheidbar
sein. Eine zu weit gehende Verbindung soll an einem konkreten Gegenfall scheitern.

[ANNEX] Vor dem Lauf gelten drei Kriterien: Das Originalpaar besteht die vorhandene
Paarprüfung; eine absichtlich falsche Herkunftsidentität wird zurückgewiesen;
ein bestandenes Paar ohne Phase trägt nicht die Behauptung vollständiger Übergabe.

## 2. Original, Deutung und Beleg

| Ebene | Konkreter Inhalt | Herkunft und Reichweite |
| --- | --- | --- |
| Ausgangsvertrag | Ein Quadrantenübergang besteht aus genau einem EXIT und ENTRY; gemeinsame pairId, Herkunftsidentität, Reihenfolge und legaler globaler Springerzug werden geprüft. | [HUD-Spezifikation §5](../spec/tesser3takt_hud_v0_2.md#5-boundary-half-step-invariant) und [Validator](../../ui-app/lib/tesser3takt-frame.ts) an der gelesenen Basis. |
| Getrennte Anforderung | Ein Slice-Receipt benötigt unter anderem phaseBefore und phaseAfter. | [HUD-Spezifikation §8](../spec/tesser3takt_hud_v0_2.md#8-hermes--caduceus--wheeler--zn). Die dortige Bindungsnotiz erklärt die Phase ausdrücklich als offen. |
| Zulässige Lesart | Die Paarprüfung belegt einen gültigen Boundary-Übergang im deklarierten Vertrag. | Enger Schluss aus dem ausgeführten Validator. |
| Zusätzlicher Prüfsatz des Reviewers | Ein gültiges Paar würde bereits die vollständige Slice-Phase transportieren. | Absichtlich zu starke Gegenlesart dieses Methodenfalls; kein Zitat und keine Behauptung des ursprünglichen Vertrags. |
| Tatsächlicher Beleg | B-Q0-Q1 hat zwei Records; Paarprüfung PASS, keine phaseBefore-/phaseAfter-Felder. | [HUD-Daten](../../ui-app/lib/tesser3takt-hud.ts) und unten wiederholbarer Lauf. |
| Negativkontrolle | ENTRY.transformedFrom wird in einer Kopie durch eine unpassende Identität ersetzt. | Ausdrücklich synthetische Mutation; die Originaldaten bleiben erhalten. |

## 3. Ausgeführter Lauf

```bash
node --experimental-strip-types --input-type=module - <<'JS'
import assert from 'node:assert/strict';
import { validateBoundaryPairs } from './ui-app/lib/tesser3takt-frame.ts';
import { HUD_BOUNDARY_TRANSITIONS } from './ui-app/lib/tesser3takt-hud.ts';
const pair = HUD_BOUNDARY_TRANSITIONS.filter(x => x.pairId === 'B-Q0-Q1');
const narrow = validateBoundaryPairs(pair);
const counter = validateBoundaryPairs(pair.map(x => x.half === 'ENTRY'
  ? { ...x, transformedFrom: 'counterfixture:unrelated' } : x));
const hasPhase = pair.some(x =>
  Object.hasOwn(x, 'phaseBefore') || Object.hasOwn(x, 'phaseAfter'));
assert.equal(pair.length, 2);
assert.equal(narrow.valid, true);
assert.equal(counter.valid, false);
assert.equal(hasPhase, false);
console.log(JSON.stringify({ narrow, counter, hasPhase }, null, 2));
JS
```

[FAKT] Am benannten Ref ausgeführt mit Node 24.19.0: `narrow.valid: true`,
`counter.valid: false`, `hasPhase: false`. Die Negativkontrolle meldet
`ENTRY transformedFrom must match EXIT stateId`. Das bestehende Node-Warning
MODULE_TYPELESS_PACKAGE_JSON bleibt sichtbar; es betrifft die Modulbehandlung,
nicht den Aussageumfang der Paarprüfung.

| Gelesene Quelle | SHA-256 der Bytes |
| --- | --- |
| tesser3takt-frame.ts | `6678f6ca57e40a2012d7cbb8c0d18894f06f225c60eeb77229afc0c80df5f3df` |
| tesser3takt-hud.ts | `32d71a442694383f27b657087bdbb778e98abf3a12ed88e00e9e4edce858caf8` |
| tesser3takt_hud_v0_2.md | `3dc6a33470ce5c37c0e4c098b0b356b4b1e03af1d03b6663bda93673d8b4fb5c` |

## 4. Ergebnis und Rücknahme

[ANNEX] Die enge Ausgangsaussage bleibt erhalten. Der zusätzlich eingeführte
Vollständigkeitsclaim scheitert: Die gültige Identitätsbrücke transportiert noch
keine Phase. Die falsche Identitätszuordnung wird unabhängig davon erkannt.
Eine erfolgreiche Teilprüfung ist weder ein Vollständigkeitsnachweis noch wertlos.

[ANNEX] Rückübersetzbar bleiben pairId, EXIT/ENTRY-Identitäten, Reihenfolge,
Koordinaten und die begrenzte Herkunftsreferenz. Fehlende Phase, Graining-Herkunft,
verschobene Blindseite und Sphärenstatus lassen sich daraus nicht rekonstruieren.
Diese Verluste bzw. fehlenden Angaben bleiben im
[Übergabe-Witness](PERSPECTIVE_TRANSITION_WITNESS_v0_1.md) sichtbar.

[UNRESOLVED] Der Methodenfall demonstriert eine nachvollziehbare Korrektur.
Er ist kein unabhängiger Wirksamkeitstest der Methode. Pearson-Blanket- und
HC/AC-Prüfungen werden hier nicht eingesetzt: Der Fall behauptet weder statistische
Abschirmung noch gemessene Mensch-KI-Synergie.
