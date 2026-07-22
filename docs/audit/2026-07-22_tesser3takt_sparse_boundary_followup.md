# Report: tesser3TAKT Sparse-Boundary-Follow-up

**Datum:** 2026-07-22
**Fokus:** Frame-Validator schließt Sparse-Array-Lücke
**Status:** [ANNEX] [FACT]

## Ziel

Den nach Merge von PR #312 gemeldeten P2-Randfall schließen, bei dem ein sparse JavaScript-Array die vollständige EXIT/ENTRY-Paarprüfung überspringen konnte.

## Aktionen

- [x] `boundaryTransitions` wird indexbasiert statt mit `forEach` traversiert.
- [x] Ein fehlender Array-Slot wird durch `validateBoundaryTransition(undefined, ...)` als malformed input zurückgewiesen.
- [x] Produktionsnaher Gegenfixture für ein Array mit unbelegtem Index ergänzt.
- [x] Reverse-Ordering (`EXIT.stepIndex >= ENTRY.stepIndex`) explizit getestet.
- [x] README-Begriff von nicht vorhandenem `halfId` auf den tatsächlich validierten Schlüssel `(pairId, half)` korrigiert.

## Verifikation

```text
node --experimental-strip-types --test ui-app/test/tesser3takt-frame.test.mjs
tests 9 | pass 9 | fail 0
```

Der vollständige Workspace-Build und die Repository-Gates bleiben Merge-Bedingung der CI.

## Nicht getan

- Keine Änderung von Collision-Semantik, globalem Lattice, Provenienzvertrag oder Fixture-Bedeutung.
- Keine Änderung an GOLD-, VOIDMAP-, Receipt-, Index- oder Runtime-Promotion-Pfaden.
- Keine Vermischung mit dem Grimm-IR-Mereotopologie-ANNEX.

## Risiken

- In JavaScript können sparse Arrays aus In-Process-Transportobjekten entstehen, obwohl JSON keine Array-Löcher serialisiert. Die Runtime-Grenze muss daher beide Eingangsformen fail-closed behandeln.

## Offene Punkte

- [ ] CI-Gates auf dem Follow-up-PR vollständig grün bestätigen.

## Artefakte

- `ui-app/lib/tesser3takt-frame.ts`
- `ui-app/test/tesser3takt-frame.test.mjs`
- `docs/tesser3takt/README.md`
