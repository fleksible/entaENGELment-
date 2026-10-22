# tesser3TAKT — Bestandsrevision vom 2026-10-22

**Status:** ANNEX · DERIVED

**Prüfart:** gezielter Dokument- und Codeabgleich, keine Kanonisierung

**Basis:** [`main@020cd06f12780e18b265bd80e5336c704973dc58`](https://github.com/fleksible/entaENGELment-/tree/020cd06f12780e18b265bd80e5336c704973dc58)

**Beobachtet und lokal geprüft:** 2026-10-22, UTC

## 1. Scope und Herkunft

[FAKT] Dieser Bericht begründet den zugehörigen Diff an sieben bestehenden Dateien.
Gelesen wurden die betroffenen Dokumente und Hook-Kommentare sowie die unten
benannten Runtime-, Test- und historischen Audit-Anker. Alle Bestandsbefunde beziehen
sich auf den gepinnten Basis-Commit. Die lokalen Läufe prüfen den darauf vorbereiteten
Patch. Die CI der PR liefert den Prüfbeleg für deren konkreten Head-Commit.

[FAKT] Quellraum dieses öffentlichen Diffs sind ausschließlich bereits öffentliche
Repo-Inhalte. Private Quelldateien, Dateinamen, Library-IDs und Gesprächsauszüge
werden nicht übernommen. Metadaten eines privaten Inhalts ersetzen keine Lektüre
dieses Inhalts. Die Revisionsmatrix und die getrennten neuen Vorhaben werden hier
nicht als weiteres Aufgabenregister abgelegt.

[FAKT] Die Autorisierung betrifft die vereinbarten Bestandskorrekturen und deren
Push/Merge nach grünen Prüfungen. Es wird kein GOLD-Pfad und kein bestehender
Receipt verändert. Der Bericht ist ein abgeleiteter Prüfbeleg; er vergibt keine
fachliche oder normative Autorität.

## 2. Befund und begrenzte Korrektur

| Bestandsanker | Befund an der Basis | Änderung dieses Diffs |
| --- | --- | --- |
| [Source Decoration Map](../tesser3takt/SOURCE_DECORATION_MAP_v0_1.md), §§0–2 | [FAKT] Der Scope nennt Navigation bereits; Regel und Rollenspalte nennen nur Dekoration/Modell. | Navigation in Regel und Spaltenkopf sichtbar machen. Guards bleiben erhalten. |
| [Lyra-Strings](../tesser3takt/LYRA_STRINGS_COMPLEMENT_v0_1.md), §§3–4 | [FAKT] Sieben verschiedene Rollen sind vorhanden; Rolle 4 ist die Mast-/Stimmachse. | [MODELL] Positionsgruppierung `3\|1\|3` ergänzen, ohne seitliche Rollen gleichzusetzen oder einen Klangadapter zu behaupten. |
| Lyra-Strings §0, [LYRA-Kenogramm](../kenograms/LYRA.md), [RF-Bericht](../../lyra/lyra_T1_1_scan_report_REAL.md) | [FAKT] Derselbe Name bezeichnet unterschiedliche Funktionen. | Die drei Namensräume mit Pfad und Funktion abgrenzen; keine Migration. |
| [HUD v0.1](../spec/tesser3takt_hud_v0_1.md), [HUD v0.2](../spec/tesser3takt_hud_v0_2.md), `HUD_FRAME_PROVENANCE` | [FAKT] v0.2 existiert und wird im HUD-Code referenziert. | v0.1 als Vorgänger erhalten und mit datiertem Hinweis auf v0.2 verbinden. |
| HUD v0.2, [Frame-Code](../../ui-app/lib/tesser3takt-frame.ts), [HUD-Code](../../ui-app/lib/tesser3takt-hud.ts) | [FAKT] Implementierungsort, mechanische Durchsetzung, Testpfad und ausgeführter Lauf sind verschiedene Belege. | Diese Angaben an diesem Dokument getrennt führen; keine repo-weite Metadatenpflicht einführen. |
| HUD v0.2 §§1, 5, 8; `BoundaryTransition`; `Kη-03` | [FAKT] Regimeanzeige und Boundary-Paarung existieren. Der Typ trägt keine `phaseBefore`/`phaseAfter`; `Kη-03` ist `UNBOUND` mit `slice-transport-receipt` als fehlendem Operator. | Die drei Ebenen und die offene Slice-Bindung ausdrücklich dokumentieren. Kein Runtime-Typ und kein Kenogramm-Status wird geändert. |
| [Intake-README](../intake/README.md) §12, [Shadow-Copy-Hook](../../tools/intake_shadow_copy.py) | [FAKT] Der Ausschluss umfasst GOLD-Pfade und weitere bereits verortete Dokumente. Die gemeinsame Bezeichnung als GOLD/Kanon verwischt dies. | Nur Beschreibung und Kommentare berichtigen. Pfadlisten und ausführbares Verhalten bleiben gleich. |
| [Traversal-Grammatik](../decisions/TRAVERSAL_GRAMMAR_v0_1.md), Kopf und §0 | [FAKT] Entscheidungsstatus und Branch-Ziel sind auf `v0.1.2-pre` bezogen. | Historischen Geltungsbereich erläutern; Status und Receipt-Grenze erhalten. Branch-Verfügbarkeit begründet keine inhaltliche Ungültigkeit. |

## 3. Offene oder unveränderte Ziele

- [UNRESOLVED] Die genaue Entstehungsfolge einzelner Motive ist nicht aus diesen
  Repo-Ankern ableitbar. Es wird keine Herkunft pauschal Nutzer oder Assistenz
  zugeschrieben.
- [FAKT] Der Majorana-Guard „Not a temperature pole; not an actual quasiparticle
  claim.“ bleibt unverändert. Eine zusätzliche Bildposition benötigt einen
  eindeutigen, freigegebenen Modellanker.
- [UNRESOLVED] Eine historische Heptachord-/Mese-Herleitung wurde in diesem Patch
  nicht geprüft. Sie ist keine Voraussetzung der positionsbezogenen Modellsetzung.
- [FAKT] Der [Mikro–Meso-Vertrag](../annex/MICRO_MESO_BRIDGE_v0_1.md) und sein Code
  bleiben unverändert. Die Scanner-Beobachterrollen und HUD-Projektionsmodi werden
  durch diesen Diff nicht aufeinander abgebildet.
- [FAKT] Der [Audit vom 14.07.](2026-07-14_tesser3takt_reentry_gap_audit.md) enthält
  im Review-Eintrag vom 15.07. bereits `attested_refs` mit `main@96bbdb9` und
  `PR#297@e0aaacd`. Er ist daher nicht pauschal „ungepinnt“. Dieser heutige Abgleich
  lässt den historischen Bericht unverändert und rekonstruiert keine fehlenden
  historischen Prüfgrundlagen.
- [UNRESOLVED] Lyra-Analysen sind in öffentlichen Korpus-Exporten als Metadaten
  indexiert. Der konkrete private Fehlertext ist damit nicht gebunden; es wird
  kein vermeintlicher Repo-Zieltext dafür erfunden oder korrigiert.

## 4. Ausgeführte lokale Prüfungen

[FAKT] Umgebung: CPython 3.12.14, Node 24.19.0; Python-Abhängigkeiten mit
`uv 0.12.18` und `tools/python_lock.py sync --group dev` aus dem vorhandenen
`uv.lock` installiert. Lockdateien wurden nicht geändert.

| Prüfung | Ergebnis und Reichweite |
| --- | --- |
| `make verify` | PASS: Port-Lint, 709 Python-Tests und 165 Subtests, strikte Core-Pointer-Prüfung, Claim-Lint. Vier optionale generierte `out/`-Pfade fehlen; alle Core-Pointer sind gültig. |
| `make verify-governance` | PASS: 15 Workflow-Posture-Prüfungen, VOID-Backlog und UI-Spiegel mit 22 VOID-Einträgen synchron. |
| `ruff check src/ tools/ tests/` | PASS. |
| `black --check src/ tools/ tests/` | PASS: 106 Dateien unverändert. |
| `mypy src/ tools/` | PASS: 51 Quelldateien. |
| `bandit -c .bandit.yaml -r src/ tools/` | PASS: keine Befunde unter der bestehenden Konfiguration. |
| Node-Tests für Frame, HUD und Bridge | PASS: 23 Tests mit `node --experimental-strip-types --test` auf den drei vorhandenen `.test.mjs`-Dateien. Bestehende Modulformat-Warnungen bleiben sichtbar. |
| AST-Vergleich des Shadow-Copy-Hooks gegen die Basis | PASS: ausführbarer Python-AST identisch; nur Kommentare geändert. |

[FAKT] Testdateien: [Frame](../../ui-app/test/tesser3takt-frame.test.mjs),
[HUD](../../ui-app/test/tesser3takt-hud.test.mjs),
[Bridge](../../ui-app/test/tesser3takt-bridge.test.mjs).
Die Tests belegen weder einen implementierten Slice-Phasentransport noch die
empirische Gültigkeit der Lyra- oder tesser3TAKT-Modellrollen. Ein vollständiger
lokaler UI-Build wurde für diesen Dokument-/Kommentarpatch nicht ausgeführt;
der UI-Build gehört zum verpflichtenden PR-Gate `All Tests Pass`.

[FAKT] Vor dem Merge sind die CI-Ergebnisse des konkreten PR-Heads maßgeblich.
Dieser Bericht setzt kein CI-Ergebnis vorab auf grün.
