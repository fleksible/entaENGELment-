# Audit: Korpus v17, Folgestand v18 und main

**Datum:** 2026-10-13 · **FOKUS:** Korpusnachtrag und Statusabgleich
**DERIVED / REVIEW-PENDING · beratende Gegenprüfung, keine Promotionsentscheidung**

## Basis und Ergebnis

Repo-Basis: `a7773db68d97dbd8271b0921d011934d2e921170`. Der Branch-Ref wurde im Folgelauf erneut aufgelöst.
Der v18-Vergleichsblock speichert den Hash des getrennten Berichts und den Hash des früheren Indexeingangs. Das ist kein Selbsthash des v18-Artefakts.

Der frühere Bericht trägt SHA-256 `249cd59174ba694583f3b6a7a49d2600e5c9d96e62db2f1ab4d0867816aa8314`.
Der [Exportvertrag](../intake/raw/2026-10-13/corpus-v17/EXPORT.md) trennt die beiden
Indexfassungen. [CSV](../intake/raw/2026-10-13/corpus-v17/corpus-matrix.csv) und
[Delta](../intake/raw/2026-10-13/corpus-v17/corpus-delta.json) enthalten alle 96 Identitäten.

## Gegenlesung: bestätigte und begrenzte Aussagen

| Gegenstand | Direkt geprüfter Befund | Konsequenz |
|---|---|---|
| Versionsfrage | v18 ist bestätigte Speicherversion, eingebettete 17 bezeichnet den Eingang | Getrennte Originalhashes, Exportmanifest für die tatsächlichen Paketbytes |
| Zähler | v17: 88 vollständig, 0 partiell, 258 Punkte; v18: 88 vollständig, 2 partiell, 259 Punkte | Kein Rechenfehler der v17-Tabelle; fehlende unmittelbare Gegenüberstellung ergänzen |
| Claim-Vokabular | FAKT, MODELL, HYPOTHESE, METAPHER, ANALOGIE, UNRESOLVED | 93 außerhalb in beiden Ständen; 84 ist für diese Menge nicht reproduzierbar |
| VOID-024 | VOIDMAP und UI-Mirror führen Audio-Bridge-Policy, GUARD, OPEN, legacy VOID-013 | Tracker-Entwurf nur mit Quellenraum/Fassung nennen; keine Registry-Änderung |
| Chronologie | Registry-Feld created=2026-06-24; Datei-Metadatum observed_modified_at=2026-07-25 | Verschiedene Zeitbegriffe. Daraus folgt kein belegtes Entstehungsdatum oder bewusste ID-Übernahme |
| Kη-07 | HUD führt UNBOUND/missingOperator und instanziiert selbst validierte pairId-Paare | Konkreter interner Zuordnungs-/Statuskonflikt, stärker als nur Cross-Datei-Ähnlichkeit |
| Kη-07-Gate | Nur needsCounterfixture=true; drei andere Flags false | Kenogramm-Metadaten sind kein Verzicht auf Repo-Review oder alle übrigen Spec-Kriterien |
| Counterfixture | Negative Fälle existieren in Tests; Spec verlangt bestandene Counterfixtures | Separate JSON-Datei ist sinnvoller Vorschlag, keine ausdrücklich vorgeschriebene Dateiform |
| Repo-Gates | verify-governance und Standard-claim-lint erfassen Intake nicht | Eigener Verifier; neue Prüfung derzeit explizit manuell |
| Pre-Commit | Trigger auf geänderte Dateien, Scan aber auf fester Scope-Liste | Kein wirksames automatisches Zählergate für diesen Diff |
| claim_lint-CLI | Verzeichnisse über --scope, keine positionalen Pfade | Ausführbaren Aufruf dokumentieren |
| make intake | Numerischer Record plus flache Kopie | Tatsächliche Helper-Ausgabe erhalten; elf statt der behaupteten neun Dateien |

## VOID-024 und Kη-07 mit konkreten Ankern

VOID-024: `VOIDMAP.yml` und `ui-app/lib/voidmap-parser.ts`;
Korpusanker `doc-1187cadc1fe1` (`VOID-024_block.yaml`) bleibt RAW/HOLD im historischen Export.
Eine unqualifizierte Übernahme des Tracker-Namens könnte die Safety-Policy-Zuordnung
verdrängen. Das ist ein Risiko einer falschen zukünftigen Transformation, kein
bereits erfolgter Registry-Writeback.

