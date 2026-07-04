# BREADCRUMB_LINT — claim_tags_v0_2

**Status:** Simulation / Intake-Kandidat  
**Datum:** 2026-07-04  
**Bezug:** `policies/claim_tags_v0_2.yaml`, `docs/governance/CLAIM_LEITER_v0_1.md`

---

## Zweck

Dieser Lint prüft, ob das Tag-System als offene Such- und Orientierungsstruktur funktioniert. Tags sollen Status klären, aber keine Zustimmung erzwingen und keine vollständige Übernahme des Frameworks verlangen.

---

## Prüfkriterien

1. Klärt ein Tag Status statt Zustimmung zu verlangen?
2. Kann ein externer Leser einzelne Tags verwenden, ohne das gesamte Framework zu übernehmen?
3. Bleibt `[METAPHER]` klar von Evidence getrennt?
4. Gibt es Raum für `ROHSEDIMENT`, Zweifel, `[VOID]` und Rücknahme?
5. Wird Inspiration als Inspiration markiert, nicht als Beweis?
6. Ist die Claim-Leiter ein Koordinatensystem statt einer Wert-Rangordnung?
7. Kann ein Artefakt verworfen oder lokal angepasst werden, ohne dass dies als Ausschluss gilt?

---

## Befund

Der Tag-Kanon ist gut ausgerichtet, wenn drei Regeln ausdrücklich erhalten bleiben:

- partielle Nutzung ist erlaubt
- Verwerfen ohne Ausschluss ist erlaubt
- Leiter ist kein Werturteil

Die wichtigste Lücke wäre eine fehlende Regel zu partieller Nutzung. Diese ist in `claim_tags_v0_2.yaml` deshalb als globale Regel aufgenommen.

---

## Empfohlene YAML-Schalter

```yaml
partial_use_allowed: true
no_framework_adoption_required: true
rejection_without_exclusion: true
metaphor_is_not_evidence: true
void_is_not_failure: true
```

---

## Fazit

Tags sind Intervalle, keine Käfige. Sie markieren Verhältnis und Status, nicht Identität oder Zugehörigkeit.
