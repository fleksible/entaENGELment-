# Exchange Archive — Zwischenraum für ehemalige Bezüglichkeit

> [MODELL] Ein Schwellenraum zwischen INBOX (untrusted, unverarbeitet) und Kanon
> (`index/`, `spec/`, `VOIDMAP.yml`). Hier liegt, was *Bezug hatte*, aber **noch
> nicht** Kanon ist — und es vielleicht nie wird.

## Zweck

Dieser Ordner bewahrt **Provenienz** und **Kontext** früherer Austausche auf:

- ehemalige Bezüglichkeiten und frühere Gesprächsstände,
- Handoff-Zustände zwischen Sessions / Modellen / Menschen,
- externe Modell-Antworten,
- semantische Zwischenschichten,
- „war wichtig, ist aber noch nicht Kanon",
- „hat Bezug, darf aber nicht unmarkiert in den Kern wandern".

## Was dieser Ordner NICHT ist

- **Nicht Kanon.** Inhalte hier gelten nicht als geltende Spezifikation. Migration
  in den Kern erfordert expliziten Review + Consent (G0) und passende Claim-Grenze.
- **Nicht Müllablage.** Wer löschen will, beachtet G3 (Deletion-Verbot): verschieben
  nach `NICHTRAUM/archive/`, nicht hierher „entsorgen".
- **Nicht Beweisarchiv.** Aussagen hier sind **nicht** Evidenz. Evidenz lebt in
  `evidence/`, `receipts/`, `data/receipts/` mit eigener Integritätskette.
- **Nicht untrusted-Eingang.** Roh-/externe Eingaben gehören zuerst in `INBOX/`
  und werden gemäß `.claude/rules/security.md` (G5) geprüft, bevor ein
  Exchange-Record entsteht.

## Beziehung zu anderen Räumen

| Raum | Rolle |
|------|-------|
| `INBOX/` | untrusted, unverarbeitet (G5) |
| `docs/exchange_archive/` | **dieser Raum**: ehemalige Bezüglichkeit, markiert, mit Provenienz |
| `NICHTRAUM/maybe/` | Unentschiedenes (Pattern D) |
| `NICHTRAUM/quarantine/` | Verdächtiges (G5) |
| `index/`, `spec/`, `VOIDMAP.yml` | Kanon (GOLD) |

## Nutzung

1. Kopiere `TEMPLATE_exchange_record.md` nach
   `docs/exchange_archive/<exchange_id>.md`.
2. Fülle alle Felder aus; setze `claim_status` und `migration_candidate` ehrlich.
3. Trage einen Zeilen-Eintrag in `INDEX.md` ein.
4. Markiere `do_not_canonize_before`, falls eine Schwelle (Review/Evidence) offen ist.

> [METAPHER] Der Nektar reift in der Wabe, bevor er Honig wird — der Exchange-Raum
> ist die Wabe, nicht der Vorratstopf. *(Symbolisch, kein Beweis.)*
