# Report: Security-Audit-Läufe #421/#422/#424 und Entscheidungsgrundlage #423

**Datum:** 2026-10-24
**Fokus:** Security-Audit-Signale einordnen

## Ziel

Die per Mail gemeldeten fehlgeschlagenen Security-Audit-Läufe (#421 Pillow, #422
Python-Lock) und die Codex-Aktivität auf #424 gegen den tatsächlichen
GitHub-Stand prüfen. Außerdem für #423 Replay-Fakten, Modellannahmen und
UNRESOLVED-Größen trennen und die kleinste nächste Entscheidung benennen.

## Aktionen

- [x] PR-Stand #422/#423/#424 und Check-Runs am jeweiligen Head gelesen
- [x] Alle `security-audit.yml`-Läufe vom 2026-10-24 samt Job-Logs ausgewertet
- [x] `filelock`-Advisories über OSV und die Safety-Metadaten über PyPI abgefragt
- [x] #423-Rechenprobe am unveränderten Producer selbst nachgerechnet
- [x] Push-CI auf `main@83caf03` (nach Merge #422) geprüft

## Befund A: Security-Audit-Läufe

[FAKT] Stand beim Prüfen: #424 gemergt 17:29:38Z, #421 gemergt danach,
#422 gemergt 17:44:05Z. Die Merge-Frage zu #422 ist damit erledigt; offen
ist nur noch der Zustand nach dem Merge.

| Lauf | Zeit (UTC) | Head | Fehlerschritt | Ursache |
| --- | --- | --- | --- | --- |
| 40048554982 | 01:10 | #422 Bot `58f9c32` | pip-audit: *Install pip-audit* | `Generated requirements drift: requirements-dev.txt`. Der Bot-Diff war defekt, der Drift-Check hat korrekt abgebrochen. Zusätzlich JS-Gate rot (s. u.) |
| 40114623803 | 17:06 | #422 korrigiert `dbe8690` | JS: *Audit gate (fail on high+)* | 4 high: Electron GHSA-jr5w-w6x2-84p9, Undici 6 und 7 GHSA-xjj6-f33q-929c, Zod GHSA-mrhx-c7xc-m3w5. **pip-audit grün** |
| 40114998021 | 17:11 | #421 `b52b06e` | JS: *Audit gate* | identisch, pip-audit grün |

[FAKT] Die beiden Fehler am Nachmittag kamen aus dem JS-Lock auf `main`. Das ist
ein Repository-Zustand unabhängig von #421 und #422: Beide PRs ändern kein
JS-Paket, und der Workflow auditiert bei jeder Lock-Änderung beide Ökosysteme.
Ursache waren weder der korrigierte Python-Head noch `filelock` oder die
Audit-Umgebung.

[FAKT] Nach #424 (Electron 44.9.1, Zod 4.6.7, Undici-Pins 6.29.1/7.30.1)
sind alle Security-Audit-Läufe grün: #424-Head, #421-Head `92816fe`,
#422-Head `bf0f27c` und `4d9fbdf`, Push `main@28b9b47` und `main@83caf03`.
Der abgebrochene Lauf auf `main@932f539` wurde per Concurrency vom nächsten
Push ersetzt und ist kein Befund.

[FAKT] Auf `main@83caf03` sind alle zehn Push-Workflows grün (DeepJump, Tests, CI,
Policy Lint, Evidence Bundle, SBOM, Security Audit, Smoke, Python Quality,
Runtime-Matrix).

[FAKT] Codex auf #424: Code-Review an `36aa1d9` ohne Befund abgeschlossen.
Ein Security-Review wurde nicht ausgelöst (`status: null`). Es gibt keine offenen
Review-Threads. Die Code-Owner-Anfrage zu #422 in der Mail ist durch den Merge
überholt.

## Befund B: `filelock`, neuer Nebenbefund

[FAKT] OSV listet für das gelockte `filelock==3.32.7` drei Advisories. Alle
wurden am 2026-10-23 zwischen 21:59Z und 22:28Z veröffentlicht, also nach dem
Lock-Audit #410 und kurz vor dem Bot-PR #422:

| Advisory | Schwere | Kern |
| --- | --- | --- |
| GHSA-v4x8-3wr5-3wq8 | HIGH (AV:L, I:H/A:H) | `ReadWriteLock`: platzierter Symlink/Journal → eigene Dateien überschrieben |
| GHSA-9vhv-jxww-xfm5 | LOW (AV:L) | `ReadWriteLock` unter Windows, SQLite-Nebendateien |
| GHSA-567q-5qvw-pf92 | LOW (AV:L) | `SoftFileLock` unter Windows, Oplock blockiert Timeout |

[FAKT] Gefixt ist das erst ab **4.2.1**. Der Bot-Vorschlag `4.1.0` ist selbst von
sechs Advisories betroffen, darunter diesen drei. Das HOLD in #422 hat also kein
wirksames Update zurückgehalten; das Upgrade auf 4.1.0 wäre ebenfalls verwundbar
gewesen.

[FAKT] Die Sperre bleibt bestehen: Safety 3.8.1 ist die neueste Version auf PyPI
und verlangt `filelock<4.0,>=3.16.1`.

[FAKT] `filelock` steht nur in `requirements-dev.txt` (über `safety` und
`cachecontrol[filecache]`), nicht in `requirements.txt`. Das pip-audit-Gate prüft
nur `requirements.txt` und sieht diese Advisories deshalb grundsätzlich nicht.
Ein grünes Python-Gate ist daher kein Nachweis für die Dev-Umgebung.

[UNRESOLVED] Ob `safety` oder `cachecontrol` `ReadWriteLock` bzw. `SoftFileLock`
nutzen, ist nicht geprüft. Alle drei Advisories setzen einen lokalen Angreifer
auf demselben System voraus. Das ist für ephemere CI-Runner wenig plausibel und
betrifft eher Entwicklerrechner mit mehreren Nutzern.

## Befund C: #423, Entscheidungsgrundlage

**C1: reproduzierbare Replay-Fakten** (nachgerechnet am `main`-Producer,
Blob `f7bd8c5`, SHA-256 `002d3857…dc28`, seit `539e87b` unverändert)

- Producer, Parameter (n=256, coupling=0.35) und RNG-Verbrauch (5 Werte pro Sample)
  stimmen mit dem Dokument überein.
- Quell-, Ziel- und Offsetwerte für die Seeds 7/42/123 sind bitgleich
  reproduziert; der Fehler war hier 0, im Dokument ≤ 1.11e-16.
- Falsche Transform-Seeds (hier jeweils seed+1) werden bei 1e-10 abgewiesen
  (Fehler 1.8e-3 bis 4.0e-3).
- PR-CI am Head `af2d092` ist grün; Merge-Status `clean`.

**C2: was die Probe nicht zeigt**

- Die Vorhersage spielt dieselbe RNG-Folge mit derselben Formel nach. Sie
  bestätigt Algebra und RNG-Reihenfolge, liefert aber keine unabhängige Evidenz
  für das Modell (das Dokument sagt das selbst).
- Die im Dokument genutzten falschen Seeds sind nicht genannt; die Gegenprobe ist
  deshalb nur sinngemäß nachvollziehbar.
- Die sieben Adapter-Gegenfälle stehen auf NOT_RUN.

**C3: offene Modellannahmen (Setzungen, keine Fakten)**

- Größe: relative Toy-Phase a − b als SIMULATION_PROXY
- Sample 0 → EXIT, Sample 1 → ENTRY von B-Q0-Q1: neu vorgeschlagen, ohne
  beobachteten Producer-Pfad
- `basisId=toy-relative-a-minus-b-v1`, `handedness=RIGHT` als Testkonvention
- Turns modulo 1: die Windungszahl geht bewusst verloren

**C4: bewusst UNRESOLVED/HOLD:** Graining-Herkunft, Blindseite, Sphärenstatus,
Kη-03 (UNBOUND), Anbindung (HOLD), HUD-Semantik.

**Kleinste nächste Entscheidung:** eine Ja/Nein-Frage, nur für den begrenzten
Test-Replay: *Wird a − b mit Sample 0 → EXIT / 1 → ENTRY als Testbezug
akzeptiert?* Bei Ja folgt der opt-in-Replay-Export mit den sieben
Adapter-Gegenfällen als Tests. HUD-Semantik, Kη-03 und die UNRESOLVED-Größen
bleiben davon unberührt. Bei Nein ist eine andere Größe oder Zuordnung ein
gültiger Ausgang (C3), und #423 bleibt Draft.

## Nicht getan

- Nichts an #423, Lock, Workflows, GOLD oder Receipts geändert. Kein Re-Run,
  kein Review-Kommentar.
- Kein `filelock`-Fix: Er ist mit Safety 3.8.1 nicht konsistent auflösbar und
  wäre ein Fokuswechsel.
- Die sieben Adapter-Gegenfälle aus #423 nicht implementiert.

## Risiken

- Das Python-Gate deckt Dev-Abhängigkeiten nicht ab (Befund B); ein grünes Gate
  kann so falsche Sicherheit vermitteln.
- Das HOLD-Narrativ in `docs/audit/2026-10-24_pr422_lock_exports.md` legt nahe,
  4.1.0 sei das zurückgehaltene Security-Update; tatsächlich ist erst ≥ 4.2.1
  wirksam.

## Offene Punkte

- [ ] ☐ Entscheiden, ob `requirements-dev.txt` informativ (nicht blockierend) mit
      pip-audit geprüft werden soll. Das wäre eine Workflow-Änderung mit eigenem
      PR und Checkpoint.
- [ ] ☐ `filelock` ≥ 4.2.1 erst, wenn Safety `<4.0` aufhebt; alternativ Safety
      aus der Dev-Gruppe herausnehmen (gesonderte Entscheidung, verknüpft mit
      #416).
- [ ] ☐ #423: die Ja/Nein-Entscheidung aus Befund C treffen; die falschen Seeds
      im Dokument nennen.

## Artefakte

- `OUT/2026-10-24_pr422-424_security_audit_review.md`
- Läufe: `actions/runs/40048554982`, `40114623803`, `40114998021` (rot);
  `40117462741` (`main@83caf03`, grün)
