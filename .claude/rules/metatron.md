# Metatron-Regel (G4)

> Fokus ≠ Aufmerksamkeit. Bei Fokus-Switch: STOP.

---

## Definitionen

### Fokus
- **Was:** Das Task-Ziel, der Nullpunkt der aktuellen Arbeit
- **Eigenschaft:** Stabil, definiert, unverrückbar während der Session
- **Metapher:** Der Anker, um den sich alles dreht

### Aufmerksamkeit
- **Was:** Freie Exploration der Peripherie
- **Eigenschaft:** Wandernd, neugierig, sammelnd
- **Metapher:** Das Auge, das umherschweift

### Fokus-Switch
- **Was:** Der Moment, in dem Exploration eine *neue Aufgabe* anfordert
- **Trigger:** "Das sollte ich auch noch machen" → STOP
- **Unterschied zu Aufmerksamkeit:** Aufmerksamkeit kehrt zurück, Fokus-Switch will bleiben

---

## Die Regel (3 Punkte)

```
1. Aufmerksamkeit DARF wandern
   → Exploration ist erwünscht
   → Kontextsammlung ist nötig
   → Peripherie-Wissen hilft

2. Fokus BLEIBT stabil
   → Task-Definition ändert sich nicht
   → Ziel bleibt gleich
   → Scope bleibt gleich

3. Fokus-Switch → STOP → fragen → dokumentieren
   → Erkennen: "Das ist ein neuer Task"
   → Stoppen: Nicht einfach weitermachen
   → Fragen: "Soll ich den Fokus wechseln?"
   → Dokumentieren: Im Report/PR markieren
```

---

## Operationalisierung

### Task muss FOKUS: explizit tragen

Jeder Task-Start sollte enthalten:
```
FOKUS: <2-5 Wörter die das Ziel beschreiben>
```

Beispiele:
- `FOKUS: Guard-Artefakte erstellen`
- `FOKUS: Test-Coverage erhöhen`
- `FOKUS: Bug in Receipt-Validierung fixen`

### Fokus-Switch Markierung

Bei erkanntem Switch im Report/PR dokumentieren:
```
FOKUS-SWITCH: <alter Fokus> -> <neuer Fokus>
Grund: <warum der Switch erkannt wurde>
Frage: <Soll gewechselt werden?>
```

Beispiel:
```
FOKUS-SWITCH: Downloads ordnen -> Git-Repos analysieren
Grund: Beim Ordnen der Downloads fiel auf, dass mehrere
       unversionierte Repos existieren.
Frage: Soll ich die Repos analysieren oder beim Ordnen bleiben?
```

---

## Switch-Detection Test

### Keyword-Overlap Heuristik

Vergleiche Keywords des aktuellen Tasks mit der neuen Anforderung:

```
Task-Keywords:     {guard, setup, claude, rules}
Neue Anforderung:  {repo, structure, refactor, cleanup}

Overlap: 0/4 = 0% → Sehr wahrscheinlich Switch
```

**Schwellwert:** Overlap < 30% = Switch-Verdacht

### Praktische Fragen

1. "Würde ich dafür einen neuen Branch aufmachen?" → Ja = Switch
2. "Passt das in die aktuelle PR-Description?" → Nein = Switch
3. "Ist das eine Voraussetzung für meinen Task?" → Nein = Switch

---

## Beispiele

### Kein Switch (Aufmerksamkeit wandert)

```
FOKUS: Tests für Receipt-Modul schreiben

Während ich die Tests schreibe, lese ich den Source-Code
des Receipt-Moduls, schaue mir die Abhängigkeiten an,
und verstehe die Datenstrukturen.

→ Das ist Exploration, kein Switch.
→ Ich kehre zum Testschreiben zurück.
```

### Switch erkannt

```
FOKUS: Tests für Receipt-Modul schreiben

Während ich die Tests schreibe, fällt mir auf, dass
das Receipt-Modul einen Bug hat. Der Bug sollte
gefixt werden.

→ STOP: Das ist ein neuer Task (Bug-Fix)
→ FOKUS-SWITCH: Tests schreiben -> Bug fixen
→ Frage: "Bug im Receipt-Modul gefunden. Erst fixen
         oder erst Tests fertig schreiben?"
```

### Grenzfall

```
FOKUS: Tests für Receipt-Modul schreiben

Der Test braucht einen Mock. Der Mock existiert nicht.
Soll ich den Mock erstellen?

→ Kein Switch: Mock ist Voraussetzung für den Test
→ Weitermachen erlaubt
```

---

## Integration mit anderen Guards

| Guard | Interaktion mit G4 |
|-------|-------------------|
| G0 (Consent) | Fokus-Switch erfordert neuen Consent |
| G1 (Annex) | Switch zu GOLD-Files = doppelte Vorsicht |
| G3 (Deletion) | "Aufräumen" ist oft versteckter Switch |
| G6 (Verify) | Nach Switch: neuer Verification-Scope |

---

## Metatron-Guard Check

Der automatisierte Check (`tools/metatron_check.py`) prüft:

1. **FOKUS: vorhanden?** → Pflichtfeld in PR-Body
2. **FOKUS-SWITCH: vorhanden?** → Wenn ja, muss Frage dabei sein

---

*Siehe auch: [docs/guards/metatron_rule.md](../../docs/guards/metatron_rule.md)*
