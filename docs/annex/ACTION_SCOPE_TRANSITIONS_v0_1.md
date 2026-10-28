# ACTION_SCOPE_TRANSITIONS_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** keines neu; beschreibt bestehende Checks und Lücken
**Datum:** 2026-10-28
**Anlass:** Vorschlag V6 (Checkup 2026-10-28, Gegen-Review)
**Bezug:** `src/core/action_gate.py`, `docs/annex/ACTION_GATE_v0_1.md`,
`docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md`, `AGENTS.md` (G0, G4)

---

## 1. Frage

Eine Einwilligung oder Freigabe gilt für eine Handlung in einem bestimmten
Handlungsraum. Welche Erweiterungen dieses Raums prüft das Repo heute, und welche
nicht? Gleichbleibendes Aufgabenziel bedeutet nicht gleichbleibenden Handlungsraum:
neue Empfänger, Ressourcen oder Nebenwirkungen können hinzukommen, ohne dass das
Ziel wechselt.

Diese Notiz führt **kein** `scope`-Feld ein. Ein solches Feld braucht zuerst eine
durchgesetzte Bedeutung; die Tabelle unten ist die Vorarbeit dafür.

## 2. Übergangstabelle

„Erweiterung“ heißt: der neue Zustand verlangt mehr Vertrauen, erreicht mehr oder
ist schwerer rückgängig zu machen als der freigegebene.

| Dimension | Erlaubt ohne neue Freigabe | Erweiterung (neue Freigabe nötig) | Bestehender Check | Lücke |
|---|---|---|---|---|
| **Effektklasse** | keine Wirkung → keine Wirkung | +Netzwerk, +Dateisystem, +Prozess | Action-Gate: jeder Effekt → `HOLD`, `HUMAN_ONLY` (`NETWORK_REQUIRED`, `FILESYSTEM_EFFECT`, `PROCESS_EFFECT`) | Vergleich „vorher/nachher“ fehlt: das Gate bewertet ein einzelnes Proposal, keinen Übergang zwischen zwei |
| **Umkehrbarkeit** | `reversible` → `reversible` | `reversible` → `irreversible`/`unknown` | Action-Gate: alles außer `reversible` → `IRREVERSIBLE_EFFECT`, `HUMAN_ONLY` | „reversible“ ist eine Angabe des Aufrufers, nicht geprüft |
| **Sichtbarkeit** | gleich oder privater | privater → öffentlicher | Action-Gate klemmt auf die Quelle (`_resolve_visibility`); ERK-Export lässt `private` ganz weg (Invariante 11) | keine |
| **Empfänger** | — | jeder neue Empfänger oder Kanal | **keiner** | Das Repo kennt kein Empfänger-Feld; Weitergabe an Dritte ist nicht modelliert |
| **Ressourcen** | dieselbe Ressource/Version | andere Ressource, andere Version, andere Registry | Action-Gate: Registry-Allowlist je Ökosystem, Versions-Pin, Quellverifikation → sonst `HOLD` | Bindung „freigegeben war Ressource X“ fehlt; jedes Proposal wird für sich bewertet |
| **Vertrauen der Quelle** | gleich oder vertrauenswürdiger | trusted → untrusted, unbekannt | `normalize_trust`: Unbekanntes → `UNTRUSTED`; Action-Gate → `HOLD`; ERK: untrusted promotet nie (Invariante 8) | Keine Ableitungsverfolgung: aus untrusted Material abgeleitetes Material erbt den Status nicht automatisch (siehe V7-Notiz) |
| **Aufgabenziel** | gleich | neues Ziel | G4 (Metatron): Fokus-Switch → STOP und fragen; `metatron_check` verlangt `FOKUS:` im PR | G4 erkennt Zielwechsel, nicht Erweiterungen bei gleichem Ziel |

## 3. Einordnung von G4

G4 ist ein **Teilaspekt**: Es stoppt, wenn die Aufgabe wechselt. Die Zeilen
„Empfänger“ und „Ressourcen“ zeigen Erweiterungen, die bei gleichem Ziel auftreten
können und die G4 nicht erfasst. Der Consent-collapse-Artikel (AI and Ethics,
2026) beschreibt genau diese Lücke zwischen autorisierter Aufgabe und tatsächlichem
Handlungsraum; sein sichtbarer Abstract nennt das eigene Framework einen
normativen Vorschlag ohne empirische Validierung. Der Volltext war nicht zugänglich.

## 4. Was ein späteres `scope`-Feld leisten müsste

Nur als Voraussetzungsliste, nicht als Entwurf:

1. eine Bindung zwischen Freigabe und den sieben Dimensionen oben;
2. ein Vergleich „angefragt vs. freigegeben“, der jede Erweiterung als neue
   Freigabepflicht meldet;
3. fail-closed bei unbekannten Werten (wie `normalize_trust`, `_resolve_visibility`);
4. Empfänger und Ressourcen als geschlossene, prüfbare Felder.

## 5. Quellen

- Code und Tests: `src/core/action_gate.py`, `src/core/evidence_routing.py`,
  `tests/unit/test_action_gate.py`, `tests/ethics/test_erk_invariants.py`,
  `tests/ethics/test_trust_visibility_boundaries.py`.
- Consent collapse in agentic AI, AI and Ethics (2026),
  https://link.springer.com/article/10.1007/s43681-026-01287-w — nur Abstract
  (Volltext hinter Anmeldung).
