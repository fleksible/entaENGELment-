# Kriterien der gezielten Governance-Pilotauswahl

**Datum:** 2026-10-30  
**Fokus:** Closing Path und Entscheidungsbelege  
**Status:** DERIVED / REVIEW-PENDING; Kriterien vor den weiteren fachlichen Läufen

## Auswahl und Vorwissen

VOID-027 (OPEN → IN_PROGRESS), VOID-011 (IN_PROGRESS → CLOSED) und ADR-0001
(Proposed → Accepted) sind eine gezielte Pilotauswahl, keine Grundgesamtheit.
Die Metadaten, Statuswechsel und Teile der Begründungen wurden bereits gelesen;
die folgende Prüfung ist daher kein Blindtest. Die Registry-Grundgesamtheit im
separat untersuchten Zeitraum ist damit nicht mit der Pilotauswahl identisch.

## Vorab festgelegte Urteile

- **NACHVOLLZIEHBAR:** Der damalige Maßstab ist identifiziert, die konkrete
  Aussage bleibt in seinem Scope, die nötigen Belege sind direkt zugänglich und
  tragen die Aussage. Erforderliche Autorisierung und ihre Reichweite sind
  separat belegt. Ein fehlender unabhängiger Readback wird nicht still ergänzt.
- **LÜCKENHAFT:** Mindestens ein erforderliches Glied ist unbekannt, nur berichtet
  oder nicht zugänglich. Fehlender Nachweis bedeutet nicht widerlegte Erfüllung.
- **WIDERSPRÜCHLICH:** Eine direkt gelesene Quelle oder reproduzierte Beobachtung
  widerspricht der konkret benannten Aussage im gleichen Scope. Widersprüche
  werden nicht aus bloßem Schweigen einer Quelle abgeleitet.

Urteile gelten pro Teilfrage. Technische Reproduzierbarkeit, damalige Erfüllung,
Owner-Autorisierung und unabhängiger menschlicher Readback erhalten keine
gemeinsame Punktzahl und ersetzen einander nicht. Gegenlese, Neuberechnung und
CI können dieselbe Implementierung oder Annahme teilen; die Trägerklasse allein
garantiert keine Unabhängigkeit.

## Geplante Beobachtungen

| Fall | Zu prüfende Aussage | Beleg und Gegenprüfung |
|---|---|---|
| VOID-027 | Teilimplementierung trägt IN_PROGRESS, nicht CLOSED | damaliger Closing Path, Quellcode-/Testanker, ausdrücklich offene Komponenten |
| VOID-011 | deterministischer SIMULATION_PROXY-Export erfüllt den damaligen Closing Path | Export-Neuberechnung mit `--check`, zugehörige Tests und getrennte Lektüre der Owner-Quelle #311 |
| ADR-0001 | Proposed wurde durch den zuständigen Entscheid zu Accepted | ursprüngliche Freigabe und damals vorgelegter Gegenstand; Dateistatus allein reicht nicht |

Für VOID-011 ist zusätzlich zu klären, ob das berichtete Owner-OK die Erfüllung
oder eine Ankündigung betraf. Diese Modellinstanz kann den Vorgang dokumentieren,
aber keine menschliche Direktbeobachtung ersetzen.

Die Suche nach früheren FD-basierten Claims ist ein separater Suchauftrag:
Fundstellen vor dem FD-Fix mit tatsächlich verwendeten Werten, Aussage und
Statusentscheidung verbinden. Implementierungsalter oder ein früherer FD-Wert
allein belegen keine Fehlpromotion. Nicht gefundene private Verläufe bleiben
außerhalb der Suchabdeckung.

## Übergang aus Forschung in Verpflichtung

`prevents` und `escape_detector` werden für einen Schutzvorschlag erforderlich,
sobald er als Feld, Gate, Check oder Pflicht umgesetzt werden soll, unabhängig
vom vorherigen Intake-Etikett. Dies ist ein Review-Kriterium dieses Piloten,
keine neu eingeführte Repo-Policy oder Laufzeit-Erzwingung.
