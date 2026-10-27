# ESLint 10: Node-Vertrag und Konfigurationskommentar

Stand: 27. Oktober 2026 · DERIVED / technischer Nachtrag zu PR #430.
Ausgangshead: `42d7e3f7db0227fc244d2641358c5a8f0e7566f0`.

[FAKT] Der neue Linter verlangt laut Lock `^20.19.0 || ^22.13.0 || >=24`.
Das Root-Manifest erlaubte `>=22.12.0`, also unter anderem die nicht unterstützten
Versionen 22.12 und 23. Der Projektbereich ist jetzt `^22.13.0 || >=24.0.0`.

Der Flat-Config-Kommentar behauptete noch einen ESLint-9-Pin und einen laufenden
ESLint-10-Absturz. Die vorhandene `eslint-config-next` 16.4.2 adaptiert jedoch
React-/Import-Regelkontexte. Der Kommentar beschreibt jetzt diesen konkreten Weg;
Parser, Plugin-Versionen und Regelkonfiguration werden nicht verändert.

## Ausgeführte Prüfung

- Node 24.22.1, pnpm 10.33.0; eingefrorene Offline-Installation ohne
  Installationsskripte bestanden, Lockfile unverändert.
- `pnpm turbo run typecheck lint build test`: fünf erfolgreiche Tasks, keiner aus
  dem Task-Cache; Shared-/UI-Typprüfung, ESLint, Next-Build und UI-Tests bestanden.
- Root-Jest: vier Suites, 66 Tests bestanden. `make verify`: 741 Tests und
  165 Subtests bestanden; Governance-Gates ebenfalls grün.
- Die zuvor gezielt gelesenen effektiven Konfigurationen verwenden den
  TypeScript-ESLint-Parser 8.70.1 für TS/TSX und Nexts Parser für JS/MJS.
  Die hervorgehobenen Core-Regeln der Release-Notizen sind dort nicht aktiviert.
- Die bisherige Head-CI des ursprünglichen Bot-Diffs war grün. Die CI muss auch
  den ergänzten Head prüfen; lokale Tests werden nicht als künftige CI ausgegeben.

Keine Regel wurde zur Herstellung eines grünen Lints ausgeschaltet. Es wurde kein
Electron-Paketstart ausgeführt und kein Desktop-/Plattformnachweis daraus abgeleitet.

## Merge-Nachtrag: kombinierter Lock

Nach den freigegebenen Wartungs-Merges kollidierte der frühere ESLint-Lock mit
den React-Query-Peerschlüsseln. Der Konflikt wurde mit pnpm 10.33.0 aufgelöst und
mit dem bereits geprüften ESLint-Graphen strukturiert verglichen: hinzu kommen
ausschließlich React Query / query-core 5.104.5 und YAML 2.9.1 aus den inzwischen
gemergten #434/#433. Gemeinsame Paketmetadaten, Overrides und Patch-Zuordnungen
bleiben gleich. Kein anderes Versionsupdate wurde dabei übernommen.

Basis für die erneute Integration:
`main@b72cfd94b6e47da559104c986bce9358e0604c41`.
Eingefrorene Installation, vollständige Turbo-Pipeline (vier Tasks ausgeführt,
ein unveränderter Shared-Typecheck aus dem Cache), Root-Jest (66 Tests),
`make verify` (859 Tests und 169 Subtests), Governance und strenger Claim-Lint
bestanden. Der aktualisierte PR-Head erhält vor Merge eine eigene CI-Abnahme.
