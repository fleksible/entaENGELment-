# Arbeitsvereinbarung: menschliche Absicht und technische Merge-Prüfung

**Datum:** 2026-11-02  
**FOKUS:** bestätigtes Arbeitsprinzip nachvollziehbar festhalten  
**Basis:** `main@05712d827b5558b595438f38a1e3c7fc739a297f` nach Merge von PR #442

## Anlass und Autorisierung

Kevin bat darum, menschliche Merge-Entscheidungen an Absicht, Wirkung und Grenzen
auszurichten, während der Agent die technische Übersetzung und Prüfung übernimmt.
Er bestätigte dieses beschriebene Arbeitsprinzip und beauftragte seine dauerhafte
Festhaltung. Im selben Gespräch bestätigte er seinen eigenen manuellen Merge von
PR #442 und beschrieb seine wahrgenommene Dringlichkeit als eher gespürt als gewusst.

Der technische Befund und diese berichtete Motivation bleiben getrennt. Aus der
einzelnen manuellen Handlung oder dieser Arbeitsvereinbarung wird kein allgemeines
oder rückwirkendes Merge-Mandat abgeleitet. Die konkrete Repo-Fassung wird als
eigener PR zur verständlichen Übernahme vorgelegt.

## Ergebnis

- `docs/annex/MERGE_INTENT_DELEGATION_v0_1.md` hält Ziel-/Wirkungsentscheidung,
  technische Prüflast, begrenzte Delegation, Rückfragen und Revision zusammen.
- `AGENTS.md` verankert die Lesbarkeit menschlicher Checkpoints und verweist auf
  die Arbeitsvereinbarung. Ein eigener Code-Audit des Menschen wird nicht verlangt.
- Bestehende passende Freigaben werden wiederverwendet. Neue Wirkungen oder Grenzen
  werden konkret zurückübersetzt; technische Unklarheit wird nicht per menschlicher
  Unterschrift zu einem bestandenen Nachweis gemacht.
- Es wird kein konkretes Mandat registriert und kein Runtime-Consent-Gate geändert.
  Der Vertrag bestehender `HumanDecision`-Events bleibt unberührt.

## Prüfung

- `make verify`: **1144 passed, 2 skipped, 169 subtests passed**;
  Port-Lint, Pointer-Prüfung und Claim-Lint erfolgreich.
- Neun lokale Dokumentverweise in `AGENTS.md` und der Arbeitsvereinbarung aufgelöst.
- `git diff --check`: erfolgreich.
- Keine neuen Tests erforderlich: Die Änderung betrifft Dokumentation und
  Agentenanweisungen; der bestehende kanonische Prüflauf wurde ausgeführt.

## Geltung und Rückweg

Das menschlich bestätigte Prinzip und die agentisch formulierte Repo-Fassung sind
ausgewiesen. Die Anweisungen stehen nach Übernahme des PR im Hauptstand zur Verfügung.
Die Formulierung bleibt korrigierbar. Eine spätere Änderung des Delegationsrahmens
wird als solche zum Menschen zurückgebracht; dieser Text autorisiert sich nicht selbst.