Kη-07: `ui-app/lib/tesser3takt-hud.ts`, `KENO_FRINGES`, `HUD_BOUNDARY_TRANSITIONS`
und `buildTesserHudFrame`; die letztgenannte Funktion prüft den Transport mit
`validateTesserTickFrame` und wirft bei einem ungültigen Ergebnis.
`ui-app/lib/tesser3takt-frame.ts` prüft EXIT/ENTRY-Paar, Reihenfolge,
`transformedFrom`, Koordinatenraum, Lattice und Springer-Legalität.
`docs/spec/tesser3takt_hud_v0_2.md` §16 nennt zusätzlich Build, Lint, Typecheck,
Overlap-Audit und Counterfixtures vor Promotion. Es gibt hier keine automatische
Statusentscheidung. Kη-07 bleibt P1; die Gegenlesung nennt es irrtümlich den zweiten P0-Fund.

## Priorisierte Kandidaten C01–C19

### C01 · P0 · Korpus-Snapshot v10 → v17

Relevanz: Sehr hoch: gemeinsame überprüfbare Ausgangsbasis. Entscheidungsvorschlag: EXTEND.

Korpusanker: 25 neue Einträge im Delta; sieben abgeschlossene Teillektüren.

Repo-Anker: `docs/intake/raw/2026-10-07/corpus-v10/README.md`, `docs/intake/raw/2026-10-07/corpus-v10/EXPORT.md`, `docs/intake/INDEX.md`.

Delta: Einen datierten, privacy-reduzierten Nachtrag mit source_id, Fassung, Lesestand, Herkunftsfamilie, Zuordnung und HOLD-Grund vorbereiten. v10 als historischen Snapshot erhalten.

Done: 88+8 Quellidentitäten vollständig disponiert; Summen und Referenzen konsistent; alle 38 alten Relationen und 5 alten Konflikte nach dem dokumentierten Exportfilter erhalten; Originale/Suchcursor nicht im öffentlichen Patch.

### C02 · P0 · Namensräume und VOID-024-Kollision

Relevanz: Sehr hoch: falsche Registry-Zuordnung verhindern. Entscheidungsvorschlag: HOLD + EXTEND.

Korpusanker: doc-1187cadc1fe1, doc-065f8e49e510, doc-72ac8ddd027c.

Repo-Anker: `VOIDMAP.yml`, `docs/decisions/DEC-VOID-016-NAMESPACE.yml`, `docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md`.

Delta: Im Audit den Konflikt mit Quellenraum/Fassung festhalten. Den Tracker nur unter seinem Quellnamen führen, ohne neue offizielle VOID-ID und ohne Umbenennung der Registry. Weitere private P7-/F-/R-/Keno-Kennungen typisieren.

Done: Kein unqualifizierter VOID-024-Verweis auf den Tracker im neuen Vorschlag; jede Kennung besitzt namespace, scope und source. Konkrete spätere Registry-Entscheidung bleibt menschlich.

### C03 · P0 · Claim-Tags, Status und Belegrolle

Relevanz: Sehr hoch: unbeabsichtigte Promotion verhindern. Entscheidungsvorschlag: REUSE + EXTEND.

Korpusanker: doc-fbf3221d393a, doc-065f8e49e510, doc-a5d6c14d0dff.

Repo-Anker: `docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md`, `policies/claim_tags_v0_2.yaml`, `tools/claim_lint.py`.

Delta: Quelltag unverändert erhalten; für den neuen Nachtrag separate Felder für Claim-Typ, Arbeitsstatus, Authority und Evidenzrolle benutzen. Unklare Mappings explizit offenlassen.

Done: Kein verlustbehaftetes globales Retagging; nachvollziehbare Mapping-Notiz je tatsächlich übersetztem Feld; Policy-/Linter-Erweiterung separat.

### C04 · P1 · Receipt-, Replay- und Persistenz-Crosswalk

Relevanz: Hoch: konkreter Wiedereinstieg und Rücknahme. Entscheidungsvorschlag: REUSE + EXTEND.

Korpusanker: doc-e430d546135a, doc-ccc226e07c29, doc-488c3cd86111, doc-065f8e49e510.

