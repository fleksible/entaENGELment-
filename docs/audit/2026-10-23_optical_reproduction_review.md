# Optischer Modellfall: wiedergefundener Code und Wiederholung

**Datum:** 2026-10-23

**Status:** ANNEX · DERIVED · Reviewfassung

**FOKUS:** optisches Modell reproduzieren

**Basis:** `a476404d095bd6dcec965953d69a19eae8153f69`

## 1. Herkunftskorrektur und Umfang

[FAKT] Bei der gezielten Suche nach dem ursprünglichen Skriptnamen wurde die
vollständige Arbeitsquelle gelesen. Ihr §6 enthält den Python-Codeblock,
Modellannahmen, drei Parametersätze und Konsistenzprüfungen. Der zuvor gelesene
reduzierte Fallplan enthielt diesen Block nicht. Die Aussage, eine ausreichend
gebundene Codequelle sei noch nicht gefunden, war damit ein vorläufiger Suchstand.

[FAKT] Ein ursprünglicher separater Dateiname ist in der gefundenen Fassung
nicht angegeben. Die Funktion heißt `reflectance`. Der neue Repo-Dateiname
`tools/thin_film_reflectance.py` wird ausdrücklich als jetzige Extraktion geführt.

[ANNEX] Der bereits autorisierte vierte Roadmap-Schritt wird mit dieser Quelle
fortgesetzt. Öffentlich exportiert werden nur der Rechenkern, synthetische
Parameter, neue Laufwerte und ihre begrenzte Einordnung. Private Quelldateinamen,
Zugangskennungen und die persönliche Entstehungsgeschichte bleiben separat.
Die Herkunftsreduktion ist keine öffentlich vollständige Genealogie.

## 2. Tatsächliche Wiederholung

[FAKT] Der extrahierte Originalblock mit SHA-256
`54f000bb2e42b9f52dffaeff07d3acf71dc55721d4c4a3f03ef8e01417d1ac3d`
wurde neu ausgeführt. Seine neun Werte für A/B/C bei 450/550/650 nm stimmen im
lokalen Interpreter exakt mit der extrahierten Repo-Funktion überein. Die früher
berichteten gerundeten Werte bei 550 nm werden wieder erhalten: 2.411 %, 0.111 %
und 2.714 %. Diese heutige Ausführung bestätigt nicht unabhängig das Datum oder
die Ausführungsgeschichte des früheren Laufs.

[ANNEX] [Modellkarte](../annex/OPTISCHER_MODELLFALL_v0_1.md),
[Rechenskript](../../tools/thin_film_reflectance.py),
[Referenzwerte](../validation/fixtures/thin_film_reference_v0_1.json) und
[Tests](../../tests/unit/test_thin_film_reflectance.py) bilden den reproduzierbaren
öffentlichen Umfang. Numerische Regressionen verwenden rel=1e-12 und abs=1e-15;
plattformübergreifende Bytegleichheit von Float-Ausgaben wird nicht behauptet.

## 3. Positive Kontrolle und scheiternde Verbindung

[MODELL] A/B verändert ausschließlich das Einfallsmedium und erhält Film, Dicke
und Substrat. Das Readout ändert sich. A/C erhält die optische Dicke n1·d = 300 nm,
aber nicht die Reflexion. Gleiche optische Dicke allein ist hier kein hinreichendes
Äquivalenzkriterium. Der Gegenfall erklärt sich im deklarierten Modell durch die
verschiedenen Grenzflächenkoeffizienten.

[FAKT] Null-Dicke, überall gleiche Indizes und eine ideal angepasste
Viertelwellenschicht liefern zusätzliche analytische Grenzfälle. Das ist eine
Konsistenzprüfung der Modellrechnung, keine Materialmessung.

## 4. Validierung und verbleibende Grenze

[FAKT] Die 22 neuen Tests bestehen. Die vollständige lokale Prüfung besteht mit
731 Python-Tests und 165 Subtests, Port-Lint, Core-Pointern und Claim-Lint.
Governance bleibt mit 15 Workflows und 22 VOID-Einträgen konsistent. Ruff und Black
prüfen beide neuen Python-Dateien, Mypy das Rechenskript. Lokale Links, JSON und
Diff wurden geprüft. Die bekannten vier optionalen generierten Pfade fehlen weiterhin.

[ANNEX] Es werden keine JS-/UI-Dateien, Lockdateien, GOLD-Bereiche oder bestehenden
Receipts geändert. Der bestehende Claim-Lint erfasst die neuen Annex-Texte nicht;
deren Reichweite wurde redaktionell geprüft. Der Code-Reproduktions-HOLD aus dem
Vorgängeraudit ist aufgehoben. Reale Materialien, wahrgenommene Farben und die
fachübergreifenden Atlas-Beziehungen bleiben ungeprüft. Die HUD-Phasenanbindung
und `Kη-03` werden durch diesen Modellfall nicht verändert.
