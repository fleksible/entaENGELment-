# HOSPITALITY_ENTRY_GRAMMAR_v0_1

**Status:** INTAKE · [SPEC-WIP] · [HOSPITALITY]  
**Authority-Status:** DERIVED  
**Runtime:** none  
**Persistence:** none  
**Promotion-Effect:** none  
**Human-Commit:** required

## 0. Zweck

Dieser Intake beschreibt eine Gastfreundschaftsgrammatik für öffentliche Einstiegspunkte des Repositories. Er ist keine Policy-Promotion und keine Vorgabe für alle Texte.

Die Grundfolge lautet:

```text
OFFER -> ORIENTATION -> BOUNDARY -> COMMITMENT
```

Ein Besucher soll eintreten können, bevor technische Kompetenz, Rollenwahl, Beitrag oder Zustimmung zur Projektdeutung verlangt werden.

## 1. Entry-Invarianten

```text
welcome != persuasion
warmth != fake_human_authenticity
ai_transparency != ai_marketing
self_irony != reader_irony
boundary != gatekeeping_of_person
contribution_standard != competence_test
no_question_yet == valid_entry_state
exit == legitimate
```

## 2. Humor

Humor darf sich richten auf:

- die eigene Lernkurve;
- GitHub-Jargon;
- Projektkomplexität;
- gemeinsame Unsicherheit;
- die Absurdität, dass Werkzeuge oft komplizierter benannt werden als nötig.

Humor darf sich nicht richten auf:

- technische Unkenntnis des Lesers;
- KI-Skepsis;
- Nicht-Techniker;
- Fehler eines Beitragenden;
- Alter, Bildung, Herkunft oder vermeintliche Kompetenz.

Ein guter Entry-Joke senkt Statusgefälle, ohne eine Person zum Gegenstand des Witzes zu machen.

## 3. AI-Transparenz

Öffentliche Entry-Texte dürfen offen sagen, dass Teile des Projekts im Dialog zwischen Mensch und KI-Instanzen entstehen.

Dabei gilt:

```text
ai_origin != authority
human_origin != authority
ai_disclosure != trust_request
human_voice != proof_of_authenticity
```

Die Offenlegung soll keine KI-Skepsis behandeln oder überwinden. Sie soll nur die Herkunft einer Formulierung oder Struktur nicht verschleiern.

## 4. Rollenfreiheit

Der Einstieg darf Wege anbieten, aber keine Identität verlangen.

Erlaubt:

```text
nur schauen
Grundidee verstehen
prüfen/kritisieren
technisch einsteigen
beitragen
noch nicht wissen
```

Nicht erforderlich:

```text
"Ich bin Entwickler"
"Ich bin Philosoph"
"Ich bin AI-friendly"
"Ich bin Contributor"
```

## 5. Rückzugsrecht

Lesen verpflichtet nicht zu:

- Zustimmung;
- Beitrag;
- Account-Aktion;
- lokaler Installation;
- Rollenwahl;
- Datenteilung;
- weiterem Aufenthalt.

Die Entry-Struktur darf technisch strenge Bereiche sichtbar machen, aber sie darf Strenge nicht als sozialen Kompetenzfilter einsetzen.

## 6. Acceptance Checks

Ein Hospitality-Entry besteht den v0.1-Check nur, wenn:

1. ein nicht-technischer Leser ohne Installation einen sinnvollen Weg findet;
2. technische Einstiegspunkte weiterhin klar erreichbar sind;
3. AI-Kollaboration transparent, aber nicht werbend beschrieben wird;
4. KI-Skepsis weder pathologisiert noch ironisiert wird;
5. Humor nicht auf Kosten des Lesers funktioniert;
6. "ich weiß noch nicht" ein legitimer Zustand bleibt;
7. Beitragspflichten erst nach einer freiwilligen Mitmach-Entscheidung erscheinen;
8. Governance-, Test- und Sicherheitsregeln inhaltlich nicht aufgeweicht werden.

## 7. Scope

Dieser Intake betrifft zunächst nur:

- `README.md`
- `WELCOME.md`
- `docs/START_HERE.md`
- `CONTRIBUTING.md`

Nicht betroffen:

- GOLD;
- Policies;
- VOIDMAP;
- Runtime-Wires;
- tesser3TAKT transport;
- Rosetta v0.2;
- zGWSTN;
- Ledger;
- FEP.

**Verdict:** HOLD bis ein fremder Reader die Entry-Pfade ohne Entstehungskontext verständlich findet.
