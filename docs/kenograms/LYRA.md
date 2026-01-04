# ☐-LYRA — Audiohook (7‑Band Sonifikation)

**Status:** Stub (Kenogramm)

## Frage
Wie lässt sich ein stabiler, auditierbarer Audiohook definieren, der Übergänge/Resonanz (z.B. TransitionAlpha, PLV) in eine 7‑Band‑Sonifikation abbildet, ohne falsche Kausalität zu behaupten?

## Hypothese
- 7 Bänder ↔ 7 Klassen / 7 Spektral-Slots (nur als Mapping-Schicht, nicht als Ontologie)
- Jede Bandpass-Änderung erzeugt ein Receipt (ClaimType: INFERENCE/HYPOTHESIS)

## Nächster Schritt
- Definiere ein kleines JSON-Schema für "AudioMappingReceipt" in `spec/`
- Toy-Demo (in-silico) mit synthetischen Signalen + deterministischem Rendering.
