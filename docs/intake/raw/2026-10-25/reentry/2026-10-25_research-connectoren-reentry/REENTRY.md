# Re-Entry: Research-Connectoren und Re-Entry-Werkzeug (Erststand)

> Save State `2026-10-25_research-connectoren-reentry` · erstellt 2026-10-25T02:25:25+00:00 · Commit `83caf03d6e80` (dirty) · Branch `ccr-392027bd-pu1nxa`
> Authority: **DERIVED** · Promotion: **NO_CANON_PROMOTION** · FOKUS: Anbindungen + Save-State-Kreislauf vorbereiten

**Vor dem Weiterarbeiten:** `python3 tools/reentry_crate.py verify --crate docs/intake/raw/2026-10-25/reentry/2026-10-25_research-connectoren-reentry` muss PASS melden. Rückführung in dauerhaften Zustand nur mit explizitem OK (Re-Entry-Schwelle).

## Stand

**Status:** GO_prepared_hold_install

Kuratierung von 15 Anbindungen (Skills, MCP-Server, Provenienz, Grimm-Ebene) und deren
Umsetzung, soweit in einer Cloud-Sitzung möglich: Save-State-Werkzeug als RO-Crate 1.2 mit
SHA-256-Siegel, Re-Entry-Skill, Basic-Memory-Konvention, Sicherheitsprüfung dreier
Community-MCP-Server, Connector-Smoke-Tests, Wolfram-Zweitrechnung und DTA-TEI-Prüfung.
Installationen auf dem eigenen Rechner und Lizenzklärung DTA stehen aus.
Öffentliche Fassung für den Intake (Pattern F); enthält keine privaten Korpusinhalte.

## Eingefroren (frozen state)

- RO-Crate 1.2 ist das Re-Entry-Paketformat (tools/reentry_crate.py)
- Save States sind privat per Default (out/reentry/, gitignored)
- Re-Entry übernimmt nur Crates mit verify = PASS

## Schwebendes Problem

Lokale Installation der MCP-Server und Wahl des Basic-Memory-Projektordners

## Aussagen

Claim-Audit: 6 Aussagen — FACT 2 · INFERENZ 1 · KORPUSBEFUND 1 · METAPHER 1 · MODELL 1

| # | Tag | Status | Aussage | Quellen |
|---|-----|--------|---------|---------|
| 1 | FACT | VERIFIED | Das Save-State-Werkzeug erzeugt RO-Crate-1.2-Pakete, die verify mit PASS bestehen; Manipulation führt zu HOLD. | tool, tests |
| 2 | FACT | VERIFIED | Wolfram-Zweitrechnung (Charakteristik-Matrix) stimmt mit thin_film_reflectance (Airy) auf ~1e-16 überein. | protocol |
| 3 | INFERENZ | REVIEW-PENDING | Basic Memory und Zotero MCP sind mit Einstellungen nutzbar; arXiv MCP ist mit gepinnter Version unbedenklich. | protocol |
| 4 | KORPUSBEFUND | UNRESOLVED | Die DTA-Lizenzangaben für KHM 1812 widersprechen sich (CC BY-NC 3.0 vs. CC BY-SA 4.0). | protocol |
| 5 | MODELL | DERIVED | Basic-Memory-Kategorien tragen die Claim-Art, Tags den Status; so bleiben Metapher und Messbehauptung getrennt. | skill_reference |
| 6 | METAPHER | DERIVED | Ein versiegeltes Paket ist ein zwischenzeitliches Ganzes, das ohne Glättung wieder betreten werden kann. | – |

## Offene Stellen (UNRESOLVED)

- MCP-Server lokal einrichten (Befehle im Prüfprotokoll, §5)
- DTA-Lizenz für KHM 1812 klären
- Figma: Code Connect / Canvas-Schreiben mit Starter-Plan und View-Seat praktisch prüfen
- Wolfram-Connector: Kosten und Limits
- status_emit-Receipt an den Crate-Hash binden (bisher eigenes SEAL.json)

## Negativbefunde

- DWB / Digitaler Grimm: keine Inhalts-API gefunden (nur OAI-PMH-Metadaten)
- Blender MCP zurückgestellt: beliebige Python-Ausführung, Socket ohne Auth
- Cloud-Gedächtnisse (Mem0, Vertiso, Meko) widersprechen lokal + hashbar

## Bekannte Verluste

- Kein Chat-Transkript im Paket
- Drive-Korpus nur gesichtet, keine Inhalte übernommen (PRIVACY_BOUNDARY)
- Siegel UNSIGNED: kein ENTA_HMAC_SECRET in dieser Sitzung
- Code-Quellen nur als URL + sha256 referenziert, nicht kopiert (öffentliche Fassung)

## Nächste Schritte

- **A1** MCP-Server lokal einrichten (Basic Memory, arXiv, Zotero) (`docs/intake/raw/2026-10-25/research-connectoren-setup-und-pruefprotokoll-v0-1.md`)
- **A2** Ersten privaten Save State aus dem Drive-Korpus mit /tesser3takt-reentry save anlegen (`.claude/skills/tesser3takt-reentry/SKILL.md`)
- **A3** Intake-Einträge sichten und über Kanonisierung entscheiden (`docs/intake/INDEX.md`)

**Nächste erlaubte Aktion:** Intake-Einträge INTAKE-2026-10-25-001/002 sichten; keine Kanonisierung ohne Review

## Quellen

| ID | Rolle | Ort | SHA-256 |
|----|-------|-----|---------|
| curation | output | `payload/docs/intake/raw/2026-10-25/kuratierte-anbindungen-entaengelment-tesser3takt-grimm-v0-1.md` | `60c7f93b0a33e36a…` |
| protocol | output | `payload/docs/intake/raw/2026-10-25/research-connectoren-setup-und-pruefprotokoll-v0-1.md` | `45bd49699ebeb76c…` |
| tool | output | `https://github.com/fleksible/entaENGELment-/blob/ccr-392027bd-pu1nxa/tools/reentry_crate.py` | `df4d5669bc085149…` |
| tests | output | `https://github.com/fleksible/entaENGELment-/blob/ccr-392027bd-pu1nxa/tests/unit/test_reentry_crate.py` | `5672b84e9839a5b4…` |
| skill_reference | output | `payload/.claude/skills/tesser3takt-reentry/reference.md` | `88dea40b72fc51cd…` |
| rocrate_spec | context | `https://www.researchobject.org/ro-crate/specification/1.2/introduction.html` | `–` |

## Lineage

- `prompt_v1` Recherche-Prompt v1 (User) (input)
- `prompt_v2` Recherche-Prompt v2 (derived)
- `curation` 15 kuratierte Anbindungen (review_pending)
- `execution` Werkzeug, Skill, Prüfungen (derived)
- `savestate` Dieser Save State (derived)
- `prompt_v1` —refined_into→ `prompt_v2`
- `prompt_v2` —produced→ `curation`
- `curation` —implemented_by→ `execution`
- `execution` —sealed_as→ `savestate`
