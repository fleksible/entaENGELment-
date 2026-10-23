# Optischer Modellfall: Einzelschicht und Umweltwechsel

**Status:** ANNEX · DERIVED · [SPEC-WIP]

**Claim-Layer:** MODEL · **Promotion-Effect:** none

## 1. Wiedergefundene Quellform

[FAKT] Die autorisierte Arbeitsquelle enthält in §6 einen vollständigen
Python-Codeblock mit der Funktion `reflectance(wavelength_nm, n0, n1, n2, d_nm)`.
Ein separater ursprünglicher Skriptdateiname ist dort nicht angegeben.
Der zuvor gelesene reduzierte Fallplan enthielt diesen Block nicht.

[ANNEX] [tools/thin_film_reflectance.py](../../tools/thin_film_reflectance.py)
ist der jetzt neu gewählte Repo-Dateiname. Aus der privaten Quelle übernommen
werden nur Rechenkern, synthetische Parameter und Grenzen. Persönliche Geschichte,
Quelldateiname und Zugangskennungen werden nicht mitveröffentlicht.
Die öffentliche Prüfbarkeit betrifft den exportierten Rechenkern und den neuen Lauf.

[FAKT] SHA-256 des aus dem gelesenen Text extrahierten vollständigen ursprünglichen
Codeblocks, einschließlich Imports, Fälle und Assertions:
`54f000bb2e42b9f52dffaeff07d3acf71dc55721d4c4a3f03ef8e01417d1ac3d`.
Der Hash bindet diesen Textblock, nicht die ganze private Quelldatei oder ihre Genealogie.

## 2. Modell und Annahmen

[MODELL] Senkrechter Einfall auf eine homogene einzelne Schicht mit ebenen idealen
Grenzflächen. Reale positive, wellenlängenunabhängige Brechungsindizes; keine
Absorption oder Dispersion. n0 bezeichnet das Einfallsmedium, n1 die Schicht,
n2 das Substrat. d und die Vakuumwellenlänge λ werden in Nanometern eingesetzt.

```text
r01 = (n0 - n1) / (n0 + n1)
r12 = (n1 - n2) / (n1 + n2)
z = exp(-4π i n1 d / λ)
r = (r01 + r12 z) / (1 + r01 r12 z)
R = |r|²
```

[FAKT] Die öffentliche fachliche Anschlussstelle ist die Einzelschichtform der
Fresnel-Rechnung in Perez Grassi et al. (2013), §2, Gleichungen 1–3:
[Primärquelle](https://pmc.ncbi.nlm.nih.gov/articles/PMC3871123/),
DOI 10.3390/s131115747. Die eigene Rechnung ist eine vereinfachte illustrative
Anwendung, keine Reproduktion der Zweischichtmessung dieser Studie.

## 3. Reproduzierte Fälle

| Fall | n0 | n1 | n2 | d in nm | n1·d in nm | R bei 550 nm |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 1.000 | 1.500 | 1.333 | 200.0 | 300.0 | 2.4113728201 % |
| B | 1.333 | 1.500 | 1.333 | 200.0 | 300.0 | 0.1109724417 % |
| C | 1.000 | 1.600 | 1.333 | 187.5 | 300.0 | 2.7143386134 % |

[FAKT] Der wiedergefundene Originalblock wurde neu ausgeführt. Die extrahierte
Repo-Funktion liefert für alle neun Kombinationen aus A/B/C und 450/550/650 nm
dieselben Float-Werte. Die [Referenzdatei](../validation/fixtures/thin_film_reference_v0_1.json)
enthält Parameter, Annahmen und ungerundete Anteile zwischen 0 und 1.
Prozentwerte in der Tabelle sind lediglich anders dargestellte Modellwerte.

[MODELL] A gegenüber B hält Film, Dicke und Substrat fest; nur das Einfallsmedium
wechselt. Das Readout ändert sich. A gegenüber C erhält n1·d und die äußeren
Indizes, ändert aber die einzelnen Grenzflächenkoeffizienten. Damit scheitert in
diesem Fall die Behauptung, gleiche optische Dicke allein garantiere gleiche Reflexion.

## 4. Wiederholung und Gegenprüfungen

```bash
python3 tools/thin_film_reflectance.py
pytest tests/unit/test_thin_film_reflectance.py
```

[ANNEX] Die CLI schreibt deterministisches JSON auf stdout und benötigt nur die
Python-Standardbibliothek. Gegenüber dem Inlineblock ergänzen Typangaben,
Eingabeprüfung und JSON-Ausgabe die unveränderte Rechenform. Es werden keine
privaten Daten, Netzwerkaufrufe oder Messgeräte verwendet.

[FAKT] Die Tests prüfen die neun Originalwerte, den Umweltwechsel und den
Gegenfall gleicher optischer Dicke. Zusätzliche analytische Kontrollen:
Null-Dicke ergibt die direkte n0/n2-Grenzfläche; gleiche Indizes ergeben null
Reflexion; eine passende Viertelwellenschicht löscht Reflexion an ihrer
Designwellenlänge aus. Die ursprünglichen Spektralprüfungen über 400–700 nm
wurden wiederholt. Der vollständige Prüfstand steht im
[Audit](../audit/2026-10-23_optical_reproduction_review.md).

## 5. Erhaltene Grenzen

[ANNEX] Reproduziert wird die Rechnung, nicht der behauptete frühere Ausführungsakt.
Ein heutiger Lauf beweist nicht unabhängig, wann der ursprüngliche Lauf stattfand.
Die Referenzwerte und ihre neue Berechnung sind keine zwei unabhängigen
empirischen Belege.

[UNRESOLVED] Keine gemessene Öl-, Polymer- oder Federprobe; keine vollständige
Farbwahrnehmungsrechnung und keine Realmaterialvalidierung. Die drei betrachteten
Wellenlängen bestimmen keine wahrgenommene Farbe. Aus diesem Modell folgt weder
eine allgemeine Material-Umwelt-Äquivalenz noch ein neuer HUD-Phasenproducer.