Repo-Anker: `docs/annex/SYNTHBIOSIS_MODULE_ADAPTER_MAP_v0_1.md`, `docs/annex/ERK_CONNECTIONS_v0_1.md`, `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md`, `docs/decisions/ADR-0005-erk-human-decision-precedence.md`.

Delta: Bestehende Contracts verlinken; nur den UI-Crosswalk mit Modus, Eventindex, Policy-Fassung, Belegfunktion und unbekannten Downstream-Folgen ergänzen.

Done: Ein Beispiel zeigt historische Information, späteres Wissen und neuen Entwurf getrennt. Sichtung erzeugt keine Persistenz; ein Integritätsreceipt bestätigt keine semantische Treue; keine automatische Retraction-Kaskade erfinden.

### C05 · P1 · Kη-07: Kenogramm gegen implementierte Boundary prüfen

Relevanz: Hoch: sichtbarer Statusdrift. Entscheidungsvorschlag: EXTEND.

Korpusanker: doc-c109ee67f3f3, doc-952bb22fd67d, doc-2d5ee24da05d, doc-72ac8ddd027c.

Repo-Anker: `ui-app/lib/tesser3takt-hud.ts`, `ui-app/lib/tesser3takt-frame.ts`, `ui-app/test/tesser3takt-frame.test.mjs`, `docs/spec/tesser3takt_hud_v0_2.md`.

Delta: Die genaue Abdeckung des Kenogramm-Begriffs mit dem vorhandenen Vertrag vergleichen und eine eng begrenzte Status-/Pointerkorrektur als eigenen Code-/UI-Diff vorbereiten.

Done: Nur belegte Operatorlücke als abgedeckt markieren; Restfragen des Kenogramms und VOID-027 bleiben offen. Keine automatische CLOSED-Promotion.

### C06 · P1 · SailObservation: indirektes Ereignisschema

Relevanz: Hoch: schließt eine konkrete Spezifikationslücke an bestehendem VOID. Entscheidungsvorschlag: EXTEND.

Korpusanker: doc-59c46100ee8c, doc-31eb564a8cf6, doc-6df3bd782cba, doc-1adb2a1436f1.

Repo-Anker: `VOIDMAP.yml`, `docs/tesser3takt/TESSER3TAKT_ASSEMBLY_NAVI_v0_1.md`.

Delta: Als ANNEX-Kandidat ein kleines Ereignisschema mit drei Fällen formulieren: Ko-Präsenz, prädiktiver Anschluss, fehlgeschlagene Relation. Bestehenden VOID-026 verknüpfen.

Done: Kein direktes Wind-, Qualia- oder Personeninnenzustandsfeld; Alternativerklärungen und negatives Ergebnis zulässig; noch keine Schließung des gesamten VOID-026.

### C07 · P1 · Switchboard: Zustandskapsel und getrennte Modulachsen

Relevanz: Hoch: weniger Wiederanlaufkosten ohne zweite Authority. Entscheidungsvorschlag: EXTEND.

Korpusanker: doc-62ec5dc091e9, doc-ccc226e07c29, doc-8580b64a01a7.

Repo-Anker: `docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md`, `docs/annex/ERK_CONNECTIONS_v0_1.md`, `docs/annex/MICRO_MESO_BRIDGE_v0_1.md`.

Delta: Zuerst einen lesenden Manifest-/Kapsel-Contract an bestehende Typen anschließen. requires-DAG und begrenzte reenters-Zyklen getrennt führen. Einen behaupteten HD-V02-1-Beschluss nur als Quellbericht behandeln.

Done: Eine Beispielkapsel enthält Parent, Quellenrevision, offene Reste, Zielprofil und Rückweg; Aktivierung verleiht keine Authority. Kein Plugin-Loader, zweites Ledger oder SQLite/CAS-System im ersten SoT-PR.

### C08 · P1 · Protected emergence und beidseitiger Reentry

Relevanz: Hoch: Schutz während noch unbestimmter Entwicklung. Entscheidungsvorschlag: REUSE + EXTEND.

Korpusanker: doc-616cd8b35fe5, doc-8195a8547cbd.

Repo-Anker: `PRIVACY_BOUNDARY.md`, `docs/intake/raw/ROSETTA_MEMBRANE_TRANSLATION_FRAME_v0_1.md`, `docs/annex/SYNTHBIOSIS_MODULE_ADAPTER_MAP_v0_1.md`.

