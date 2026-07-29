# ADR-0004: Application-Owned Event Bus, Explicitly Injected — No Singleton

- **Status:** Accepted
- **Datum:** 2026-07-29
- **Kontext-Fokus:** Event-Bus-Besitz in `Fractalsense/integration.py`

## Context

`Fractalsense/integration.py` verbindet Fractal-Visualization, Sensor-Integration und
Hypergraph-Visualization mit dem ResonanceEnhancer. Der Einstiegspunkt
`integrate_resonance_enhancer(app_context)` erhält den Bus der Anwendung über
`app_context["event_system"]` und registriert darauf vier Forwarding-Handler.

Die Handler emittierten das abgeleitete Event jedoch **nicht** auf diesem Bus. Jeder
von ihnen konstruierte lokal eine neue Instanz:

```python
from modular_app_structure import EventSystem
event_system = EventSystem()
event_system.emit_event("update_resonance_parameters", {...})
```

`EventSystem.__init__` legt ein eigenes `_event_handlers`-Dict an — die Registry ist
instanzgebunden. Die Emits liefen daher in eine sofort verworfene Registry: der Kreis
**UI → integration → UI schloss sich nie**. Die Integrationsschicht war inert, ohne
dass ein Test das bemerkt hätte.

Betroffen sind alle vier Ketten:

| Quell-Event | abgeleitetes Event |
|---|---|
| `colormap_updated` | `update_fractal_colormap` |
| `fractal_updated` | `generate_fractal_sound` |
| `sensor_data_updated` | `update_resonance_parameters` |
| `hypergraph_updated` | `generate_hypergraph_sound` |

## Decision

**Der Event-Bus gehört der Anwendung und wird explizit injiziert. Kein Singleton.**

1. **Eine Instanz, ein Besitzer.** Die Instanz, die `integrate_resonance_enhancer()`
   im `app_context` erhält, ist der explizite Besitzer des vollständigen Event-Kreises.
   Alle weitergeleiteten Events werden auf genau dieser Instanz emittiert.
2. **Injektion per Closure.** `_make_forwarder(event_system, mapper)` erzeugt einen
   Handler, der den Bus als Closure-Variable trägt. Kein Modul-Global, keine
   Registry, kein `functools.partial` nötig — der Bus wird zur Registrierungszeit
   gebunden.
3. **Abbildung von Transport getrennt.** Die `_on_*`-Funktionen sind reine
   Abbildungen `(event_type, event_data) -> (ziel_event, payload)` und emittieren
   nicht mehr selbst. Sie bleiben ohne Bus testbar; `_make_forwarder` übernimmt den
   Transport.
4. **`EventSystem` bleibt unverändert.** Kein globaler Zustand, keine Klassenattribute,
   kein Singleton-Zugriffspunkt. Zwei Instanzen bleiben vollständig unabhängig.
5. **Idempotente Registrierung.** `integrate_resonance_enhancer()` setzt den Marker
   `_resonance_enhancer_connected` **auf der Bus-Instanz** und überspringt einen
   zweiten Aufruf mit demselben Bus (Rückgabe weiterhin `True`). Der Marker hängt
   pro Instanz, nicht an der Klasse — ein frischer Bus ist nie vorbelastet.
6. **Verträge unverändert.** Event-Namen und Payload-Formen bleiben exakt wie zuvor;
   dies ist ein Transport-Fix, keine Protokolländerung.

## Consequences

- (+) Die Kette UI → `integration` → UI schließt sich; Abonnenten auf dem geteilten
  Bus erhalten die abgeleiteten Events tatsächlich.
- (+) Kein verstecktes globales Gedächtnis: wer den Bus besitzt, ist im Code sichtbar.
  Tests können beliebig viele unabhängige Busse aufbauen.
- (+) Die Abbildungslogik ist ohne Bus prüfbar (reine Funktionen).
- (+) Wiederholte Integration verdoppelt die Weiterleitung nicht mehr.
- (−) Die `_on_*`-Funktionen geben jetzt zurück statt zu emittieren. Ihre Signatur
  `(event_type, event_data)` bleibt, aber wer sie direkt aufruft, erhält ein Tupel
  statt eines Seiteneffekts.
- (−) Der Idempotenz-Marker wird per `setattr` auf einer fremden Instanz gesetzt.
  Bewusst gewählt gegenüber einer Modul-Registry (die wäre globaler Zustand) und
  gegenüber einer Listing-API auf `EventSystem` (die wäre eine Fremdänderung an
  `modular_app_structure`).

## Alternatives Considered

1. **`EventSystem` als Singleton** (`get_instance()` / Modul-Global) — verworfen.
   Löst das Symptom, führt aber globalen Zustand ein: Tests werden voneinander
   abhängig, mehrere unabhängige Busse werden unmöglich, und der Besitz des Kreises
   verschwindet aus dem Code. Ausdrücklich ausgeschlossen.
2. **Bus als drittes Argument durch die `_on_*`-Handler reichen**
   (`functools.partial(_on_x, event_system)`) — funktionsfähig, ändert aber die
   Signatur der `_on_*`-Funktionen und damit bestehende Aufrufstellen. Die
   Closure-Variante hält die Signatur stabil.
3. **Modul-weite `WeakSet` bereits integrierter Busse** für die Idempotenz —
   verworfen: das wäre erneut verstecktes globales Modulgedächtnis, genau die
   Eigenschaft, die diese Entscheidung vermeidet.
4. **Idempotenz nur dokumentieren statt erzwingen** — verworfen: eine doppelte
   Integration wäre still und würde jedes Event doppelt weiterleiten. Ein
   erzwungener No-Op ist billiger als eine Konvention.

## Essence Preservation Note

Die Entscheidung ändert **wer** ein Event zugestellt bekommt, nicht **was** zugestellt
wird. Event-Namen, Payload-Schlüssel und Ableitungsformeln (Magnituden, Basisfrequenz,
Modulationsindex, Akkordkomplexität) bleiben identisch — nachgewiesen durch
`Fractalsense/tests/integration/test_integration_event_bus.py`.

## Verification

`Fractalsense/tests/integration/test_integration_event_bus.py` (19 Fälle) prüft:

- alle vier Ketten auf **einem** geteilten Bus (Abonnent empfängt tatsächlich);
- unveränderte Payload-Formen inkl. Defaults;
- Idempotenz bei wiederholter Integration;
- Unabhängigkeit zweier `EventSystem`-Instanzen (kein Singleton-Verhalten);
- dass die Weiterleitung ausschließlich den injizierten Bus trifft.

Gegen die frühere Implementierung schlagen 14 dieser 19 Fälle fehl — darunter alle
vier Kettentests.
