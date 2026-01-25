# Witness Mode Skill

> Read-only Exploration ohne Side-Effects

---

## Use Case

Witness Mode ist für Situationen, in denen:
- Nur beobachtet werden soll
- Keine Änderungen erwünscht sind
- Ein Überblick benötigt wird
- Exploration ohne Risiko stattfinden soll

---

## Allowed Tools

| Tool | Erlaubt | Verwendung |
|------|---------|------------|
| `read` | ✓ | Dateien lesen |
| `grep` | ✓ | Pattern suchen |
| `glob` | ✓ | Dateien finden |
| `list_directory` | ✓ | Verzeichnisse auflisten |

---

## Forbidden Tools

| Tool | Verboten | Grund |
|------|----------|-------|
| `write_file` | ✗ | Ändert Dateien |
| `edit` | ✗ | Ändert Dateien |
| `delete_file` | ✗ | Löscht Dateien |
| `bash` (write) | ✗ | Side-Effects möglich |
| `git commit` | ✗ | Ändert Repository |
| `git push` | ✗ | Ändert Remote |

### Bash Ausnahmen

Folgende Bash-Commands sind erlaubt (read-only):
```bash
git status
git log
git diff
git branch -a
ls
cat  # nur zum Lesen
head
tail
wc
find  # ohne -exec
```

---

## Output

Alle Ergebnisse werden nach `docs/audit/` geschrieben:

```
docs/audit/<name>_exploration.md
```

### Output Format

```markdown
# Exploration: <Thema>

**Datum:** YYYY-MM-DD
**Modus:** Witness (Read-Only)
**Fokus:** <2-5 Wörter>

## Scope
<Was wurde untersucht?>

## Beobachtungen

### Beobachtung 1
<Beschreibung>
- Relevante Dateien: `path/to/file`
- Pattern gefunden: <ja/nein>

### Beobachtung 2
...

## Statistiken
- Dateien gescannt: N
- Pattern-Matches: M
- Verzeichnisse: K

## Offene Fragen
- [ ] ☐ Frage 1
- [ ] ☐ Frage 2

## Nächste Schritte (Vorschläge)
- <Vorschlag 1>
- <Vorschlag 2>

---
*Generiert im Witness Mode - keine Änderungen vorgenommen*
```

---

## Workflow Pattern

```
┌─────────────────────────────┐
│     Witness Mode Start      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   1. Nur beobachten         │
│   - read, grep, glob        │
│   - Keine Writes            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   2. Scannen & Analysieren  │
│   - Pattern suchen          │
│   - Struktur verstehen      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   3. Dokumentieren          │
│   - Beobachtungen sammeln   │
│   - Fragen formulieren      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   4. Report schreiben       │
│   - docs/audit/<name>_exploration  │
│   - ☐ Offene Punkte         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Witness Mode Ende       │
│   (keine Side-Effects)      │
└─────────────────────────────┘
```

---

## Aktivierung

### Explizit durch User

```
"Bitte im Witness Mode: Analysiere die src/ Struktur"
"Read-only: Was macht das Receipt-Modul?"
"Nur schauen, nicht anfassen: Wie ist tests/ organisiert?"
```

### Automatisch bei

- Fragen ohne Änderungsauftrag
- "Erkläre mir...", "Zeig mir...", "Was ist...?"
- Exploration von unbekannten Bereichen

---

## Beispiel Session

```
User: "Witness Mode: Wie ist das Tools-Verzeichnis aufgebaut?"

Claude (Witness Mode):
- Lese tools/
- Liste alle .py Dateien
- Analysiere Imports und Funktionen
- Erstelle docs/audit/tools_exploration.md

Output:
"Exploration abgeschlossen. Report: docs/audit/tools_exploration.md

Zusammenfassung:
- 7 Python-Dateien gefunden
- Hauptfunktionen: claim_lint, port_lint, snapshot_guard
- Gemeinsame Abhängigkeit: pathlib, re

☐ Offene Fragen:
- Wie interagieren die Linter miteinander?
- Gibt es eine zentrale Konfiguration?

Keine Dateien wurden verändert."
```

---

## Integration mit Guards

| Guard | Wie Witness Mode hilft |
|-------|----------------------|
| G0 (Consent) | Kein Consent nötig für Read-Only |
| G1 (Annex) | Kann GOLD sicher lesen |
| G4 (Metatron) | Exploration ohne Fokus-Switch-Risiko |
| G5 (Security) | Sicheres Analysieren von untrusted Content |

---

## Einschränkungen

1. **Kein Caching von Ergebnissen** (außer in OUT/)
2. **Keine Interaktion mit externen Services**
3. **Keine Git-Operationen außer Status/Log/Diff**
4. **Keine Ausführung von gefundenem Code**

---

*Letzte Aktualisierung: 2026-01-16*
