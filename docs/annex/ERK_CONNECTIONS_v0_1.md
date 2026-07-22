# ERK_CONNECTIONS_v0_1

**Status:** Draft
**Claim-Status:** [SPEC-WIP]
**Authority-Status:** ANNEX
**Datum:** 2026-07-21
**Bezug:** [EVIDENCE_ROUTING_KERNEL_v0_1.md](EVIDENCE_ROUTING_KERNEL_v0_1.md)

Dieses Dokument beschreibt die ersten Anschlusswerkzeuge rund um den Evidence
Routing Kernel v0.1a. Alle Werkzeuge sind ANNEX, rein lesend oder append-only,
und keines trifft eine Entscheidung, die dem Menschen vorbehalten ist.

---

## 1. Intake-Adapter (`tools/erk_intake_adapter.py`)

Verbindet den Calm Intake Layer (Pattern F) mit dem Kernel: Ein Intake-Artefakt
wird als `MATERIAL_REGISTERED`-Event erfasst — Pfad, SHA-256-Digest und
Metadaten, **niemals der Rohinhalt**.

- Trust-Default ist `UNTRUSTED` (G5); unbekannte Trust-Angaben werden auf
  `UNTRUSTED` reduziert, nie aufgewertet. Der Adapter besitzt bewusst keinen
  Trust-Upgrade-Parameter; eine spätere Aufwertung braucht einen getrennten,
  review-gebundenen Prozess. Die Policy-Regel `intake_first` (alles beginnt als
  ROHSEDIMENT) wird damit technisch gespiegelt.
- Rein lesend gegenüber `docs/intake/`; append-only gegenüber dem
  Ziel-Eventstream (Ledger-Hash-Chain, `ledger.event()`).
- Ohne `--ledger` läuft der Adapter als Dry-Run.
- Der Kernel garantiert bereits (Invariante 8), dass untrusted Material nie
  allein eine Promotion trägt.

```bash
make erk-intake FILE=docs/intake/raw/2026-07-21/wrapup.md
make erk-intake FILE=... LEDGER=out/erk/erk_events.jsonl
```

## 2. Verify-Emitter (`tools/erk_verify_emit.py`)

Zeichnet Verify-Läufe als `VERIFY_PASS` / `VERIFY_PASS_UNSIGNED` auf — das
Vokabular stammt aus `spec/runtime_eventlog_v0_1.json`, der Transport ist die
öffentliche `ledger.event()`-API. Damit wird der DeepJump-Prozess selbst zur
replaybaren Eventgeschichte.

- Kein Ersatz für `make status` (HMAC-Receipt); nur eine Eventspur.
- Das Event dokumentiert, dass ein Lauf stattfand — es macht kein Ergebnis wahr.
- `actor` ist ein Rollen-Label, keine authentifizierte Identität (siehe
  Kernel-Spec §9.1).

```bash
python tools/erk_verify_emit.py --scope core
python tools/erk_verify_emit.py --scope core --unsigned --reason "no HMAC secret"
```

## 3. VOID-Resonanz-Report (`tools/erk_void_resonance.py`)

Liest `VOIDMAP.yml` (GOLD, **nur lesen**) und einen ERK-Eventstream und stellt
beide Seiten nebeneinander: offene VOIDs, Claims aktuell in `[VOID]`, und wie
viele Evidence-Relationen sich je `[VOID]`-Claim ansammeln.

- Es gibt **keine** automatische Verknüpfung zwischen `claim_id` und VOID-IDs.
- Der Report schließt nichts und schlägt keine Schließung vor — VOID ist ein
  gültiger Dauerzustand (Invariante 5). Ansammelnde Relationen sind Hinweise
  auf menschliche Review-Kandidaten, kein Evidenz-Urteil.
- Kompassnadel, kein Entscheider.

```bash
python tools/erk_void_resonance.py --stream out/erk/erk_events.jsonl
python tools/erk_void_resonance.py --stream ... --out OUT/erk_void_resonance.md
```

## 4. Guard-Drill (`tools/erk_drill.py`, `make erk-drill`)

Replayt die fünf ERK-Fixtures als lebende Grenz-Übung (im Geist von
`docs/governance/GUARD_DRILL_CONTRACT_v0_1.md`) und zeigt menschenlesbar, dass
die Grenzen halten: Proposal bleibt Vorschlag, Retagging braucht den Menschen,
Metapher trägt nicht, Rücknahme löscht nichts, der Export bleibt reduziert.

- Rein lesend; erzeugt keine Events und keine Dateien.
- Ergänzt die Testsuite, ersetzt sie nicht: `HÄLT`/`BRUCH` je Fixture statt
  eines anonymen grünen Balkens.

```bash
make erk-drill
```

---

## 5. Entscheidungsnotiz: Claim-Lint ↔ Draft-Register (nicht umgesetzt)

`docs/audit/CLAIM_TAG_RUNTIME_MAPPING_v0_1.md` §6 hält die offenen Fragen einer
Linter-Angleichung fest. Der Kernel liefert inzwischen die Bausteine, mit denen
`tools/claim_lint.py` das Draft-Register konsumieren *könnte*:

- `load_claim_policy()` — eine Quelle für Tags samt Version und SHA-256-Digest,
- `normalize_claim_tag()` — dieselbe Alias-Behandlung wie zur Laufzeit,
- `POLICY_DIGEST_MISMATCH` — Drift würde sichtbar statt still.

Offen bleiben (bewusst **nicht** hier entschieden):

1. Akzeptiert der Linter Register-Tags nur, oder werden auch Transitionen geprüft?
2. Bleiben `[TODO]`/`[RISK]` auxiliary marker?
3. Scope-Erweiterung auf `docs/`/`policies/` oder separater Dokument-Linter?
4. Umgang mit historischen Receipts (IMMUTABLE — niemals umschreiben)?
5. Failure- und Rücknahmebedingungen bei False Positives?

Eine Umsetzung wäre ein eigener Code-/Policy-PR mit eigener Review. Diese Notiz
erzeugt **keine** neue kanonische VOID-ID und verändert `VOIDMAP.yml` nicht;
sie ist ein ANNEX-Vermerk, kein Backlog-Eintrag.

## 6. Zurückgestellt (HOLD)

- **`tools/erk_audit.py`** (Fountain-CLI): auf Wunsch des Projektinitiators
  temporär zurückgestellt.
- **UI-Fountain-Ansicht** (`ui-app/`): wartet, bis PR #304 (tesser3TAKT HUD)
  und PR #312 (Frame Contract) entschieden sind — keine Berührung offener PRs.
  Der reduzierte Export (deterministische exportlokale Referenzen, keine
  Roh-IDs) ist als spätere Datenquelle bereits dafür ausgelegt.
- **tesser3TAKT-Adapter**: unverändert nur dokumentierter Adapterpunkt
  (Kernel-Spec §12).

## 7. Grenzen aller Anschlüsse

- Kein Werkzeug retaggt, promotet, schließt VOIDs oder synthetisiert eine
  HumanDecision.
- Kein Werkzeug schreibt in GOLD-Bereiche (`index/`, `policies/`,
  `VOIDMAP.yml`), in Receipts oder in `NICHTRAUM/`.
- Die Schreibwerkzeuge erzwingen diese Grenze nach Pfadauflösung; ein CLI-
  Zielparameter kann sie nicht überschreiben oder über einen vorhandenen
  Symlink umgehen.
- Ledger-Hash-Chain, DeepJump-Receipts und ERK-State-Digest bleiben drei
  getrennte Integritätszeugnisse; keines beweist Wahrheit, Authentizität oder
  Autorenschaft.
