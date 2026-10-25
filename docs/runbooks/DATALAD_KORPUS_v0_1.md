# Runbook: Privates Korpus als DataLad-Dataset (v0.1)

**Status:** [SPEC-WIP] · **Authority:** ANNEX · **Werkzeug:** [`tools/corpus_datalad.py`](../../tools/corpus_datalad.py)
**Dataset-Skripte:** [`tools/corpus_code/`](../../tools/corpus_code/) · **Tests:** [`tests/unit/test_corpus_datalad.py`](../../tests/unit/test_corpus_datalad.py)

> [MODEL] Die Originale des Korpus liegen inhaltsadressiert (SHA-256) im git-annex eines
> privaten DataLad-Datasets; Extraktion und Inventar sind per `datalad run` aufgezeichnet
> und mit `datalad rerun` wiederholbar. Das Dataset liegt **lokal** und **außerhalb jedes
> Git-Repos**; dieses Werkzeug legt kein Remote an und überträgt nichts ins Netz.

---

## 0. Grenzen

| Gilt | Gilt nicht |
|------|------------|
| Jede importierte Datei ist per SHA-256 gebunden; `git annex fsck` prüft Inhalt gegen Schlüssel. | Kein Beleg für Wahrheit, Datum oder Urheberschaft eines Inhalts. |
| Extrahierter Text ist reproduzierbar (`datalad rerun` erzeugt bytegleiche Ausgaben, im Prototyp geprüft). | Text aus PDF/DOCX ist eine Lesehilfe; Layout, Bilder, Formeln können fehlen. |
| `public_anchor.json` enthält keine Dateinamen, nur Anzahl und Wurzelhash. | Die Einzelhashes in `inventory.json` sind privat (Bestätigungsangriff möglich). |
| Import aus einem Ordner-Export; Drive-Datei-IDs werden nicht übernommen. | Keine Zuordnung zur Drive-Datei-ID (der Drive-Connector liefert keine Prüfsummen). |

## 1. Einmalig installieren (eigener Rechner)

