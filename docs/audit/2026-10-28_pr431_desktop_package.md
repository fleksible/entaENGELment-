# PR #431: Desktop-Paketierung und Sandbox-Start

FOKUS: Den fehlenden konkreten Paketnachweis ergänzen

Status: DERIVED. Bot-Head `c96f21337d0d509bc1e85cb3334aae1296ae1b36`;
erste Basis `main@995450d3f1552d160b6dbfca4c6bad656f9323dc`;
der korrigierte Python-Stand `main@e0c3781e923b54464d62d11644a834a8e21d62ff`
wird vor Veröffentlichung integriert.

## Lücke und Ergänzung

Die bisherigen grün geprüften Jobs bauen die Next.js-UI und testen unter
anderem die tatsächlich aufgelösten Packaging-Glob-Konsumenten. Sie bauen
und starten kein gepacktes Electron-Programm.

`ci-desktop.yml` installiert eingefroren mit pnpm 10.33.0, prüft die vorhandenen
Glob-Regressionen und baut das konfigurierte Linux-AppImage mit Electron
Builder 26.18.0. Dabei wird der echte Dependency-Collector durchlaufen. Das
Root-Projekt hat keine Produktions-Node-Abhängigkeiten.

Der Job extrahiert das erzeugte AppImage ohne FUSE. Gestartet wird dessen
`AppRun` mit seiner tatsächlichen `resources/app.asar`, kein Ersatz-Einstieg.
Der veröffentlichte Paket-Hash und die Laufbeobachtung werden als kurzlebige
CI-Artefakte erhalten.

`tools/desktop_smoke.cjs` prüft unter Xvfb als normaler Benutzer:

- gepackte Ausführung, deklarierte Electron-Version und lokale `Index.html`;
- die vorhandene minimale Preload-Bridge und deren tatsächliche Versionswerte;
- Sandbox-/Isolations-Einstellungen sowie fehlenden Node-Zugriff der Seite;
- keine Sandbox-abschaltenden Schalter, Renderer-Seccomp-Modus 2 und
  `NoNewPrivs: 1` am tatsächlich laufenden Prozess;
- blockierte Datei-Popups, blockierte Dateinavigation und sauberes Beenden.

Der SUID-Helper erhält ausschließlich im flüchtigen Runner die erforderlichen
Eigentums-/Moduswerte. Die Anwendung läuft weiterhin als normaler Benutzer,
ohne `--no-sandbox`. Der vorübergehende Debugger ist auf Loopback beschränkt.
`main.js` und `preload.js` bleiben unverändert.

## Tatsächlicher Fehler im gepackten Launcher

Der erste neue CI-Lauf scheiterte in Job **122742354810** an einem tatsächlich
gesetzten `--no-sandbox`. Die Extraktion des lokal gebauten AppImages zeigt
zwei getrennte Ursachen in Builder 26.18.0: der Desktop-Eintrag lautet standardmäßig
`Exec=AppRun --no-sandbox %U`; zudem hängt das erzeugte AppRun-Skript nach einem
fehlgeschlagenen `unshare -Ur true` selbständig diesen Schalter an. Ein korrekter
SUID-Helper wird durch diese reine Namespace-Heuristik nicht berücksichtigt.

`build.appImage.executableArgs: []` entfernt das Desktop-Defaultargument.
Der versionsgebundene pnpm-Patch für `app-builder-lib@26.18.0` entfernt außerdem
den automatischen Sandbox-Downgrade aus dem tatsächlichen Launcher-Generator.
Chromium wählt weiter seinen Namespace-/SUID-Sandboxweg. Fehlen beide, muss der
Start scheitern; der Launcher startet nicht stillschweigend ohne Sandbox.

Zwei Prozess-Gegenproben mit fehlgeschlagenem bzw. fehlendem Namespace-Probe
(Exit 1 und 127) beobachten vor dem Patch das zusätzliche `--no-sandbox` und
bestehen danach mit unverändert weitergegebenen, auch leerzeichenhaltigen
Argumenten. Root-Jest besteht danach **fünf Suites mit 68 Tests**. Der
strukturierte Lock-Vergleich bestätigt gleiche Paketnamen, -versionen,
Paketmetadaten, Settings und Overrides; ergänzt werden der Patch-Hash und
normalisierte vorhandene Peer-Schlüssel. Der bestehende Brace-Patch bleibt erhalten.
Die Paketprobe prüft zusätzlich den tatsächlich verteilten Desktop-Eintrag.

## Abnahme und Grenze

Am 27.10. wurde der volle lokale AppImage-Build mit Builder 26.18.0 und
Electron 44.9.1 ausgeführt; seine Logs belegen die pnpm-Suche und den
Traversal-Fallback des Collectors. Root-Jest (66 Tests) und fünf ausgeführte
Turbo-Tasks bestanden. Die Wiederaufnahme prüft JavaScript und Governance
erneut; vor Merge muss der neue CI-Job tatsächlich grün abgeschlossen sein.

Der lokale Container bildet nur UID/GID 0 ab. Ein normaler Benutzerwechsel
und damit der erforderliche lokale Sandbox-Start sind dort nicht möglich.
Dieser Bericht behauptet deshalb keinen lokalen Startnachweis. Der neue Job
liefert ihn am konkreten veröffentlichten Head oder blockiert die Abnahme.

Die automatische Freigabeprüfung lehnte einen lokalen Next.js-Build wegen
eines Telemetrieabrufs an Vercel mit unbekanntem Payload ab. Die Wiederholung
nutzt die im installierten Next 16.4.2 und Turbo 2.11.7 belegten Opt-outs:
`NEXT_TELEMETRY_DISABLED=1`, `TURBO_TELEMETRY_DISABLED=1`, `DO_NOT_TRACK=1`.
Die betroffenen CI-Jobs setzen diese Werte ebenfalls. `globalEnv` reicht den
Next-Wert im weiterhin strikten Turbo-Environment an den Build weiter und
bindet ihn in den Cache-Key ein. Kein Wechsel in den losen Environment-Modus.
Der installierte Next-Telemetrieclient meldet mit diesem Wert `isEnabled: false`.
Der erneute vollständige JS-/TS-Lauf besteht fünf tatsächlich ausgeführte
Tasks ohne Cache-Treffer; Root-Jest besteht vier Suites mit 66 Tests.

Die Probe belegt Linux-AppImage-Payload, Start und die genannten Grenzen.
Windows-NSIS, macOS-DMG, FUSE-Mount und volle WebGL-/Audio-/CDN-Interaktion
werden damit nicht getestet. #432 muss denselben Job separat mit Electron 45
bestehen; ein Erfolg mit 44.9.1 wird nicht übertragen. GOLD, bestehende
Receipts und fachliche Modellentscheidungen sind nicht Teil dieses Patches.
