# SIGNED_BYTES_DECISION_NOTE_v0_1

**Status:** Entscheidungsnotiz (keine Entscheidung getroffen)
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Datum:** 2026-10-28
**Anlass:** Vorschläge V2 (Kanonisierung) und V1 (asymmetrische Signatur)
**Bezug:** `tools/status_emit.py`, `tools/status_verify.py`, `SECURITY.md`,
`.claude/rules/annex.md`

Bestehende Receipts bleiben unverändert (IMMUTABLE). Diese Notiz implementiert
nichts; sie bereitet eine spätere Entscheidung vor.

---

## 1. Ist-Stand

- Signiert wird mit HMAC-SHA256 über `json.dumps(payload, sort_keys=True,
  separators=(",", ":"))` (Bezeichnung `json_c14n_v1`). Ohne Secret: `UNSIGNED`.
- HMAC ist symmetrisch: Wer prüfen kann, kann auch signieren. Es gibt daher
  Manipulationserkennung für Inhaber des Secrets, aber **keine Nicht-Abstreitbarkeit**
  und keine Prüfung durch Dritte ohne das Secret.

## 2. Was signiert wird: festgelegte Bytes

Für jede Signatur (HMAC, Ed25519, COSE, Sigstore) ist entscheidend, dass die
signierten **Bytes** eindeutig festgelegt sind. JCS (RFC 8785) ist eine Möglichkeit,
aber keine allgemeine Voraussetzung: Man kann auch die serialisierten Bytes selbst
transportieren und signieren (z. B. als COSE-Payload) und beim Prüfen nicht neu
serialisieren.

Gemessene Abweichungen zwischen `json_c14n_v1` (Python) und einer JCS-artigen
Serialisierung in JavaScript (`JSON.stringify` + Schlüsselsortierung nach
UTF-16-Codeunits; keine zertifizierte JCS-Implementierung), Node 22.22, Python 3.13:

| Vektor | Eingabe | Python json_c14n_v1 | JS (JCS-artig) | SHA-256 Python / JS (Präfix) |
|---|---|---|---|---|
| escaping | `{"a":"ä"}` | `{"a":"\u00e4"}` | `{"a":"ä"}` | `ba42eceab1bf32f0` / `46e7684c4b194411` |
| float_integral | `{"f":1.0}` | `{"f":1.0}` | `{"f":1}` | `3fd3fc1b51eda523` / `fcc1504e92491760` |
| large_float | `{"x":1e+16}` | `{"x":1e+16}` | `{"x":10000000000000000}` | `21d6bea42b17fd31` / `d9ea702067d662ee` |
| negative_zero | `{"z":-0.0}` | `{"z":-0.0}` | `{"z":0}` | `29546c5002ef1837` / `e313adcae40818c4` |
| line_separator | `{"s":"<U+2028>"}` | `{"s":"\u2028"}` | `{"s":"<U+2028>"}` | `3ae2ec9d6d322c77` / `d2dcdddd0f4b645d` |
| key_order_non_bmp | `{"｡":1,"😀":2}` | `{"\uff61":1,"\ud83d\ude00":2}` | `{"😀":2,"｡":1}` | `94ba397c86081c24` / `c265de3d33291482` |

Backslashes in den Zellen sind wörtlich. `<U+2028>` steht für ein einzelnes
rohes Unicode-Zeichen; der Platzhalter gehört nicht zu den gehashten Bytes.
Gegenprobe am 28.10.2026: Python 3.12.14, Node v24.22.1; alle sechs
Hash-Paare stimmen mit der ersten Messung überein.

Ursachen laut RFC 8785:
- Zahlen werden nach ECMAScript serialisiert (§ 3.2.2.3), Python-`repr` weicht ab;
- Strings werden ohne Unicode-Normalisierung „as is“ übernommen (§ 3.1, § 3.2.2.2),
  Pythons `ensure_ascii` escaped dagegen alles außerhalb von ASCII;
