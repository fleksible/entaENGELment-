# S4 ↔ LOG-ZN Bridge

Claim-Tags: [FACT] [MODEL] [INFERENCE] [HYPOTHESIS]
Status: [ANNEX] — Brückendokument, keine Identitätsbehauptung

## 0. Problemstellung

Annex F beschreibt `S4` als diskreten Zustandsraum des tesser3TAKT: Permutationsstruktur, Inversionszahl, Cayley-Graph und Phasenübergangslogik.

`LOG-ZN-ORBIT-001` beschreibt dagegen eine kontinuierliche Hebung: Ein scheinbar geschlossener Orbit wird durch den entwickelten Winkel und die Windungszahl `k` zu einer geschichteten Struktur.

Dieses Dokument trennt beide Operatoren sauber und markiert ihren gemeinsamen Nenner.

## 1. Nicht-Gleichsetzung

[FACT] `S4` ist die symmetrische Gruppe auf vier Elementen.

[FACT] `log(z)` ist der mehrwertige komplexe Logarithmus.

[MODEL] Beide können als Gedächtnisoperatoren für Transformation gelesen werden.

Nicht zulässig:

```text
S4 = log(z)
log(z) = tesser3TAKT
tesser3TAKT = physikalischer Spinor
```

Zulässig:

```text
S4 und LOG-ZN markieren verschiedene Arten, Transformationsgeschichte nicht als Reset zu behandeln.
```

## 2. Vergleichsmatrix

| Aspekt | S4 | LOG-ZN |
|---|---|---|
| Strukturtyp | diskret | kontinuierlich / mehrblättrig |
| Grundraum | 24 Permutationen | Orbit um 0 / Branch Point |
| Gedächtnis | Inversionszahl `inv(π)` / Pfadlänge | Windungszahl `k` |
| lokale Operation | Transposition / Permutation | Winkelentwicklung |
| globale Operation | Reordering | Umkreisung |
| Framework-Funktion | tesser3TAKT-Pulsation zählbar machen | RZT-Orbit/Wiederkehr lesbar machen |
| Risiko | Überalgebraisierung | Symbolüberdehnung |
| Testidee | Random Walk / Inversionsverlauf | Orbit-Replay / k-Tracking |

## 3. Gemeinsamer Nenner

[MODEL] Der gemeinsame Nenner ist nicht Geometrie, sondern Gedächtnis:

```text
Transformation + nichtgelöschte Spur = Zustand mit Geschichte
```

Bei S4:

```text
Permutation π + inv(π) = diskretes Reordering-Gedächtnis
```

Bei LOG-ZN:

```text
Orbit + k = kontinuierliches Windungs-Gedächtnis
```

## 4. RZT-Lesart

[INFERENCE] RZT verlangt, dass eine Distinktion ihren Geltungsbereich, ihre Mitte und ihren Setzungsstatus markiert.

S4 erfüllt das für diskrete Zustandswechsel:

```text
Zustand π → Pfad auf Cayley-Graph → Distanz / Inversion
```

LOG-ZN erfüllt das für Wiederkehrbewegungen:

```text
θ mod 2π → sichtbare Wiederkehr
θ + 2πk → entwickelte Rückkehr
```

Beide verhindern denselben Fehler:

> Ein scheinbar gleicher Zustand wird nicht automatisch als identisch behandelt.

## 5. Hypothese für tesser3TAKT

[HYPOTHESIS] S4 und LOG-ZN können als zwei komplementäre Leseschichten des tesser3TAKT behandelt werden:

```text
S4        → lokale Permutations-/Reordering-Schicht
LOG-ZN    → globale Windungs-/Reentry-Schicht
```

Möglicher Mapping-Vorschlag:

| tesser3TAKT-Moment | S4-Lesung | LOG-ZN-Lesung |
|---|---|---|
| Systole | konkrete Permutation | sichtbarer Orbitpunkt |
| Diastole | Pfad-/Reordering-Raum | entwickelte Winkelspur |
| Reentry | neue Permutation / geringere Inversion | neue Windung `k+1` |
| A4-Bruch | diskontinuierlicher Sprung im Graphen | Branch-/Cut-Konflikt |
| Receipt | dokumentierte Transformation | gespeicherter Windungsstand |

## 6. Falsifikationspfad

LOG-ZN bleibt ein poetisch-operativer Annex, wenn:

- `k` keine zusätzliche Klassifikationsleistung gegenüber `inv(π)` bringt;
- Wiederkehrqualitäten besser allein durch S4-Pfade beschrieben werden;
- keine operationalisierbaren Reentry-Fälle gefunden werden.

LOG-ZN wird als eigener RZT-Operator stärker, wenn:

- Reentry-Fälle existieren, bei denen sichtbare Wiederholung gleich bleibt, aber Windungsstand die Deutung ändert;
- `k` hilft, A4d/Nektar/Nichtraum-Übergänge zu unterscheiden;
- ein VOID- oder Receipt-Pfad ohne `k` schlechter auditierbar wäre.

## 7. Minimaler Testfall

```text
Input: Wiederkehrender Prozess P mit identischer sichtbarer Position X.
Frage 1: Gibt es einen entwickelbaren Verlauf θ_unwrapped?
Frage 2: Gibt es einen diskreten Windungszähler k?
Frage 3: Ändert k die Claim-/VOID-/Receipt-Entscheidung?
```

Wenn Frage 1–3 positiv sind, ist LOG-ZN operational relevant.

## 8. Schlussformel

```text
S4 zählt Umordnungen.
LOG-ZN zählt Umkreisungen.
RZT entscheidet, ob die gezählte Spur als legitime Distinktion auftreten darf.
```
