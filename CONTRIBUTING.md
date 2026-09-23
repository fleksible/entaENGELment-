# Contributing to entaENGELment Framework

Danke, dass du darüber nachdenkst, etwas beizutragen.

Ein Tippfehler zählt. Eine unklare Formulierung zählt. Eine kritische Frage zählt. Ein zusätzlicher Test zählt.

Du musst GitHub nicht souverän beherrschen, bevor du etwas bemerken darfst. Wenn du noch nie einen Pull Request gemacht hast, ist das keine Eintrittsprüfung. Niemand muss beim ersten Besuch gleich einen Compiler mitbringen.

Die Standards unten bleiben trotzdem bewusst streng: **Sie gelten für Änderungen am Projekt, nicht als Bewertung der Person, die sie vorschlägt.**

Wenn du nur eine Frage oder Beobachtung hast, darf sie zuerst eine Frage bleiben.

---

## Entwicklungsumgebung einrichten

```bash
# Repository klonen
git clone https://github.com/fleksible/entaENGELment-.git
cd entaENGELment-

# Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# oder: .venv\Scripts\activate  # Windows

# Development Dependencies installieren
make install-dev
```

Wenn du gerade erst GitHub kennenlernst, hilft [`docs/START_HERE.md`](docs/START_HERE.md) mit den wichtigsten Begriffen und dem technischen Einstieg.

## Code-Qualität

Vor jedem Commit müssen folgende Checks erfolgreich sein:

```bash
make lint        # Linting mit ruff
make format      # Formatierung mit black
make type-check  # Type-Checking mit mypy
make test        # Alle Tests
```

## Testing

Das Framework hat drei Test-Kategorien:

- **Unit Tests**: `make test-unit` - Isolierte Komponenten-Tests
- **Integration Tests**: `make test-integration` - Komponenten-Zusammenspiel
- **Ethics Tests**: `make test-ethics` - Fail-Safes und Consent-Management

Alle Tests müssen bestehen. In CI gilt als minimale Overall-Coverage-Baseline `50%` (`coverage report --fail-under=50`).
Für JavaScript gelten zusätzlich die Jest-Schwellen: `branches: 50` sowie `functions/lines/statements: 60`.

## Commit-Konventionen

Commits folgen dem Format: `type(scope): message`

**Typen:**
- `feat`: Neue Features
- `fix`: Bugfixes
- `docs`: Dokumentation
- `test`: Tests
- `refactor`: Code-Refactoring
- `chore`: Build/Config-Änderungen

**Beispiele:**
```text
feat(metrics): add trust decay function
fix(gate): correct phi threshold validation
docs(readme): update installation instructions
test(ethics): add consent expiration test
```

## Pull Requests

PRs nur nach vorheriger Absprache. Jeder PR muss:

1. Alle CI-Checks bestehen (Verify → Build → Security → Gate Policy)
2. Tests für neue Features/Fixes enthalten
3. Dokumentation aktualisieren
4. Von CODEOWNERS reviewt werden

Für eine kleine Beobachtung musst du nicht sofort einen fertigen PR liefern. Eine Frage oder ein Issue kann der bessere erste Schritt sein.

## Architektonische Prinzipien

Das Framework folgt strengen Invarianten:

- **Non-Leakage**: Rohdaten nur am Edge
- **Consent-First**: Kein Zugriff ohne expliziten Consent
- **Auditierbarkeit**: Jede kritische Operation muss nachvollziehbar sein
- **Fail-Safe**: Bei Unsicherheit immer blockieren

## Fragen?

Siehe [`./CODEOWNERS`](./CODEOWNERS) für Kontakte.

## Local Guard Enforcement

Run `make install-hooks` to enable pre-commit guards.
This enforces Receipt-Lint (blocking) and Claim-Lint (warning)
before every commit. Receipt-lint failures prevent the commit.
