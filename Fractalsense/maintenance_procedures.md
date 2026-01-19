# FractalSense EntaENGELment - Wartungsanleitung

## Übersicht

Dieses Dokument enthält Anweisungen zur Wartung und Aktualisierung der FractalSense EntaENGELment-Website, die unter [https://cpktjghp.manus.space](https://cpktjghp.manus.space) gehostet wird.

## Hosting-Informationen

- **Hosting-Plattform**: Die Website wird auf Netlify gehostet
- **Deployment-Typ**: Statische Website
- **URL**: [https://cpktjghp.manus.space](https://cpktjghp.manus.space)

## Dateien und Struktur

Die Website besteht aus folgenden Hauptdateien:

- `index.html` - Hauptseite der Anwendung
- `styles.min.css` - Minifizierte CSS-Stile
- JavaScript-Module:
  - `app.min.js` - Hauptanwendungslogik
  - `fractal-visualizer.min.js` - Fraktal-Visualisierungsmodul
  - `sensor-simulator.min.js` - Sensor-Simulationsmodul
  - `resonance-enhancer.min.js` - Klang- und Farbmodul
  - `presentation-mode.min.js` - Präsentationsmodus
- `netlify.toml` - Konfigurationsdatei für Netlify

## Aktualisierung der Website

### Methode 1: Direkte Aktualisierung über Netlify

1. Melden Sie sich bei Ihrem Netlify-Konto an
2. Navigieren Sie zum FractalSense EntaENGELment-Projekt
3. Gehen Sie zum "Deploys"-Tab
4. Ziehen Sie einen neuen Ordner mit aktualisierten Dateien per Drag & Drop in den Bereich "Drag and drop your site folder here"
5. Netlify wird automatisch ein neues Deployment erstellen

### Methode 2: Lokale Entwicklung und Deployment

1. Klonen Sie das Repository oder laden Sie die Quelldateien herunter
2. Nehmen Sie die gewünschten Änderungen vor
3. Optimieren Sie die Dateien für die Produktion:
   - Minifizieren Sie CSS mit einem Tool wie [CSS Minifier](https://cssminifier.com/)
   - Minifizieren Sie JavaScript mit einem Tool wie [JavaScript Minifier](https://javascript-minifier.com/)
4. Testen Sie die Änderungen lokal, indem Sie die `index.html` in einem Browser öffnen
5. Erstellen Sie einen neuen Ordner für das Deployment und kopieren Sie alle optimierten Dateien hinein
6. Laden Sie den Ordner zu Netlify hoch (siehe Methode 1)

## Hinzufügen neuer Module

Die Anwendung ist modular aufgebaut, sodass neue Funktionen einfach hinzugefügt werden können:

1. Erstellen Sie eine neue JavaScript-Datei für Ihr Modul (z.B. `new-module.js`)
2. Implementieren Sie die Modulklasse mit folgender Grundstruktur:
   ```javascript
   class NewModule {
     constructor() {
       // Initialisierung
     }
     
     // Methoden implementieren
     
     // Event-Listener einrichten
   }
   
   // Modul exportieren
   window.NewModule = NewModule;
   ```
3. Minifizieren Sie die Datei zu `new-module.min.js`
4. Fügen Sie einen Verweis auf das neue Modul in `index.html` hinzu:
   ```html
   <script src="new-module.min.js"></script>
   ```
5. Aktualisieren Sie `app.min.js`, um das neue Modul zu initialisieren und mit den bestehenden Modulen zu verbinden
6. Testen Sie die Änderungen lokal
7. Deployen Sie die aktualisierten Dateien zu Netlify

## Anpassung des Designs

Um das Design anzupassen:

1. Bearbeiten Sie die `styles.css`-Datei (nicht minifiziert)
2. Ändern Sie Farben, Schriftarten oder Layouts nach Bedarf
3. Minifizieren Sie die aktualisierte CSS-Datei zu `styles.min.css`
4. Testen Sie die Änderungen lokal
5. Deployen Sie die aktualisierten Dateien zu Netlify

## Fehlerbehebung bei Deployment-Problemen

### Problem: Deployment schlägt fehl

1. Überprüfen Sie die Deployment-Logs in Netlify
2. Stellen Sie sicher, dass alle erforderlichen Dateien im Deployment-Ordner vorhanden sind
3. Überprüfen Sie die `netlify.toml`-Konfigurationsdatei auf Fehler
4. Versuchen Sie ein manuelles Deployment über die Netlify-Befehlszeilenschnittstelle (CLI)

### Problem: Website wird nicht korrekt angezeigt

1. Überprüfen Sie die Browser-Konsole auf JavaScript-Fehler
2. Stellen Sie sicher, dass alle Pfade zu CSS- und JavaScript-Dateien korrekt sind
3. Testen Sie die Website in verschiedenen Browsern
4. Leeren Sie den Browser-Cache und laden Sie die Seite neu

## Domainverwaltung

Um eine benutzerdefinierte Domain einzurichten:

1. Melden Sie sich bei Ihrem Netlify-Konto an
2. Navigieren Sie zum FractalSense EntaENGELment-Projekt
3. Gehen Sie zum "Domain settings"-Tab
4. Klicken Sie auf "Add custom domain"
5. Folgen Sie den Anweisungen, um Ihre Domain zu konfigurieren und DNS-Einstellungen zu aktualisieren

## Backup und Wiederherstellung

### Backup erstellen

1. Laden Sie alle Quelldateien herunter und speichern Sie sie an einem sicheren Ort
2. Exportieren Sie die Netlify-Konfiguration über die Netlify-Einstellungen
3. Dokumentieren Sie alle benutzerdefinierten Einstellungen oder Anpassungen

### Wiederherstellung

1. Erstellen Sie ein neues Netlify-Projekt
2. Laden Sie die gesicherten Dateien hoch
3. Konfigurieren Sie die Netlify-Einstellungen entsprechend Ihrer Dokumentation
4. Aktualisieren Sie DNS-Einstellungen, falls Sie eine benutzerdefinierte Domain verwenden

## Kontakt für Support

Bei Fragen oder Problemen mit der Website wenden Sie sich bitte an:

- **E-Mail**: support@fractalsense.example.com
- **GitHub**: [github.com/fractalsense/entaengelment](https://github.com/fractalsense/entaengelment)

## Regelmäßige Wartung

Für optimale Leistung und Sicherheit empfehlen wir folgende regelmäßige Wartungsaufgaben:

1. **Monatlich**:
   - Überprüfen Sie die Website auf Fehler oder Probleme
   - Testen Sie die Website in verschiedenen Browsern
   - Überprüfen Sie die Netlify-Analytics auf ungewöhnliche Aktivitäten

2. **Vierteljährlich**:
   - Aktualisieren Sie JavaScript-Bibliotheken, falls verwendet
   - Überprüfen Sie die Sicherheitseinstellungen in der `netlify.toml`-Datei
   - Erstellen Sie ein Backup aller Dateien

3. **Jährlich**:
   - Erneuern Sie die Domain, falls Sie eine benutzerdefinierte Domain verwenden
   - Überprüfen Sie die Netlify-Preispläne und Kontingente
   - Führen Sie eine umfassende Überprüfung der Website durch
