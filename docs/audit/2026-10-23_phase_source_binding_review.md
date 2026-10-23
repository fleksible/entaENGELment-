# Phasenquelle und Zuordnung: ausgeführter Quellenabgleich

**Datum:** 2026-10-23

**Status:** ANNEX · DERIVED · Reviewfassung

**FOKUS:** Phasenquelle und Zuordnung prüfen

**Basis:** `e173790d4d883f1098fd37d6813dab7e608d2b96`

## 1. Auftrag und Ergebnis

[FAKT] Nach dem Wrap-up beauftragt der Nutzer die Fortsetzung. Erster Anschluss
ist die tatsächliche Phasenquelle und ihre Boundary-/Frame-/Slice-Zuordnung.
Gelesen wurden der HUD-Aufrufer, Builder, Frame- und Phasenvalidator,
Mikro–Meso-Trace, Toy-Generator, PLV, Metrikexport, LOG-ZN-Dokumente und die
einschlägigen Tests. Die [Ergebniskarte](../annex/PHASENQUELLE_UND_ZUORDNUNG_v0_1.md)
trennt vorhandene Producer von einer ausgewählten und angebundenen Quelle.

[ANNEX] Die Anbindung bleibt HOLD. Ein vorhandener Generator liefert relative
synthetische Phasen; seine Auswahl als HUD-Größe ist nicht durch die Bezeichnung
Phase oder eine erfolgreiche Einheitenumrechnung entschieden. Die feste
HUD-Kennung trennt im Gegenlauf keine zwei zeitlichen Snapshots. Vorhandene
Modell- und Datenlücken werden nicht durch erfundene Prozesswerte geschlossen.

## 2. Gegenlauf an den tatsächlichen HUD-Eingaben

```bash
node --experimental-strip-types --input-type=module - <<'JS'
import assert from 'node:assert/strict';
import { buildTesserHudFrame, PORTAL_LEFT_STATE_ID,
  PORTAL_DISTINCT_RIGHT_STATE_ID } from './ui-app/lib/tesser3takt-hud.ts';
import { validateBoundaryPairs } from './ui-app/lib/tesser3takt-frame.ts';
import { validateSlicePhaseTransport } from './ui-app/lib/tesser3takt-slice-phase.ts';
const input = { observerMode: 'OUTER', control: -0.34, torsion: 0.48, zLayer: 4,
  leftStateId: PORTAL_LEFT_STATE_ID, rightStateId: PORTAL_DISTINCT_RIGHT_STATE_ID };
const a = buildTesserHudFrame(input);
const b = buildTesserHudFrame({ ...input, observerMode: 'INVERSE',
  control: 0.4, torsion: 0.9, zLayer: 8 });
assert.notDeepEqual(a.regime, b.regime);
assert.notEqual(a.observerMode, b.observerMode);
assert.notEqual(a.zLayer, b.zLayer);
assert.deepEqual(a.transport, b.transport);
assert.equal(validateBoundaryPairs(a.transport.boundaryTransitions).valid, true);
const missing = validateSlicePhaseTransport(undefined, undefined, undefined, undefined);
assert.equal(missing.valid, false);
assert.equal(a.kenograms.find(x => x.id === 'Kη-03').status, 'UNBOUND');
console.log(JSON.stringify({ frameIds: [a.transport.frameId, b.transport.frameId],
  unchangedTransport: true, missingPhaseRejected: !missing.valid }));
JS
```

[FAKT] Ausgeführt: beide frameIds sind `tesser3takt-hud-v0.2`; der gesamte
Transport bleibt gleich. Die Paarprüfung besteht, fehlende Phaseneingaben werden
zurückgewiesen. Das bestehende MODULE_TYPELESS_PACKAGE_JSON-Warning bleibt
sichtbar. Der Gegenlauf prüft diese konkret gewählten Ansichten und ist kein
Beweis über alle denkbaren Einstellungen oder externen Producer.

## 3. Vorhandener Generator und Verlustkontrolle