Delta: Eine kurze Ergänzung als SPEC-WIP mit konkreter verbotener Operation anbieten: weder Stille noch noch unbenannte Entwicklung automatisch klassifizieren oder publizieren.

Done: Zwei Gegenfälle zeigen verweigerte Benennung und misslungenen Rückweg. Keine zusätzliche Behauptung über KI-Innerlichkeit; Rückübersetzbarkeit bleibt verlustbegrenzt.

### C09 · P2 · Freeze-Frame und Reentry-Qualitätsfilter

Relevanz: Mittel bis hoch: operativ präzisere Wiedereinstiege. Entscheidungsvorschlag: REUSE + EXTEND.

Korpusanker: doc-4ee21fcdcbd8, doc-20448581f742, doc-256c894b475d, doc-2d5ee24da05d, doc-9b8e7fb40e37, doc-2a4497a20bc6.

Repo-Anker: `docs/decisions/TRAVERSAL_GRAMMAR_v0_1.md`, `docs/intake/raw/ROSETTA_MEMBRANE_TRANSLATION_FRAME_v0_1.md`, `docs/annex/MICRO_MESO_BRIDGE_v0_1.md`.

Delta: Feld-Crosswalk erstellen; optionale View-Felder ergänzen, bestehende Consent-/Exit-/Falsifikatorpflichten erhalten. Reentry-Qualität zunächst als qualitative Rubrik behandeln.

Done: Eine Verdichtung verliert weder ungewählte Branches noch Schutzstatus; kein globaler Goldnugget-Score und keine behauptete verlustfreie Inversion.

### C10 · P2 · Sphinx-/Phasen-Traversal: Basis, Grain und sechs Fixtures

Relevanz: Mittel: konkrete Anschlussidee mit Definitionsarbeit. Entscheidungsvorschlag: EXTEND + HOLD.

Korpusanker: doc-952bb22fd67d.

Repo-Anker: `ui-app/lib/tesser3takt-frame.ts`, `ui-app/lib/tesser3takt-bridge.ts`, `docs/annex/MICRO_MESO_BRIDGE_v0_1.md`.

Delta: Kategoriale Zusatzfixture statt Neubau des Transports: konstruktiv, destruktiv, neutral, Basisfehler, Kontextverlust, ehrliches HOLD. Begriffe vor Messwerten definieren.

Done: Jeder Fall schließt eine unzulässige Interpretation aus; Typ-/Grainwechsel hält Provenienz und Verlust fest. Physikalische Interferenz und Spin-Identität bleiben HOLD.

### C11 · P2 · Scale-Invariance Derivation Ledger

Relevanz: Mittel: prüfbare Skalenübersetzung. Entscheidungsvorschlag: REUSE + EXTEND.

Korpusanker: doc-59c46100ee8c, doc-31eb564a8cf6, doc-6df3bd782cba, doc-1adb2a1436f1.

Repo-Anker: `docs/annex/MICRO_MESO_BRIDGE_v0_1.md`, `docs/annex/SPHAERENLOGIK_SCALE_SCANNER_v0_1.md`, `src/core/evidence_bridge_adapter.py`.

Delta: Vier Fragen als menschenlesbare Ansicht oder Zusatzfixture auf bestehenden Brücken erproben. Eigenes Ledger nur bei nachgewiesenem Restbedarf.

Done: Ein Gegenbeispiel verhindert Aufstieg von lokaler Ähnlichkeit zu Makrogesetzmäßigkeit. Kein zweiter dauerhafter Ledger-Stand.

### C12 · P2 · POV-/Readout-Probe mit Farbe und Stille

Relevanz: Mittel: kleiner testbarer Schritt. Entscheidungsvorschlag: REUSE + EXTEND.

Korpusanker: doc-c109ee67f3f3, doc-72ac8ddd027c.

Repo-Anker: `ui-app/fixtures/tesser3takt-minimal-frame.json`, `ui-app/test/tesser3takt-frame.test.mjs`, `ui-app/test/tesser3takt-bridge.test.mjs`.

Delta: Zwei Projektionen derselben Fixture vergleichen; Farb-/Audioänderung darf IDs, Reihenfolge oder Claim-Layer nicht umdeuten.

Done: Gleiches Inputobjekt ergibt dieselben Beziehungen trotz Readoutwechsel; Informationsverlust sichtbar. Kein Wirkungsclaim über Wahrnehmung oder Bewusstsein.

