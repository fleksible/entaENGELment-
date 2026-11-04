# Menschliche Absicht und technische Merge-Prüfung

**Version:** 0.1 — 2026-11-02  
**Status:** Arbeitsprinzip von Kevin im Gespräch bestätigt; konkrete Repo-Fassung zur Übernahme im PR  
**Authority-Status:** ANNEX / Arbeitsablauf  
**Durchsetzung:** Agentenanweisung über `AGENTS.md`; keine neue Runtime-Prüfung  
**Herkunft:** Gespräch im Anschluss an PR #442; Formulierung durch den Coding-Agenten

## 1. Vereinbarung

**Der menschliche Commit gilt der gewollten Wirkung und ihren Grenzen. Die technische
Übersetzung, Prüfung und begründete Merge-Empfehlung sind Aufgabe des Coding-Agenten.**

Die Zustimmung setzt keine eigene Beherrschung der Programmiersprache voraus. Der
Agent muss eine Entscheidung in die Sprache der menschlichen Absicht rückübersetzen
können: Was verändert sich, was ist daran belegt, welche Folgen bleiben offen?

Technische Kompetenz überträgt keine Autorität über Ziele oder Werte. Kann der Agent
eine technische Frage selbst nicht tragfähig beurteilen, benennt er die Lücke und
stellt zurück oder bereitet einen geeigneten fachlichen Review vor. Ein menschliches
Abnicken ersetzt diesen fehlenden Nachweis nicht.

## 2. Intuition und Zustimmung

Intuition darf Richtung, Priorität, Dringlichkeit oder Unbehagen anzeigen. Sie muss
nicht erst in Codesprache übersetzt werden, um als menschlicher Anlass ernst genommen
zu werden. Ihre technische Interpretation bleibt eine korrigierbare Lesart des Agenten.

Ein empfundenes Dringlichkeitsgefühl ist kein Beleg für einen technischen Befund und
keine eigenständige Erlaubnis zum Handeln. Maßgeblich ist die geäußerte Absicht samt
Kontext und Grenzen. Der Agent darf Zustimmung weder aus Stimmung noch aus Schweigen,
fehlenden Codekenntnissen oder einer vermuteten Intuition herstellen.

## 3. Ein begrenztes Mandat verwenden

Eine verständliche Freigabe benennt den Arbeitsgegenstand, das gewünschte Ergebnis,
wesentliche Grenzen und die erlaubte Ausführung. Sie kann ausdrücklich einschließen,
die geprüfte Umsetzung nach `main` zu übernehmen. Dazu ist kein festes Schlüsselwort
und kein vom Menschen geprüfter Commit-Hash erforderlich; der Handlungsumfang muss
aus dem geäußerten Auftrag eindeutig hervorgehen.

Beispiel für eine mögliche Freigabe, **keine bereits erteilte Erlaubnis**:

> Setze diese Absicht technisch um und übernimm die geprüfte Änderung in den Hauptstand.
> Bleibe bei diesem Ziel und den besprochenen Grenzen. Neue wesentliche Folgen oder
> Wertentscheidungen bringst du verständlich zu mir zurück.

Der Agent hält knapp fest, welche Äußerung welches Mandat trägt. Bereits passende
Autorisierung wird weiterverwendet. Technische Korrekturen innerhalb dieses Rahmens
brauchen kein wiederholtes Code-Abnicken. Nach Änderungen müssen die technischen
Nachweise zum tatsächlich übernommenen Stand passen; frühere grüne CI wird nicht
auf einen neuen Head übertragen. Der Agent prüft das, der Mensch muss dafür nicht
jede technische Revision erneut freigeben.

Diese Vereinbarung ist selbst kein Merge-Mandat. Sie erweitert weder einen Auftrag
zum Prüfen automatisch auf Ausführen noch eine einzelne Freigabe auf andere Aufgaben.

## 4. Wann die Entscheidung zum Menschen zurückkommt

