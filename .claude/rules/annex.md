# Annex-Prinzip (G1)

> Index/Policy = GOLD, Code = ANNEX, Receipts = IMMUTABLE

---

## Grundprinzip

Das Repository hat eine klare Hierarchie:

1. **GOLD** — Der unveränderliche Kern
2. **ANNEX** — Der änderbare Arbeitsbereich
3. **IMMUTABLE** — Niemals modifizieren (Audit-Trail)

Änderungen fließen von ANNEX nach GOLD, nie umgekehrt ohne explizite Genehmigung.

---

## GOLD (Unveränderlich)

### Pfade

| Pfad | Inhalt | Warum geschützt? |
|------|--------|-----------------|
| `index/` | Master-Index, Pointer | Strukturelle Integrität |
| `policies/` | Policy-Definitionen | Governance |
| `VOIDMAP.yml` | Projekt-Kompass | Navigation |
| `VOIDMAP.yaml` | (Alternative Extension) | Navigation |

### Regeln

```
1. Nur lesen, nicht schreiben
2. Änderungen nur nach expliziter Anweisung
3. Bei jeder Änderung: Begründung im Commit
4. Review erforderlich vor Merge
```

### Änderungsprozess für GOLD

```
1. User gibt explizite Anweisung
2. Begründung dokumentieren
3. Minimal-invasive Änderung planen
4. CHECKPOINT: Plan zeigen
5. Nach OK: Änderung durchführen
6. Commit mit ausführlicher Message
7. PR mit GOLD-CHANGE Label
```

---

## ANNEX (Änderbar)

### Pfade

| Pfad | Inhalt | Änderungsfreiheit |
|------|--------|-------------------|
| `src/` | Source Code | Frei (nach Plan) |
| `tools/` | Utility Scripts | Frei |
| `tests/` | Test-Code | Frei |
| `docs/` | Dokumentation | Frei (außer `negations.md`) |
| `scripts/` | Build/Deploy Scripts | Mit Vorsicht |
| `reports/` | Generierte Reports | Frei |
| `tickets/` | Task-Tickets | Frei |
| `schedules/` | Zeitpläne | Frei |
| `overlay/` | Overlay-Module | Frei |
| `aggregates/` | Aggregat-Module | Frei |
| `Plugins/` | Plugin-System | Mit Vorsicht |
| `Fractalsense/` | Fractalsense-Modul | Frei (nach Plan) |
| `bio_spiral_viewer/` | Visualisierung | Frei |
| `dashboard/` | Dashboard-UI | Frei |
| `lyra/` | Lyra-Subsystem | Frei |
| `ui-app/` | Next.js UI App | Frei (nach Plan) |
| `__tests__/` | Jest Tests | Frei |
| `adapters/` | Adapter-Schicht | Frei |
| `diagrams/` | Diagramme | Frei |
| `runbooks/` | Runbook-Docs | Frei |

### Regeln

```
1. Plan-First gilt trotzdem (G0)
2. Tests müssen grün bleiben (G6)
3. Keine Breaking Changes ohne Consent
4. Deletion-Verbot beachten (G3)
```

### Sonderstatus: docs/negations.md

`docs/negations.md` ist Teil von ANNEX, hat aber erhöhten Schutz:
- Enthält die "Negative Theologie" des Projekts
- Änderungen nur nach Diskussion
- Behandeln wie Semi-GOLD

---

## IMMUTABLE (Niemals modifizieren)

### Pfade

| Pfad | Inhalt |
|------|--------|
| `data/receipts/` | Signierte Receipts |
| `receipts/` | (Legacy-Pfad) |

### Warum IMMUTABLE?

Receipts sind der Audit-Trail des Projekts:
- HMAC-signiert
- Chronologisch
- Nicht-repudiierbar

Jede Modifikation würde:
- Die Signatur invalidieren
- Den Audit-Trail kompromittieren
- Das Vertrauensmodell brechen

### Erlaubte Operationen

```
✓ Neue Receipts HINZUFÜGEN
✓ Receipts LESEN
✓ Receipts VERIFIZIEREN

✗ Receipts MODIFIZIEREN
✗ Receipts LÖSCHEN
✗ Receipts UMBENENNEN
```

---

## Entscheidungsbaum

```
Änderung angefordert
        │
        ▼
   ┌─────────────┐
   │ Welcher Typ? │
   └──────┬──────┘
          │
    ┌─────┼─────┬──────────┐
    ▼     ▼     ▼          ▼
  GOLD  ANNEX  IMMUTABLE  Unklar
    │     │       │          │
    ▼     ▼       ▼          ▼
  STOP  Plan   REFUSE     Fragen
    │   First     │          │
    ▼     │       ▼          ▼
  Frage   │    "Receipts   "Welcher
  User    │     sind       Kategorie
    │     │    immutable"   gehört
    ▼     ▼                  X an?"
  Nur mit OK
  fortfahren
```

---

## Beispiele

### Beispiel 1: ANNEX-Änderung (Normal)

```
User: "Füge einen neuen Test hinzu"

Pfad: tests/new_test.py → ANNEX
Aktion: Direkt nach Plan-First möglich
Report: Standard-Report nach OUT/
```

### Beispiel 2: GOLD-Änderung (Vorsicht)

```
User: "Aktualisiere den Index"

Pfad: index/master.yaml → GOLD
Aktion:
1. STOP
2. "Index ist GOLD. Welche Änderung genau?"
3. Plan zeigen
4. Auf OK warten
5. Minimal-invasiv ändern
6. Commit: "GOLD-CHANGE: Update index/master.yaml - Reason: ..."
```

### Beispiel 3: IMMUTABLE (Refuse)

```
User: "Korrigiere den Typo im Receipt"

Pfad: data/receipts/2026-01-15_receipt.json → IMMUTABLE
Aktion:
1. REFUSE
2. "Receipts sind IMMUTABLE. Ein Typo kann nicht korrigiert werden.
    Stattdessen kann ein neues Receipt mit Korrektur-Vermerk
    erstellt werden. Soll ich das tun?"
```

### Beispiel 4: Grenzfall

```
User: "Räum mal docs/ auf"

Pfad: docs/ → ANNEX (aber docs/negations.md = Semi-GOLD)
Aktion:
1. "docs/ ist ANNEX, aber docs/negations.md hat Sonderstatus.
    Ich werde negations.md nicht anfassen.
    Soll ich den Rest aufräumen?"
```

---

## Schnellreferenz

| Kategorie | Pfade | Darf ich? |
|-----------|-------|-----------|
| GOLD | index/, policies/, VOIDMAP.*, spec/, seeds/ | Nur nach explizitem OK |
| ANNEX | src/, tools/, tests/, docs/, ui-app/, Fractalsense/, reports/, tickets/, schedules/, overlay/, aggregates/, Plugins/, bio_spiral_viewer/, dashboard/, lyra/, __tests__/, adapters/, diagrams/, runbooks/ | Ja, nach Plan |
| IMMUTABLE | data/receipts/, receipts/ | Nur neue hinzufügen |
| Semi-GOLD | docs/negations.md | Mit erhöhter Vorsicht |

---

*Letzte Aktualisierung: 2026-01-17*
