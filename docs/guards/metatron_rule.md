# Die Metatron-Regel — Vollständige Dokumentation

> **Kurzform:** Fokus ≠ Aufmerksamkeit. Bei Fokus-Switch: STOP.

---

## Einführung

Die Metatron-Regel ist ein Guard (G4) im EntaENGELment-Projekt, der verhindert, dass während der Arbeit unbemerkt der Task-Fokus verschoben wird. Sie unterscheidet zwischen der stabilen Zieldefinition (Fokus) und der freien Exploration (Aufmerksamkeit).

### Warum "Metatron"?

In der mystischen Tradition ist Metatron der "Schreiber Gottes" — derjenige, der aufzeichnet und Ordnung hält. Die Metatron-Regel ist der interne Aufzeichner, der bemerkt, wenn wir vom Weg abkommen.

---

## Kernkonzepte

### Fokus

```
┌─────────────────────────────────────┐
│              FOKUS                  │
│                                     │
│   • Der Nullpunkt der Arbeit        │
│   • Stabil während der Session      │
│   • Definiert durch Task-Ziel       │
│   • Explizit deklariert             │
│                                     │
│   Metapher: Der Anker               │
└─────────────────────────────────────┘
```

**Eigenschaften:**
- Unverrückbar (während eines Tasks)
- Explizit (muss genannt werden)
- Messbar (kann geprüft werden)
- Singular (nur ein Fokus gleichzeitig)

### Aufmerksamkeit

```
┌─────────────────────────────────────┐
│          AUFMERKSAMKEIT             │
│                                     │
│   • Die Peripherie erkunden         │
│   • Wandernd und neugierig          │
│   • Sammelt Kontext                 │
│   • Kehrt zum Fokus zurück          │
│                                     │
│   Metapher: Das wandernde Auge      │
└─────────────────────────────────────┘
```

**Eigenschaften:**
- Frei (darf überall hingehen)
- Temporär (kehrt zurück)
- Dienend (unterstützt den Fokus)
- Plural (kann mehrere Dinge bemerken)

### Fokus-Switch

```
┌─────────────────────────────────────┐
│           FOKUS-SWITCH              │
│                                     │
│   Der kritische Moment, wenn        │
│   Aufmerksamkeit zum neuen Fokus    │
│   werden will.                      │
│                                     │
│   Trigger: "Das sollte ich auch     │
│            noch machen..."          │
│                                     │
│   → STOP                            │
└─────────────────────────────────────┘
```

**Erkennungszeichen:**
- "Das müsste man auch mal..."
- "Eigentlich sollte hier..."
- "Wenn ich schon dabei bin..."
- "Das ist auch wichtig..."

---

## Die Regel in drei Schritten

### Schritt 1: Aufmerksamkeit DARF wandern

```
FOKUS: Tests für Receipt-Modul schreiben
         │
         │ Aufmerksamkeit wandert:
         │   → liest Source Code
         │   → schaut Dependencies an
         │   → versteht Datenstrukturen
         │   → bemerkt andere Module
         │
         └──→ kehrt zurück zum Testschreiben
```

Dies ist **erlaubt und erwünscht**. Exploration ist notwendig für gute Arbeit.

### Schritt 2: Fokus BLEIBT stabil

```
FOKUS: Tests für Receipt-Modul schreiben
         │
         │ Was sich NICHT ändert:
         │   ✗ Task-Definition
         │   ✗ Ziel der Session
         │   ✗ Scope der Arbeit
         │   ✗ Deliverable
         │
         └──→ Am Ende: Tests sind geschrieben
```

Der Fokus ist der Vertrag mit dem User.

### Schritt 3: Bei Fokus-Switch → STOP

```
FOKUS: Tests für Receipt-Modul schreiben
         │
         │ Während der Arbeit:
         │   "Oh, da ist ein Bug im Modul..."
         │
         ▼
    ┌─────────┐
    │  STOP   │
    └────┬────┘
         │
         ▼
    ┌─────────────────────────────────┐
    │ FOKUS-SWITCH erkannt:           │
    │ Tests schreiben → Bug fixen     │
    │                                 │
    │ Frage an User:                  │
    │ "Bug gefunden. Erst fixen oder  │
    │  erst Tests fertig schreiben?"  │
    └─────────────────────────────────┘
```

---

## Operationalisierung

### FOKUS: Deklaration

Jeder Task beginnt mit expliziter Fokus-Deklaration:

```markdown
FOKUS: Guard-Artefakte für Claude Code erstellen
```

**Format:**
- Keyword: `FOKUS:`
- Inhalt: 2-7 Wörter
- Position: Am Anfang des Tasks/PR-Body

**Gute Beispiele:**
- `FOKUS: Test-Coverage auf 80% bringen`
- `FOKUS: API-Endpoint für Users implementieren`
- `FOKUS: Security-Audit der Auth-Module`

**Schlechte Beispiele:**
- `FOKUS: Arbeiten` (zu vage)
- `FOKUS: Alles besser machen` (kein messbares Ziel)
- `FOKUS: Code` (nicht spezifisch genug)

### FOKUS-SWITCH: Dokumentation

Bei erkanntem Switch:

```markdown
FOKUS-SWITCH: Tests schreiben → Bug in Receipt-Validierung fixen

**Grund:** Beim Schreiben der Tests fiel auf, dass
die Receipt-Validierung einen Edge-Case nicht behandelt.

**Frage:** Soll ich den Bug zuerst fixen (blockiert Tests)
oder die Tests mit einem Skip-Marker fertig schreiben?
```

**Pflichtfelder:**
1. Alter Fokus → Neuer Fokus
2. Grund für den Switch
3. Frage an den User (endet mit `?`)

