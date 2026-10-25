# tesser3TAKT Re-Entry — Referenz

## 1. Paketaufbau (RO-Crate 1.2)

```
out/reentry/<id>/
├── ro-crate-metadata.json   # JSON-LD, conformsTo https://w3id.org/ro/crate/1.2
├── REENTRY.md               # Kurzfassung für den Wiedereinstieg
├── savestate.json           # normalisiertes Manifest + claim_audit + input_hashes + git
├── payload/
│   ├── cards/reentry_vector.json   # Kartenformat von tools/verify_cards.py
│   ├── <repo-relativer Pfad>       # kopierte Repo-Quellen
│   ├── external/<datei>            # kopierte Quellen außerhalb des Repos
│   └── notes/…                     # kopierte Memory-Notizen
└── SEAL.json                # SHA-256 je Datei, state_fingerprint, HMAC oder UNSIGNED
```

Abbildung im Graph: Aussagen sind `Claim`-Entitäten (`keywords` = Tag,
`creativeWorkStatus` = Status, `isBasedOn` = Quellen); der Save-Vorgang ist eine
`CreateAction` mit `instrument` = `tools/reentry_crate.py@<commit>`; entfernte Quellen
(Drive, DOI, URL) sind `CreativeWork`-Kontextentitäten, keine Dateien im Paket.

Verify meldet `HOLD` in diesen getesteten Fällen (`tests/unit/test_reentry_crate.py`):
geänderte, fehlende oder nachträglich hinzugefügte Datei (auch gleichnamig `SEAL.json` in
Unterordnern — ausgenommen ist nur das Siegel im Paketwurzelverzeichnis), abweichender
`state_fingerprint`, ungültige, fehlende oder formal falsche HMAC-Signatur, fehlende
RO-Crate-Pflichtteile, `File`- oder `hasPart`-Einträge ohne gültige String-`@id` bzw.
außerhalb des Crates, Symlinks ohne Dateiinhalt (etwa auf Verzeichnisse, deren Inhalt sonst
am Siegel vorbeiliefe), JSON-Dateien mit falscher Objektform, ungültige
`reentry_vector`-Karte — und mit `--require-signed` auch bei
UNSIGNED oder ohne prüfenden Schlüssel. Das ist kein Beweis gegen jede denkbare
Manipulation: Ein vollständig neu geschriebenes UNSIGNED-Paket kann sich selbst wieder
konsistent versiegeln.

**Quellhashes:** Für lokale Quellen (`path`) wird ein angegebener `sha256` vor dem
Anlegen des Ziels gegen die Datei geprüft (Abweichung → Abbruch) und nach dem Kopieren
erneut abgeglichen; Ergebnis in `input_hashes`. Für entfernte Quellen (`uri`) bleibt ein
angegebener `sha256` eine ungeprüfte Angabe in `declared_hashes` (im Brief markiert).

## 2. Vokabular

**Claim-Arten (`tag`)** — Projekt-Tags und Save-State-/Receipt-Vokabular:

| Gruppe | Werte |
|--------|-------|
| claim_lint | FACT, HYP, MET, TODO, RISK |
| EPISTEMIC_HYGIENE | MODEL, HYPOTHESIS, METAPHOR |
| Save State / Receipt | FAKT, BEOBACHTUNG, REKONSTRUKTION, INFERENZ, MODELL, HYPOTHESE, METAPHER, GUARD, VOID, CLAIM, POESIE, SPEC, KORPUSBEFUND, EXTRAPOLATION |

**Status (`status`, `authority`)**: DERIVED, REVIEW-PENDING, HOLD, UNRESOLVED, VERIFIED,
RETRACTED. Default für `authority`: REVIEW-PENDING.

**Promotion (`promotion_status`)**: NO_CANON_PROMOTION (Default) oder REVIEW_REQUESTED.
Kanonisierung passiert nie im Save State selbst.

`save` bricht ab (fail-closed) bei: unbekannten Feldern auf oberster Ebene und in
`sources[]`, `claims[]`, `next_actions[]`, `lineage`, `lineage.nodes[]`, `lineage.edges[]`;
falschen Containertypen (z. B. `sources` als Mapping, `paths` als String); Werten
außerhalb des Tag-, Status- oder Promotion-Vokabulars; Kanten auf unbekannte Knoten.

## 3. Basic-Memory-Konvention (lebendes Gedächtnis zwischen Save States)

[MODEL] Basic Memory speichert Notizen als Markdown; Beobachtungen stehen als
`- [kategorie] Inhalt #tag`, Relationen als `[[Wikilinks]]`. Konvention für dieses Projekt:

- **Kategorie = Claim-Art** (Metapher und Messbehauptung bleiben getrennt).
- **Tag = Status** als `#status-derived`, `#status-hold`, `#status-unresolved` …
- **Quelle** als Tag `#src-<id>` (gleiche IDs wie im Manifest).
- **Relationen** benennen die Art der Kopplung, nicht nur „related“.

```markdown
---
title: tesser3TAKT – Skaleninvarianz
tags: [tesser3takt, savestate]
---
# tesser3TAKT – Skaleninvarianz

## Observations
- [MODELL] Formähnlichkeit statt Identität über Skalen #status-derived #src-savestate-0715
- [METAPHER] Segel als indirekte Lesbarkeit #status-derived
- [HYPOTHESE] Reentry-Pflicht verhindert Perspektiv-Drift #status-unresolved

## Relations
- crosswalk_not_identity [[VA-P1 Phase Linear]]
- requires_receipt [[Governance Consent Receipt Verify]]
```

Ablage: eigenes Basic-Memory-Projekt **außerhalb** des öffentlichen Repos (z. B.
`~/basic-memory/tesser3takt`). In einen Save State gelangen Notizen nur über `notes:` —
dann landen sie im privaten Crate unter `payload/notes/`.

## 4. Ältere Save States (Drive)

Frühere Pakete (z. B. `reentry_save_state_v1`, Receipt-JSONs mit `input_hashes`) als
`uri`-Quelle mit `sha256` referenzieren; die Feldnamen `authority`, `known_losses`,
`next_allowed_action`, `frozen_state`, `floating_problem`, `next_actions` sind
kompatibel übernommen.
