# Metatron Guard — Pre-Protocol Amnesty

**Datum:** 2026-02-15
**Guard:** metatron_check.py (FOKUS-Marker Enforcement)
**Amnesty Cutoff:** 929f2a80b85d4d70d3d977dc5e9c68571e22a346 (2026-01-16 22:36:09 +0000)

## Kontext

Der Metatron-Guard erzwingt FOKUS-Marker in Commit-Nachrichten.
Vor seiner Einführung existierte diese Regel nicht.

## Regelung

- Alle Commits VOR dem Amnesty-Cutoff sind von der FOKUS-Pflicht ausgenommen.
- Alle Commits NACH dem Cutoff müssen FOKUS enthalten.
- Violations nach dem Cutoff werden in `metatron_violations.txt`
  dokumentiert und sind technische Schuld.

## Aktuelle Post-Cutoff Violations

**92 von 94** Post-Cutoff-Commits haben keinen FOKUS-Marker.

**Status:** Dokumentiert. Retrospektive Korrektur nicht möglich
(Rebase würde Commit-Hashes und damit Receipt-Referenzen brechen).