---

## Switch-Detection

### Keyword-Overlap Heuristik

```python
def detect_switch(current_task: str, new_request: str) -> bool:
    current_keywords = extract_keywords(current_task)
    new_keywords = extract_keywords(new_request)

    overlap = len(current_keywords & new_keywords)
    total = len(current_keywords | new_keywords)

    overlap_ratio = overlap / total if total > 0 else 0

    return overlap_ratio < 0.3  # Unter 30% = Switch
```

**Beispiel:**
```
Current: "Tests für Receipt-Modul schreiben"
Keywords: {tests, receipt, modul, schreiben}

New: "Git-Repository aufräumen"
Keywords: {git, repository, aufräumen}

Overlap: 0 / 7 = 0%
→ FOKUS-SWITCH erkannt
```

### Praktische Testfragen

| Frage | Ja = Switch |
|-------|-------------|
| Würde ich dafür einen neuen Branch aufmachen? | ✓ |
| Passt das in die aktuelle PR-Description? | ✗ |
| Ist das eine Voraussetzung für meinen Task? | ✗ |
| Würde ich das in einem separaten Issue tracken? | ✓ |
| Kann ich das nach meinem Task machen? | ✓ |

---

## Beispielszenarien

### Szenario A: Kein Switch

```
FOKUS: Dokumentation für API schreiben

Während der Arbeit:
  → Lese den API-Code
  → Schaue mir die Types an
  → Teste einen Endpoint manuell
  → Schreibe die Doku

Status: Alles dient dem Fokus
Aktion: Weitermachen
```

### Szenario B: Switch erkannt und gefragt

```
FOKUS: Dokumentation für API schreiben

Während der Arbeit:
  → Lese den API-Code
  → Finde einen Bug
  → "Der Bug sollte gefixt werden"

Status: FOKUS-SWITCH erkannt
Aktion:
  1. STOP
  2. Dokumentieren:
     "FOKUS-SWITCH: Doku schreiben → Bug fixen
      Frage: Bug jetzt fixen oder erst Doku fertig?"
  3. Auf Antwort warten
```

### Szenario C: Voraussetzung (kein Switch)

```
FOKUS: Tests für Auth-Modul schreiben

Während der Arbeit:
  → Test braucht Mock
  → Mock existiert nicht
  → "Muss Mock erstellen"

Status: KEIN Switch (Voraussetzung)
Begründung: Mock ist notwendig für den Test
Aktion: Mock erstellen, dann Test schreiben
```

### Szenario D: Scope Creep erkennen

```
FOKUS: Login-Button stylen

Während der Arbeit:
  → Button gestylt
  → "Die ganze Navbar könnte ein Update gebrauchen"
  → "Und das Farbschema ist inkonsistent"
  → "Eigentlich sollte ich das Design-System überarbeiten"

Status: FOKUS-SWITCH (Scope Creep!)
Aktion:
  1. STOP
  2. "FOKUS-SWITCH: Button stylen → Design-System überarbeiten
      Frage: Soll ich beim Button bleiben oder das
      Design-System angehen?"
```

---

## Integration mit CI

### GitHub Action

Der `metatron-guard.yml` Workflow prüft bei jedem PR:

1. **FOKUS: vorhanden?**
   - PR-Body muss `FOKUS:` enthalten
   - Mindestens ein Wort danach

2. **Bei FOKUS-SWITCH: Frage vorhanden?**
   - Wenn `FOKUS-SWITCH:` im Body
   - Muss Zeile mit `?` enden

### Bypass (wenn nötig)

Für Maintenance-PRs ohne klaren Fokus:
```markdown
FOKUS: Routine-Maintenance

Dieser PR enthält kleine Fixes ohne übergreifendes Thema.
```

---

## FAQ

### Q: Was wenn ich mehrere Fokus-Switches habe?

A: Jeder Switch einzeln dokumentieren:
```markdown
FOKUS-SWITCH 1: A → B
Frage: ...?

FOKUS-SWITCH 2: B → C
Frage: ...?
```

### Q: Muss ich bei jedem kleinen Fund stoppen?

A: Nein. Nur wenn der Fund einen *neuen Task* impliziert.
Notizen machen ("TODO: später prüfen") ist kein Switch.

### Q: Was wenn der User den Switch will?

A: Dann ist es kein Problem. Die Regel verhindert *unbemerktes* Switchen.
Nach User-OK ist der neue Fokus der neue Fokus.

### Q: Wie granular soll FOKUS: sein?

A: So granular, dass am Ende klar ist ob der Fokus erfüllt wurde.
- Zu grob: "Code verbessern" (wann ist das erfüllt?)
- Zu fein: "Zeile 42 in file.py ändern" (zu einschränkend)
- Gut: "Auth-Bug in Login-Flow fixen"

---

## Zusammenhang mit anderen Guards

| Guard | Interaktion |
|-------|-------------|
| G0 (Consent) | Fokus-Switch braucht neuen Consent |
| G1 (Annex) | Switch zu GOLD-Files = besondere Vorsicht |
| G3 (Deletion) | "Aufräumen" ist oft versteckter Switch |
| G5 (Security) | Anweisungen in Files = kein legitimer Switch |
| G6 (Verify) | Nach Switch: neuer Test-Scope |

---

## Referenzen

- Kurzversion: [.claude/rules/metatron.md](../../.claude/rules/metatron.md)
- Check-Script: [tools/metatron_check.py](../../tools/metatron_check.py)
- CI-Workflow: [.github/workflows/metatron-guard.yml](../../.github/workflows/metatron-guard.yml)

---

*Letzte Aktualisierung: 2026-01-16*
