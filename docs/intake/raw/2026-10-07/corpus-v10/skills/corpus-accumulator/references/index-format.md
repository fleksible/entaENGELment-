# Indexformat v0.1 mit optionalen Vergleichsfeldern

Verwende eine Markdown-Datei mit lesbarem Laufüberblick und genau einem JSON-Block für den wiederaufnehmbaren Stand. Erhalte alte Einträge; fasse lange Historien nur mit unverändert zugänglichen Originalreferenzen zusammen. Verwende echte Werte statt ausgedachter Beispiele. Die folgenden Feldbeschreibungen sind Schemahinweise, keine Beobachtungsdaten.

## Kopf und Stand

- Titel: `entaENGELment · Korpusindex`
- Rolle: `generated_index`; Status: `DERIVED / REVIEW-PENDING`
- Scope: aktivierte Quellen und genaue Projektgrenzen, ausdrücklich ausgeschlossene Räume.
- Letzter gesicherter Lauf: Zeitpunkt, Anzahl und tatsächlich erfasster Umfang. Der Index enthält vor dem Write den vorgesehenen Laufzeitpunkt; bestätige Speichern nur aus dem Schreibresultat.
- Lücken: nicht verfügbare Chatverläufe, ungeprüfte Links, begrenzte Suchabdeckung.
- Kurzübersicht: neue Einträge, Revisionen, offene Lesefortsetzungen und Konflikte.

## JSON-Felder

```json
{
  "schema_version": "0.1",
  "artifact_role": "generated_index",
  "authority": "DERIVED",
  "review_status": "REVIEW-PENDING",
  "scope": [],
  "run": {"started_at": null, "run_id": null, "mode": "bounded-intake"},
  "discovery": [],
  "entries": [],
  "relations": [],
  "excluded_source_ids": [],
  "gaps": []
}
```

## Eintrag je Quellversion

- `source_id`, `source_space`, `title`: exakte Identität; Quellraum Library/Drive/GitHub/Chat.
- `source_version`: echte Versions-ID; sonst `null`.
- `observed_modified_at`, `observed_size_bytes`: zurückgegebene Metadaten oder `null`.
- `version_reliability`: `version_id`, `provisional`, `unknown`.
- `source_kind`: original, summary, export, metadata; unabhängig vom Lesestand.
- `read_state`: `DISCOVERED`, `PARTIAL`, `READ_COMPLETE`, `RETRY`.
- `read_ranges`: tatsächlich gelesene Zeilen/Seiten; `next_read`: vom Dienst zurückgegebene Fortsetzung oder konkrete nächste Stelle.
- `first_seen_at`, `last_checked_at`: reale Beobachtungszeitpunkte.
- `intake_status`: Liste aus RAW/DERIVED/HOLD; `hold_reasons`: Gründe.
- `receipt`: kompakte Ausgabe aus corpus-gate einschließlich Writeback-Grenze.
- `points`: Liste mit Aussage, lokalem Tag, Originaltag soweit vorhanden, Belegstelle und Prüfgrenze.
- `errors`: Fehler/Unsicherheiten mit Zeitpunkt; leere Liste falls keine.

Führe bei unvollständiger Lektüre keine source-weite Inhaltszusammenfassung als vollständig ein. `READ_COMPLETE + HOLD` ist zulässig: Der Text ist gelesen, die Behauptung weiter ungeklärt. `RAW` heißt nicht falsch.

## Suche und Relationen

Speichere pro Suchdurchlauf Quellraum, tatsächliche Query, Filter, Sortierung, nächsten Cursor und Zeitpunkt. Markiere Suchabdeckung stets als begrenzt, bis eine vollständige Inventur belegt ist. Ein Nulltreffer beweist keine Abwesenheit.

Verknüpfe Relationen mit zwei konkreten Quellversionen und den betroffenen Belegstellen. Halte Typ, Begründung und Status `proposed` oder `compared` fest; eine Relation erhöht keine epistemische Autorität.

## Optionale Vergleichsfelder

Ergänze bei bearbeiteten Einträgen additive Felder, ohne bestehende Schlüssel umzudeuten:

- `source_family`, `parent_refs`: belegte Herkunftsfamilie und Elternanker; unknown/null zulassen.
- `contact_stage`: PRE_CONTACT, POST_CONTACT, UNKNOWN; mit Beleg und relativ zu welchem Kontakt.
- `event_evidence`, `event_at`, `source_modified_at`, `observed_at`: Ereignisbeleg und getrennte Zeitachsen; keine erfundenen Zeiten.
- `independence_basis`: bestätigte Gemeinsamkeiten, offene Abhängigkeiten und Grenzen.
- `delta_kind`: new_file, new_version, new_wording, new_operation_candidate, status_drift, no_substantive_delta.
- `precision_comparison`: ältere/aktuelle Anker, Scope, erhaltene Pflichtfelder, Ergänzungen, Regressionen, Entscheidung REUSE/EXTEND/KEEP_BOTH/HOLD.
- `implementation_state`, `validation_state`: nur belegte Zustände; unbekannt bleibt unbekannt.
- `human_action_scope`, `human_readback_status`: autorisierte Handlung gegenüber Bedeutungsprüfung getrennt.

Ein neuer Lauf darf unberührte Bestandszeilen ohne diese Felder belassen. Unterscheide „nicht erfasst“ von „geprüft und leer“. Ein Quellenfamilienlink ist keine Lösch- oder Merge-Anweisung.
