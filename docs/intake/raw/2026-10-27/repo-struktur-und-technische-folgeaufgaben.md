# Repo-Struktur und technische Folgeaufgaben

Stand: 27. Oktober 2026 · DERIVED / REVIEW-PENDING · Lesekarte, kein Kanon.
Beobachtete Basis: `main@83caf03d6e8039637f147f1313238ca5cab611f6`.

## Was dieses Repository heute zusammenhält

[INFERENZ] entaENGELment ist technisch ein Verbund aus Governance-Verträgen,
Python-Prüf- und Modellcode, mehreren Oberflächen und einem wachsenden
Provenienz-/Dokumentationsraum. Diese Schichten haben unterschiedliche Aufgaben
und Prüfkriterien. Eine gemeinsame Ablage macht daraus noch keine durchgängig
verdrahtete Anwendung.

[FAKT] Die gepinnte Basis enthält 727 versionierte Dateien. Die Zählung liest
Git-Pfade mit NUL-Trennung; erzeugte Dateien, lokale Umgebungen und offene
PR-Deltas sind darin nicht enthalten. Dateimenge misst keine fachliche Reife.

| Schicht | Tatsächliche Orte | Wozu sie dient / entscheidende Grenze |
|---|---|---|
| Einstieg und Projektverständnis | `WELCOME.md`, `README.md`, `docs/START_HERE.md`, `REPOSITORY_ESSENZ_ANALYSE.md` | Verschiedene Lesetiefen. Ältere Analysen liefern Kontext; aktuelle Manifeste und Prüfungen bestimmen den heutigen Implementierungsstand. |
| Governance-Verträge | `AGENTS.md`, `CLAUDE.md`, `EPISTEMIC_HYGIENE.md`, `PRIVACY_BOUNDARY.md`, `GITHUB_USE_POLICY.md` | Regeln für Veränderung, Claim-Geltung und Öffentlichkeit. Ein dokumentierter Guard ist getrennt von seiner technischen Durchsetzung zu prüfen. |
| Geschützter Kern | `index/` (6 Dateien), `spec/` (7), `policies/` (6), `seeds/` (2), `VOIDMAP.yml` | GOLD; Änderungen brauchen konkrete menschliche Autorisierung. Der Schutzstatus ist kein empirischer Wahrheitsbeweis. |
| Python-Kern | `src/` (23) | Metriken, Gates, Stabilität, Ledger, Evidence Routing, Claim-Bridge und lesende Bridge-Projektion. ANNEX; Python bleibt eine eigene Domäne. |
| Prüf- und Arbeitswerkzeuge | `tools/` (31), `tests/` (62), `Makefile`, `pyproject.toml`, `uv.lock` | CLIs, Gegenfälle und Installationsvertrag. Tests belegen den geprüften Vertrag, nicht die Wahrheit aller Forschungsbilder. |
| Web-Oberfläche und geteilte Typen | `ui-app/` (50), `packages/` (6), `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `turbo.json` | Next.js mit separater Typ-, Lint-, Build- und Testsuite. Gemeinsame Typen spiegeln GOLD; sie schreiben es nicht um. |
| Desktop-Hülle | `main.js`, `preload.js`, `Index.html`, Root-`package.json` | Electron startet die lokale Oberfläche. Ein Next-Build oder Packaging-Glob-Test beweist keinen erfolgreichen Start des gepackten Desktop-Artefakts. |
| Weitere Modell-/Visualisierungsräume | `Fractalsense/` (46), `bio_spiral_viewer/` (7), `Plugins/` (9) | Eigene Python-/Jest-Pfade, Console-Viewer und Unreal-C++-Quellen. Ihre Laufzeitabdeckung darf nicht aus dem Kern-Pytest-Lauf abgeleitet werden. |
| Nachweise und Arbeitsstände | `receipts/`, `data/receipts/`, `ark/p4/receipts/`, `audit/`, `evidence/`, `docs/audit/`, `OUT/` | Receipts, Fixtures, Berichte und Laufspuren mit unterschiedlichem Status. Ein Name wie REAL oder ein Hash allein belegt keine externe Messung. |
| Aufnahme und offene Gedanken | `INBOX/`, `docs/intake/`, `docs/exchange_archive/`, `NICHTRAUM/` | Untrusted Eingang, datierter Intake, Provenienz und bewahrtes Unentschiedenes. Keine automatische Promotion in Spec oder VOIDMAP. |
| Aufgabensteuerung | `VOIDMAP.yml`, GitHub-Issues, offene PRs, `TASKS/`, `tickets/` | Unterschiedliche Register: fachliche Lücken, Arbeitspakete, konkrete Diffs und Arbeitsaufträge. Ihre Statuswerte werden nicht automatisch vereinigt. |

## Die wichtigsten Verbindungen

`SYNTHBIOSIS.md` beschreibt die souveränen Python-, JS/TS- und Governance-Domänen.
Für die praktische Navigation sind fünf Übergänge besonders relevant:

| Übergang | Was erhalten werden muss | Was daraus nicht automatisch folgt |
|---|---|---|
| Material → Intake / Suche | Originalquelle, Version, Sichtbarkeit, Textrepräsentation, Suchmodus | Quellenunabhängigkeit oder Bedeutungsidentität |
| Register → Claim-Bridge → ERK | benannte übertragene Eigenschaft, `known_loss`, erlaubte Relation, Review-Pointer | Identität zwischen Registern oder ein automatisch verliehenes FACT-Tag |
| ERK / Ledger → öffentliche Projektion | Schema/Policy-Bindung, erlaubte Statuswerte, reduzierte Feldmenge | Erlaubnis zur Veröffentlichung privater Quellen oder Rekonstruktion privater Bedeutung |
| Lauf → Receipt / Snapshot | tatsächlich ausgeführte Prüfung, Eingangsbytes, Parameter, Signaturstatus | Wahrheit des Inhalts, Autoridentität oder ein verpflichtend signierter CI-Lauf |
| Producer → Phase / Slice / HUD | Bedeutung der Größe, zwei Beobachtungen, Transformation, Identitäts-/Boundary-Bezug | Auswahl des Modells, Kη-03-Bindung oder Abschluss offener Sphären-/Graining-Fragen |

[FAKT] Die Claim-Bridge in `src/core/evidence_bridge_adapter.py` ist reine
Übersetzung. `bridge_view.py` ist eine lesende Projektion. Die geschützten
Governance-Texte, die Implementierung dieser Grenzen und der menschliche
Bedeutungsentscheid bleiben getrennte Ebenen.

## Was geprüft wird – und was separat bleibt

| Prüfpfad | Tatsächlicher Scope |
|---|---|
| `make verify` | Port-Lint, `tests/`, strenge Pointer-Prüfung und Claim-Lint |
| Strenger Claim-Lint | Zusätzlicher Lauf mit `--strict`; das normale Make-Ziel ist nicht automatisch dieselbe Strenge |
| `make verify-governance` | Workflow-Posture, VOID-Backlog-Drift und UI-VOID-Mirror |
| `make verify-js` | Eingefrorene pnpm-Installation und Turbo für Typprüfung, Lint, Build und Tests |
| FractalSense / Root-Jest | Eigene Pfade; kein Beleg aus ausschließlich bestandenem Kern-Pytest |
| `make status` / Signatur | Eigener Schritt. Ohne Schlüssel kann ein lokaler Status UNSIGNED sein; der PR-CI-Pfad darf Signing explizit überspringen |
| `make all` | Verify, Test und Snapshot; kein automatisches `make status` |
| Opt-in / externer Betrieb | Frame-Lint-Scope, echte DataLad-/Annex-Läufe, Electron-Paketstart und Owner-/Account-Prüfungen separat betrachten |

Installationsdetails gehören zum zentralen Vertrag unter `docs/ci/PYTHON_LOCK.md`
und `tools/python_lock.py`. Requirements-Exporte sind abgeleitete Produkte des
Locks, keine unabhängig zu pflegenden Paketwunschlisten.

## Main und offene PRs auseinanderhalten

Am 27.10. wurden zwölf offene PRs und vier offene Issues gefunden. Die PR-Heads
wurden direkt aufgelöst; für nicht vertieft geprüfte PRs wird kein Merge-PASS
behauptet. Die nachstehenden SHA-Werte bezeichnen den Eingang dieses Auftrags,
nicht die anschließend ergänzten Reparatur-Commits.

| PR | Eingang | Rolle / verbleibender Abschluss |
|---|---|---|
| [#423](https://github.com/fleksible/entaENGELment-/pull/423) | `af2d092dcff2136d675c10d80c6991d1a3bff714`, Draft | Phasen-/Sample-Kandidat. Bedeutungs- und Zuordnungsentscheidung bleibt offen; kein Adapterauftrag daraus erfinden. |
| [#425](https://github.com/fleksible/entaENGELment-/pull/425) | `673cbbfbfbf46377af6932daa242f3742378979c`, Draft | Datierter Auditbericht; Aussagen am jeweiligen Lauf halten, keine neue Modellwahl daraus ableiten. |
| [#426](https://github.com/fleksible/entaENGELment-/pull/426) | `2e82ff8f3ea552dbd473fe512eedc031b168226b`, Draft | Lesende Korpussuche. Bereits geprüfter Claim-Lint-Fix; Merge-Review und späterer Korpusadapter sind verschiedene Schritte. |
| [#427](https://github.com/fleksible/entaENGELment-/pull/427) | `d886c8e72633b561e4c6a80eb93c0f701b6bc2d0` | Reentry / RO-Crate. Folgekorrektur trennt externe gleiche Dateinamen über Quellen-IDs. Vorhandene versiegelte Erststände bleiben unverändert. |
| [#428](https://github.com/fleksible/entaENGELment-/pull/428) | `fc1aaec52b9e942266032a0afa564ef39c89e3b1` | Privates DataLad-Korpus. Folgekorrektur präzisiert Auswahlgrenze und lässt fehlende lokale Eingaben die Skriptlogs erreichen. |
| [#429](https://github.com/fleksible/entaENGELment-/pull/429) | `de11de19a6fdd77e447816161c841d98f3b6093e` | setup-python-Pin. Geprüfter begrenzter Merge-Kandidat; kein Custom-Mirror im Repo. |
| [#430](https://github.com/fleksible/entaENGELment-/pull/430) | `42d7e3f7db0227fc244d2641358c5a8f0e7566f0` | ESLint 10. Folgekorrektur gleicht Node-Vertrag und alten Kommentar ab; lokaler kompletter Workspace-Lauf besteht. |
| [#431](https://github.com/fleksible/entaENGELment-/pull/431) | `c110d98b23f8e57173d73cf387e36acc8338d532` | electron-builder. Eigener gezielter Packaging-Review bleibt erforderlich; in diesem Strukturauftrag nicht vertieft geprüft. |
| [#432](https://github.com/fleksible/entaENGELment-/pull/432) | `b61567e2ad4b0d4ce8c657e26449876a0a3cd54b` | Electron 45. Vorhandener Review fordert echten gepackten Desktop-Start; hier nicht ausgeführt. |
| [#433](https://github.com/fleksible/entaENGELment-/pull/433) | `ab553670dbd9d0844578ecd9805bd00df25f3928` | yaml. Eigener Abgleich mit den Parser-Verwendungen bleibt erforderlich; hier nicht als geprüft freigegeben. |
| [#434](https://github.com/fleksible/entaENGELment-/pull/434) | `be93ef7d085715557020de37e0f7899b6b129bf1` | React Query. Vorhandener Review empfiehlt Merge im derzeit unbenutzten Anwendungspfad; kein behaupteter neuer Query-Runtime-Test. |
| [#435](https://github.com/fleksible/entaENGELment-/pull/435) | `06c691a7edebeaaa1912248c2a1656442d147592` | Python-Gruppe. Vorhandener Review: Export-Drift und Safety-Konflikte; als Gesamtpaket HOLD. In diesem Auftrag keine neue Resolverprobe. |

Die Abhängigkeit `#428 sources → #427 save/verify` wurde in diesem Auftrag mit
echtem DataLad und synthetischen Dateien geprüft. Der Suchanschluss
`#428 → #426 --corpus` benötigt dagegen noch ein Manifest, das Original und
Textderivat mit eigener Identität und Leseabdeckung verbindet. Ein Verzeichnis
voller Textdateien ist noch kein solches Manifest.

