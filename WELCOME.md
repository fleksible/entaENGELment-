# Willkommen bei entaENGELment

Falls du mit dem Wort **Repository** ungefähr so viel anfangen kannst, wie ich lange Zeit:

**Willkommen. Ich lerne die Mechanik davon ehrlich gesagt bis heute noch.**

Fürs Erste reicht völlig: Das hier ist ein Ort, an dem Dinge liegen. Manche sind fertig, manche werden ausprobiert, manche widersprechen einander, und manche bleiben absichtlich offen.

Du musst keinen Code verstehen, nichts installieren und nicht wissen, wie GitHub funktioniert. Du darfst lesen, springen, Fragen stellen, widersprechen, einen einzelnen Gedanken mitnehmen oder wieder gehen.

Es gibt hier keine richtige Reihenfolge und keinen Test am Eingang.

---

## Was möchtest du gerade tun?

Du musst dich nicht erst als Entwickler:in, Philosoph:in, Reviewer:in oder irgendetwas anderes einordnen.

- **Ich möchte nur schauen.**  
  Dann bleib einfach hier und folge dem, was interessant wirkt.

- **Ich möchte verstehen, worum es geht.**  
  Starte mit [`REPOSITORY_ESSENZ_ANALYSE.md`](REPOSITORY_ESSENZ_ANALYSE.md).

- **Ich möchte wissen, ob das solide ist.**  
  Schau in [`tests/`](tests/), [`docs/audit/`](docs/audit/) und [`CLAUDE.md`](CLAUDE.md).

- **Ich möchte technisch einsteigen.**  
  [`docs/START_HERE.md`](docs/START_HERE.md) ist die Werkstatt.

- **Ich möchte etwas beitragen.**  
  [`CONTRIBUTING.md`](CONTRIBUTING.md) erklärt die Spielregeln.

- **Ich weiß noch nicht, wonach ich suche.**  
  Auch das ist ein gültiger Ausgangspunkt.

Keiner dieser Wege ist der „richtige“.

---

## Was ist entaENGELment?

entaENGELment ist ein experimentelles, consent-first und anti-capture orientiertes Forschungs- und Governance-Framework für menschengeführte, überprüfbare und teilweise mythopoetische Systeme.

Einige Teile sind Code. Andere sind Governance, Tests, Forschung, Philosophie, Narration oder bewusst offene Fragen.

Das Projekt ist **kein** fertiges Produkt, **kein** Production-Security-System und **kein** empirischer Beweis seiner symbolischen Modelle.

Es soll auch nicht zu einer Überwachungsarchitektur, einem semantischen Profiling-System, einer versteckten Personalisierungsschleife oder einer Lock-in-Maschine werden.

Symbolische Sprache ist willkommen. Sie ersetzt hier aber keine Evidenz.

---

## Wer spricht hier eigentlich?

Dieses Projekt entsteht in einem dokumentierten Dialog zwischen einem Menschen und verschiedenen KI-Instanzen.

Das wird nicht versteckt und nicht als Qualitäts- oder Autoritätsargument verwendet.

KI-Beiträge werden nicht dadurch wahrer, dass sie von einer KI stammen. Menschliche Beiträge werden nicht dadurch richtiger, dass sie menschlich sind. Was in dieses Repository übernommen wird, bleibt als menschlicher Commit, Review und nachvollziehbare Entscheidung sichtbar.

Du musst KI weder mögen noch ihr vertrauen, um das Projekt lesen oder kritisieren zu können.

Das Ziel dieser Transparenz ist nicht, Skepsis auszuräumen. Sie soll nur verhindern, dass über die Herkunft einer Formulierung oder Struktur eine falsche Geschichte erzählt wird.

---

## Was hier zuerst zählt

> Beziehung ohne Vereinnahmung.  
> Übersetzung ohne Identitätsbehauptung.  
> Herkunft sichtbar lassen.  
> Offenen Rest erlauben.  
> Grenzen und Rückzug respektieren.

Technisch zeigt sich das unter anderem in:

- Consent- und Boundary-Guards,
- Claim-Status und Provenienz,
- Tests und auditierbaren Receipts,
- geschützten offenen Zuständen (VOIDs / Kenogramme),
- reversiblen Revisionen und Forks,
- Anti-Capture- und Privacy-Grenzen.

Das sind Designziele und Arbeitsregeln, keine Behauptung einer universalen Ontologie.

