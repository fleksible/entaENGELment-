# PR #442: Nennergrenzen und kontrollierte numerische Eingabefehler

**Datum:** 2026-11-02
**Status:** geprüfter ANNEX-Folgepatch; Owner-Mergeentscheidung bleibt offen
**FOKUS:** numerische Fehlerschranke und Eingabevalidierung von `compute_hessian_numerical`
**Prüfbasis:** `90ddeafeddfbe052cb95eae4f9273c1a35c6788e`

## GitHub-Zustand vor dem Folgepatch

- PR #442 ist offen: `merged=false`, `merged_at=null`, `mergeable=true`.
- `main` steht auf `3b72b9db7da703e2f3c90bd3d69c4cdfb5e37bec`.
- `3d4d9a9cd8925e0d7d8503c2b6175bede90dcd09` gehört zu
  `refs/pull/442/merge`, dem automatischen Testmerge. Seine Eltern sind die
  genannten Main- und PR-Commits; sein Tree ist identisch zum PR-Head.
- Die fünf Pflichtchecks auf `90ddeaf` sind erfolgreich. Der Codex-Kommentar
  vom 2026-10-30 dokumentiert einen abgeschlossenen Code-Review ohne Befunde
  auf genau diesem Commit. Die formale Review-Liste und die Thread-Liste sind leer.
  Dieser Review ist kein Nachweis für den späteren Folgepatch.

Quellen: [PR #442](https://github.com/fleksible/entaENGELment-/pull/442),
[Testmerge-Ref](https://api.github.com/repos/fleksible/entaENGELment-/git/ref/pull/442/merge),
[Review-Kommentar](https://github.com/fleksible/entaENGELment-/pull/442#issuecomment-6529683403).

## Reproduktion und Ursache

Für die identisch nullwertige Funktion sind `M4=0` und `e=0` gültige Annahmen.
Trotzdem löste folgender Aufruf auf der Prüfbasis `ZeroDivisionError` aus:

```python
compute_hessian_numerical(
    lambda q: 0.0,
    np.zeros(1),
    eps=1e-200,
    fourth_derivative_bound=0.0,
    evaluation_error=0.0,
)
```

`_central_differences` dividierte durch den zu null unterlaufenen Nenner,
bevor `_declared_error_bound` ihn bewerten konnte. Das ist eine bereits vor
PR #442 vorhandene Exception-Lücke; die neue pauschale UNRESOLVED-Zusage
beschrieb sie nicht zutreffend. Eine zusätzliche Randprobe reproduzierte
`OverflowError` bei der Wahl nicht darstellbarer Schritte.

## Änderung und beobachtetes Verhalten

| Fall | Prüfbasis | Folgepatch |
|---|---|---|
| `eps` = kleinste Subnormalzahl, `1e-200` oder `1e-162`, jeweils mit/ohne Deklarationen | `ZeroDivisionError` (6 Fälle) | kontrollierter `ValueError` vor Division |
| Koordinate ±größtes float mit automatischem Schritt oder größtes float als `eps` bei null | `OverflowError` (3 Fälle) | kontrollierter `ValueError` bei Schrittwahl |
| Kleinster positiver subnormaler Nenner (`eps=2e-162`) | UNRESOLVED | UNRESOLVED; auch mit Consent blockiert |
| Nenner unmittelbar unter der Normalgrenze | UNRESOLVED | UNRESOLVED; auch mit Consent blockiert |
| Nenner genau an der Normalgrenze, Nullfunktion mit gültigen Deklarationen | FLAT | FLAT; expliziter Consent erforderlich |

Die Prüfung erfolgt in der gemeinsam genutzten Nennerfunktion. Die Behandlung
von `OverflowError` umfasst ausschließlich die Schrittwahl, keine Aufrufe der
übergebenen Funktion. Richardson bleibt explorativ und optional. Bei einem
Nullnenner wird keine Ersatz-Hessian erzeugt. ANNEX und CHANGELOG unterscheiden
nun Eingabefehler ohne Ergebnis von endlichen Schätzungen ohne tragfähige Schranke.

## Lokale Nachweise

Umgebung: Python 3.12.14, NumPy 2.5.3, Hypothesis 6.170.12; Installation mit
`make install-dev`, exakt uv 0.12.18 und unverändertem `uv.lock`.

| Prüfung | Ergebnis |
|---|---|
| `make verify` auf unverändertem `90ddeaf` | 1132 passed, 2 skipped, 169 subtests passed |
| 12 zusätzliche Fälle vor dem Code-Fix | 9 failed, 3 passed, 52 deselected |
| `pytest tests/stability/test_hessian_uncertainty.py -q` nach Fix | 64 passed |
| `make verify` nach Fix | 1144 passed, 2 skipped, 169 subtests passed; Ports, Pointer und Claims grün |
| `ruff check src/ tools/ tests/` | bestanden |
| `black --check src/ tools/ tests/` | bestanden |
| `mypy src/ tools/` | bestanden, 58 Quelldateien |
| `bandit -q -c .bandit.yaml -r src/ tools/` | bestanden |
| `make verify-governance` | bestanden |
| `python tools/python_lock.py check` | bestanden |

Die 12 Fälle bestehen aus 9 Regressionen und 3 Kontrollen des erhaltenen Verhaltens.
Der vollständige Testlauf umfasst außerdem alle sechs ursprünglichen
Regressionstests aus PR #442. Die ursprünglichen Unterlauf- und Richardson-Fehler
wurden zuvor auch direkt gegen `main` und `90ddeaf` gegengeprüft.

## Grenzen und nächste Entscheidung

Der Patch normiert die hier nachgewiesenen numerischen Eingabefehler. Er führt
keine Intervallarithmetik ein und überprüft die fachliche Gültigkeit deklarierter
Ableitungs- oder Auswertungsfehler nicht. Matrix-only-Zugänge und die getrennten
Core-/MOD_18-Toleranzen bleiben die dokumentierten fachlichen Grenzen von B9.

Für den Folgepatch sind CI-Nachweise an dessen eigenem PR-Head zu prüfen; die
oben genannten historischen Checks und Reviews werden nicht auf ihn übertragen.
Der nächste Entscheidungspunkt ist die Owner-Freigabe dieses begrenzten Teilfixes
nach erfolgreichen Checks am neuen Head.
