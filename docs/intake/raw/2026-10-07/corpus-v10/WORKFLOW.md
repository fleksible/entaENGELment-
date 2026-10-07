# Korpusarbeit: Workflow, Kategorien und Ziele

**MODELL / Arbeitsvertrag · DERIVED / REVIEW-PENDING**

Diese Übersicht verbindet die drei mitgelieferten Skills mit der vorhandenen
Intake-Struktur. Sie legt keinen zusätzlichen Aufgabenbestand und keine neue
Automation an. Der öffentliche Snapshot ist ein fester Review-Stand; fortlaufende
Lektüre und Suchcursor bleiben im bestehenden privaten Index.

## Bearbeitungsfolge

| Schritt | Eingang → Ergebnis | Grenze / Abbruch |
|---|---|---|
| Laden | Konkreter Index + bestätigte Version → Ausgangsstand | Lesefehler erzeugt keine Ersatzkopie |
| Finden | Projektbezug + höchstens 2 Suchseiten → Kandidaten | Suchtreffer ist keine Inhaltslektüre |
| Lesen | Maximal 12 Quellen / 24 Abschnitte → genaue Bereiche | Mindestens 2 Plätze für älteste offene Quellen; Versionswechsel beginnt neu |
| Einordnen | Passage + Herkunft → corpus-gate-Receipt | UNKNOWN, RAW/DERIVED/HOLD und Originaltags erhalten |
| Vergleichen | Neue Formulierung + konkret gelesene Vorarbeit → REUSE/EXTEND/KEEP_BOTH/HOLD | Kein Guard-Verlust, keine Unabhängigkeit aus Kopien |
| Sichern | Beobachtungen + Fortsetzungen → derselbe Index | Versionsschutz; bei Konflikt erneut lesen; Erfolg erst nach bestätigtem Speichern |
| Diskutieren | Höchstens 3 Fragen / 6 Quellen → kleine Review-Karten | Vorschlag, menschlicher Entscheid, Code und ausgeführter Test getrennt |
| Veröffentlichen | Autorisierter konkreter Export → Intake-PR | Privacy-Prüfung und grüne CI; Merge ist keine Kanonisierung |

## Kategorien getrennt führen

| Dimension | Beispiele | Nicht daraus ableiten |
|---|---|---|
| Lesestand | DISCOVERED, PARTIAL, READ_COMPLETE, RETRY | wissenschaftliche Richtigkeit |
| Intake | RAW, DERIVED, HOLD | wahr/falsch oder Produktionsreife |
| Aussage | FAKT, MODELL, HYPOTHESE, METAPHER, ANALOGIE, UNRESOLVED | Gesamtqualität des Dokuments |
| Herkunft | source_family, parent_refs, contact_stage, independence_basis | unabhängige Entstehung allein aus verschiedenen Chats/Modellen |
| Delta | new_file, new_version, new_wording, new_operation_candidate, status_drift, no_substantive_delta | kausal bewiesene Emergenz |
| Umsetzung | Vorschlag → normative Entscheidung → Implementierung → ausgeführte Validierung | dass ein späterer Schritt schon erledigt sei |

Historische Index-Tags außerhalb des oben vorgesehenen Vokabulars bleiben im
Snapshot sichtbar; siehe EXPORT-03. Die Tabelle beschreibt den Skill-Vertrag,
nicht die Behauptung einer bereits abgeschlossenen Migration.

## Ziele und überprüfbarer Abschluss

| Ziel | Ausgangsstand dieses Snapshots | Nächste erlaubte Prüfung | Abschlusskriterium |
|---|---|---|---|
| Leselücken schließen | 5 aktive PARTIAL, 11 DISCOVERED | Älteste offene Quelle derselben Version ab gespeicherter Stelle lesen | Vollständigkeit durch reale Abschnitte und Endmarker belegt |
| Herkunft präzisieren | 10 Einträge ohne source_family | Nur bei erneuter Bearbeitung Elternanker und Kontaktbezug prüfen | Belegter Bezug oder begründetes UNKNOWN; keine Globalmigration |
| Guard-Verlust verhindern | 38 historische Relationen, 5 Konflikte | Pro Aussage Input/Output, Guard, Falsifikator, Verlust, Rest und Rücknahme vergleichen | Konkrete REUSE/EXTEND/KEEP_BOTH/HOLD-Entscheidung mit Ankern |
| Indexkonsistenz verbessern | EXPORT-01 bis EXPORT-03 offen | Veraltete Metadaten, Zähler und Tag-Vokabular am Originalindex prüfen | Separat nachvollziehbare Korrektur ohne Statuspromotion |
| Integration prüfen | Dieser öffentliche Intake-Snapshot | Dateiintegrität, Grenzen, Repo-Gates und PR-Checks | Autorisierter Merge bei grünen Prüfungen |

Das Schließen einer Leselücke erhöht keine wissenschaftliche Autorität.
Die zwei zurückgestellten Research-Radar-Berichte bleiben Wegweiser; alle
generated_index/generated_review-Artefakte und ihre Kopien sind von erneutem
Import als unabhängige Evidenz ausgeschlossen.

## Dienste passend zur konkreten Frage

- GitHub verwaltet diesen versionierten Review-Stand und vorhandene Code-/Spec-Anker.
- Die Library bleibt der Zugang für die privaten Projektoriginale und den laufenden Index.
- Wolfram kommt für konkret definierte endliche Regeln/Formalmodelle infrage;
  Hugging Face für ausdrücklich beauftragte Passage-/Modellsuche.
- Supabase oder weitere Plugins erhalten durch diesen PR keinen Datenbestand,
  Upload, neuen Scope oder zusätzliche Berechtigungen.

Diese Rollen beschreiben mögliche Arbeitswege, keine bestätigten Integrationen.
Verfügbarkeit und konkreter Scope müssen jeweils durch tatsächlichen Zugriff
belegt werden. Der Skill allein läuft weder im Hintergrund noch erkennt er,
ob die App gerade benutzt wird.