### C13 · P2 · Autonomer Grimm-Gästetest und Chronologie

Relevanz: Mittel: Fremdlesbarkeit statt weiterer interner Verdichtung. Entscheidungsvorschlag: REUSE + EXTEND / Chronologie HOLD.

Korpusanker: doc-c22f49968652, doc-72ac8ddd027c.

Repo-Anker: `docs/narratives/grimm2/README.md`, `docs/narratives/grimm2/_template.md`, `docs/annex/SYNTHBIOSIS_MODULE_ADAPTER_MAP_v0_1.md`, `PRIVACY_BOUNDARY.md`.

Delta: Eine neutrale Szene mit ACCEPT/REVISE/REJECT/SILENCE und profilfreiem Exit als späteren Test anbieten. Die Chronologiekorrektur als zugeschriebenen Herkunftshinweis erhalten, bis Originalturns vorliegen.

Done: Ein externer Leser darf die Szene sinnvoll ablehnen oder verlassen; kein verstecktes Profil. Private Herkunft bleibt unrekonstruierbar.

### C14 · P2 · Strukturmeißel: getypte partielle Komposition

Relevanz: Mittel: Formalisierungspunkt mit guten Negativfällen. Entscheidungsvorschlag: REUSE + EXTEND.

Korpusanker: doc-a5d6c14d0dff.

Repo-Anker: `src/core/evidence_bridge_adapter.py`, `docs/intake/raw/ROSETTA_MEMBRANE_TRANSLATION_FRAME_v0_1.md`, `docs/narratives/grimm2/GRIMM_IR_MEREOTOPOLOGY_INTAKE_v0_1.md`.

Delta: Einen kleinen Contract-Crosswalk und zwei neue negative Kompositionsfälle vorschlagen. Zustandsabhängige Guards nicht als allgemein assoziative Kategorie ausgeben.

Done: Verbotene Metapher→Physik- und Crossing→Collision-Aufwertungen scheitern; keine neue allgemeine Metagrammatik als bereits bewiesen deklarieren.

### C15 · P3 · Genealogien, Dossiers, Kopien und historische Reports

Relevanz: Archivisch hoch; Umsetzungsdringlichkeit niedrig. Entscheidungsvorschlag: KEEP_BOTH + REUSE.

Korpusanker: doc-cf2291080049, doc-b8dce646de5f, doc-b091c6213337, doc-8277af3a67fb, doc-4ad3f7a35130, doc-2a4497a20bc6.

Repo-Anker: `docs/intake/raw/2026-10-07/corpus-v10/corpus-snapshot.json`, `docs/rzt/LOG_ZN_ORBIT_001.md`, `docs/tesser3takt/S4_LOGZN_bridge.md`.

Delta: Quellenfamilien und Art des Gleichheitsbefunds erhalten; transferierte und ähnliche Texte getrennt halten. Historische Repo-Berichte durch datierte aktuelle Overlays ergänzen.

Done: Keine Kopie zählt als unabhängige Evidenz; keine rekonstruierte Genesis als zeitgenössischen Beleg ausgeben.

### C16 · P3 · Nektar-Membran v2.1: statischer Code und Gegenbefunde

Relevanz: Forschung später; Gegenbefunde schon im Intake wichtig. Entscheidungsvorschlag: HOLD.

Korpusanker: doc-5b5615982a60.

Repo-Anker: `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md`, `docs/annex/PHOTONIC_THERMAL_AIRLOCK_v0_1.md`.

Delta: Diese negativen Befunde im Nachtrag mitführen. Später Originalcode, Abhängigkeiten und kontrollierte Topologie-Gegenfälle beschaffen; nicht PDF-Prosa als getesteten Repo-Code importieren.

Done: Ein reproduzierbares synthetisches Experiment trennt Eingabe, Detektorausgabe und kausale Interpretation. Bis dahin keine Implementierungs- oder Empiriepromotion.

### C17 · HOLD · Privates P7, neue Hardware-/Bio-/Qualia-Schichten

Relevanz: Scope- und Beleglücke. Entscheidungsvorschlag: HOLD.

Korpusanker: doc-fbf3221d393a, doc-065f8e49e510, doc-5b5615982a60, doc-72ac8ddd027c.

