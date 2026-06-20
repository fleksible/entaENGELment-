# Exchange Archive — Index

> [FAKT] Manuell gepflegter Index der Exchange-Records. Ein künftiger
> `exchange_lint.py` kann diese Tabelle gegen die vorhandenen Record-Dateien
> prüfen (siehe Roadmap). Bis dahin: bei jedem neuen Record eine Zeile ergänzen.

## Spalten

- **ID** — `exchange_id` (eindeutig, z. B. `EX-2026-06-16-001`).
- **Datum** — Datum des Austauschs (YYYY-MM-DD).
- **Quelle / Gegenüber** — Modell, Person oder Kontext der Herkunft.
- **Thema** — Kurzbeschreibung.
- **Bezug** — verknüpfte Canon / VOID / Spec.
- **Claim-Status** — höchster Claim-Status im Record ([FAKT]…[POESIE]).
- **Migration** — `none` | `candidate` | `migrated` | `rejected`.
- **Review** — `open` | `done` | `n/a`.
- **Zielpfad** — wohin migriert (falls `migrated`), sonst `—`.

## Records

| ID | Datum | Quelle / Gegenüber | Thema | Bezug | Claim-Status | Migration | Review | Zielpfad |
|----|-------|--------------------|-------|-------|--------------|-----------|--------|----------|
| _(noch keine Records)_ | — | — | — | — | — | — | — | — |