Quelle: [DataLad-Handbuch, Installation](https://handbook.datalad.org/en/latest/intro/installation.html).

| System | Befehle |
|--------|---------|
| macOS | `brew install datalad` (zieht git-annex mit) · für PDF: `brew install poppler` |
| Debian/Ubuntu | `sudo apt-get install datalad` (zieht git-annex mit; neuere Versionen über NeuroDebian) · für PDF: `sudo apt-get install poppler-utils` |
| Windows | WSL2 und dann die Linux-Befehle, oder nativ: `uv tool install git-annex` und `uv tool install datalad` |

Prüfen: `datalad --version`, `git annex version`, `pdftotext -v` (optional; ohne `pdftotext`
werden PDFs im Log als `skipped` geführt, nicht still ausgelassen).

Das Werkzeug braucht nur das entaENGELment-Repo und Python ≥ 3.10; keine weiteren Pakete.

## 2. Drive-Ordner exportieren

1. In Google Drive den Ordner **„entaENGELment Sortieren“** herunterladen (Rechtsklick → Herunterladen).
   Drive liefert Zip-Dateien; Google-Dokumente werden dabei in Office-Formate umgewandelt.
2. Alle Teile in **einen** Staging-Ordner entpacken, z. B. `~/korpus-staging/2026-10-25/`.
3. Zips **im** Korpus (Repo-Snapshots, Generator-Pakete) **nicht** entpacken: Das Inventar
   hasht ihre Mitglieder, ohne sie auszupacken, und findet so Duplikate auch über Archive hinweg.

## 3. Dataset anlegen und importieren

```bash
cd ~/pfad/zu/entaENGELment-          # nur für den Aufruf des Werkzeugs
python3 tools/corpus_datalad.py init --dataset ~/korpus
python3 tools/corpus_datalad.py import --dataset ~/korpus \
  --from ~/korpus-staging/2026-10-25 --label "Drive entaENGELment Sortieren 2026-10-25"
```

- `init` verweigert Ziele in einem Git-Arbeitsbaum (insbesondere im öffentlichen Repo) und nicht-leere Ordner.
- `import` kopiert nach `inbox/<label>/`, prüft jede Kopie per SHA-256, schreibt
  `derived/inventory/imports/<label>.json` und speichert mit `datalad save`. Symlinks werden
  nicht übernommen (im Record vermerkt). Git-Steuerdateien aus dem Export (`.git`,
  `.gitattributes`, `.gitignore`, `.gitmodules`) werden mit Suffix `~import` als gewöhnliche
  Daten abgelegt (`stored_as` im Record), damit sie im Dataset nicht wirken. Ein Label wird nie
  überschrieben.
- Der Staging-Ordner bleibt unverändert; löschen erst, wenn `git annex fsck` im Dataset sauber ist.

## 4. Textextraktion und Inventar (`datalad run`)

```bash
python3 tools/corpus_datalad.py extract --dataset ~/korpus
python3 tools/corpus_datalad.py inventory --dataset ~/korpus
```

| Ergebnis | Inhalt |
|----------|--------|
| `derived/text/<pfad>.txt` | Text je Quelle (Markdown/Text direkt, DOCX per Standardbibliothek, PDF per `pdftotext`) |
| `derived/text/_extraction_log.json` | je Datei: Status `ok`/`skipped`/`error`/`missing`, Eingangs- und Ausgangshash; `stale_outputs` statt Löschen |
| `derived/inventory/inventory.json` | Größe und SHA-256 je Datei, Duplikatgruppen, Zip-Mitglieder mit Hash, Duplikate über Archive |
| `derived/inventory/SUMMARY.md` | Kennzahlen und größte Duplikatgruppen |
| `derived/inventory/public_anchor.json` | `entryCount`, `distinctContentCount`, `snapshotRootHash` — ohne Dateinamen |

Beide Läufe nutzen die beim `init` kopierten Skripte unter `code/`; der Run-Record in der
Commit-Nachricht nennt Befehl, Eingaben und Ausgaben.

## 5. Prüfen und wiederholen

```bash
cd ~/korpus
git log --oneline                    # import / [DATALAD RUNCMD] extract / inventory
datalad rerun <commit>               # Lauf wiederholen; gleiche Ausgaben → kein neuer Commit
git annex fsck                       # Inhalte gegen ihre SHA-256-Schlüssel prüfen
datalad status                       # nichts Ungespeichertes
```

Fehlt Inhalt lokal (`missing` in Log/Inventar): `datalad get <pfad>`.

## 6. Anschluss an Save States (`/tesser3takt-reentry`)

```bash
python3 tools/corpus_datalad.py sources --dataset ~/korpus --glob "*Save_State*"
```

Gibt `sources`-Einträge mit absolutem Pfad und `sha256` aus. In ein Save-State-Manifest
übernommen, prüft `tools/reentry_crate.py save` den Hash gegen die Datei und bricht bei
Abweichung ab. Voraussetzung: `tools/reentry_crate.py` aus PR #427.

## 7. Später, bewusst und getrennt

- **Drive als Speicher:** git-annex-Remote über rclone
  ([git-annex: rclone](https://git-annex.branchable.com/special_remotes/rclone/)); vorher rclone
  bei Google anmelden, Verschlüsselung (`encryption=…`) erwägen.
- **Privates GitHub für Versionsgeschichte:** `datalad create-sibling-github --private …`;
  GitHub hostet dabei keine annex-Inhalte
  ([Doku](https://docs.datalad.org/en/stable/generated/man/datalad-create-sibling-github.html)).
- **Öffentlicher Anker:** Nur `snapshotRootHash` und `entryCount` aus `public_anchor.json`
  dürfen in das öffentliche Repo, und nur als bewusster Schritt (PRIVACY_BOUNDARY.md).