## Reihenfolge der nächsten Arbeiten

| Reihenfolge | Arbeit / Zuständigkeit | Abschlusskriterium |
|---|---|---|
| 1 | Drei konkrete Reparaturen in #427/#428/#430 und diese Lesekarte bereitstellen | Kleine getrennte Diffs, lokale relevante Gates, anschließend aktuelle Head-CI und Review |
| 2 | Reentry + Korpus gemeinsam integrieren | Gleiche Basenames mit gleichen/verschiedenen Bytes, Hashabweichung, Missing-/Stale-Fälle, rerun und fsck bestehen |
| 3 | Reine Wartungs-Merge-Kandidaten #429/#434 getrennt abnehmen | Unveränderter geprüfter Scope und weiterhin grüne relevante Checks; kein pauschaler Sammel-Merge |
| 4 | #431/#433 gezielt reviewen und #432 paketiert starten | Tatsächlich genutzte Builder-/Parserpfade bzw. erfolgreicher Desktop-Smoke-Test auf beanspruchtem Ziel |
| 5 | #435 nach Verfahren aus [#416](https://github.com/fleksible/entaENGELment-/issues/416) aufteilen | Kompatible Updates im zentralen uv-Lock, vier Exporte, frische Installation, Tests und SBOM; Safety-/Filelock-Rest ausdrücklich offen |
| 6 | Korpus → Suche anbinden | Manifest je Original/Textderivat mit Quellenkennung, Hashes, Methode, Leseabdeckung und Verlustgrenze; private Daten bleiben lokal |
| 7 | Menschliche Phasenentscheidung aus [#418](https://github.com/fleksible/entaENGELment-/issues/418) bearbeiten, wenn gewählt | Eine Bedeutung und ein begrenzter Sample-/Boundary-Vertrag; erst dann opt-in Adapter samt Gegenfällen |
| 8 | Konto- und Forschungsreste gezielt fortsetzen | [#332](https://github.com/fleksible/entaENGELment-/issues/332): beobachtete Settings/Empfangstest; [#305](https://github.com/fleksible/entaENGELment-/issues/305): Originalscanner/Rohlisten und vorab definiertes Nullmodell |

[FAKT] VOIDMAP enthält 22 Einträge: zehn CLOSED, neun OPEN, zwei IN_PROGRESS,
einen SUSPENDED. CLOSED bedeutet jeweils den dokumentierten Closing-Path.
Beispiel VOID-011: deterministischer SIMULATION_PROXY-Export und Tests, keine
Messung realer zwischenmenschlicher Resonanz. Diese Übersicht ändert keinen
dieser Statuswerte.

## Lesestand und Herkunft

Direkt gelesen wurden die aktuellen Leitdateien, Struktur/Manifeste und relevante
Verknüpfungen in Python, UI, Tooling und CI sowie alle offenen PR-/Issue-Eingänge.
Die technische Vertiefung betrifft die drei jüngst besprochenen PRs und ihren
Reentry-/DataLad-Übergang. Keine vollständige semantische Lektüre aller 727
Dateien, kein Vollkorpus- oder universeller Security-Audit.

Der private Korpusindex und frühere Reviews dienten nur als Wegweiser. Der hier
öffentliche Text enthält ausschließlich öffentliche Repo-Bezüge und synthetische
Testergebnisse; keine privaten Quellen, Einzelhash-Inventare oder persönlichen
Gesprächsinhalte.

## Nachtrag: technische Übernahme am 27. Oktober

Die oben gepinnten Eingänge bleiben als Ausgangskarte erhalten. Nach erneuter
Head-/CI-Abnahme wurden #425, #426, #427, #428, #429, #430, #433 und #434
übernommen. #430 erhielt zuvor eine erneut geprüfte Lockfile-Auflösung gegen die
bereits gemergten React-Query-/YAML-Versionen. Gemeinsame lokale Abnahme:
859 Tests und 169 Subtests, Governance, strenger Claim-Lint, JS/TS und Root-Jest
bestanden. Die aktuelle Arbeitsliste und der datierte Mergebericht nennen die
tatsächlichen Commit-IDs und getrennten Abschlusskriterien.

#423 bleibt wegen der Bedeutungs-/Zuordnungsentscheidung offen, #431/#432 wegen
ausstehender Paketnachweise und #435 wegen der nicht erfüllten Lock-/Dependency-
Gates. Diese Grenzen werden nicht durch den technischen Merge verändert.
