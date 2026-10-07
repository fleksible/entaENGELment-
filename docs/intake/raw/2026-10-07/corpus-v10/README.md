# Korpusstand · 7. Oktober 2026

**DERIVED / REVIEW-PENDING · Intake `raw` · generated_index_snapshot**

[FAKT] Öffentlicher Projekt-Snapshot aus Version 10 des privaten Korpusindex.
Der Export umfasst alle 63 erfassten Quellen und 11 offenen Metadatenkandidaten.
Er ist ein Wegweiser zu Projektformulierungen und offenen Prüfungen. Er ist keine
neue Evidenz, kein neuer Kanon und kein vollständiges Archiv der Originaldokumente.

## Einstieg

| Datei | Verwendung |
|---|---|
| [corpus-matrix.csv](corpus-matrix.csv) | Filterbare Übersicht: 74 Dokumente/Kandidaten, Version, Lesestand, Herkunftsfamilie, nächste Lesestelle |
| [corpus-snapshot.json](corpus-snapshot.json) | Alle Indexpunkte, Belegstellen, Grenzen, Beobachtungen, Relationen und Konflikte |
| [WORKFLOW.md](WORKFLOW.md) | Ziele, Bearbeitungsfolge, Kategorien und Grenzen |
| [EXPORT.md](EXPORT.md) | Herkunft, bekannte Inkonsistenzen und Transfergrenzen |
| [MANIFEST.json](MANIFEST.json) | SHA-256 der Exportdateien und unveränderten Skill-Kopien |
| [skills/corpus-gate/SKILL.md](skills/corpus-gate/SKILL.md) | Herkunft und Claim-/Intake-Prüfung v0.2 |
| [skills/corpus-accumulator/SKILL.md](skills/corpus-accumulator/SKILL.md) | Begrenzte Erschließung und Fortsetzung v0.2 |
| [skills/complementarity-review/SKILL.md](skills/complementarity-review/SKILL.md) | Kleine Entscheidungsfläche und Gegenlesart v0.2 |

Die Skill-Pakete sind unveränderte archivierte Kopien mit Referenzen, UI-Metadaten
und Icons. Diese Ablage installiert keinen Skill, richtet keine Automation ein und
aktiviert keine Datenquelle. Die im Paket beschriebene Library-Abhängigkeit ist
hostabhängig und wird nicht mitgeliefert.

## Erfasster Stand

| Kennzahl | Anzahl | Bedeutung |
|---|---:|---|
| Indexierte Quellen | 63 | Im Index erfasste Dokumente, nicht unabhängige Belege |
| READ_COMPLETE | 56 | Vom Index gemeldete vollständige Textlektüre |
| PARTIAL aktiv | 5 | Offene Fortsetzung |
| PARTIAL zurückgestellt | 2 | Generierte Research-Radar-Berichte; keine neue Evidenz |
| DISCOVERED | 11 | Nur Metadaten; keine Inhaltslektüre |
| Indexpunkte | 192 | Aussagen mit dokumentierten Grenzen; historische Tags erhalten |
| Relationen / Konflikte | 38 / 5 | Aus dem Index übernommen; keine neue Bestätigung |

Bei diesem Export wurden die Originalquellen nicht erneut gelesen. `READ_COMPLETE`
ist ausdrücklich kein wissenschaftlicher, visueller oder Runtime-Validierungsstatus.
Quellversionen ohne tatsächliche Versions-ID bleiben vorläufig markiert.

## Dokumentmatrix

Die lokalen `doc-…`-IDs sind Navigationsanker. Exakte Quell-IDs und Versionsmarker
stehen in JSON/CSV; private Quellen sind dadurch nicht öffentlich abrufbar.

