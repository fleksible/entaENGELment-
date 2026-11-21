# Unabhängige Evidence-Gegenprüfung – Lean 4 / PR #478

**Datum:** 2026-11-21  
**Repository:** `fleksible/entaENGELment-`  
**PR-Head:** `0b50c4d6e284aa06cf43a03aec98ace616d1ce65`  
**Untersuchungsgegenstand:** hochgeladenes `Lean4-PR478-Evidence.zip`  
**Wirkungsgrenze:** reine Inspektion, kein Push, Merge, Claim-Promotion oder Canon-Writeback.

## Unabhängig ausgeführt

1. SHA-256 des ZIP neu berechnet: `ef036331329250a57d65b115ec9f0ca474afda50138f2ad360c59b2ac265ee68` – stimmt mit dem gemeldeten Wert überein.
2. ZIP-Integritätsprüfung: keine beschädigten Einträge. Inhalt: 65 Einträge, davon `SHA256SUMS` und 64 dokumentierte Dateien.
3. `SHA256SUMS` anhand aller Datei-Originalbytes geprüft: **64/64 korrekt**, keine fehlenden oder unaufgeführten Dateien.
4. Die sechs archivierten Quellen anhand SHA-256 und selbst berechneter Git-Blob-SHA-1 geprüft: **6/6 korrekt**. Die sechs Git-Blob-IDs anschließend mit dem verbundenen GitHub-Repository am exakten PR-Head abgeglichen: **6/6 übereinstimmend**.
5. Gesicherte Audit-stdout: **413 Bytes**. Gesicherte Audit-stderr: **0 Bytes**. Für `lake build` und `lake env lean CrosswalkProbe/Audit.lean` sind jeweils Exit-Code `0` aufgezeichnet. Die Originalausgaben sind in `raw/` enthalten.
6. Offline-Replay mit dem beigefügten `tools/read-audit.py` sowie dem aus dem PR-Head archivierten `lean_crosswalk.py` und den aufgezeichneten Originalbytes: **Exit 0, kein stderr, reproduziertes JSON bytegenau identisch zu `results/audit_raw.json`**. `unknown_lines` ist leer.
7. Die Release-Versionsangaben des Archivs nennen Lean 4.35.0 (`eb6cafb7290e8bd5f2937522d8d804f58f02bafc`). Der im Evidence-Bericht angegebene Download-Hash `7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d` wird auch von der öffentlichen SourceForge-Spiegelung dieses Lean-Releases angegeben.

## Erneut berechnete Klassifikationen

| Deklaration | `audit_raw()`-Status | Zusatzbefund |
| --- | --- | --- |
| `thm_direct_gap` | `OPEN_OBLIGATION` | `sorryAx` |
| `thm_transitive_gap` | `OPEN_OBLIGATION` | `sorryAx` |
| `thm_closed_formal` | `FORMAL_CLOSED` | Axiomliste leer (`True`, `by trivial`) |
| `thm_custom_axiom` | `HOLD_TRUST_BOUNDARY` | `CrosswalkProbe.Basic.externalAssumption` |
| `thm_mixed` | `OPEN_OBLIGATION` | Fremdaxiom in `foreign_axioms` erhalten |

## Reichweite und offene Grenzen

- Die gesicherten Prozessausgaben und Build-Artefakte sind mit einem echten Lean-Lauf konsistent und dokumentieren das Verhalten der fünf konstruierten Testdeklarationen. **Diese Gegenprüfung hat Lean nicht erneut gestartet** und kann die ursprüngliche Ausführung allein aus archivierten Dateien nicht vollständig unabhängig attestieren.
- Die eigentliche 594 MB große Toolchain-Distribution liegt nicht im Evidence-ZIP. Ihre Prüfsumme wurde im gelieferten Protokoll aufgezeichnet und mit einer extern veröffentlichten Prüfsumme verglichen, aber nicht aus der Binärdistribution unabhängig neu berechnet.
- Der Nachweis ist keine allgemeine Validierung des Parsers für beliebige Lean-Ausgaben und keine semantische Prüfung menschlicher Behauptungen.
- Es gibt weiterhin keine automatisch an die reale Lean-Ausgabe gebundene, vollständig geprüfte Karten-Provenienzkette. Der Schritt `audit_raw()` und der Nachweis der Originalbytes sind dokumentiert; eine gesonderte Belegbindung der erzeugten Karten bleibt offen.
- Die Evidence-Dateien wurden in dieser Prüfung **nicht** in PR #478 hochgeladen. Die im PR enthaltene frühere Kennzeichnung `NOT_RUN` beschreibt daher noch den unveränderten PR-Stand.

**Fazit:** Evidence-Kapsel intern konsistent, beim Quellstand verankert und im Python-Auswertungsteil offline reproduzierbar. Der reale Lauf ist durch nachvollziehbare Artefakte belegt; keine semantische Claim-Promotion. Vor einem Merge sollten Evidence-Receipt und Archiv im PR nachvollziehbar referenziert und die verbleibenden Grenzen vom Owner bewertet werden. **ANNEX / SPEC-WIP / HOLD bleibt vorerst bestehen.**
