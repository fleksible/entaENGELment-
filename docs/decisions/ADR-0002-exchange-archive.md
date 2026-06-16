# ADR-0002: Einführung eines Exchange-Archivs (`docs/exchange_archive/`)

- **Status:** Accepted (additiv, risikoarm)
- **Datum:** 2026-06-16
- **Kontext-Fokus:** Revolutionary Repository Audit

## Context

Das Repository hat klar definierte Räume für untrusted Eingaben (`INBOX/`),
Unentschiedenes (`NICHTRAUM/maybe/`), Verdächtiges (`NICHTRAUM/quarantine/`) und
Kanon (`index/`, `spec/`, `VOIDMAP.yml`). Es fehlte ein **markierter Zwischenraum**
für „ehemalige Bezüglichkeit": frühere Gesprächsstände, Handoff-Zustände, externe
Modell-Antworten und semantische Zwischenschichten, die Bezug haben, aber **nicht**
unmarkiert in den Kern wandern dürfen.

## Decision

Einführung von `docs/exchange_archive/` mit:

- `README.md` — Zweck und Abgrenzung (nicht Kanon, nicht Müll, nicht Beweis).
- `INDEX.md` — manuell gepflegte Tabelle aller Records.
- `TEMPLATE_exchange_record.md` — Vorlage mit Provenienz-, Claim- und
  Consent-Feldern.

## Consequences

- (+) Provenienz und Kontext werden bewahrt, ohne Kanon zu verwässern.
- (+) Klare Migrations-Schwelle (`do_not_canonize_before`, Review).
- (−) Pflegeaufwand für `INDEX.md`, bis ein `exchange_lint.py` ihn prüft (Roadmap).

## Alternatives Considered

1. **INBOX/ wiederverwenden** — verworfen: INBOX ist untrusted/unverarbeitet (G5),
   nicht für markierte, bereits gesichtete Bezüglichkeit.
2. **NICHTRAUM/maybe/** — verworfen: dort liegt Unentschiedenes ohne Provenienz-
   Struktur; Exchange-Records brauchen Felder (Quelle, Claim-Status, Migration).

## Essence Preservation Note

Additiv. Verstärkt die Consent-First-/Claim-Disziplin, indem Bezüglichkeit
explizit markiert und von Evidenz/Kanon getrennt wird. Kein Kerntext geändert.

## Linked VOID / Spec / Claim

- Audit: `docs/audit/revolutionary_repo_audit_2026-06-16.md` §7
- Artefakte: `docs/exchange_archive/{README,INDEX,TEMPLATE_exchange_record}.md`
