# Research-Connectoren: Setup & Prüfprotokoll (v0.1)

**Stand:** 2026-10-25 · **Status:** [INTAKE] REVIEW-PENDING · NO_CANON_PROMOTION
**Bezug:** Kuratierte Anbindungen v0.1 (gleicher Intake-Tag) · Skill `.claude/skills/tesser3takt-reentry/`

> Alles hier ist Prüfprotokoll einer Sitzung, keine Spezifikation. Installiert oder
> ausgeführt wurde **kein** Drittanbieter-Code (statische Prüfung, `repo-pruefer`-Regel 1).

---

## 1. Connector-Smoke-Tests (in dieser Sitzung ausgeführt)

| Connector | Test | Ergebnis |
|-----------|------|----------|
| Wolfram | Wolfram-Language-Auswertung (s. §2) | [FACT] funktioniert, obwohl das Verzeichnis „needs reconnect“ meldet |
| PubMed | `Levin M[Author] AND bioelectric AND morphogenesis` | [FACT] 70 Treffer, PMIDs geliefert |
| bioRxiv | Preprints `developmental biology`, letzte 7 Tage | [FACT] liefert DOI/Titel/Abstract; [FACT] keine Stichwortsuche (nur Datum/Kategorie) |
| Google Drive | Volltextsuche nach Projektbegriffen | [FACT] Korpus-Ordner mit früheren Save States, Receipts, Lineage-Graph gefunden (Dateinamen bewusst nicht im Repo, PRIVACY_BOUNDARY) |
| Figma | `whoami` | [FACT] Starter-Plan, View-Seat → Lesen ja; Canvas-Schreiben außerhalb eigener Drafts braucht laut Figma-Hilfe einen Full-Seat |
| alphaXiv | Verzeichnisstatus | [FACT] „connect_incomplete“ – nicht nutzbar bis Abschluss in den claude.ai-Einstellungen |

## 2. Wolfram-Zweitrechnung: `tools/thin_film_reflectance.py`

[FACT] Unabhängige Formulierung in Wolfram (Charakteristik-Matrix, Abelès) gegen die
Airy-Formel des Repo-Tools, Fälle A/B/C × 450/550/650 nm:

| Fall | λ (nm) | Repo (Python) | Wolfram (Matrix) |
|------|--------|---------------|------------------|
| A | 450 | 0.05461304404981052 | 0.054613044049810565 |
| A | 550 | 0.02411372820116544 | 0.024113728201165436 |
| A | 650 | 0.02307505823767966 | 0.02307505823767962 |
| B | 450 | 0.0103884156291668 | 0.010388415629166809 |
| B | 550 | 0.001109724416560689 | 0.0011097244165606886 |
| B | 650 | 0.0008009723752357962 | 0.0008009723752357942 |
| C | 450 | 0.08081567838869527 | 0.0808156783886953 |
| C | 550 | 0.02714338613442897 | 0.02714338613442895 |
| C | 650 | 0.02526766274769636 | 0.025267662747696356 |

[FACT] Maximale Abweichung im Bereich 1e-16 (Gleitkomma-Rundung). [MODEL] Das bestätigt
nur die Rechnung im deklarierten Modell (senkrechter Einfall, keine Absorption), keine
Materialaussage.

## 3. DTA: Kinder- und Haus-Märchen 1812, Bd. 1

| Prüfpunkt | Befund |
|-----------|--------|
| Format | [FACT] TEI-XML (`http://www.tei-c.org/ns/1.0`, DTA-Basisformat), 991 880 Byte |
| SHA-256 | `ba85b9611d31012ffa61fff552921cca7760517bb9026120312e2eb3d53e0936` (Abruf 2026-10-25) |
| Umfang | [FACT] 86 nummerierte Märchen + Vorrede, Zeugnisse, Inhalt |
| Zugang | Handle `21.11120/0000-000C-52B6-A` → DTA-Download; DTA setzt eine einfache Cookie-Abfrage (`verified=1`) vor den Download |
| Lizenz | **UNRESOLVED:** CLARIN-Eintrag nennt CC BY-NC 3.0, der TEI-Header (publicationStmt 2025-02-28) nennt CC BY-SA 4.0. Vor Nutzung klären, welche gilt. |

Datei nicht ins Repo übernommen (Größe, Lizenzfrage).

## 4. Sicherheitsprüfung Community-MCP-Server (`repo-pruefer`, statisch)

### Basic Memory · Commit `4bcfc0665744` · PyPI 0.24.1 · AGPL-3.0 — ⚠️ mit Einstellung nutzbar
- Nur den **MCP-Server** nutzen, **nicht** das Claude-Code-Plugin: dessen Hooks laufen automatisch
  bei SessionStart/PreCompact (`uv run … session_start.py`, `pre_compact.py`).
