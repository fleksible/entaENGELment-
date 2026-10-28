"""Hessian-basierte Void-Analyse (MOD_16).

Implementiert Stabilitäts-Klassifizierung via Hessian-Eigenwertanalyse:
- STABLE: alle λ > 0 (Minimum, sicher)
- FLAT: λ ≈ 0 und kein λ < 0 (VOID, Consent erforderlich)
- UNSTABLE: mindestens ein λ < 0 (Sattel/Maximum, blockieren), auch wenn
  zusätzlich flache Richtungen vorliegen
- UNRESOLVED: nur bei numerisch geschätzter Hessian (``EstimatedHessian``),
  wenn deklarierte Fehlerannahmen fehlen oder die Fehlerschranke die
  Entscheidung nicht trägt (blockieren, auch mit Consent)

Zwei Eingangsarten werden unterschieden:
- eine vom Aufrufer vorgegebene Matrix (``np.ndarray``) gilt als exakt;
- eine von ``compute_hessian_numerical`` geschätzte Hessian ist ein
  ``EstimatedHessian`` und trägt ihre Unsicherheit. Freigaberelevant ist nur eine
  Fehlerschranke aus deklarierten Annahmen (Schranke der vierten Ableitungen und
  der Auswertungsfehler von f). Der Richardson-Wert ist explorativ.

Details, Annahmen und verbleibende Matrix-only-Zugänge:
``docs/annex/STABILITY_NUMERICS_v0_1.md``.
"""

import math
import numbers
from collections.abc import Callable
from fractions import Fraction
from typing import Any

import numpy as np

_EPS_MACH = float(np.finfo(float).eps)


class EstimatedHessian(np.ndarray):
    """Numerisch geschätzte Hessian mit Unsicherheitsangaben (ndarray-kompatibel).

    Attribute:
        error_bound: Elementweise Fehlerschranke unter den deklarierten Annahmen,
            sonst ``None``. Nur sie ist freigaberelevant.
        richardson_estimate: Explorativer Fehlerschätzer ``|H(h) - H(2h)| / 3``.
            Kein Zertifikat: Übereinstimmung zweier Schrittweiten belegt kein
            Vorzeichen (Gegenbeispiel in den Tests).
        steps: Verwendete Schrittweiten je Koordinate.
        assumptions: Deklarierte Annahmen als lesbare Liste.

    Jede abgeleitete Matrix (Arithmetik, Slicing, ``copy``) bleibt als geschätzt
    markiert, verliert aber alle Fehlerangaben und wird daher UNRESOLVED.
    Eine Schranke gilt nur für den ursprünglichen Matrix- und Fehlerinhalt.
    In-place-Änderungen, auch über NumPy-Aliase, machen sie unbrauchbar.
    ``np.asarray``/``np.array``/``.view(np.ndarray)`` liefern eine gewöhnliche
    Matrix ohne Markierung: ein verbleibender Matrix-only-Zugang.
    """

    error_bound: np.ndarray | None
    richardson_estimate: np.ndarray | None
    steps: np.ndarray | None
    assumptions: tuple[str, ...]
    _bound_snapshot: tuple[Any, ...] | None

    def __new__(
        cls,
        matrix: np.ndarray,
        *,
        error_bound: np.ndarray | None = None,
        richardson_estimate: np.ndarray | None = None,
        steps: np.ndarray | None = None,
        assumptions: tuple[str, ...] = (),
    ) -> "EstimatedHessian":
        obj: EstimatedHessian = np.asarray(matrix, dtype=float).view(cls)
        bound = None if error_bound is None else np.array(error_bound, dtype=float, copy=True)
        if bound is not None and (
            bound.shape != obj.shape or not np.all(np.isfinite(bound)) or np.any(bound < 0)
        ):
            raise ValueError("error_bound must match the matrix and be finite and non-negative")
        obj.error_bound = bound
        obj.richardson_estimate = richardson_estimate
        obj.steps = steps
        obj.assumptions = assumptions
        obj._bound_snapshot = obj._snapshot() if bound is not None else None
        return obj

    def __array_finalize__(self, obj: Any) -> None:
        # Abgeleitete Arrays: markiert, aber ohne übertragene Fehlerangaben.
        self.error_bound = None
        self.richardson_estimate = None
        self.steps = None
        self.assumptions = ()
        self._bound_snapshot = None

    def _snapshot(self) -> tuple[Any, ...]:
        """Bind the bound to values, shape and dtype; not a same-process sandbox."""
        bound = np.asarray(self.error_bound)
        return (
            self.shape,
            self.dtype.str,
            self.tobytes(),
            bound.shape,
            bound.dtype.str,
            bound.tobytes(),
        )

    def eigenvalue_uncertainty(self) -> float | None:
        """Schranke für die Abweichung aller Eigenwerte (Weyl), sonst ``None``.

        ``δ = ||error_bound||_F + 10·n·ε·||H||_F``: Der erste Term begrenzt die
        Spektralnorm des Schätzfehlers, der zweite den Rundungsfehler von
        ``eigvalsh``. Gilt nur unter den deklarierten Annahmen.
        """
        if (
            self.error_bound is None
            or self._bound_snapshot is None
            or not isinstance(self.error_bound, np.ndarray)
            or self._bound_snapshot != self._snapshot()
        ):
            return None
        matrix = np.asarray(self)
        n = matrix.shape[0]
        return float(np.linalg.norm(self.error_bound) + 10 * n * _EPS_MACH * np.linalg.norm(matrix))