Eine neue Entscheidung ist nötig, wenn Ziel oder Handlungsraum wesentlich wachsen,
etwa durch andere Empfänger, zusätzliche Veröffentlichung oder Deployment, neue Kosten,
schwerer rückgängig zu machende Folgen oder eine neue fachliche Wertsetzung. Auch eine
veränderte Risikolage außerhalb der vereinbarten Grenzen kommt zurück zum Menschen.
Die Dimensionen aus [ACTION_SCOPE_TRANSITIONS](ACTION_SCOPE_TRANSITIONS_v0_1.md)
helfen, solche Übergänge zu erkennen.

Die Rückfrage beschreibt genau diese Veränderung und ihre Folgen. Sie fordert keinen
stellvertretenden Code-Audit. Innerhalb eines bereits gedeckten Mandats wird kein
zusätzlicher Owner-Stop allein wegen technischer Implementierungsdetails erzeugt.
Fehlende Prüfbelege oder rote CI führen zur Nachbesserung beziehungsweise zum Halten.

Eine spätere Korrektur, Ablehnung oder Rücknahme des Menschen gilt für die weitere
Ausführung. Bereits erfolgte Änderungen werden als solche benannt; ein Revert erzeugt
einen nachvollziehbaren Folgeschritt und löscht die Geschichte nicht.

## 5. Form der Entscheidungsgrundlage

Bei einem neuen Entscheidungspunkt macht der Agent folgende Inhalte kurz und
alltagssprachlich zugänglich. Bekannter Kontext darf vorausgesetzt werden; dies ist
kein Pflichtformular für bereits gedeckte Routineausführung:

1. **So verstehe ich deine Absicht:** Ziel und Grenzen; offene Deutung kenntlich machen.
2. **Das bewirkt die Umsetzung:** beobachtbares Vorher/Nachher und wesentliche Folgen.
3. **Meine technische Empfehlung:** übernehmen, nachbessern oder zurückstellen; Belege und Grenzen.
4. **Was jetzt gedeckt ist:** bestehendes Mandat und nächster Schritt oder die konkret neue Entscheidung.

Technische Details bleiben im Prüfbericht zugänglich. Die Kurzfassung muss auch ohne
Diff-Lektüre eine wirksame Zustimmung oder Korrektur ermöglichen. Ein unbestimmtes
„Owner-Entscheidung offen“ genügt nicht, wenn es die technische Prüflast zurückreicht.

## 6. Herkunftsfall PR #442

Kevin bestätigte im Gespräch, PR #442 selbst manuell gemergt zu haben. Er beschrieb
die Dringlichkeit als eher gespürt als gewusst. Das dokumentiert seine berichtete
Entscheidungsmotivation. Die technische Begründung liegt getrennt davon im
[Prüfbericht](../audit/2026-11-02_pr442_denominator_followup.md).

Die alltagssprachliche Wirkung des Fixes: Unzuverlässige Berechnungen sollen keine
Freigabe vortäuschen; nicht berechenbare Eingaben sollen kontrolliert stoppen.
Der tatsächliche Merge ist [PR #442](https://github.com/fleksible/entaENGELment-/pull/442)
mit Commit `05712d827b5558b595438f38a1e3c7fc739a297f`. Diese einzelne Handlung
erteilt dem Agenten keine rückwirkende oder allgemeine Merge-Erlaubnis.

## 7. Geltungsgrenze und Revision

Diese Arbeitsvereinbarung beschreibt die Zusammenarbeit bei Repository-Änderungen.
Sie erzeugt keine `HumanDecision`-Events, keine Claim-Promotion und keine Ausnahme
von geschützten Bereichen, Receipts oder bestehenden Prüfpflichten.
Die [Consent-Zuordnung](CONSENT_RECORD_MAPPING_v0_1.md) und
[ADR-0005](../decisions/ADR-0005-erk-human-decision-precedence.md) bleiben getrennte
Verträge; eine Freigabe für einen Merge wird nicht als Zustimmung zu anderen
Requests oder Geltungsübergängen weiterverwendet.

Die Formulierung bleibt revidierbar. Änderungen am Delegationsrahmen selbst werden
dem Menschen als solche vorgelegt; der Agent autorisiert sie nicht mit diesem Text.
