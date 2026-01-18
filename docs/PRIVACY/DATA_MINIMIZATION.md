# DATA MINIMIZATION (Policy)

Ziel: **Auditierbarkeit ohne unnötige Daten**.

## Was wir loggen (allowed)
- Hashes statt Rohdaten (input_hash, output_hash, replay_hash)
- Canonicalized Text *nur*, wenn unbedingt nötig und ohne Personenbezug
- Konfigurationsparameter (segmentation, metrics) ohne Identifikatoren
- Transform-Schritte als strukturierte Metadaten
- Pseudonymisierte Nutzerkennung (user_id_hash)

## Was wir NICHT loggen (default deny)
- Klarnamen, E-Mails, Telefonnummern, Adressen
- Roh-Biometrics, wenn nicht zwingend (z.B. komplette RR-Intervalle)
- GPS/Standortdaten
- Freitext, der Dritte identifizieren könnte
- Unnötige Device-Identifiers (MAC, Advertising IDs)

## Redaction-Regeln
- Wenn Text gespeichert wird: automatische Redaction (Emails/Phone/URLs)
- Für human studies: separate, verschlüsselte Schlüsseldatei **außerhalb** des Repos

## Zugriff & Aufbewahrung
- Least-privilege Zugriff (Role-based)
- Retention: _[z.B. 12 Monate]_ , danach Aggregation/Deletion
