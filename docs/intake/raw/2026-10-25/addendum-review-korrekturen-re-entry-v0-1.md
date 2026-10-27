# Addendum: Review-Korrekturen zum Re-Entry-Erststand (v0.1)

**Stand:** 2026-10-25 · **Status:** [INTAKE] REVIEW-PENDING · NO_CANON_PROMOTION
**Bezug:** INTAKE-2026-10-25-001, INTAKE-2026-10-25-002, versiegelter Erststand
`docs/intake/raw/2026-10-25/reentry/2026-10-25_research-connectoren-reentry/`
**Anlass:** Review zu PR #427 vom 2026-10-25 (vom Owner bereitgestellt).

> Korrektur als Nachtrag, nicht als Neuversiegelung: Der Erststand bleibt bytegleich
> und datiert erhalten.

---

## 1. Korrekturen am Werkzeug (`tools/reentry_crate.py`, PR #427)

| # | Befund im Review | Korrektur | Nachtest |
|---|------------------|-----------|----------|
| 1 | Jede Datei namens `SEAL.json` war von der Siegelliste ausgenommen | Ausgenommen ist nur noch das Siegel im Paketwurzelverzeichnis | Nachträgliches `payload/SEAL.json` → HOLD; gleichnamige Quelle wird gehasht |
| 2 | Vorgegebener `sources[].sha256` wurde still durch den berechneten Wert ersetzt | Lokale Quelle: Vorgabe wird vor Zielanlage geprüft (Abweichung → Abbruch), Kopie wird erneut abgeglichen; `uri`-Hashes bleiben als `declared_hashes` getrennt | Falsche Vorgabe → Abbruch ohne Ziel; richtige bleibt; fehlende wird berechnet |
| 3 | Unbekannte Felder in Unterobjekten wurden still verworfen | Geschlossene Schlüsselmengen und Typprüfung für `sources[]`, `claims[]`, `next_actions[]`, `lineage` (+ Knoten/Kanten) | Je Unterobjekt ein Tippfehler- und ein Typfall → Abbruch ohne Ziel |
| 4 | Erfolgreiches `brief` gab Authenticity und Warnungen nicht aus | Prüfergebnis auf stderr, Brief allein auf stdout; Skill verlangt die wörtliche Nennung | UNSIGNED, SIGNED_UNCHECKED, SIGNED_VALID, falscher Schlüssel, `--require-signed` |
| 5 | Fehlendes Signaturfeld galt als SIGNED_UNCHECKED; falsche JSON-Formen warfen Ausnahmen | Signatur muss exakt `UNSIGNED` oder `0x` + 64 Hex sein; Objektformen werden vor Zugriff geprüft; `File`-@id außerhalb des Crates → HOLD | Fehlend/leer/kurz/Zahl/klein geschrieben → HOLD; `[]`-Formen → strukturiertes HOLD |

## 2. Formulierungen, an den Beleg gebunden

- **Erststand, Aussage #1** („Manipulation führt zu HOLD“): Sie gilt nur für die damals
  getesteten Fälle. Die Lücken 1, 2 und 5 bestanden zu diesem Zeitpunkt.
- **Erststand, Aussage #3, und Prüfprotokoll §4** („arXiv MCP … unbedenklich“ / ✅): Der Beleg
  trägt nur die Aussage „im statisch gelesenen Umfang keine weitere Auffälligkeit gefunden“.
  Es gab keine Installation, keine Laufzeitbeobachtung und keine rekursive
  Abhängigkeitsprüfung. Sinngemäß gilt das auch für „mit Einstellung nutzbar“ bei Basic
  Memory und Zotero MCP.

## 3. Erststand bleibt unverändert

- Versiegelt, `verify` weiterhin PASS / UNSIGNED, auch mit dem strengeren Verifier.
- Seine per URL + sha256 referenzierten Code-Quellen (`tools/reentry_crate.py`,
  `tests/unit/test_reentry_crate.py`) binden den Stand **vor** diesen Korrekturen
  (Commit `7275007`). Am neuen Head stimmen diese Hashes absichtlich nicht mehr überein.
- Ein späterer Save State erhält eine neue ID; das alte Siegel wird nicht neu geschrieben.

## 4. Weiter bewusst offen

- UNSIGNED: interner Hashabgleich ohne externen Herkunftsanker.
- Freigabe der konkreten öffentlichen Save-State-/Intake-Fassung (Owner-Entscheidung).
- MCP-Server: Laufzeitverhalten, Abhängigkeiten, lokale Konfiguration.
- DTA KHM 1812: widersprüchliche Lizenzangaben (UNRESOLVED).
- Anbindung an ein `status_emit`-Receipt.