- Schlüssel werden nach UTF-16-Codeunits sortiert (§ 3.2.3), Python sortiert nach
  Codepoints; außerhalb der BMP ergibt das eine andere Reihenfolge.

Folge: Eine abweichende JavaScript-/JCS-Neu-Serialisierung erzeugt bei diesen
Werten andere Hashes. Ein Prüfer muss die festgelegten Originalbytes verwenden
oder exakt die vorhandene Kanonisierung reproduzieren. JavaScript als Sprache
ist kein Hindernis; entscheidend ist dieselbe Byte-Darstellung.

## 3. Entscheidungspunkte

| # | Frage | Optionen | Hinweis |
|---|---|---|---|
| E1 | Welche Bytes werden signiert? | (a) `json_c14n_v1` beibehalten und Bytes mitliefern; (b) neue Version `json_jcs_v1` nach RFC 8785; (c) Bytes als opake Payload (COSE) | Jede neue Variante bekommt eine eigene Versionskennung; `json_c14n_v1` bleibt für Bestandsreceipts gültig |
| E2 | Wer bezeugt was? | CI-Identität, Werkzeug, Mensch | siehe § 4 |
| E3 | Schlüsselverwaltung | Repo-Secret (heute), lokaler Schlüssel je Person, schlüsselloses OIDC (Sigstore) | Rotation, Widerruf, Verlust jeweils festlegen |
| E4 | Prüfung durch Dritte | nur Secret-Inhaber (heute) oder öffentlich | öffentlich verlangt asymmetrische Signatur oder Attestation |

## 4. Wessen Handlung bezeugt eine Signatur?

Eine gültige Signatur bindet Bytes an einen Verifikationsschlüssel. Die Zuordnung
zu einer Person oder einem Workflow und die Bedeutung als Freigabe benötigen
zusätzliche Identitäts- und Prozessannahmen. Sie belegt weder das Lesen noch die
Wahrheit des Inhalts (vgl. ERK § 9.1: Integrität ≠ Authentizität ≠ Autorisierung ≠ Wahrheit).

| Signierende Instanz | bezeugt | bezeugt **nicht** |
|---|---|---|
| CI-Attestation (z. B. GitHub OIDC/Sigstore) | „dieser Workflow lief auf diesem Commit und erzeugte diese Bytes“ | menschliche Prüfung oder Freigabe |
| Werkzeug lokal (z. B. `status_emit` mit Secret) | „ein Inhaber des Secrets hat diese Bytes erzeugt“ | welche Person; Richtigkeit des Inhalts |
| Persönlich zugeordneter Schlüssel | „diese Bytes sind unter diesem Schlüssel signiert“; als menschliche Freigabe nur nach explizitem Freigabeprozess und belegter Schlüsselzuordnung interpretierbar | tatsächliche Bedienperson, Lesen, Zustimmung oder inhaltliche Richtigkeit allein aus der Signatur |

CI-Attestation und menschliche Freigabe sind getrennt zu halten: Eine grüne,
signierte CI erzeugt keine menschliche Freigabe (PROPOSE ≠ AUTHORIZE).

## 5. Empfehlung zur Reihenfolge (nicht beschlossen)

1. Sprachliche Korrektur „nicht-repudiierbar“ (in diesem PR erledigt).
2. E1 entscheiden und die Vektoren oben als Python- und JS-Tests festschreiben.
3. Erst danach E2–E4 und eine asymmetrische Signatur.

## 6. Quellen

- RFC 8785, JSON Canonicalization Scheme, https://www.rfc-editor.org/rfc/rfc8785.html
  — gelesen: § 3.1, § 3.2.2.2, § 3.2.2.3, § 3.2.3.
- `SECURITY.md` (Formulierung „non-repudiable“ vermeiden).
- Vektoren: erzeugt mit `tools/status_emit.canonical_json` und einem kurzen
  Node-Skript (Funktion `canon` = rekursives `JSON.stringify` mit `Object.keys().sort()`).
