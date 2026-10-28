# STABILITY_NUMERICS_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Runtime-Enforcement:** nur bei explizitem Aufruf (kein Laufzeit-Aufrufer im Repo)
**Datum:** 2026-10-28
**Module:** `src/stability/hessian_void.py`, `src/stability/spectral_void.py`,
`src/core/stability_guard.py`, `src/stability/stability_guard.py`
**Anlass:** Befund B9 in `docs/audit/2026-10-28_repo_checkup.md`

---

## 1. Leitsatz

STABLE bezeugt ausschließlich eine geometrische Klassifikation einer Matrix unter
benannten Annahmen. Es ist keine Einwilligung und keine normative Freigabe.
Unsicherheit bleibt sichtbar: Ist eine numerische Freigabebedingung nicht
entscheidbar, lautet der Status UNRESOLVED und die davon abhängige Handlung wird
blockiert, auch mit Consent.

## 2. Datenfluss (geprüft auf `e8bea51` und diesem Branch)

| Schritt | Ort | Bemerkung |
|---|---|---|
| Matrix entsteht (a): vom Aufrufer vorgegeben | beliebig | wird als exakt behandelt |
| Matrix entsteht (b): geschätzt | `compute_hessian_numerical(func, point, ...)` | liefert `EstimatedHessian` |
| Eigenwerte entstehen | `eigenvalue_bounds`, `classify_stability`, `np.linalg.eigvalsh` | nur die ersten beiden kennen δ |
| Klassifikation (Core) | `classify_stability` → STABLE/FLAT/UNSTABLE/UNRESOLVED | |
| Klassifikation (MOD_18) | `classify_hessian_spectral_void` (mit δ), `classify_spectral_void` (Eigenwerte, optional δ) | UNRESOLVED → UNDEFINED |
| Freigabe (Core) | `stability_gate` → `(allow, reason)` | ALLOW nur bei STABLE oder FLAT+Consent |
| Freigabe (MOD_18) | `map_taxonomy_to_gate` → ALLOW/BLOCK | UNDEFINED → `BLOCK_UNDEFINED_STATE` |

`git grep` findet im Repo **keinen Laufzeitpfad**, der eine geschätzte Hessian an
einen Guard übergibt. Alle Pfade sind öffentliche Bibliotheks-API
(`src/stability/__init__.py`, `src/core/stability_guard.py`). Eine Runtime-Kopplung
wird hier nicht behauptet.

## 3. Entscheidungsregel

Drei Größen sind getrennt:

| Größe | Bedeutung | Abhängigkeit |
|---|---|---|
| τ (`threshold`, Core 1e-6; `eps`, MOD_18 1e-8) | fachliche Flach-Toleranz in Krümmungseinheiten | fest, nicht von f-Werten abhängig |
| Krümmungsskala | Größe der Eigenwerte selbst | nur berichtet, nicht Teil der Schwelle |
| δ (`eigenvalue_uncertainty`) | Schranke für den Eigenwertfehler der Schätzung | darf von \|f\| abhängen (Rundung) |

Jeder Eigenwert μ wird als Intervall `[μ − δ, μ + δ]` gelesen:

1. irgendein `μ + δ < −τ` → **UNSTABLE** (sicher negative Krümmung, Vorrang vor allem anderen);
2. sonst irgendeine Richtung weder sicher flach (`|μ| + δ ≤ τ`) noch sicher positiv (`μ − δ > τ`) → **UNRESOLVED**;
3. sonst irgendeine sicher flache Richtung → **FLAT**;
4. sonst → **STABLE**.

Eine vorgegebene Matrix hat δ = 0; dann tritt UNRESOLVED nie auf und die Regel ist
die aus B2 (negativ vor flach). Eine `EstimatedHessian` ohne Schranke (δ unbekannt)
ist immer UNRESOLVED.

## 4. Fehlermodell und Annahmen

`compute_hessian_numerical` nutzt zentrale Differenzen mit Schrittweite
`h_k = ε^(1/4)·max(1, |x_k|)` (≈ 1.2e-4), gerundet auf exakt darstellbare
Stencil-Punkte `x ± h` (per `Fraction` geprüft), oder ein festes `eps`.

Eine Fehlerschranke entsteht **nur**, wenn beide Annahmen deklariert sind:

- `fourth_derivative_bound` M4: f ∈ C⁴ auf dem Stencil-Quader `[x − h, x + h]`, alle
  vierten partiellen Ableitungen betragsmäßig ≤ M4;
- `evaluation_error` e: `|f̃(y) − f(y)| ≤ e` an allen Stencil-Punkten.

Dann gilt elementweise (Taylor mit Lagrange-Rest, Standard-Fehleranalyse):

| Anteil | Diagonale | gemischt (i ≠ j) |
|---|---|---|
| Abbruch | `M4·h²/12` | `M4·(h_i+h_j)⁴/(24·h_i·h_j)` |
| Auswertung | `4e/h²` | `e/(h_i·h_j)` |
| Gleitkomma der Formel | `8ε·Σ|f̃|/h²` | `8ε·Σ|f̃|/(4·h_i·h_j)` |

Eigenwerte: Nach Weyl gilt `|λ_i(H + E) − λ_i(H)| ≤ ‖E‖₂ ≤ ‖E‖_F`; dazu kommt
`10·n·ε·‖H‖_F` für `eigvalsh`. Daraus folgt δ.

Ohne Deklaration, bei nur einer Deklaration (Fehler) oder bei nicht exakt
darstellbaren Stencil-Punkten gibt es keine Schranke.