def _require_nonneg_finite(name: str, value: object) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, numbers.Real)
        or not math.isfinite(value)
        or value < 0
    ):
        raise ValueError(f"{name} must be a finite number >= 0, got {value!r}")
    return float(value)


def _central_differences(
    func: Callable[[np.ndarray], float], x: np.ndarray, steps: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Zentrale Differenzen; liefert (H, S) mit S = Σ|f|/Nenner je Eintrag."""
    n = x.size
    H = np.zeros((n, n))
    S = np.zeros((n, n))

    def f(y: np.ndarray) -> float:
        value = float(func(y))
        if not math.isfinite(value):
            raise ValueError(f"func returned a non-finite value at {y!r}")
        return value

    f0 = f(x)
    for i in range(n):
        e = np.zeros(n)
        e[i] = steps[i]
        f_p, f_m = f(x + e), f(x - e)
        denom: float = float(steps[i] ** 2)
        H[i, i] = (f_p - 2.0 * f0 + f_m) / denom
        S[i, i] = (abs(f_p) + 2.0 * abs(f0) + abs(f_m)) / denom
    for i in range(n):
        for j in range(i + 1, n):
            e_i = np.zeros(n)
            e_j = np.zeros(n)
            e_i[i] = steps[i]
            e_j[j] = steps[j]
            f_pp, f_pm = f(x + e_i + e_j), f(x + e_i - e_j)
            f_mp, f_mm = f(x - e_i + e_j), f(x - e_i - e_j)
            denom = float(4.0 * steps[i] * steps[j])
            H[i, j] = H[j, i] = (f_pp - f_pm - f_mp + f_mm) / denom
            S[i, j] = S[j, i] = (abs(f_pp) + abs(f_pm) + abs(f_mp) + abs(f_mm)) / denom
    return H, S


def _representable_steps(x: np.ndarray, raw: np.ndarray) -> np.ndarray:
    # (x + h) - x macht die Schrittweite darstellbar (x + h ist dann exakt).
    steps: np.ndarray = (x + raw) - x
    if not np.all(steps > 0):
        raise ValueError("step size is too small for the point's magnitude")
    return steps


def _is_exact_offset(xk: float, d: float) -> bool:
    """True, wenn ``xk + d`` in float exakt dem rationalen Wert entspricht."""
    return Fraction(xk + d) == Fraction(xk) + Fraction(d)


def _exact_steps(x: np.ndarray, raw: np.ndarray) -> np.ndarray | None:
    """Schrittweiten, für die ``x ± h`` je Koordinate exakt darstellbar ist.

    Versucht zuerst ``(x + h) - x``, dann Zweierpotenzen ab der Nähe von ``h``.
    Gibt ``None`` zurück, wenn das nicht gelingt (etwa bei winzigen Koordinaten
    neben großem ``h``); dann gibt es keine belastbare Fehlerschranke.
    """
    steps: np.ndarray = np.empty_like(x)
    for k, (xk, rk) in enumerate(zip(x.tolist(), raw.tolist(), strict=True)):
        candidates = [(xk + rk) - xk]
        h = 2.0 ** round(math.log2(rk))
        for _ in range(12):
            candidates.append(h)
            h *= 2.0
        for h in candidates:
            if h > 0 and _is_exact_offset(xk, h) and _is_exact_offset(xk, -h):
                steps[k] = h
                break
        else:
            return None
    return steps


def compute_hessian_numerical(
    func: Callable[[np.ndarray], float],
    point: np.ndarray,
    eps: float | None = None,
    *,
    fourth_derivative_bound: float | None = None,
    evaluation_error: float | None = None,
) -> EstimatedHessian:
    """Numerische Hessian-Schätzung via zentrale Differenzen.

    Schrittweite: ohne ``eps`` je Koordinate ``ε^(1/4)·max(1, |x_k|)`` (≈ 1.2e-4),
    das balanciert den Abbruchfehler O(h²) gegen den Rundungsfehler O(ε|f|/h²)
    bei O(1)-skalierten Ableitungen. ``eps`` setzt eine feste Schrittweite.

    Fehlerschranke (nur wenn beide Annahmen deklariert sind):
    - ``fourth_derivative_bound`` M4: Schranke für alle vierten partiellen
      Ableitungen von f auf dem Stencil-Quader ``[x - h, x + h]`` (f ∈ C⁴ dort);
    - ``evaluation_error`` e: Schranke für ``|f̃(y) - f(y)|`` an den Stencil-Punkten.
    Abbruch: Diagonale ``M4·h²/12``, gemischt ``M4·(h_i+h_j)⁴/(24·h_i·h_j)``
    (Taylor mit Lagrange-Rest). Auswertung: ``4e/h²`` bzw. ``e/(h_i·h_j)``.
    Gleitkomma-Arithmetik der Formel: konservativ ``8ε·Σ|f̃|/Nenner``.
    Die Schranke setzt exakt darstellbare Stencil-Punkte ``x ± h`` voraus (per
    rationaler Arithmetik geprüft); gelingt das nicht, gibt es keine Schranke.
    Die Schranke ist nur so gut wie die deklarierten Annahmen; sie werden nicht
    geprüft. Fehlen sie, bleibt ``error_bound`` ``None`` und eine Freigabe
    auf Basis dieser Schätzung ist UNRESOLVED.

    Verhaltensänderung gegenüber der Vorwärtsdifferenz (``eps=1e-5``) vor B9:
    zentrale Differenzen, automatische Schrittweite und Rückgabetyp
    ``EstimatedHessian`` (ndarray-Subklasse).

    Args:
        func: Skalare Funktion f: R^n -> R
        point: Punkt an dem Hessian berechnet wird
        eps: Optionale feste Schrittweite (> 0)
        fourth_derivative_bound: Deklarierte Schranke M4 (>= 0)
        evaluation_error: Deklarierte Schranke für den Auswertungsfehler (>= 0)

    Returns:
        ``EstimatedHessian`` mit Matrix, ggf. Fehlerschranke, explorativem
        Richardson-Wert, Schrittweiten und Annahmen.

    Raises:
        ValueError: Bei ungültigem Punkt, ungültiger Schrittweite oder Schranke,
            nur einer der beiden Annahmen oder nicht endlichen Funktionswerten.
    """
    try:
        x = np.asarray(point, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"point is not numeric: {exc}") from exc
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("point must be a non-empty finite 1-D vector")
    if (fourth_derivative_bound is None) != (evaluation_error is None):
        raise ValueError("declare fourth_derivative_bound and evaluation_error together")

    if eps is None:
        raw = _EPS_MACH**0.25 * np.maximum(1.0, np.abs(x))
    else:
        raw = np.full(x.size, _require_nonneg_finite("eps", eps))
        if not np.all(raw > 0):
            raise ValueError("eps must be > 0")
    exact = _exact_steps(x, raw)
    steps = exact if exact is not None else _representable_steps(x, raw)

    H, S = _central_differences(func, x, steps)
    H_2h, _ = _central_differences(func, x, _representable_steps(x, 2.0 * steps))
    richardson = np.abs(H - H_2h) / 3.0

    error_bound = None
    assumptions: tuple[str, ...] = (
        f"central differences, steps={steps.tolist()}",
        "richardson_estimate is exploratory, not a certified bound",
    )
    if exact is None and fourth_derivative_bound is not None:
        assumptions += ("no error bound: stencil points x ± h not exactly representable",)
    elif fourth_derivative_bound is not None and evaluation_error is not None:
        m4 = _require_nonneg_finite("fourth_derivative_bound", fourth_derivative_bound)
        e = _require_nonneg_finite("evaluation_error", evaluation_error)
        hi = steps[:, None]
        hj = steps[None, :]
        truncation = m4 * (hi + hj) ** 4 / (24.0 * hi * hj)
        evaluation = e / (hi * hj)
        diag = np.diag_indices(x.size)
        truncation[diag] = m4 * steps**2 / 12.0
        evaluation[diag] = 4.0 * e / steps**2
        error_bound = truncation + evaluation + 8.0 * _EPS_MACH * S
        assumptions += (
            f"declared: |4th partial derivatives| <= {m4!r} on [x-h, x+h], f in C^4 there",
            f"declared: |f_computed - f| <= {e!r} at stencil points",
        )

    return EstimatedHessian(
        H,
        error_bound=error_bound,
        richardson_estimate=richardson,
        steps=steps,
        assumptions=assumptions,
    )


def _validated_hessian(hessian: np.ndarray) -> np.ndarray:
    """Prüft die Matrix kontrolliert; ungültige Eingaben lösen ``ValueError`` aus.

    ``np.linalg.eigvalsh`` liest nur das untere Dreieck. Eine nicht symmetrische
    Matrix würde daher still als eine andere Matrix klassifiziert; sie wird
    stattdessen abgewiesen.
    """
    try:
        matrix: np.ndarray = np.asarray(hessian, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"hessian is not numeric: {exc}") from exc
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
        raise ValueError(f"hessian must be a non-empty square matrix, got shape {matrix.shape}")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("hessian contains NaN or infinite entries")
    scale = float(np.max(np.abs(matrix)))
    if float(np.max(np.abs(matrix - matrix.T))) > 1e-10 * scale:
        raise ValueError("hessian is not symmetric")
    return matrix


def _validated_threshold(threshold: object) -> float:
    if (
        isinstance(threshold, bool)
        or not isinstance(threshold, numbers.Real)
        or not np.isfinite(threshold)
        or threshold < 0
    ):
        raise ValueError(f"threshold must be a finite number >= 0, got {threshold!r}")
    return float(threshold)


def eigenvalue_bounds(hessian: np.ndarray) -> tuple[np.ndarray, float | None]:
    """Eigenwerte und deren Unsicherheit δ.

    Für eine vorgegebene Matrix ist δ = 0 (als exakt behandelt). Für eine
    ``EstimatedHessian`` ist δ die Schranke aus deklarierten Annahmen oder
    ``None``, wenn keine vorliegt.

    Raises:
        ValueError: Bei ungültiger Matrix.
    """
    eigvals = np.linalg.eigvalsh(_validated_hessian(hessian))
    if isinstance(hessian, EstimatedHessian):
        return eigvals, hessian.eigenvalue_uncertainty()
    return eigvals, 0.0


def classify_stability(hessian: np.ndarray, threshold: float = 1e-6) -> tuple[str, np.ndarray]:
    """Klassifiziert Stabilitätstyp via Hessian-Eigenwerte.

    ``threshold`` ist die fachliche Flach-Toleranz in Krümmungseinheiten:
    Eigenwerte mit ``|λ| <= threshold`` gelten als flach. Sie hängt nicht von den
    Funktionswerten ab. Negative Krümmung (``λ < -threshold``) hat Vorrang vor
    flachen Richtungen: ein degenerierter Sattel wie ``[-1, 0]`` ist UNSTABLE.

    Bei einer ``EstimatedHessian`` wird jeder Eigenwert als Intervall
    ``[μ - δ, μ + δ]`` gelesen. Sicher negativ (``μ + δ < -τ``) → UNSTABLE; sonst
    jede nicht eindeutig zuordenbare Richtung → UNRESOLVED; ohne deklarierte
    Fehlerannahmen (δ unbekannt) immer UNRESOLVED. Übereinstimmende Schätzwerte
    allein genügen nicht.

    Args:
        hessian: Symmetrische Hessian-Matrix oder ``EstimatedHessian``
        threshold: Fachliche Flach-Toleranz (endlich, >= 0)

    Returns:
        Tuple (status, eigenvalues) wobei status in
        {'STABLE', 'FLAT', 'UNSTABLE', 'UNRESOLVED'}; UNRESOLVED nur für
        ``EstimatedHessian``.

    Raises:
        ValueError: Bei nicht quadratischer, nicht endlicher oder nicht
            symmetrischer Matrix oder ungültiger Toleranz.
    """
    tau = _validated_threshold(threshold)
    eigvals, delta = eigenvalue_bounds(hessian)
    if delta is None:
        return "UNRESOLVED", eigvals  # geschätzt, aber ohne tragfähige Fehlerannahmen

    if np.any(eigvals + delta < -tau):
        return "UNSTABLE", eigvals  # sicher negative Richtung, auch neben flachen
    certainly_flat = np.abs(eigvals) + delta <= tau
    certainly_positive = eigvals - delta > tau
    if not np.all(certainly_flat | certainly_positive):
        return "UNRESOLVED", eigvals  # nur bei δ > 0 möglich
    if np.any(certainly_flat):
        return "FLAT", eigvals  # VOID: flache Richtung
    return "STABLE", eigvals


def detect_void_type(hessian: np.ndarray) -> str:
    """Vereinfachte Void-Typ-Erkennung.

    Args:
        hessian: Symmetrische Hessian-Matrix

    Returns:
        'stable', 'flat', 'unstable' oder 'unresolved'
    """
    status, _ = classify_stability(hessian)
    return status.lower()


def rosenbrock(x: np.ndarray, a: float = 1.0, b: float = 100.0) -> float:
    """Rosenbrock-Funktion: (a-x)² + b(y-x²)².

    Standard-Testfunktion mit globalem Minimum bei (a, a²).
    """
    return float((a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2)
