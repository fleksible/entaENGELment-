# Phasenanschluss: konkreten Kandidaten vorbereiten

**Datum:** 2026-10-24 · **Status:** ANNEX / DERIVED

**FOKUS:** Phasenbindung konkret zur Entscheidung vorlegen

[ANNEX] Der [ausgefüllte Kandidat](../annex/PHASEN_REPLAY_KANDIDAT_v0_1.md)
setzt #413/#415/#418 fort: vorgeschlagene Größe, Parameter, Bezug, Identitäten,
synthetische Zuordnung und Transformationsregel werden konkret lesbar.

[FAKT] Rechenprobe am Stand `539e87b`: Producer direkt importiert, n=256,
coupling=0.35, Seeds 7/42/123. Sample 1 wurde aus Sample 0 und passendem
RNG-Schritt vorhergesagt; die Zielphase wurde erst zum Vergleich gelesen.
Drei Vergleiche bestehen mit maximal etwa 1.11e-16 Umläufen Abweichung.
Drei falsche Transform-Seeds werden bei Toleranz 1e-10 zurückgewiesen.

[ANNEX] Diese sechs Vergleiche prüfen die konkrete Algebra-/RNG-Zuordnung,
keinen implementierten HUD-Adapter und keine unabhängige Naturtheorie.
Die zusätzlichen Adapterfälle bleiben NOT_RUN. Die Bearbeitungserlaubnis
für den Entwurf legt keine HUD-Semantik fest. Kη-03 bleibt UNBOUND;
Graining, Blindseite und Sphärenstatus bleiben jeweils UNRESOLVED.

[ANNEX] Kern-/Governance-Prüfung, relative Links, Producer-Hash und
Diff-Umfang werden vor Veröffentlichung geprüft und im PR ausgewiesen.
Eine bestandene Dokumentprüfung wird nicht zur bestandenen Runtime-Anbindung.


[FAKT] Abschluss der Dokumentprüfung: `make verify` mit 741 Tests und
165 Subtests, `make verify-governance`, relative Links, Producer-Hash und
`git diff --check` bestanden. Ausführbarer Code, GOLD und Receipts sind
im Dokumentdiff unverändert; die Rechenprobe ist gesondert oben ausgewiesen.