```bash
python3 - <<'PY'
import math
from src.tools.toy_resonance_dataset import generate_mycel_signals
from src.core.metrics import plv
from tools.void011_metrics_export import build_rows
settings = dict(n=8, seed=42, coupling=0.35)
ds = generate_mycel_signals(**settings)
assert ds == generate_mycel_signals(**settings)
assert len(ds.phases) == 8
assert all(-math.pi <= p < math.pi for p in ds.phases)
turns = [(p / (2 * math.pi)) % 1 for p in ds.phases]
assert all(0 <= p < 1 for p in turns)
first = plv([0.0] * 4)
second = plv([math.pi / 2] * 4)
assert math.isclose(first, second, abs_tol=1e-14)
rows = build_rows()
assert all('phase' not in r and 'sliceId' not in r and 'frameId' not in r for r in rows)
print(dict(relativePhaseCount=len(ds.phases),
  firstRadians=ds.phases[0], firstTurns=turns[0],
  plvControls=[first, second], metricRows=len(rows)))
PY
```

[FAKT] Ausgeführt: acht relative Phasen, erste Phase −0.0076576979163962555 rad,
umgerechnet 0.9987812395239011 Umläufe. Die beiden verschieden phasigen
Kontrollreihen liefern jeweils PLV = 1.0. Der bestehende Metrikexport erzeugt
42 Kennzahlzeilen ohne rohe Phasensamples oder Frame-/Slice-Zuordnung. Es werden
keine Exportdateien geschrieben. Die genaue Float-Darstellung ist ein lokaler
Laufwert; keine plattformübergreifende Bytegleichheit wird behauptet.

[ANNEX] Der Lauf belegt einen vorhandenen synthetischen Kandidaten und eine
Verlustgrenze der Aggregation. Er wählt diesen Kandidaten nicht als HUD-Phase.
Der vorhandene LOG-ZN-Test und der Phasenvertrag halten zusätzlich den Verlust
der Windungsinformation durch reine Endwerte modulo 1 sichtbar.

## 4. Quellbindung

| Gelesene Quelle | SHA-256 der Bytes an der Basis |
| --- | --- |
| ui-app/lib/tesser3takt-frame.ts | `9d4cf7edb9a428cb966346d4b15cb4be6c42cae4b68a92ed9596f8fbbc2689bd` |
| ui-app/lib/tesser3takt-hud.ts | `32d71a442694383f27b657087bdbb778e98abf3a12ed88e00e9e4edce858caf8` |
| ui-app/lib/tesser3takt-slice-phase.ts | `68ce82ab343d0e4123b56175814145a1495acfc9fbadcec3cd8a05afe44be446` |
| ui-app/lib/tesser3takt-bridge.ts | `4f889c49bb96c59ca173f609cc6721fbdff894484297976971040764a21146e8` |
| ui-app/components/tesser3takt/Tesser3TaktHudV2.tsx | `ee942ad168c4bb82632d0f3474db5e05864ab1549b8cbb5394594bfdc60a6828` |
| src/tools/toy_resonance_dataset.py | `002d3857301225e8075fe2999f1a28d27ba67e5d781fb9ba174386ef8df5dc28` |
| src/core/metrics.py | `cbeb64d95c46445014c626f734dbd27280b60c34fa52f9bf511b797fa277c7cb` |
| tools/void011_metrics_export.py | `71a129cb871007c3d29c89ce18d8b2f2c1f36e50d4d56892e94dafeea6614984` |
| tests/unit/test_logzn_orbit.py | `a6e8add0781931fcbb6fa9a741f152d2113d25b2a3dd882a25ad5a64a7586434` |

## 5. Validierung und Umfang

[FAKT] Basis- und Nachprüfung bestehen mit jeweils 731 Python-Tests und
165 Subtests, Port-Lint, Core-Pointern und Claim-Lint. Governance besteht mit
15 Workflows und 22 synchronen VOID-Einträgen. Beide direkt aus diesem Audit
extrahierten Gegenläufe bestehen; 19 lokale Dokumentlinks, neun Quellhashes und
`git diff --check` sind geprüft. Vier optionale generierte Pfade fehlen weiterhin
wie an der Basis. CI und Review sind erst am konkreten PR-Head maßgeblich.

[ANNEX] Der Diff ergänzt zwei Dokumente und einen Anschlussverweis im bestehenden
Slice-Vertrag. Keine Laufzeit-, Lock-, GOLD-, Receipt- oder Kenogrammänderung;
keine privaten Quellenkennungen. Für diesen Dokumentdiff ist kein neuer
vollständiger lokaler UI-Build erforderlich. Der bestehende Claim-Lint erfasst
die Annex-Texte nicht; deren begrenzte Aussagen werden redaktionell geprüft.
