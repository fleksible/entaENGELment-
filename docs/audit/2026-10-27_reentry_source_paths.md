# Reentry: externe Quellen mit gleichem Dateinamen

Stand: 27. Oktober 2026 · DERIVED / technischer Nachtrag zu PR #427.
Ausgangshead: `d886c8e72633b561e4c6a80eb93c0f701b6bc2d0`.

## Problem und Änderung

[FAKT] Zwei externe Quellen aus verschiedenen Ordnern mit demselben Dateinamen
wurden beide auf `payload/external/<name>` abgebildet. Eindeutige Manifest-IDs
verhinderten diese Kollision nicht; `save_state` brach vor der Zielanlage ab.

Neue Pakete verwenden `payload/external/<source-id>/<name>`. Die Quellen-ID ist
bereits normalisiert und eindeutig. Der Name eines Annex-Symlinks bleibt erhalten;
kopiert und gehasht werden weiterhin seine Inhaltsbytes. Repo-interne Pfade und die
Prüfung reservierter Kartenpfade bleiben beim bisherigen Vertrag.

Vorhandene Crates werden nicht umgeschrieben oder neu versiegelt. Ihre Pfade stehen
in den jeweiligen Metadaten und werden vom bestehenden Verifier geprüft.

## Ausgeführte Prüfung

- Vier neue Regressionen: gleicher Dateiname in verschiedenen Ordnern, gleiche und
  unterschiedliche Bytes, jeweils reguläre Dateien und Annex-artige Symlinks.
  Signiertes Speichern und Verifizieren bestehen mit getrennten Payload-Pfaden.
- Reentry-Suite: 67 bestanden; `make verify`: 808 Tests und 165 Subtests bestanden.
- Ruff, Black, mypy, Bandit, strenger Claim-Lint und Governance-Gates bestanden.
- Gemeinsame synthetische Probe mit dem korrigierten #428: echtes DataLad 1.7.1,
  git-annex 10.20261026; drei `save_state.md` aus verschiedenen Ordnern, davon zwei
  inhaltsgleich. Drei Payload-Pfade; `PASS / SIGNED_VALID`.
- Falsche deklarierte Quellhashes werden weiterhin vor Zielanlage abgewiesen;
  die bestehenden Manipulations-, Siegel- und Kartenprüfungen bleiben grün.

Der gemeinsame Lauf verwendet eigene synthetische Daten und einen künstlichen
Testschlüssel. Er ist ein Integrationsnachweis dieser beiden Werkzeugstände,
keine Prüfung privater Korpusoriginale und keine Herkunfts- oder Kanonfreigabe.
