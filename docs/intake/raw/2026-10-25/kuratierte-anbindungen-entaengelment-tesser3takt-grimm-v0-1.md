# Kuratierte Anbindungen: entaENGELment · tesser3TAKT · Grimm (v0.1)

**Stand:** 2026-10-25 · **Status:** [INTAKE] REVIEW-PENDING · NO_CANON_PROMOTION
**Herkunft:** Claude-Code-Sitzung (Recherche + Ausführung), Primärquellen siehe Links.
**Begleitdokument:** Setup & Prüfprotokoll (gleicher Intake-Tag).

> Status-Logik: **VERIFIZIERT** = Quelle selbst geprüft · **TEILGEPRÜFT** = Existenz belegt,
> Detail offen · **UNGEPRÜFT**. „Kann“ = belegte Funktion, „Idee“ = Nutzungsvorschlag.

---

## 1. Verbesserter Recherche-Prompt (v2)

```
Du bist ein erfahrener Kurator für KI-Werkzeuge, Claude Skills, MCP-Server und Forschungs-Workflows.
Du arbeitest gründlich, quellentreu und ohne Glättung. Du darfst widersprechen, umgewichten und Lücken benennen.

PROJEKT: entaENGELment · tesser3TAKT · Grimm  [Essenz-Block unverändert]

VORGEHEN
0. Bestand zuerst: Prüfe, was schon verbunden/installiert ist (Connectors, Skills, Repo-Tools).
1. Nur Primärquellen: Anthropic-Doku und Skill-Repos, offizielles MCP-Registry bzw. Anthropic-
   Connector-Verzeichnis, Projekt-Repos/Paketregister (Release-Datum = Pflegesignal),
   Fach- und Forschungsinfrastruktur.
2. Passung = Ebene (entaENGELment / tesser3TAKT / Grimm) × Phase (Korpus / Analyse / Save State /
   Re-Entry). Plus: Klartext, lokal, versionier-/hashbar, Replay-fähig, offene Lizenz.
   Minus: Cloud-Lock-in, Code-Ausführung ohne Sandbox, ungepflegt.

KATEGORIEN (zusammenlegbar)  [1–5 wie gehabt]

FÜR JEDEN EINTRAG
Name + Link · Kann [FACT] (1 Satz) · Idee [IDEE] (1–2 Sätze, Ebene + Phase) ·
Aufwand · Kosten · Lizenz · letzte Release · Status (VERIFIZIERT/TEILGEPRÜFT/UNGEPRÜFT) · Risiko

REGELN
Nichts erfinden. Höchstens 15 Einträge nach Passung. Liste „geprüft, aber zurückgestellt“ mit Grund.

ABSCHLUSS
3 Startpunkte + Workflow in 5 Schritten mit Anschluss an Repo-Tools. Offen: was ungeprüft blieb und warum.
```

---

## 2. Die 15 Einträge (beste Passung zuerst)

