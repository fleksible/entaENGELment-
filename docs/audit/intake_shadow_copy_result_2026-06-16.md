# Intake Shadow-Copy Hook — Result Report (PR #256)

**Datum:** 2026-06-16
**Fokus:** Automatischer Briefkasten via Claude-Code PostToolUse-Hook (additiv)
**Branch:** `chore/intake-shadow-copy-hook`
**Basis-HEAD:** `64e29f0` (main nach #252–#255)

> Zielsatz: *Der Briefkasten soll schneller sein als das Vergessen, aber langsamer
> als die Wahrheit.*

---

## 1. Was wurde angelegt?

- `tools/intake_shadow_copy.py` — fail-soft Hook-Helper (liest Hook-JSON von stdin).
- `.claude/settings.json` — projektlokaler PostToolUse-Hook (`async`).
- `docs/intake/raw/auto/.gitkeep` — Briefkasten-Zielordner.
- `docs/intake/README.md` §12 — „Automatic Shadow Copy / Briefkasten-Hook".
- `CLAUDE.md` Pattern F — Hinweis zum aktiven Hook.
- Dieser Bericht.

## 2. Wie funktioniert der Hook?

```
Claude schreibt/ändert Datei (Write|Edit|MultiEdit)
  → PostToolUse-Hook feuert ASYNC (Hintergrund)
  → python3 tools/intake_shadow_copy.py liest {tool_name, tool_input.file_path, cwd} von stdin
  → wenn dokumentartig UND nicht ausgeschlossen:
       Kopie → docs/intake/raw/auto/<YYYY-MM-DD>/<stem>__<sha8><ext>
       Zeile → docs/intake/raw/auto/<date>/_shadow_log.jsonl  (status: raw/auto)
  → Claude arbeitet ununterbrochen weiter
```

[FAKT] Hook-Schema gemäß offizieller Claude-Code-Doku verifiziert
(`hooks.PostToolUse[].{matcher, hooks:[{type,command,async}]}`; stdin-Felder
`tool_name`, `tool_input.file_path`, `cwd`; `async: true` = nicht-blockierend,
Output verworfen).

## 3. Welche Dateien/Pfade werden erfasst?

Dokumentartig: `.md` `.txt` `.docx` `.pdf` `.json` `.yml` `.yaml`,
nur bei Tool `Write`/`Edit`/`MultiEdit`, nur Dateien **innerhalb** des Repos.

## 4. Welche Pfade sind ausgeschlossen?

- **Mechanisch/Build/Cache:** `docs/intake/**`, `.git/**`, `node_modules/**`,
  `.venv|venv/**`, `dist/**`, `build/**`, `__pycache__/**`, `.pytest_cache/**`,
  `.mypy_cache/**`, `htmlcov/**`, Lockfiles, Temp-/Scratch-Dateien.
- **GOLD/Kanon (Verfeinerung):** `VOIDMAP.yml/.yaml`, `index/`, `spec/`,
  `policies/`, `seeds/`, `docs/spec|specs|canon|glossary|roadmap/`.
  **[MODELL]** Begründung: Kanon hat bereits ein Zuhause; der Briefkasten ist für
  das Heimatlose. So sammelt er keine Kanon-Kopien an (Anti-Staubsauger). Dies
  ergänzt die reine Write-Sperre aus der Auftragsvorgabe um eine **Source**-Sperre.

## 5. Warum unterbricht das den Flow nicht?

[FAKT] Der Hook ist `async: true` → läuft im Hintergrund, Claude wartet nicht, der
Output wird verworfen. Zusätzlich ist der Helper **fail-soft**: jeder Fehler (inkl.
JSON-Parse-Fehler) endet in `sys.exit(0)`; nie Exit 2, also nie blockierend.

## 6. Welche Tests wurden ausgeführt?

Simuliertes Hook-JSON über stdin, 10/10 PASS:

| Test | Ergebnis |
|------|----------|
| Doc-Datei → Shadow-Copy erzeugt | ✓ |
| Exit 0 (fail-soft) | ✓ |
| Quelle nicht gelöscht/verschoben | ✓ |
| Ledger `_shadow_log.jsonl` geschrieben | ✓ |
| Re-Edit gleicher Inhalt → Dedupe (keine Duplikate) | ✓ |
| `docs/intake/**` ausgeschlossen | ✓ |
| `VOIDMAP.yml` nicht geshadowt, Quelle unverändert | ✓ |
| Nicht-Doc (`.js`) ignoriert | ✓ |
| Nicht-passendes Tool (`Bash`) ignoriert | ✓ |
| Malformed stdin → fail-soft Exit 0 | ✓ |

Zusätzlich: `py_compile` ok · `claim_lint --strict` / `verify_pointers --strict` /
`workflow_posture_check` → exit 0 · `.claude/settings.json` ist valides JSON.
**Alle Testresiduen entfernt** (Cleanup verifiziert via `git status`).

**Limitierung (Anti-F7):** `pytest`/`ruff` nicht in der Umgebung installiert; nicht
lokal gelaufen. CI deckt beide ab. Der Hook selbst hat noch keinen pytest-Test
(siehe Risiken).

## 7. Welche Risiken bleiben offen?

- **[INFERENZ]** `async`-Feld ist laut Doku unterstützt; sollte eine Claude-Code-
  Version es ignorieren, läuft der Hook synchron — bleibt aber schnell und
  fail-soft, also unkritisch.
- **[FAKT]** Committeter Hook führt `python3 tools/intake_shadow_copy.py` in jeder
  Contributor-Session aus. Das Skript ist transparent, lokal, ohne Netzwerk und
  fail-soft; Deaktivierung in README §12 dokumentiert.
- **[HYPOTHESE]** `_shadow_log.jsonl` und `raw/auto/` können über Zeit wachsen;
  bewusst getrennt von der kuratierten `INDEX.md`. Ein späterer Aufräum-/Rotations-
  Helfer wäre möglich (nicht in diesem PR).
- **[FAKT]** Kein `intake_lint` erzwingt Ledger-/Briefkasten-Konsistenz (Roadmap).

## 8. Warum keine Essenzänderung?

[FAKT] Kein Kanon-, Spec-, VOID-, Claim-, Glossary- oder Roadmap-Inhalt verändert.
Rein additiv: ein Helper, eine Hook-Config, ein Zielordner, Doku-Ergänzungen. GOLD
wird nicht nur nicht beschrieben, sondern nicht einmal kopiert.

## 9. Warum keine Kanonisierung?

[FAKT] Der Hook setzt ausschließlich `raw/auto`, deutet nichts, vergibt keinen
verbindlichen Claim-Status, migriert nichts. Kopie ja — Deutung nein —
Kanonisierung verboten. Spätere Triage bleibt menschlich.
