# Gegenprüfung der Checkup- und Fix-PRs · 28.10.2026

**FOKUS:** Fail-closed Gates und nachvollziehbare Prüfnachweise  
**Status:** DERIVED / REVIEW-PENDING; generated_review  
**Scope:** #437–#441 und der historische AppImage-Fehler aus #431.  
**Geprüfte main-Basis:** `e8bea51be1e1787e6cb654d666e7231512cf2f1d`

Abgeleiteter Review-Bericht, keine Kanonisierung und kein empirischer Nachweis der
Projektmodelle. Kein Merge; keine GOLD-, Receipt- oder NICHTRAUM-Änderung.

## 1. Tatsächlicher Stand

Die weitergereichte Zusammenfassung von #437 beschrieb Revision 1. Geprüft wurde
Revision 2 (`88b39e3`) mit B9 und ausführbarem Mess-Harness. Dessen Anteile sind
Ergebnisse genau dieser Testmatrizen, keine allgemeine Fehlerwahrscheinlichkeit.

#431 ist bereits gemergt. Das gelesene alte Log von Job **122742354810** zeigt
einen tatsächlichen Fehler: unerwartetes `no-sandbox` beim gepackten Start.
Die Abhilfen am Desktop-Defaultargument und am Launcher stehen im gemergten PR.

