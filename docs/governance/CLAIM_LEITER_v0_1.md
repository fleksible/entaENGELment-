# CLAIM_LEITER_v0_1

**Status:** Draft / Intake-Kandidat  
**Datum:** 2026-07-04  
**Claim-Status:** [SPEC-WIP]  
**Bezug:** `policies/claim_tags_v0_2.yaml`

---

## 1. Zweck

Die Claim-Leiter beschreibt mögliche Bewegungen zwischen Claim-Status. Sie ist kein Werturteil und kein Fortschrittszwang.

Ein Claim darf dauerhaft `ROHSEDIMENT`, `[METAPHER]` oder `[VOID]` bleiben, wenn dies der sauberste Status ist.

---

## 2. Grundregel

> Die Leiter ist ein epistemisches Koordinatensystem, keine Rangordnung.

Höhere Tags bedeuten nicht höhere Wahrheit für fremde Nutzer. Sie bedeuten nur einen stärker eingegrenzten Status innerhalb dokumentierter Annahmen.

---

## 3. Typische Bewegungen

```text
ROHSEDIMENT
  -> [METAPHER]
  -> [HYPOTHESE]
  -> [INFERENZ]
  -> [MODEL]
  -> [SPEC-WIP]
  -> [SPEC]
  -> [CANON]
```

Diese Darstellung ist nur eine Leseschneise. Seitensprünge, Rücknahmen und dauerhafte Grenzen sind erlaubt.

---

## 4. Dauerzustände

### ROHSEDIMENT
Raw material, Spur, Notiz, Intuition oder Chat-Treffer vor Review. ROHSEDIMENT ist kein Defizit.

### [METAPHER]
Metapher, Analogie, Bild oder Rosetta-Sprache. Wertvoll für Orientierung, aber keine Evidence.

### [VOID]
Offene Grenze, ungelöste Frage, Widerspruch oder bewusst nicht geschlossener Raum. VOID darf dauerhaft bleiben.

---

## 5. Anti-Capture-Regeln

1. Partielle Nutzung ist erlaubt.
2. Niemand muss das gesamte Framework übernehmen, um einzelne Tags zu verwenden.
3. Verwerfen, Umbauen oder lokale Nutzung ist kein Ausschluss.
4. Tags sind Intervalle, keine Käfige.
5. Claim-Status klärt Beziehung, nicht Identität.

---

## 6. Provenienz-Schutz

Ein Material Pointer, Receipt, Chat-Treffer oder späteres Artefakt kann Herkunft oder Einfluss zeigen. Er ist nicht automatisch Beweis für den Claim.

Metapher, Inspiration und Analogie dürfen eine Hypothese motivieren, aber nicht direkt `[INFERENZ]`, `[MODEL]`, `[SPEC]` oder `[CANON]` begründen.

---

## 7. Empfohlene Review-Fragen

- Erzwingt der Tag Zustimmung oder klärt er Status?
- Kann ein fremder Leser den Tag nutzen, ohne die Symbolwelt zu übernehmen?
- Bleibt Metapher von Evidence getrennt?
- Gibt es Raum für Zweifel, VOID und Rücknahme?
- Kann jemand das Artefakt verwerfen, ohne aus dem System herauszufallen?

---

## 8. Tooling-Hinweis

Die vorhandenen Lint-Werkzeuge können enger sein als dieser Draft-Kanon. Harte Enforcement-Schritte brauchen erst Tool-Anpassung und Testabdeckung.
