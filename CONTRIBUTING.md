# Contributing to entaENGELment Framework

Dieses Repository folgt dem Inner-Codex und strengen Qualitätsstandards.

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

Alle Tests müssen bestehen und Coverage >= 70% sein.

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
```
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

## Architektonische Prinzipien

Das Framework folgt strengen Invarianten:

- **Non-Leakage**: Rohdaten nur am Edge
- **Consent-First**: Kein Zugriff ohne expliziten Consent
- **Auditierbarkeit**: Jede kritische Operation muss nachvollziehbar sein
- **Fail-Safe**: Bei Unsicherheit immer blockieren

## Fragen?

Siehe [`./CODEOWNERS`](./CODEOWNERS) für Kontakte.