- CLI-Analytics: Umami-Events (Promo-Anzeige, Cloud-Login) mit Versionsnummer an
  `api-gateway.umami.dev`. [FACT] Code gelesen: Der `mcp`-Startpfad löst weder Promo noch
  Auto-Update aus (nicht-interaktiv bzw. `mcp` ausgenommen). Abschalten: `BASIC_MEMORY_NO_PROMOS=1`.
- Logfire-Telemetrie per Default aus. Version pinnen.
- Scanner-Treffer gelesen und als harmlos eingestuft: „KI-Umsteuerung“ in einem Entwickler-Skill
  des Projekts (`.agents/skills/cmux-settings/SKILL.md`), Bidi-Zeichen als Testdaten für
  Namensnormalisierung (`tests/services/test_note_authorship.py`).

### Zotero MCP · Commit `eb016b1b746d` · PyPI `zotero-mcp-server` 0.15.1 · MIT — ⚠️ mit Einstellung nutzbar
- Nur den **MCP-Server** nutzen, **nicht** das Zotero-Chat-Plugin (`plugin/`, AGPL): Es startet
  Agenten mit wählbaren Modi inkl. `bypassPermissions`, und sein Doctor führt `curl … | sh` aus.
- `ZOTERO_LOCAL=true` → kein Web-API-Key nötig. Chroma-Telemetrie explizit aus
  (`anonymized_telemetry=False`); `_log_telemetry` ist lokales Logging.
- Semantische Suche: lokale Embeddings wählen, sonst gehen Texte an OpenAI/Gemini.
- `zotero-mcp setup` schreibt `claude_desktop_config.json` (mit Backup); Updater nur per `update`.
- Scanner-Treffer gelesen: „Ignore previous instructions“ sind Testfälle des Plugins für
  Übersetzungsrobustheit; Bidi-Treffer ist Code, der Bidi-Zeichen entfernt. Harmlos.

### arXiv MCP Server · Commit `572e301bb319` · PyPI 0.8.2 · Apache-2.0 — ✅ (Version pinnen)
- Netzverkehr nur zu `arxiv.org`/`export.arxiv.org`, für den Zitationsgraphen zu
  `api.semanticscholar.org`. Keine Hooks, keine Secrets, keine KI-Anweisungen gefunden.
- Ablage der Paper per `--storage-path` steuerbar.

**Grenzen:** statische Mustersuche + gezieltes Lesen; keine Garantie gegen gut versteckten
Schadcode; Abhängigkeiten nicht rekursiv geprüft; GitHub-Metadaten in dieser Sitzung nicht
abrufbar (Pflegesignal = PyPI-Release-Daten).

## 5. Einrichtung (Claude Code, `--scope user`)

[IDEE] Gepinnte Versionen, Datenablage außerhalb des öffentlichen Repos.

```bash
# Basic Memory – nur MCP-Server, Promo/Analytics aus
claude mcp add --scope user -e BASIC_MEMORY_NO_PROMOS=1 --transport stdio basic-memory \
  -- uvx --prerelease=allow --from 'basic-memory==0.24.1' basic-memory mcp

# arXiv – Paper in eigenem Ordner
claude mcp add --scope user --transport stdio arxiv \
  -- uvx --from 'arxiv-mcp-server==0.8.2' arxiv-mcp-server --storage-path ~/arxiv-papers

# Zotero – lokaler Modus (Zotero 7+: „Allow other applications to communicate“ aktivieren)
claude mcp add --scope user -e ZOTERO_LOCAL=true --transport stdio zotero \
  -- uvx --from 'zotero-mcp-server==0.15.1' zotero-mcp-server serve

# Optional: Referenz-Memory (Node >= 24), JSONL-Datei außerhalb des Repos
claude mcp add --scope user -e MEMORY_FILE_PATH=$HOME/tesser3takt/memory.jsonl --transport stdio memory \
  -- npx -y @modelcontextprotocol/server-memory@2.0.0
```

Hinweis zur Syntax: Der Servername darf nicht direkt nach `-e` stehen (sonst als `KEY=value`
gelesen) — daher `--transport stdio` dazwischen.

claude.ai-Connectoren: Wolfram optional neu verbinden (funktionierte trotz Status);
alphaXiv abschließen oder zugunsten des arXiv-MCP weglassen.

## 6. Offen

- [ ] Lizenz DTA KHM 1812 klären (CC BY-NC 3.0 vs. CC BY-SA 4.0).
- [ ] Wolfram-Connector: Kosten/Limits (Verzeichnis nennt keine).
- [ ] Figma: Code Connect/Canvas-Schreiben mit Starter/View-Seat praktisch prüfen.
- [ ] DataLad + git-annex lokal einrichten (nicht in dieser Sitzung).
- [ ] Graphiti erst bei Bedarf (Graph-DB + LLM-Kosten).