Repo-Anker: `PRIVACY_BOUNDARY.md`, `docs/spec/synthosia_scope.md`, `docs/annex/RESEARCH_VALIDATION_GATE_v0_1.md`.

Delta: Nur reduzierte Herkunfts- und HOLD-Verweise in einen SoT-Nachtrag aufnehmen. Die Arbeit an privaten Apps, Messungen, Hardware oder globalen Theoriebehauptungen bleibt eine getrennte Aufgabe.

Done: Konkreter Quellstand, Zweck, Freigabe und eigene Prüfbedingung liegen vor. Keine aus dem Index erfundene Aktivierung.

### C18 · P1 separat · Reviewpaket #389/#390/#391: operative Repo-Arbeit

Relevanz: Hoch für Betrieb; eigener PR-Strang. Entscheidungsvorschlag: REUSE + aktueller Status.

Korpusanker: doc-b87d9aec98bb.

Repo-Anker: `docs/ci/PYTHON_LOCK.md`, `OUT`.

Delta: Im SoT-Bericht nur exakte PR-Pointer und Beobachtungszeit führen. Code-, Dependency- und Geräteprüfungen in ihren bestehenden PRs belassen.

Done: Frischer Status je konkretem Head; kein Modellreview ersetzt CODEOWNERS-Entscheid oder physischen Gerätetest.

### C19 · P1 · SoT-Spine: Enforcement-Abschnitt aktualisieren

Relevanz: Hoch: Dokumentstatus von tatsächlicher Abdeckung trennen. Entscheidungsvorschlag: REUSE + Statuskorrektur.

Korpusanker: doc-ccc226e07c29, doc-065f8e49e510, doc-b87d9aec98bb.

Repo-Anker: `docs/governance/SOURCE_OF_TRUTH_SPINE_v0_2_1.md`, `docs/annex/EVIDENCE_ROUTING_KERNEL_v0_1.md`, `docs/decisions/ADR-0005-erk-human-decision-precedence.md`, `src/core/evidence_routing.py`.

Delta: Einen datierten Abdeckungsnachtrag mit Implementierungspfad, Tests und verbleibenden Lücken formulieren. Die ursprüngliche Zielbeschreibung historisch erhalten; keinen globalen live-Status daraus machen.

Done: Die Tabelle trennt vorhanden/partiell/offen und benennt den Scope. Personen-Authentisierung und vollständige Claim-Policy bleiben nicht behauptet.

## Negativer Befundkatalog und Reichweite

- Kein Beleg, dass der Tracker-Entwurf die Registry schon überschrieben hat.
- Kein Entstehungsnachweis aus Dateiänderungszeiten; keine kausale Genealogie daraus.
- Kein Gate, das Kη-07 allein aufgrund von `needsHumanCommit: false` automatisch schließt.
- Keine ausdrückliche JSON-Dateipflicht für Counterfixtures in der gelesenen Spec.
- Keine Prüfung der Indexzähler durch die bisherigen allgemeinen Repo-Gates.
- Keine CI-Verdrahtung des neuen Verifiers durch diesen Diff.
- Keine vollständige erneute Lektüre der Originalquellen; kein Zugriff auf privates P7.
- Keine unabhängige Evidenz durch Kopien, Research-Radare oder diesen Auditbericht.
- Kein aktualisierter Review der Inhalte von PR #389/#390/#391; ihre Arbeit bleibt separat.
- Kein Nachweis, dass die Sphinx-/Phasenidee oder statischer Nektar-Code valide Runtime sei.

## Validierung dieses Vorschlags

