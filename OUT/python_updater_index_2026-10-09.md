# Report: Python-Updater mit explizitem PyPI-Index

**Datum:** 2026-10-09
**Fokus:** Python-Updater entblocken
**Authority:** DERIVED / REVIEW-PENDING
**Basis:** main `a7773db68d97dbd8271b0921d011934d2e921170`.

## Ziel
Den Fehler `unknown url type: '/pypi/rpds-py/json'` in Dependabots Hash-Abfrage
adressieren, ohne Lock, Hashes, Python-Unterstützung oder Security-Gates zu lockern.

## Aktionen
- [x] Original-Log gelesen: [Run 37258615411](https://github.com/fleksible/entaENGELment-/actions/runs/37258615411),
  Job 111600855630, 5. Oktober 2026, 03:15:12 UTC. Fehler entsteht im UV
  CompileFileUpdater → Python-Helper → hashin → urllib, beim Update von numpy.
- [x] Upstream-Code geprüft: `Uv::FileUpdater#pip_compile_index_urls` bildet ohne
  `replaces-base` auch sonstige Credentials auf Index-URLs ab. Der Python
  `AuthedUrlBuilder` liefert bei fehlendem `index-url` einen leeren String.
  [INFERENZ] Das ist ein zum Log passender Weg zur relativen URL; die vollständigen
  Eingabe-Credentials des historischen Jobs wurden nicht ausgelesen.
- [x] Reproduktion mit hashin 1.0.5: leeres `index_url` erzeugt exakt dieselbe
  ValueError-Meldung; explizites `https://pypi.org/simple` liefert für
  `rpds-py==2026.6.3` erfolgreich 116 SHA-256-Hashes.
- [x] Anonyme PyPI-Registry in `.github/dependabot.yml` eingetragen, ausschließlich
  dem UV-Job zugewiesen, mit `replaces-base: true`. Damit nutzt der geprüfte
  Upstream-Zweig den absoluten Index statt der Liste mit sonstigen Credentials.
- [x] `python tools/python_lock.py check` mit uv 0.12.18: Lock und alle vier
  erzeugten Requirements-Dateien konsistent. `make verify-governance`: erfolgreich.
- [x] YAML und Diff geprüft. Keine zusätzlichen Secrets erforderlich.

## Nicht getan
- Keine Paketversion, kein Lockfile, keine Requirements-Datei geändert.
- Kein neuer automatischer Export-/Writeback-Workflow und keine Auto-Merge-Regel.
- Kein erfolgreicher Dependabot-Gesamtlauf behauptet: GitHub verweigert das
  Wiederholen des historischen Runs mit HTTP 403, „This workflow run cannot be retried“.

## Risiken
- Der Fix adressiert den reproduzierten Index-Fehler. Erst ein neuer verwalteter
  Dependabot-Lauf bestätigt, dass GitHub diese Konfiguration übernimmt und der
  gesamte Updatepfad funktioniert.
- Auch ein erzeugter Update-PR muss den Lock-/Export-Konsistenzcheck bestehen.
  Ein weiterer Export-Drift wäre ein eigener Fehler, kein Grund, das Gate abzuschalten.

## Offene Punkte
- [ ] Review, CI und Integration der Konfiguration.
- [ ] Anschließend neuer UV-Dependabot-Lauf (regulär montags oder „Check for updates“).
- [ ] Run-URL und Ergebnis dokumentieren; bei Update-PR zusätzlich konsistente
  `uv.lock`-/Requirements-Änderungen und grüne CI bestätigen.

## Artefakte
- `.github/dependabot.yml`

## Quellen
- [UV FileUpdater](https://github.com/dependabot/dependabot-core/blob/main/uv/lib/dependabot/uv/file_updater.rb)
- [CompileFileUpdater](https://github.com/dependabot/dependabot-core/blob/main/uv/lib/dependabot/uv/file_updater/compile_file_updater.rb)
- [AuthedUrlBuilder, Blob bcbbea65dc6dd81239d69bca4b0ef983f2deca68](https://github.com/dependabot/dependabot-core/blob/main/python/lib/dependabot/python/authed_url_builder.rb)
- [GitHub: Registry-Konfiguration einschließlich anonymer Registries](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-access-to-private-registries)