**Die Annahmen werden nicht geprüft.** Eine falsche Deklaration kann eine falsche
Freigabe erzeugen (Test `test_documented_limit_false_declarations_are_not_detected`).
Die Annahmen stehen in `EstimatedHessian.assumptions`.

## 5. Richardson ist explorativ

`richardson_estimate = |H(h) − H(2h)| / 3` wird mitgeliefert, aber nie für eine
Freigabe genutzt. Gegenbeispiel: `f(t) = −t² + 10t⁴ − 8t⁶` bei t = 0. Zentrale
Differenzen mit h = 1 und h = 0.5 ergeben beide +2, tatsächlich ist f''(0) = −2.
Übereinstimmung mehrerer Schätzwerte zertifiziert kein Vorzeichen. Mit gültiger
Deklaration (M4 = 480 auf [−0.5, 0.5]) ist die Schranke dort 10, der Status also
UNRESOLVED; mit automatischer Schrittweite und M4 = 241 wird die negative Krümmung
erkannt (UNSTABLE).

## 6. Verbleibende Matrix-only-Zugänge

Diese Zugänge tragen keine Unsicherheit und werden als exakt behandelt; B9 bleibt
für sie offen, wenn eine geschätzte Matrix auf diesem Weg in einen Guard gelangt:

- `np.asarray(H)`, `np.array(H)`, `H.view(np.ndarray)`, `H.tolist()` und daraus
  neu gebaute Arrays einer `EstimatedHessian`;
- selbst gebaute oder extern geschätzte Matrizen (ohne `EstimatedHessian`);
- `classify_spectral_void(eigvals)` ohne `eigval_uncertainty`, insbesondere mit
  Eigenwerten aus `np.linalg.eigvalsh(H)` einer Schätzung.

Abgeleitete Arrays einer `EstimatedHessian` (Arithmetik, Slicing, `copy`, `.T`)
bleiben markiert, verlieren aber die Schranke und sind damit UNRESOLVED
(fail-closed). Ein serialisierter und wieder geladener Wert verhält sich ebenso.

Die ursprüngliche Schranke ist außerdem an einen Snapshot von Matrix und
Fehlerangabe gebunden (Werte, Form und Datentyp). Änderungen an derselben Instanz,
etwa per `H[:] = ...`, `H *= ...`, `np.copyto` oder einem schreibbaren
`np.asarray(H)`-Alias, machen sie für die nächste Guard-Auswertung unbrauchbar:
UNRESOLVED, auch mit Consent. Dasselbe gilt für veränderte Fehlerangaben.
Dieser Konsistenzcheck ist keine Authentisierung gegen Code im selben Prozess.
Der direkte Matrix-only-Zugang über `np.asarray(H)` bleibt wie oben beschrieben
offen; seine Änderungen dürfen aber nicht die alte Schranke auf `H` weiterverwenden.

## 7. Verhaltensänderungen

- `compute_hessian_numerical`: zentrale statt Vorwärtsdifferenzen, automatische
  Schrittweite (`eps=None`), Rückgabetyp `EstimatedHessian`, `ValueError` bei
  ungültigem Punkt oder nicht endlichen Funktionswerten.
- `classify_stability`/`detect_void_type`: neuer Status `UNRESOLVED`
  (`'unresolved'`) für Schätzungen; `stability_gate` blockiert ihn auch mit Consent.
- `classify_spectral_void`: neuer optionaler Parameter `eigval_uncertainty`;
  ohne ihn unverändert. Neu: `classify_hessian_spectral_void`.

## 8. Abdeckung des getesteten Gültigkeitsbereichs

Testmatrizen wie im B9-Harness (7×7 Raster × 6 Offsets = 294; 400 Fälle aus
`default_rng(0)`), Funktionen `a·x² + b·y² + C` mit gültigen Deklarationen
(M4 = 0, e = 4ε·((|a|+|b|)·R² + |C|)):

| Referenz | Ergebnis (294 / 400) | Freigabe ohne Consent |
|---|---|---|
| FLAT (`diag(2, 2e-8)`) | 15 FLAT + 279 UNRESOLVED / 400 UNRESOLVED | 0 / 0 (vorher 57 / 104) |
| STABLE (`diag(2, 2)`) | 294 STABLE / 400 STABLE | erwartungsgemäß |
| UNSTABLE (`diag(2, −2)`) | 294 UNSTABLE / 400 UNSTABLE | 0 / 0 |

Kein Ergebnis widerspricht der analytischen Referenz in freigebende Richtung. Der
Preis: Ein Eigenwert von 2e-8 ist bei τ = 1e-6 und Funktionswerten ≳ 1 nicht
entscheidbar, der FLAT-Zweig (mit Consent) ist dort meist nicht erreichbar.
Ohne Deklaration sind alle Fälle UNRESOLVED.

Diese Zahlen beschreiben nur die genannten Matrizen. Grüne Tests sind kein Beweis
für andere Funktionen, Punkte oder Offsets.

## 9. Offene Punkte

- [ ] ☐ Fachliche Flach-Toleranz vereinheitlichen? Core nutzt `threshold=1e-6`,
  MOD_18 `eps=1e-8`. Übereinstimmende Blockierentscheidungen sind nur bei gleicher
  Toleranz belegt. Die Wahl des Werts ist eine inhaltliche Setzung (siehe PR).
- [ ] ☐ Matrix-only-Zugänge (§6) bei künftigen Laufzeit-Aufrufern ausschließen
  oder dort Unsicherheit mitführen.