| Prüfung | Ergebnis | Reichweite |
|---|---|---|
| Eigener Export-Verifier, einschließlich --input-v18 | PASS | Rekonstruktion, beide Zählerspalten, Tagmenge, CSV, Fortsetzungen, neun Manifestdateien, direkte v18-Bytes |
| Zwölf isolierte Negativproben | 12/12 korrekt abgewiesen | Falsche Payload-/README-/EXPORT-Zähler, Vokabular, Fortsetzung, doppelte Quelle, interner Schlüssel, alte Update-Basis, CSV, Hash, fehlender Manifestpfad, doppelter JSON-Schlüssel |
| make verify | PASS; 665 Tests und 165 Subtests; 104 Warnungen | Core-Regression; vier optionale Pointer fehlen laut bestehendem Gate |
| Frame-/Bridge-Tests | 19/19 PASS | Neun Frame- und zehn Bridge-Tests; keine UI-/Geräteprüfung |
| make verify-governance | PASS | 15 Workflow-Verträge, Backlog, 22 VOID/UI-Zuordnungen |
| ruff / black für verify_counts.py | PASS | Neue Python-Datei; kein globaler Style-Fix |
| claim_lint mit explizitem Intake-/Audit-Scope | WARN, nicht blockierend | Heuristische Warnungen einschließlich Python-require-Aufrufen; keine Zählerprüfung |
| Lokale Markdown-Links | PASS | Alle Links der neun manifestierten Dateien aufgelöst |
| make verify-js | BLOCKED vor Turbo | pnpm meldet ERR_PNPM_IGNORED_BUILDS für @parcel/watcher, electron-winstaller, unrs-resolver |

Die initial fehlende pytest-Startdatei wurde für den Core-Lauf durch einen lokalen
Launcher auf den vorhandenen Python-Runtime und die vorhandenen Test-Pakete ersetzt.
Das ist kein neuer Nachweis einer reproduzierbaren uv-Lock-Installation.
Der JS-Installationsversuch ergänzte lokal Platzhalter in pnpm-workspace.yaml;
diese allein durch den Versuch erzeugte Änderung wurde auf den unveränderten
Basisstand zurückgesetzt. Es wurden keine Build-Skripte freigegeben und keine
Dependency-Dateien in den Vorschlag aufgenommen. Ein vollständiger JS-Gate-Pass
liegt nicht vor. Der Fehler stammt aus dem installierten Dependency-Setup, nicht
aus einer ausgeführten Zählerprüfung.

Dieser Auditbericht beschreibt lokale Ergebnisse; GitHub-CI und CODEOWNERS-Review
sind nicht ausgeführt. Er ist keine menschliche Freigabe.

Die Tabelle oben beschreibt den ersten Lauf mit der damaligen CLI-Form
(`--strict`, optionales `--input-v18`). Sie wird nicht rückwirkend als Lauf der
zweimodigen CLI ausgewiesen.

## Folgelauf 2026-10-13: Prüfumfang und Intake-Navigation

Der Folgepatch entfernt das wirkungslose `--strict`, verlangt genau einen
ausdrücklich gewählten Prüfumfang und ersetzt die rohe Teilstringzählung der
Intake-Zeile durch eine Tabellenzeilen- und Linkzielprüfung.

**Umgebung:** flüchtiger Linux-Container, Python 3.13 als `/usr/bin/python3`,
Node 22 mit `pnpm` 10.33.0 unter `/opt/node22/bin/pnpm`, flacher Klon von
`fleksible/entaengelment-` auf `a7773db68d97dbd8271b0921d011934d2e921170`, darauf
`entaENGELment_corpus_v17_reconcile.patch` per `git apply --index` angewandt, kein
Commit. Keine Dependency-Freigabe, keine Änderung an `pnpm-workspace.yaml`,
`package.json` oder Lockfiles. `pnpm install` erzeugte nur ignorierte
`node_modules`; `pnpm turbo` legte eine `AGENTS.md` im Arbeitsbaum an, die als
Umgebungsartefakt entfernt und nicht in den Patch aufgenommen wurde.