Der spätere [Job 122759545882 auf main](https://github.com/fleksible/entaENGELment-/actions/runs/40671622033/job/122759545882)
baut Electron 45.0.0 und startet das echte `AppRun/app.asar`. Das Log meldet
`PASS: actual AppImage payload, preload, sandbox and navigation guards`,
`sandbox: true`, keine abschaltenden Flags und Seccomp-Modus 2.
Daher kein neuer AppImage-Fix. Ein weiterer lokaler Paketbuild wurde nicht behauptet.
Die Aussage ist auf diesen Linux-Payload-Test begrenzt.

## 2. Nachbesserungen und Identität der geprüften Dateien

Die Veröffentlichung über die GitHub-App erzeugt andere Commit-IDs als lokal.
Vor jedem Branch-Update wurde derselbe Tree nachgewiesen; ein ähnlicher Diff
wurde nicht als Identität ausgegeben. Ref-Updates verwenden den vorherigen Head
als Lease und kein Force-Update.

| PR | veröffentlichter Code-Head | lokaler Code-Teststand | identischer Tree |
|---|---|---|---|
| #438 | `89bc3da960b422fb7c28a777ade140e5b2020850` | `179a360920421a964fa65aea7d0e717d32e6a48a` | `25aa6cd481b99b4cdd747322af5a9a2662ef2d13` |
| #439 | `f1bd24ea8dffdc25c2d3ae6e5620a0d5465e1cde` | `1f8e89d60eccd94c22cbf363c635bf610334ab2a` | `ed3cb332c85f48c24e11df6f8e6a1f2f2aa2123a` |
| #440 | `b9d1a66bbe4eba6b79099f55245b0a2d4ac57f59` | `30f46db554f94e90936e784314c1e142a5af3817` | `6e572ca8278c665ceea9f919e12467f44c6a2004` |
| #441 | `7962f48b57b7e8ea24f35e154826c76a85acacd8` | `d194314e852069d126a2f9d570973779c099d4da` | `a5549d8f726bd9e860958fbf202c1320436f67ce` |

#439 und #440 enthalten den korrigierten P1-Code. #441 bleibt unabhängig.

### B9: veraltete Schranke nach Änderungen an derselben Matrix

Auf `432df72` blieb die alte Fehlerangabe bei `H[:] = ...`, `H *= -1`,
`np.copyto` und Änderungen über einen `np.asarray(H)`-Alias verwendbar.
Eine ursprünglich negative Schätzung konnte danach als STABLE freigeben.
Auch eine geänderte `H.error_bound` konnte die Freigabe verstärken.

Nun bindet ein Snapshot die Schranke an Werte, Form und Datentyp von Matrix und
Fehlerangabe. Nach einer Änderung liefert die Guard-Auswertung keine verwendbare
Eigenwertschranke: Core und MOD_18 blockieren, auch mit Consent.
Alle fünf neuen Regressionen scheiterten vorher und bestehen danach.
Dieser Konsistenzcheck ist keine Authentisierung gegen Code im selben Prozess.

### Bootstrap: NaN trotz endlicher Eingaben

`bootstrap_ci([1e308, 1e308], seed=1)` und gemischte große Vorzeichen ergaben
NaN: Mittelwertbildung und Perzentilinterpolation liefen über. Beide Schritte
rechnen jetzt auf positiv skalierten Daten; erst die Grenzen werden zurückskaliert.
Perzentil-Methode und lokaler RNG bleiben erhalten. Konstante und gemischte extreme
Werte sowie der Nullfall sind getestet.

### B5: Integritätsleser akzeptierte nicht endliche Zahlen

Vorhandene Events mit `NaN`, `Infinity` oder `-Infinity` wurden bei passendem
Hash als gültig angenommen. Auch eine JSON-Zahl wie `1e999` konnte beim Decodieren
zu Infinity werden und durchgehen.

Der Dateiprüfer lehnt solche Werte nun fail-closed ab. Gleichlautende gewöhnliche
Strings bleiben gültig. Standardkonforme endliche Datensätze und ihre Hashes
werden nicht geändert. Bestehende Ledger- und Receipt-Dateien wurden nicht
umgeschrieben.

P1-Gegenprobe auf dem alten Code: **8 fehlgeschlagen, 34 bestanden**.
Mit Fixes: **64 gezielte Statistik-/Ledger-Tests bestanden**.

### Doku: sichtbare Bytes und Signaturbedeutung

Die Signatur-Notiz zeigte teils gleiche Unicode-Darstellungen trotz verschiedener
Hashes. Escape-Sequenzen sind jetzt wörtlich dargestellt, U+2028 ist sichtbar
markiert. Alle sechs ursprünglichen Python-/JS-Hash-Paare wurden reproduziert.

JavaScript verhindert keine Prüfung; entscheidend ist dieselbe Byte-Darstellung.
Eine Signatur unter einem persönlich zugeordneten Schlüssel belegt allein weder
Bedienperson noch Lesen oder Zustimmung. Der Freigabeprozess bleibt ein eigener
Nachweis.

## 3. Lokale Abnahme und Integration

| Stand | Ergebnis make verify |
|---|---|
| korrigierter P1-Code | 1034 passed, 2 skipped, 169 subtests passed |
| korrigierter P2-Code einschließlich P1 | 1091 passed, 2 skipped, 169 subtests passed |
| gemeinsame Integration aller fünf PRs | **1126 passed, 2 skipped, 169 subtests passed** |

Der lokale Integrations-Commit ist
`df8b5e623ecd51f2441206cb4db70667d3b532e7`: konfliktfreie Zusammenführung aller
PRs und Nachbesserungen, kein Merge nach main und keine eigene Produktversion.

Frische Umgebung über den vorgesehenen Lock-Workflow:
Python 3.12.14, uv 0.12.18, NumPy 2.5.3, SciPy 1.18.1, Hypothesis 6.170.12.

- make verify-governance: 16 Workflows bestanden; 22 VOIDs synchron.
- Ruff, Black, mypy, Bandit und python tools/python_lock.py check: bestanden.
- make demo ohne Secret: ausdrücklich UNSIGNED / signature not verified.
- make demo mit ausschließlich lokalem Testschlüssel: Signatur verifiziert.
- Keine geschützten Pfade im kombinierten Diff geändert.

Die zwei Skips betreffen DataLad (nicht installiert).
Vor Veröffentlichung dieses Nachtrags wurden die neuen Heads erneut geprüft:
Alle Jobs sind abgeschlossen, kein Fehlschlag. #438, #439 und #441 haben jeweils
47 erfolgreiche und 9 übersprungene Checks; #440 hat 49 erfolgreiche und
9 übersprungene Checks. Die fünf vorgeschriebenen Checks sind auf jedem neuen
Head erfolgreich: DeepJump-Audit, Pointer/Lint, All Tests Pass, Python-Qualität
und FOKUS-Guard. Dies sind neue Läufe, keine Übernahme der alten grünen Ergebnisse.

- [#438: All Tests Pass](https://github.com/fleksible/entaENGELment-/actions/runs/40733913796/job/122977677551)
- [#439: All Tests Pass](https://github.com/fleksible/entaENGELment-/actions/runs/40734009905/job/122978768280)
- [#440: All Tests Pass](https://github.com/fleksible/entaENGELment-/actions/runs/40734061508/job/122978454950)
- [#441: All Tests Pass](https://github.com/fleksible/entaENGELment-/actions/runs/40734113165/job/122979010752)

## 4. Merge-Relevanz, Reihenfolge und Offenheit

1. #437: historischer Befundbericht mit Harness und diesem Nachtrag; kann
   unabhängig von den Fixes reviewed werden und behauptet keine Fehlerfreiheit.
2. #438: zuerst für Code-Merges. B1 hat Vorrang; B2 sowie Ledger- und
   Statistik-Nachbesserungen sind mit deterministischen Regressionen belegt.
3. #439 und #440: danach, beide setzen den korrigierten P1-Code voraus.
4. #441: fachlich unabhängig, separat reviewbar.
5. Vor jedem Merge gilt die CI des dann aktuellen Heads. Nach dem ersten Merge
   bei Bedarf den Integrationsstand der übrigen PRs erneut prüfen.

**B9 bleibt teilweise offen:** `np.asarray(H)` und andere explizite Matrix-only-
Zugänge können die Herkunftsmarkierung entfernen. Falsche deklarierte Fehler- und
Funktionsannahmen werden nicht erkannt. Im Repo wurde kein Laufzeit-Aufrufer der
numerischen Guard-Kette gefunden; externe Consumer sind nicht erfasst.

Core (1e-6) und MOD_18 (1e-8) behalten verschiedene Flach-Toleranzen.
Übereinstimmung ist bei gleicher Toleranz geprüft; keine stillschweigende
Vereinheitlichung.

B3 bleibt vorläufig stillgelegt, bis ein fachliches Testdesign feststeht.
Die neuen Standard-/Consent-Notizen sind ANNEX-Entwürfe, keine Beschlüsse.
Hypothesis prüft die formulierten Invarianten und liefert keinen allgemeinen
Sicherheitsbeweis.

**Kleinste Owner-Entscheidung:** Die begrenzten Fixes nach aktuellem CI und Review
in obiger Reihenfolge übernehmen; B9 als Teilfix mit benannten offenen Zugängen
führen. Für diese Reparaturen ist keine weitere GOLD-, Toleranz- oder
Standardentscheidung erforderlich.

