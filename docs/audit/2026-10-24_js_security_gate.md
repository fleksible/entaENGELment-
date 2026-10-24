# JS-Security-Gate: veröffentlichte Fixversionen nachführen

**Datum:** 2026-10-24 · **Status:** ANNEX / DERIVED

**FOKUS:** blockierende JS-Dependency-Befunde beheben

## Beobachteter Blocker

[FAKT] Am korrigierten #422-Head `dbe86902` besteht der Python-Audit.
Der separate JS-Job `120933245825`, Run `40114623803`, scheitert an vier
hohen Paketbefunden: Zod, Electron und zwei Undici-Linien. Es wird daraus
keine nachgewiesene Ausnutzbarkeit der konkreten Anwendung abgeleitet.

## Gezielte Dependency-Änderungen

| Paket | Vorher | Nachher | Veröffentlichter Fixanker |
| --- | --- | --- | --- |
| Electron | 44.7.0 | 44.9.1 | [GHSA-jr5w-w6x2-84p9](https://github.com/advisories/GHSA-jr5w-w6x2-84p9) |
| Zod | 4.6.5 | 4.6.7 | [GHSA-mrhx-c7xc-m3w5](https://github.com/advisories/GHSA-mrhx-c7xc-m3w5), Fix ab 4.6.6 |
| Undici 6 | 6.28.1 | 6.29.1 | [GHSA-xjj6-f33q-929c](https://github.com/advisories/GHSA-xjj6-f33q-929c) |
| Undici 7 | 7.29.1 | 7.30.1 | derselbe Advisory, getrennte Major-Linie |

[FAKT] Die bestehende zentrale Override-Konfiguration hielt beide
Undici-Versionen fest. Deren Untergrenzen und Fix-Pins werden gemeinsam
nachgeführt; ein reiner transitiver Update-Aufruf konnte diese Pins nicht
überschreiben. Electron bleibt innerhalb Major 44. Der Resolver zieht außerdem
das Jest-Hilfspaket react-is von 19.3.0 auf 19.3.1 nach und normalisiert einen
Peer-Snapshot-Schlüssel. pnpm 10.33.0 erzeugt den konsistenten Lock.

## Audit und Grenzen

[FAKT] `pnpm audit --audit-level=high` besteht lokal. Vier niedrigere
Meldungen bleiben sichtbar: zwei low, zwei moderate. Die bestehenden
Audit-Ausnahmen und die Altersgrenze für neue Versionen bleiben unverändert;
es wurde kein neuer Befund ausgeblendet und kein Gate abgeschwächt.

[ANNEX] Der lokale Audit bewertet Paketmetadaten mit der bestehenden
Audit-Konfiguration. Er ist kein vollständiger Security-Scan der Anwendung.
Die aktuellen Advisory-Seiten wurden für die Fixgrenzen direkt gelesen.
Python-Lock, GOLD, Receipts und Projekt-Claim-Status sind nicht betroffen.

[ANNEX] Vor Merge sind eingefrorene Installation, vollständige JS-/TS-Prüfung,
Root-Jest-Suite, Kern-/Governance-Gates und aktuelle PR-CI maßgeblich.
Ein Electron-Desktop-Paket wird in diesem Auftrag nicht veröffentlicht.


## Ausgeführter lokaler Abschluss

[FAKT] Eingefrorene Installation mit pnpm 10.33.0 und `make verify-js`
bestanden: Typprüfung, Lint, optimierter Next.js-Produktionsbuild,
58 Node-Tests und sechs Canvas-Tests. Root-Jest besteht mit 66 Tests in vier Suiten. `make verify` besteht mit
741 Tests und 165 Subtests; Governance und `git diff --check` bestehen. Bestehende
Peer-/Modulformatwarnungen werden nicht unterdrückt.