---

## Die Schichten des Hauses

1. **Governance**  
   Consent, Grenzen, Review-Gates, Claim-Status und Anti-Overclaim-Regeln.

2. **Verification**  
   Wiederholbare Checks wie `make verify`, Pointer-Validierung, Claim-Linting, Tests und Receipts.

3. **Gläserne Agora & Receipt-Ledger**  
   Ein user-souveräner Claim-Raum. Bedeutungen sollen hinzugefügt, revidiert, geforkt oder zurückgenommen werden können, ohne ältere Aussagen still zu überschreiben.

4. **Essence Architecture**  
   Öffentliche symbolische und visuelle Grammatik, Schemas, Prompt-Module, Operatoren, Gates und Tests.

5. **Commons & Anti-Capture**  
   Offene Entwicklung ohne Profiling, versteckte Personalisierung, private-data extraction oder Lock-in als Designziel.

6. **Exploration**  
   Der Forschungsraum für Resonanz, Membranen, VOID, tesser3TAKT, Grimm Narration 2.0 und Mensch–KI-Koordination.

Du musst diese Schichten nicht in dieser Reihenfolge lesen.

---

## Wenn du wirklich Code ausführen möchtest

Wenn du jetzt freiwillig `git clone` lesen möchtest: **Ab hier beginnt die Werkstatt.**

Der praktische technische Einstieg lebt in [`docs/START_HERE.md`](docs/START_HERE.md).

Der kürzeste Verify-Pfad ist:

```bash
git clone https://github.com/fleksible/entaENGELment-.git
cd entaENGELment-
make install-dev
make verify
```

Für die optionale UI:

```bash
corepack enable
pnpm install --frozen-lockfile
pnpm --filter entaengelment-ui dev
```

Wenn du nur lesen möchtest, brauchst du davon nichts.

---

## GitHub als öffentlicher Raum

GitHub wird hier als öffentlicher Entwicklungs-, Dokumentations- und Witness-Layer verwendet.

Es darf öffentlichen Code, Dokumentation, Schemas, Tests, reduzierte Integrity-Anker und Audit-Notizen enthalten.

Es soll **nicht** zum semantischen Generator privater Nutzerdaten werden.

Standardmäßig nicht nach GitHub gehören:

- private rohe User-Claims,
- private Nutzerbilder,
- persönliche symbolische Profile,
- Embeddings privater Inhalte,
- inferierte psychologische Profile,
- private Ledger-Exporte,
- versteckte Personalisierungsschleifen,
- aus privaten Nutzerdaten erzeugte Prompt-Seeds.

> GitHub darf Integrität bezeugen, aber nicht heimlich Bedeutung aus privaten Nutzerdaten erzeugen.

Siehe auch [`GITHUB_USE_POLICY.md`](GITHUB_USE_POLICY.md) und [`PRIVACY_BOUNDARY.md`](PRIVACY_BOUNDARY.md).

---

## Anti-Capture

Kommerzielle Nutzung und extractive capture sind nicht dasselbe.

Das Projekt richtet sich gegen Überwachung, Profiling, versteckte Personalisierung, semantische Extraktion und Lock-in. Was davon rechtlich durchsetzbar ist, hängt von Lizenz, Contribution-Regeln und konkretem Deployment ab.

Siehe [`ANTI_CAPTURE_POLICY.md`](ANTI_CAPTURE_POLICY.md) und [`LICENSE_REVIEW.md`](LICENSE_REVIEW.md).

---

## Wenn du etwas beitragen möchtest

Kleine, fokussierte Beiträge sind ausdrücklich willkommen.

Ein Tippfehler zählt. Eine unklare Stelle zählt. Eine kritische Frage zählt. Ein Test zählt.

Niemand muss beim ersten Besuch gleich einen Compiler mitbringen.

Die vollständigen Regeln stehen in [`CONTRIBUTING.md`](CONTRIBUTING.md). Die technischen und Governance-Grenzen bleiben dort absichtlich streng; sie schützen Änderungen, nicht den Status einer Person.

Wenn du unsicher bist, wähle die kleinere Änderung — oder öffne erst eine Frage.

---

## Noch ein letzter Satz

Du musst dieses Projekt nicht mögen, übernehmen oder vollständig verstehen, um hier willkommen zu sein.

**Die Tür ist ein Angebot, kein Funnel.**