| # | Eintrag | Kann [FACT] | Idee [IDEE] | Aufwand · Kosten | Status |
|---|---------|-------------|-------------|------------------|--------|
| 1 | Agent Skills + `skill-creator` — [Doku](https://code.claude.com/docs/en/skills), [anthropics/skills](https://github.com/anthropics/skills) | `SKILL.md` + Skripte, stufenweises Laden, `/name` oder automatisch | Repo-Skill für Save/Re-Entry — **umgesetzt** als `.claude/skills/tesser3takt-reentry/` | niedrig · im Plan | VERIFIZIERT |
| 2 | RO-Crate 1.2 — [Spec](https://www.researchobject.org/ro-crate/specification/1.2/introduction.html) | JSON-LD/schema.org-Paket mit `ro-crate-metadata.json`, Provenienz über Actions | Re-Entry-Paketformat — **umgesetzt** in `tools/reentry_crate.py` (stdlib, ohne Zusatz-Abhängigkeit) | mittel · kostenlos | VERIFIZIERT |
| 3 | Basic Memory — [GitHub](https://github.com/basicmachines-co/basic-memory) | Markdown-Gedächtnis, `- [kategorie] Fakt #tag`, `[[Wikilinks]]`, SQLite-Index; 0.24.1 (23.10.2026), AGPL-3.0 | Lebendes Gedächtnis zwischen Save States; Konvention in `reference.md` des Skills | niedrig · lokal kostenlos | VERIFIZIERT + Security-Review |
| 4 | DataLad — [datalad.org](https://www.datalad.org/), [run](https://handbook.datalad.org/en/latest/basics/101-108-run.html) | Git + git-annex, `datalad run` schreibt Run-Record, `rerun` spielt ab; 1.7.1, MIT | Korpus als Dataset, Extraktion per `run` → Replay | mittel–hoch · kostenlos | VERIFIZIERT |
| 5 | Google Drive Connector — [Hilfe](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors) | Suche, Lesen von Docs/PDF/Office (nur Text) | Korpuszugriff; Drive-ID + Hash als Quellenanker | niedrig · im Plan | VERIFIZIERT, verbunden |
| 6 | Zotero MCP — [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) | Suche (auch semantisch), Volltext, Annotationen, BibTeX, Retraction-Alerts; PyPI `zotero-mcp-server` 0.15.1 | Zotero-Key je Messbehauptung; Retraction → HOLD | mittel · kostenlos | VERIFIZIERT + Security-Review |
| 7 | Wolfram Connector — [Verzeichnis](https://claude.com/marketplace/connectors/wolfram) | Wolfram\|Alpha, Context, Language Evaluator; Anthropic verified | Unabhängige Zweitrechnung — **durchgeführt** für `thin_film_reflectance` (Übereinstimmung) | niedrig · Kosten UNGEPRÜFT | VERIFIZIERT (funktioniert) |
| 8 | PubMed + bioRxiv Connectoren | Suche/Metadaten/Volltext bzw. Preprints nach Datum/Kategorie | Levin-Strang; Preprint ohne Journal → REVIEW-PENDING | niedrig · kostenlos | VERIFIZIERT, verbunden |
| 9 | arXiv MCP Server — [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | Suche, Download, Abschnitt-/LaTeX-Lesen, BibTeX, Zitationsgraph; 0.8.2, Apache-2.0 | Claims zitieren exakten Abschnitt | niedrig · kostenlos | VERIFIZIERT + Security-Review |
| 10 | Graphiti — [getzep/graphiti](https://github.com/getzep/graphiti) | Bi-temporaler Graph, Invalidierung statt Löschung, Episoden-Provenienz; braucht Graph-DB + LLM | G3-Entsprechung; erst wenn Basic Memory nicht reicht | hoch · OSS + LLM-Kosten | VERIFIZIERT |
| 11 | MCP Memory (Referenz) — [src/memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | Entitäten/Relationen/Beobachtungen in JSONL (`MEMORY_FILE_PATH`) | Leichteste diffbare Variante | niedrig · kostenlos | VERIFIZIERT |
| 12 | ink / inkjs — [ink](https://www.inklestudios.com/ink/) | Erzählskriptsprache, Inky, Unity-Plugin, JSON-Export; MIT | Grimm-2.0-Template als ink-Knoten; JSON hashbar | niedrig–mittel · kostenlos | VERIFIZIERT |
| 13 | DTA: KHM 1812, Bd. 1 — [CLARIN](https://clarin.bbaw.de/en/objects/dta:382/) | TEI-XML (DTA-Basisformat), 86 Märchen, Handle-PID | Genealogischer Nullpunkt für Motiv-Vergleiche | niedrig · kostenlos | **VERIFIZIERT** (TEI geprüft) · Lizenz UNRESOLVED (s. Protokoll) |
| 14 | Figma MCP — [Hilfe](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) | Design-Kontext lesen, Canvas schreiben (Beta) | HUD-Spiegel zu `ui-app` | niedrig · Freemium | VERIFIZIERT, verbunden · Plan begrenzt (s. Protokoll) |
| 15 | React Three Fiber + @react-three/xr — [pmndrs/xr](https://github.com/pmndrs/xr) | WebXR (VR/AR) für R3F | Grimm-VR-Kapsel als Route im Next.js-`ui-app` | mittel · kostenlos | VERIFIZIERT (Geräte/Lizenz offen) |

## 3. Geprüft, aber zurückgestellt (Negativbefunde)

- **GitHub MCP:** bereits aktiv, kein eigener Eintrag.
- **W3C PROV / `prov`:** überschneidet sich mit RO-Crate-Provenienz.
- **DVC:** überschneidet sich mit DataLad; `rerun` näher am Replay-Gedanken.
- **Zenodo-GitHub:** DOI je Release; Repo ist öffentlich → technisch möglich, Entscheidung offen.
- **Blender MCP:** Community-Projekt, `execute_blender_code` führt beliebiges Python aus, Socket ohne Auth.
- **DWB / Digitaler Grimm (TCDH):** keine Inhalts-API gefunden, nur OAI-PMH-Metadaten.
- **Mem0, Vertiso, Meko:** Cloud-Gedächtnis, widerspricht „lokal und hashbar“.
- **Twine, A-Frame:** ink bzw. R3F passen besser zum Stack.

## 4. Startpunkte und Workflow

Start: #1 Skill · #2 RO-Crate · #3 Basic Memory (Drive #5 liefert den Korpus).

1. **Korpus:** Quellen über Drive; Text extrahieren; je Quelle sha256 + Drive-ID.
2. **Analyse:** Basic-Memory-Notizen mit Kategorie = Claim-Art, Tag = Status.
3. **Save State:** `/tesser3takt-reentry save` → Manifest → CHECKPOINT → versiegeltes RO-Crate.
4. **Ablage:** privat in `out/reentry/`; Veröffentlichung nur bewusst (`--publish`, Pattern F).
5. **Re-Entry:** `/tesser3takt-reentry load <crate>` → verify → bei PASS „Stand · Offen · Nächster Schritt“.
