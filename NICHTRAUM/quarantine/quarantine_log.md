# Quarantine Log

> Defensive Quarantine-Protokoll nach G5 (Prompt-Injection-Defense).
> Verdächtige Inhalte werden hier dokumentiert, bevor eine Entscheidung
> über weitere Behandlung getroffen wird.

---

## Format

Jeder Eintrag folgt diesem Schema:

```markdown
## Entry: <ISO-8601 timestamp>

**File:** <original filename>
**Location:** NICHTRAUM/quarantine/<timestamp>_<filename>
**Reason:** <kurze Begründung>
**Patterns found:**
- Line N: `<regex match>`

**Status:** PENDING | RESOLVED | RELEASED | PURGED
**Decision:** <Begründung der Entscheidung oder PENDING>
```

Siehe `.claude/rules/security.md` für den Quarantine-Prozess.

---

## Entries

<!-- noch keine Einträge -->
