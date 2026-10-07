# Herkunft und Exportgrenzen

**DERIVED / REVIEW-PENDING · Transfer-Receipt, keine Claim-Promotion**

## Eingefrorener Eingang

[FAKT] Eingelesen wurde `entaENGELment_Korpusindex.md`, Quell-ID
`libfile_1b71e31990a88191ab9ea40acc4c71d0`, bestätigte Version **10**,
Änderungsmarker `2026-10-07T01:21:32.318881Z`, **499907 Bytes**.
SHA-256 der unveränderten Eingangsbytes:

```text
f7f3aaa4773ab073c55a7e6a7e911f4764e50a830d0c4bb3cf9153345e402a54
```

Der Hash verankert die verwendete Fassung. Er beweist weder Richtigkeit noch
semantische Vollständigkeit ihrer Aussagen. Die Originalquellen des Index wurden
für diesen Export nicht erneut gelesen; alle Angaben zu deren Inhalt bleiben
dem Index zugeschrieben. Die Originaldokumente sind nicht Teil dieses PRs.

## Transformation

1. Den einen JSON-Block aus der eingefrorenen Markdown-Datei parsen.
2. Alle 63 `entries`, 38 `relations`, 5 `conflicts`, historischen Zugangslücken
   und globalen Guards übernehmen. Historische Beobachtungen innerhalb der
   Einträge bleiben erhalten und werden nicht mit neuen Versionen verschmolzen.
3. `pending_candidates` aus den Suchbeobachtungen nach exakter `source_id`
   zusammenstellen, bereits indexierte IDs ausschließen: 11 Kandidaten.
   Sortierung für die Übersicht: Änderungsmarker, dann ID. Ein Änderungsmarker
   ist kein Entstehungs- oder Kontaktzeitpunkt.
4. Rekursiv ausschließlich folgende Schlüssel aus diesen übernommenen Bereichen
   entfernen: `file_id`, `input_file_id`, `run_id`, `recorded_before_run`,
   `writeback`, `cursor`, `cursor_used`, `next_cursor`, `page_2_cursor_used`.
5. Einträge um lokale `document_id` ergänzen: `doc-` plus erste 12 Hexzeichen von
   SHA-256 der UTF-8-`source_id`. Exakte Quell-IDs bleiben daneben erhalten.
   Lokale IDs dienen Navigation, nicht Anonymisierung oder Ursprungsbeweis.
6. Zähler aus den übernommenen Einträgen berechnen; eine CSV-Zeile pro erfasstem
   Dokument/Kandidaten erzeugen. Fehlende CSV-Werte heißen `NOT_RECORDED`,
   unbekannte Quellversionen `UNKNOWN`. Im JSON bleiben null und fehlend getrennt.
   Verschachtelte Werte stehen in CSV als JSON; Formeleinleitungen werden bei
   Bedarf mit einem Apostroph neutralisiert.

**Erhalten:** Aussagen, Belegstellen, lokale und originale Tags, genaue Quell-IDs,
Fassungsmarker, Lesebereiche, nächste Lesestellen, HOLD/UNRESOLVED, Herkunftsfamilien,
Vergleichsentscheidungen, Schutzbedingungen und frühere Beobachtungen.

**Bekannter Transferverlust:** Die Suchinventare, Cursor, Metadaten ausgeschlossener
projektfremder Medien, Laufsteuerung, globale Laufhistorie und veraltete
`index_identity` werden nicht publiziert. Damit ist der Export kein zweiter
fortschreibbarer Korpusindex und kein Wiederanlaufzustand der Erschließung.
Historische Beobachtungen verlieren ihre internen Lauf-IDs; ihre vorhandenen
Zeit-/Versionsmarker bleiben erhalten.

**Quellauslassungen:** Originalchats, Quelldateien, Bilder/Layout und externe
Referenzen waren schon im eingelesenen Index keine vollständig nachprüfbaren
Originale. Ihr Fehlen ist nicht erst durch diesen Export entstanden.

**Unübersetzter Rest:** Bedeutungstreue, historische Lesebehauptungen und
inhaltliche Vergleichsurteile bleiben unbestätigt. Die Weitergabe ist keine
verlustfreie Umkehr und kein semantischer Readback.

## Erkannte Inkonsistenzen

| ID | Befund im Eingang | Behandlung im Export |
|---|---|---|
| EXPORT-01 | Eingebettete Identität nennt Version 8; Kopf/Writeback ist gegen Version 9 vorbereitet | Bestätigte Materialisierung v10 ist der Herkunftsanker; alte Metadaten werden nicht als aktueller Speicherstatus ausgegeben |
| EXPORT-02 | Laufzähler nennt 11 zurückgestellte Sammelberichte, Einträge markieren nur 2 | Aus Einträgen berechnet: 2 zurückgestellt, 5 aktive PARTIAL, 11 DISCOVERED; Quelldatei unverändert |
| EXPORT-03 | 100 von 192 Indexpunkten verwenden Tags außerhalb der sechs corpus-gate-v0.2-Claim-Tags | Tags unverändert erhalten; keine stille Umdeutung von SPEC/GUARD/REPORTED usw.; Mapping bleibt Review-Aufgabe |

Die maschinenlesbaren Details stehen unter `export_findings` im JSON. Diese
Prüfung ist keine globale Schema-Migration des Index.

## Autorisierung, Sichtbarkeit und Rücknahme

[FAKT] Der Nutzerauftrag erlaubt die Bereitstellung auf GitHub als PR und dessen
Merge. Ziel ist das öffentliche Repository `fleksible/entaENGELment-`; Intake bleibt
`raw`, wissenschaftlicher und normativer Status bleiben unverändert.

Publiziert werden abgeleitete Projektpunkte und Projektmetadaten, die drei
Skill-Pakete sowie dieser Exportvertrag. Private Originaldokumente, persönliche
Medien, Zugangstokens und Suchcursor sind nicht enthalten. Quell-IDs sind
Herkunftsanker; sie gewähren keinen Zugriff auf die privaten Originale.

Ein Folge-PR kann einen fehlerhaften Snapshot als überholt kennzeichnen und einen
korrigierten Stand danebenstellen. Öffentliche Forks, Klone und Caches sind nicht
zuverlässig zurückrufbar. Nach Repo-Regel werden alte Artefakte nicht still
gelöscht oder umgeschrieben. Ein Widerspruch zu den eingefrorenen Eingangsbytes
oder ein nachgewiesener Guard-Verlust ist ein konkreter Falsifikator des Exports.

Die historische Aussage „Repo nicht geprüft“ innerhalb eines Eintrags bezeichnet
die damalige Quellsichtung. Der aktuelle PR prüft die Repo-Integration und CI,
validiert damit aber keine historischen Repo-/Runtime-Behauptungen im Korpus.