| Lokale ID | Dokument | Lesestand | Nächste Zeile |
|---|---|---|---:|
| doc-c109ee67f3f3 | entaENGELment_Save_State_2026-09-26.md | READ_COMPLETE | — |
| doc-67acd0f788b8 | entaENGELment_Research_Radar_2026-09-25.pdf | PARTIAL | 46 |
| doc-f01460f009f2 | entaENGELment_Research_Radar_2026-09-18.pdf | PARTIAL | 46 |
| doc-924d99f5c819 | Forensische_Genealogie_v2_5.md | READ_COMPLETE | — |
| doc-a6feed699526 | Handoff_SOL_v2_5.md | READ_COMPLETE | — |
| doc-deb7499ef8a9 | ANALYSE_v3_2_entaENGELment_Tiefenanalyse.pdf | READ_COMPLETE | — |
| doc-5c468ffe7dc3 | ANALYSE_v3_2_entaENGELment_Tiefenanalyse.docx | READ_COMPLETE | — |
| doc-e430d546135a | entaENGELment_Figma_Core_Loop_Reentry_Package.md | READ_COMPLETE | — |
| doc-aa1fa2ef0dee | grimm-apparat-crosswalk-v0-1(1).md | READ_COMPLETE | — |
| doc-96d2ab1ddffa | grimm-apparat-crosswalk-v0-1.md | READ_COMPLETE | — |
| doc-1187cadc1fe1 | VOID-024_block.yaml | READ_COMPLETE | — |
| doc-f9e3d8fb7322 | entaENGELment_Vorschlagsartefakt_2026-07-29.md | READ_COMPLETE | — |
| doc-881652917ec5 | entaENGELment_Save_State_2026-07-25.docx | READ_COMPLETE | — |
| doc-4354923b6fdc | Synthbiosis_Empatheia_Universalisis_Paper-2.pdf | READ_COMPLETE | — |
| doc-f887c5094928 | Synthbiosis_EntaENGELment_Tiefenanalyse_v3_2.pdf | READ_COMPLETE | — |
| doc-ad3854ed16c9 | Synthbiosis_EntaENGELment_Tiefenanalyse_v3_2.docx | READ_COMPLETE | — |
| doc-d04b85f5d800 | von_Franz_x_Grimm_Apparat_Spiegelung.md | READ_COMPLETE | — |
| doc-730332d0630f | tesser3takt_monade_annotiert_update_2026-02-06_REVIEWER_SAFE_v3.pdf | READ_COMPLETE | — |
| doc-e149e3e2d6cd | Synthbiosis_EntaENGELment_lineage_graph.json | READ_COMPLETE | — |
| doc-c609886edc8d | Synthbiosis_EntaENGELment_lineage_graph(1).json | READ_COMPLETE | — |
| doc-fb0884b913cf | EntaENGELment_Graphen_Skalen_Uebergangsgrammatik_v0_1(4).pdf | READ_COMPLETE | — |
| doc-d783f089a4f6 | borromean_projection_manifest_v0_1.example.json | READ_COMPLETE | — |
| doc-dbe60ee34b98 | grimm_narration_2_save_state_handoff(2).docx | READ_COMPLETE | — |
| doc-580fb8f70dd5 | ASTRA_HOLISTIC_READ_MODEL_v0_1_2026-09-13.md | READ_COMPLETE | — |
| doc-efa515bb5e6e | EntaENGELment_Graphen_Skalen_Uebergangsgrammatik_v0_1(3).pdf | READ_COMPLETE | — |
| doc-fb31b6e1848b | Grimm_Narrativ_2_0_Konzeptpapier(2).docx | READ_COMPLETE | — |
| doc-edc761de5317 | CHAT_SOLUTION_RECOVERY_RUN_v0_2_DELTA_MERGE.md | READ_COMPLETE | — |
| doc-3465c34a699f | grimm_narration_2_save_state_handoff(1).docx | READ_COMPLETE | — |
| doc-cedbf5bdbd9a | grimm_apparat_2_0_save_state_red_team_handover.pdf | READ_COMPLETE | — |
| doc-b8febc4435cd | grimm_apparat_2_0_save_state_red_team_handover.docx | READ_COMPLETE | — |
| doc-2e13447b83dd | grimm_apparat_2_0_save_state_red_team_handover_mit_kielzeichnung.docx | READ_COMPLETE | — |
| doc-b4aea3437aea | grimm_apparat_2_0_save_state_red_team_handover_mit_kielzeichnung-1.docx | READ_COMPLETE | — |
| doc-1fd1cc1bebcb | grimm_apparat_2_0_save_state_red_team_hardened_v0_3.docx | READ_COMPLETE | — |
| doc-c844ce6b73e6 | grimm_apparat_2_0_save_state_red_team_hardened_v0_3(1).docx | READ_COMPLETE | — |
| doc-17996c245840 | Samstagsessay_X_zn7u_2026-10-03.md | READ_COMPLETE | — |
| doc-5ea4f87b177a | Chatvergleich_Tunneln_MetaGrammatik_2026-10-03.md | READ_COMPLETE | — |
| doc-3e90b574e98e | 01_STRAND_MANIFEST_MAERCHEN_SAGA.md | READ_COMPLETE | — |
| doc-c4e960d15efe | entaENGELment_save_state_2026-07-08.docx | READ_COMPLETE | — |
| doc-35b2c1624c0b | entaENGELment_save_state_2026-07-08(1).docx | READ_COMPLETE | — |
| doc-a31b781252ec | Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_2.docx | READ_COMPLETE | — |
| doc-7133f83b2f3f | EntaENGELment_Komplementaritaets_Resonanz_Updatefassung.pdf | READ_COMPLETE | — |
| doc-b93cdeca99c7 | grimm_narration_2_save_state_handoff.docx | READ_COMPLETE | — |
| doc-339898458b2e | Grimm_tesser3TAKT_Save_State_2026-07-09.docx | READ_COMPLETE | — |
| doc-d3f0bcf9a99e | Lyra_Ausgangsreceipt_und_Drei_Anschlag_Pruefblatt_2026-10-05.md | READ_COMPLETE | — |
| doc-f785477e0359 | Lyra_Ausgangsreceipt_und_Drei_Anschlag_Pruefblatt_2026-10-05_v0.2.md | READ_COMPLETE | — |
| doc-000bd0da0f43 | Lyra_Jazz_POV_S_Stichwortabgleich_2026-10-04.md | READ_COMPLETE | — |
| doc-a8648093582c | Kreuzung_Lyra_Jazz_POV_S_2026-10-05.md | READ_COMPLETE | — |
| doc-b2eca42c0429 | entaENGELment_SAVE_STATE_2026-10-04.pdf | READ_COMPLETE | — |
| doc-08d6d0bdd379 | entaENGELment_SaveState_ReEntry_v1.pdf | READ_COMPLETE | — |
| doc-5b5aa6695900 | entaENGELment_SAVE_STATE_2026-10-04.docx | READ_COMPLETE | — |
| doc-d519ca0978da | entaENGELment_SaveState_ReEntry_v1.docx | READ_COMPLETE | — |
| doc-4ee21fcdcbd8 | Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_0.docx | PARTIAL | 961 |
| doc-20448581f742 | Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_0(2).docx | PARTIAL | 241 |
| doc-5e9c56267d05 | Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_1.docx | PARTIAL | 241 |
| doc-fbf3221d393a | ANALYSE_PROMPT_v3_2_Strukturmeissel_entaENGELment_2026-07-12.docx | PARTIAL | 241 |
| doc-5bfa6ac2327c | EntaENGELment_Komplementaritaets_Resonanz_Updatefassung(1).pdf | READ_COMPLETE | — |
| doc-88116e5e33d9 | grimm_apparat_2_0_save_state_red_team_handover(1).docx | READ_COMPLETE | — |
| doc-70dde1e94c4e | EntaENGELment_Komplementaritaets_Resonanz_Updatefassung(1).docx | READ_COMPLETE | — |
| doc-bc3631da95a3 | grimm_apparat_2_0_save_state_red_team_handover_mit_kielzeichnung-1(1).docx | READ_COMPLETE | — |
| doc-c1f6c9a42d31 | grimm_apparat_2_0_save_state_red_team_handover(1).pdf | READ_COMPLETE | — |
| doc-83c73afd6b00 | entaENGELment_save_state_2026-07-08(2).docx | READ_COMPLETE | — |
| doc-256c894b475d | Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_0(3).docx | PARTIAL | 241 |
| doc-d77426927fa1 | grimm_apparat_2_0_save_state_red_team_hardened_v0_3(2).docx | READ_COMPLETE | — |
| doc-616cd8b35fe5 | Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_1(2).docx | DISCOVERED | 1 |
| doc-952bb22fd67d | Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_3.docx | DISCOVERED | — |
| doc-59c46100ee8c | EntaENGELment_SaveState_Skaleninvarianz_2026-07-15(1).docx | DISCOVERED | — |
| doc-31eb564a8cf6 | EntaENGELment_SaveState_Skaleninvarianz_2026-07-15(2).docx | DISCOVERED | — |
| doc-2d5ee24da05d | Zwischenzeitliches_Ganzes_tesser3TAKT_entaENGELment_SaveState_v1_2(1).docx | DISCOVERED | — |
| doc-62ec5dc091e9 | SWITCHBOARD_BAUPLAN_v0_1.md | DISCOVERED | — |
| doc-8580b64a01a7 | enta-switchboard-bauplan.html | DISCOVERED | — |
| doc-ccc226e07c29 | SWITCHBOARD_BAUPLAN_v0_2.md | DISCOVERED | — |
| doc-488c3cd86111 | entaENGELment_Figma_Core_Loop_Reentry_Package(1).md | DISCOVERED | — |
| doc-6df3bd782cba | EntaENGELment_SaveState_Skaleninvarianz_2026-07-15(3).docx | DISCOVERED | — |
| doc-cf2291080049 | Counterfactual_Genealogy_Report_2026-09-28.md | DISCOVERED | — |
