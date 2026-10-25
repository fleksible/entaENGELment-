# Report: Research-Connectoren und tesser3TAKT-Re-Entry

**Datum:** 2026-10-25
**Fokus:** Anbindungen + Save-State-Kreislauf

## Ziel

Die kuratierten Anbindungen (Skills, MCP-Server, Provenienz-Werkzeuge, Grimm-Ebene) so weit
umsetzen und vorbereiten, wie es in einer Cloud-Sitzung möglich ist, mit Fokus auf den Kreislauf
Korpus → Analyse → Save State → Re-Entry.

## Aktionen

- [x] Recherche-Prompt v2 und 15 kuratierte Anbindungen als Intake abgelegt (`INTAKE-2026-10-25-001`)
- [x] Save-State-Werkzeug `tools/reentry_crate.py`: RO-Crate 1.2, SHA-256-Siegel mit HMAC oder UNSIGNED, `verify` (PASS/HOLD), `brief`; Felder kompatibel zum bestehenden Save-State-/Receipt-Vokabular; `reentry_vector`-Karte im Format von `tools/verify_cards.py`
- [x] Privatsphäre-Schranke: Standardziel `out/reentry/` (gitignored), committbare Ziele nur mit `--publish`
- [x] 25 Unit-Tests (`tests/unit/test_reentry_crate.py`), Make-Ziele `reentry-save` / `reentry-verify`
- [x] Skill `.claude/skills/tesser3takt-reentry/` (save/load, nur auf Aufruf) mit Vorlage und Basic-Memory-Konvention
- [x] Sicherheitsprüfung (statisch, `repo-pruefer`) für Basic Memory, Zotero MCP, arXiv MCP
- [x] Connector-Smoke-Tests: Wolfram, PubMed, bioRxiv, Google Drive, Figma
- [x] Wolfram-Zweitrechnung für `tools/thin_film_reflectance.py` (Übereinstimmung ~1e-16)
- [x] DTA KHM 1812: TEI geprüft, 86 Märchen, SHA-256 notiert, Lizenzwiderspruch gefunden
- [x] Setup- und Prüfprotokoll als Intake abgelegt (`INTAKE-2026-10-25-002`)
- [x] Erster Save State dieser Sitzung: privat in `out/reentry/`, öffentliche Fassung in `docs/intake/raw/2026-10-25/reentry/` (verify PASS; ro-crate-py 0.16.0 liest das Paket als RO-Crate 1.2)

## Nicht getan

- Keine MCP-Server installiert oder Drittanbieter-Code ausgeführt (nur statische Prüfung; Installation gehört auf den eigenen Rechner)
- Keine Drive-Korpusinhalte ins Repo übernommen (PRIVACY_BOUNDARY); bestehende Save-State-Formate nur gelesen, um Felder anzugleichen
- Keine GOLD-Dateien (`index/`, `spec/`, `policies/`, `VOIDMAP.yml`, `data/receipts/`) berührt; keine Kanonisierung
- Keine `ro-crate-py`-Abhängigkeit ins Projekt aufgenommen (Werkzeug bleibt stdlib + PyYAML)
- DataLad, Graphiti, ink/inkjs, R3F/WebXR nicht eingerichtet (eigene Fokusse, siehe Offene Punkte)

## Risiken

- UNSIGNED-Siegel sichern nur Integrität, nicht Herkunft (`ENTA_HMAC_SECRET` setzen für Signatur)
- Save States können private Bedeutung tragen; `--publish` nur nach Prüfung gegen PRIVACY_BOUNDARY.md
- Statische Sicherheitsprüfung findet keine gut versteckten Muster; Abhängigkeiten nicht rekursiv geprüft
- DTA-Lizenz für KHM 1812 widersprüchlich (CC BY-NC 3.0 vs. CC BY-SA 4.0)

## Offene Punkte

- [ ] ☐ MCP-Server lokal einrichten (Befehle: Prüfprotokoll §5)
- [ ] ☐ DTA-Lizenz klären
- [ ] ☐ `status_emit`-Receipt an Crate-Hash binden (bisher eigenes `SEAL.json`)
- [ ] ☐ Figma Code Connect / Canvas-Schreiben mit Starter-Plan + View-Seat prüfen
- [ ] ☐ Fokus-Entscheidung: DataLad-Korpus, ink-Template für Grimm 2.0, WebXR-Kapsel

## Artefakte

- `tools/reentry_crate.py`
- `tests/unit/test_reentry_crate.py`
- `.claude/skills/tesser3takt-reentry/SKILL.md`
- `.claude/skills/tesser3takt-reentry/reference.md`
- `.claude/skills/tesser3takt-reentry/templates/savestate.yaml`
- `Makefile` (Ziele `reentry-save`, `reentry-verify`)
- `docs/intake/raw/2026-10-25/kuratierte-anbindungen-entaengelment-tesser3takt-grimm-v0-1.md`
- `docs/intake/raw/2026-10-25/research-connectoren-setup-und-pruefprotokoll-v0-1.md`
- `docs/intake/raw/2026-10-25/reentry/2026-10-25_research-connectoren-reentry/`
- `docs/intake/records/INTAKE-2026-10-25-001.md`, `docs/intake/records/INTAKE-2026-10-25-002.md`