| Befehl | Stand | Exit | Ergebnis |
|---|---|---:|---|
| `verify_counts.py --export-only` | Basis + Originalpatch + Folgepatch | 0 | `PASS_EXPORT_ONLY`, `input_v18_checked: false` |
| `verify_counts.py --input-v18 <v18-Original>` | dto. | 0 | `PASS_WITH_V18_INPUT`, echte Originalbytes `66de61ff…` |
| `verify_counts.py` ohne Umfang | dto. | 2 | CLI-Fehler, kein Status ausgegeben |
| `verify_counts.py --export-only --input-v18 …` | dto. | 2 | CLI-Fehler, kein Status ausgegeben |
| `verify_counts.py --input-v18 <fehlt>` | dto. | 1 | `missing or not a file`, kein Rückfall |
| `verify_counts.py --input-v18 <falsche Bytes>` | dto. | 1 | `byte hash mismatch` |
| `test_verify_counts.py` | dto. | 0 | 22 Fälle PASS, 1 übersprungen ohne `ENTA_V18_INPUT` |
| `ENTA_V18_INPUT=… test_verify_counts.py` | dto. | 0 | 23 Fälle PASS, kein Überspringen |
| `make verify-governance` | dto. | 0 | 15 Workflow-Verträge, Backlog, 22 VOID/UI-Zuordnungen |
| `pnpm install --frozen-lockfile` | unverändertes `main` | 0 | `ERR_PNPM_IGNORED_BUILDS` erscheint nur als Warning |
| `pnpm turbo run typecheck lint build test` | unverändertes `main` | 0 | 5/5 Tasks |
| `make verify-js` | Basis + beide Patches | 0 | 5/5 Tasks, Lockfile eingefroren |
| `tools/metatron_check.py` < PR-Body | PR-Body des Pakets | 0 | FOKUS-Marker erkannt |
| `claim_lint.py --scope docs/intake,docs/audit` | Basis + beide Patches | 0 | WARN, nicht blockierend |
| dieselbe Prüfung mit `--strict` | dto. | 1 | 420 Treffer, davon drei Dateien aus diesem Diff |
| `make verify` | dto. | — | **nicht validiert**, siehe unten |

Der frühere Befund `make verify-js BLOCKED` ist in dieser Umgebung nicht
reproduzierbar: `ERR_PNPM_IGNORED_BUILDS` ist hier eine Warnung, nicht ein
Abbruch, und das Turbo-Gate läuft auf dem unveränderten `main` ebenso durch wie
auf dem gepatchten Stand. Der Befund wird damit als umgebungsabhängig
eingeordnet, nicht als Eigenschaft des Repositories oder dieses Diffs. Welche
Ursache die abweichende lokale pnpm-Konfiguration hatte, ist hier nicht geprüft.

`make verify` konnte nicht validiert werden. Das hier verfügbare `pytest` stammt
aus einer separaten uv-Tool-Installation ohne PyYAML; `tools/workflow_posture_check.py`
ruft bei fehlendem Import `sys.exit(2)` auf Modulebene auf, was die gesamte
pytest-Collection mit `INTERNALERROR` abbricht statt eine Datei zu überspringen.
Als CLI läuft dasselbe Werkzeug im Governance-Gate fehlerfrei. Der Befund ist
vorbestehend und nicht Teil dieses Folgepatchs; eine geeignete Umgebung und ein
importierbares CLI brauchen eine gesonderte Prüfung, und ein blosses
`raise ImportError` behebt weder die fehlende Abhängigkeit noch führt es ohne
weitere Behandlung zu übersprungenen Tests.

Die Treffer von `claim_lint.py` in diesem Paket sind Stichwortfehlalarme auf
`verify`, `require` und `requires` — Befehlsnamen, ein Python-Funktionsname und
Prosa über Gates, keine ungetaggten Behauptungen. Eine künftige Umstellung dieses
Gates auf `--strict` scheitert daran an Benennungen, nicht an Claim-Disziplin.

**Beobachtungsstand der Quellenanker.** Der Vergleich gegen das echte
materialisierte v18-Artefakt ist in diesem Folgelauf erneut ausgeführt: die
vorgelegte Datei trägt den festgehaltenen Hash `66de61ff…`, und der direkt
rekonstruierte Indexvergleich bestand. Die synthetischen Fälle in
`test_verify_counts.py` prüfen denselben Codepfad reproduzierbar ohne privates
Original; sie ersetzen diesen Lauf nicht. Die v17-Originalbytes waren in diesem
Folgelauf nicht erneut verfügbar; ihr erneuter Bytevergleich bleibt **UNOBSERVED**.
Der v17-Quellenanker stützt sich auf den beim ursprünglichen Einlesen festgehaltenen
Hash. Das ist keine Aussage, dass die Bytes auch damals unbeobachtet waren.

Fachliche Korpusdaten, beide Originalhashes, historische Zähler und Quellstände
sind unverändert. Geändert sind der Verifier, die neue Testdatei, die verlinkte
Intake-Zeile, die betroffenen Prüfhinweise in README/WORKFLOW/EXPORT, dieser
Abschnitt und die technischen Paketverweise in `manifest_files` und `MANIFEST.json`.
Ausstehende GitHub-CI bleibt eine ausstehende Prüfung; eine menschliche Zustimmung
ersetzt ihr Ergebnis nicht.
