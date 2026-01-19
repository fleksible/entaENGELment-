// FractalSense EntaENGELment - Presentation Mode Module

// Hauptklasse für den Präsentationsmodus
class PresentationMode {
    constructor() {
        // Präsentationsdaten
        this.slides = [
            {
                title: "Willkommen zu FractalSense EntaENGELment",
                tab: "fractal",
                description: "Eine multisensorische Reise durch fraktale Strukturen, Klang und Farbe.",
                actions: [
                    { type: "showFractal", params: { center: { x: -0.75, y: 0 }, zoom: 1.0 } }
                ],
                narration: "Willkommen zu FractalSense EntaENGELment, einer interaktiven Erfahrung, die Mathematik, Kunst und Philosophie verbindet. Diese Anwendung verwandelt abstrakte fraktale Strukturen in eine sinnliche Reise durch Klang, Farbe und Bewegung."
            },
            {
                title: "Fraktale Grundlagen",
                tab: "fractal",
                description: "Entdecken Sie die unendliche Komplexität des Mandelbrot-Fraktals.",
                actions: [
                    { type: "showFractal", params: { center: { x: -0.75, y: 0 }, zoom: 2.0 } },
                    { type: "zoomIn", delay: 3000 },
                    { type: "zoomIn", delay: 3000 }
                ],
                narration: "Was Sie hier sehen, ist ein Mandelbrot-Fraktal – eine mathematische Struktur mit unendlicher Komplexität. Beobachten Sie, wie mit jeder Vergrößerung neue Details erscheinen. Diese 'Selbstähnlichkeit' ist ein Grundprinzip von Fraktalen – Muster wiederholen sich auf verschiedenen Ebenen."
            },
            {
                title: "Sensorische Integration",
                tab: "sensors",
                description: "Erleben Sie, wie Bewegungssensoren die Navigation durch das Fraktal steuern.",
                actions: [
                    { type: "activateSensors" },
                    { type: "simulateSensorMovement", delay: 2000 }
                ],
                narration: "Im Sensor-Modus nutzt die Anwendung Bewegungssensoren, um durch das Fraktal zu navigieren. Eine Neigung nach vorne zoomt hinein, nach hinten zoomt heraus. Seitliche Bewegungen verschieben den Blickpunkt. So wird die mathematische Struktur zu einer physischen Erfahrung."
            },
            {
                title: "Klangliche Dimension",
                tab: "resonance",
                description: "Hören Sie, wie das Fraktal in Klang übersetzt wird.",
                actions: [
                    { type: "activateSound", params: { type: "harmonic" } },
                    { type: "changeSoundType", params: { type: "fractal" }, delay: 5000 },
                    { type: "changeSoundType", params: { type: "resonant" }, delay: 10000 }
                ],
                narration: "Die Klänge, die Sie hören, werden in Echtzeit aus den mathematischen Eigenschaften des Fraktals generiert. Der 'Harmonische Modus' basiert auf dem goldenen Schnitt. Der 'Fraktale Modus' erzeugt Klänge mit selbstähnlicher Struktur. Der 'Resonante Modus' nutzt Resonanzfrequenzen, die auf der mathematischen Struktur basieren."
            },
            {
                title: "Farbliche Dimension",
                tab: "resonance",
                description: "Erleben Sie, wie Farben die mathematische Struktur visualisieren.",
                actions: [
                    { type: "changeColorMode", params: { mode: "resonant" } },
                    { type: "changeColorMode", params: { mode: "spectral" }, delay: 5000 },
                    { type: "changeColorMode", params: { mode: "cosmic" }, delay: 10000 }
                ],
                narration: "Die Farben sind nicht zufällig. Jedes Farbschema repräsentiert einen anderen Aspekt der mathematischen Struktur. Das 'Resonante' Schema verwendet einen Verlauf von Violett zu Gold. Das 'Spektrale' Schema basiert auf dem Lichtspektrum. Das 'Kosmische' Schema erinnert an einen Sternenhimmel und stellt eine Verbindung zwischen mikroskopischen Strukturen und dem Universum her."
            },
            {
                title: "EntaENGELment-Konzept",
                tab: "fractal",
                description: "Verstehen Sie die philosophischen Grundlagen des Projekts.",
                actions: [
                    { type: "showFractal", params: { center: { x: -0.1, y: 0.8 }, zoom: 3.0 } }
                ],
                narration: "FractalSense EntaENGELment basiert auf einem philosophischen Rahmenwerk, das Technologie, Bewusstsein und Natur verbindet. Das Konzept der 'Resonanz als Einheit' beschreibt, wie verschiedene Systeme in einen harmonischen Dialog treten können. 'Autopoiesis' bedeutet Selbsterschaffung – die Anwendung entwickelt sich durch Interaktion ständig weiter."
            },
            {
                title: "Praktische Anwendungen",
                tab: "fractal",
                description: "Entdecken Sie die vielfältigen Einsatzmöglichkeiten.",
                actions: [
                    { type: "activateAllModules" }
                ],
                narration: "Diese Technologie hat vielfältige Anwendungsmöglichkeiten. Als meditative Erfahrung kann sie helfen, einen Zustand der Achtsamkeit zu erreichen. Für Künstler und Musiker bietet sie neue Wege der Inspiration. Wissenschaftler können komplexe Datensätze auf intuitive Weise erkunden, indem sie abstrakte Zahlen in Klang und Farbe übersetzen."
            },
            {
                title: "Ihre eigene Erfahrung",
                tab: "fractal",
                description: "Erkunden Sie die Anwendung selbst.",
                actions: [
                    { type: "resetAll" }
                ],
                narration: "Ich lade Sie ein, die Anwendung selbst zu erkunden. Jede Erfahrung ist einzigartig, da sie auf Ihrer eigenen Interaktion basiert. Experimentieren Sie mit verschiedenen Fraktaltypen, Klangmodi und Farbschemata, um Ihre persönliche Resonanz zu finden."
            }
        ];
        
        // Aktueller Slide
        this.currentSlideIndex = 0;
        
        // Präsentationsstatus
        this.isPlaying = false;
        this.isPaused = false;
        
        // Timer für automatische Wiedergabe
        this.autoplayTimer = null;
        this.autoplayDelay = 15000; // 15 Sekunden pro Slide
        
        // UI-Elemente
        this.initializeUI();
        
        // Module-Referenzen
        this.fractalVisualizer = null;
        this.sensorSimulator = null;
        this.resonanceEnhancer = null;
    }
    
    // UI-Elemente initialisieren
    initializeUI() {
        // Präsentations-Steuerelemente
        this.prevButton = document.getElementById('prev-slide');
        this.nextButton = document.getElementById('next-slide');
        this.pauseButton = document.getElementById('pause-presentation');
        
        // Overlay für Präsentationsinformationen
        this.createPresentationOverlay();
        
        // Event-Listener hinzufügen
        this.setupEventListeners();
    }
    
    // Präsentations-Overlay erstellen
    createPresentationOverlay() {
        // Container für Overlay
        this.overlay = document.createElement('div');
        this.overlay.className = 'presentation-overlay';
        this.overlay.style.cssText = `
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            background-color: rgba(45, 45, 45, 0.85);
            border-radius: 10px;
            padding: 15px;
            color: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            z-index: 100;
            display: none;
            transition: opacity 0.5s ease;
        `;
        
        // Titel
        this.overlayTitle = document.createElement('h2');
        this.overlayTitle.style.cssText = `
            margin-top: 0;
            color: #b388ff;
            font-size: 1.5em;
        `;
        
        // Beschreibung
        this.overlayDescription = document.createElement('p');
        
        // Narration
        this.overlayNarration = document.createElement('div');
        this.overlayNarration.style.cssText = `
            margin-top: 15px;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.2);
            border-left: 3px solid #9d00ff;
            font-style: italic;
        `;
        
        // Fortschrittsanzeige
        this.progressContainer = document.createElement('div');
        this.progressContainer.style.cssText = `
            margin-top: 15px;
            height: 5px;
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
            overflow: hidden;
        `;
        
        this.progressBar = document.createElement('div');
        this.progressBar.style.cssText = `
            height: 100%;
            width: 0%;
            background-color: #9d00ff;
            transition: width 0.3s ease;
        `;
        
        this.progressContainer.appendChild(this.progressBar);
        
        // Elemente zum Overlay hinzufügen
        this.overlay.appendChild(this.overlayTitle);
        this.overlay.appendChild(this.overlayDescription);
        this.overlay.appendChild(this.overlayNarration);
        this.overlay.appendChild(this.progressContainer);
        
        // Overlay zum DOM hinzufügen
        document.querySelector('.content-area').appendChild(this.overlay);
    }
    
    // Event-Listener einrichten
    setupEventListeners() {
        this.prevButton.addEventListener('click', () => this.previousSlide());
        this.nextButton.addEventListener('click', () => this.nextSlide());
        this.pauseButton.addEventListener('click', () => this.togglePause());
    }
    
    // Module registrieren
    registerModules(fractalVisualizer, sensorSimulator, resonanceEnhancer) {
        this.fractalVisualizer = fractalVisualizer;
        this.sensorSimulator = sensorSimulator;
        this.resonanceEnhancer = resonanceEnhancer;
    }
    
    // Präsentation starten
    startPresentation() {
        this.isPlaying = true;
        this.isPaused = false;
        this.currentSlideIndex = 0;
        
        // UI aktualisieren
        this.pauseButton.innerHTML = '⏸';
        this.overlay.style.display = 'block';
        
        // Ersten Slide anzeigen
        this.showSlide(this.currentSlideIndex);
        
        // Autoplay starten
        this.startAutoplay();
    }
    
    // Präsentation stoppen
    stopPresentation() {
        this.isPlaying = false;
        this.isPaused = false;
        
        // Timer löschen
        if (this.autoplayTimer) {
            clearTimeout(this.autoplayTimer);
            this.autoplayTimer = null;
        }
        
        // UI aktualisieren
        this.overlay.style.display = 'none';
    }
    
    // Pause umschalten
    togglePause() {
        if (!this.isPlaying) {
            this.startPresentation();
            return;
        }
        
        this.isPaused = !this.isPaused;
        
        if (this.isPaused) {
            // Präsentation pausieren
            this.pauseButton.innerHTML = '▶';
            
            // Timer löschen
            if (this.autoplayTimer) {
                clearTimeout(this.autoplayTimer);
                this.autoplayTimer = null;
            }
        } else {
            // Präsentation fortsetzen
            this.pauseButton.innerHTML = '⏸';
            
            // Autoplay fortsetzen
            this.startAutoplay();
        }
    }
    
    // Zum vorherigen Slide wechseln
    previousSlide() {
        if (!this.isPlaying) return;
        
        // Timer zurücksetzen
        if (this.autoplayTimer) {
            clearTimeout(this.autoplayTimer);
            this.autoplayTimer = null;
        }
        
        // Index aktualisieren
        this.currentSlideIndex = Math.max(0, this.currentSlideIndex - 1);
        
        // Slide anzeigen
        this.showSlide(this.currentSlideIndex);
        
        // Autoplay fortsetzen, wenn nicht pausiert
        if (!this.isPaused) {
            this.startAutoplay();
        }
    }
    
    // Zum nächsten Slide wechseln
    nextSlide() {
        if (!this.isPlaying) return;
        
        // Timer zurücksetzen
        if (this.autoplayTimer) {
            clearTimeout(this.autoplayTimer);
            this.autoplayTimer = null;
        }
        
        // Index aktualisieren
        this.currentSlideIndex = Math.min(this.slides.length - 1, this.currentSlideIndex + 1);
        
        // Slide anzeigen
        this.showSlide(this.currentSlideIndex);
        
        // Autoplay fortsetzen, wenn nicht pausiert
        if (!this.isPaused) {
            this.startAutoplay();
        }
    }
    
    // Autoplay starten
    startAutoplay() {
        if (this.isPaused || !this.isPlaying) return;
        
        // Timer löschen, falls vorhanden
        if (this.autoplayTimer) {
            clearTimeout(this.autoplayTimer);
        }
        
        // Neuen Timer setzen
        this.autoplayTimer = setTimeout(() => {
            // Zum nächsten Slide wechseln
            if (this.currentSlideIndex < this.slides.length - 1) {
                this.nextSlide();
            } else {
                // Präsentation beenden, wenn letzter Slide erreicht
                this.stopPresentation();
            }
        }, this.autoplayDelay);
    }
    
    // Slide anzeigen
    showSlide(index) {
        const slide = this.slides[index];
        
        // Tab aktivieren
        this.activateTab(slide.tab);
        
        // Overlay aktualisieren
        this.overlayTitle.textContent = slide.title;
        this.overlayDescription.textContent = slide.description;
        this.overlayNarration.textContent = slide.narration;
        
        // Fortschritt aktualisieren
        const progress = ((index + 1) / this.slides.length) * 100;
        this.progressBar.style.width = `${progress}%`;
        
        // Aktionen ausführen
        this.executeSlideActions(slide.actions);
    }
    
    // Tab aktivieren
    activateTab(tabName) {
        // Alle Tabs deaktivieren
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Alle Tab-Inhalte ausblenden
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        // Gewünschten Tab aktivieren
        const tabElement = document.querySelector(`.nav-tab[data-tab="${tabName}"]`);
        if (tabElement) {
            tabElement.classList.add('active');
        }
        
        // Gewünschten Tab-Inhalt anzeigen
        const contentElement = document.getElementById(`${tabName}-tab`);
        if (contentElement) {
            contentElement.classList.add('active');
        }
    }
    
    // Slide-Aktionen ausführen
    executeSlideActions(actions) {
        if (!actions || !actions.length) return;
        
        // Jede Aktion ausführen
        actions.forEach(action => {
            // Sofort ausführen oder verzögern
            const executeAction = () => {
                switch (action.type) {
                    case 'showFractal':
                        this.showFractal(action.params);
                        break;
                    case 'zoomIn':
                        this.zoomFractal(true);
                        break;
                    case 'zoomOut':
                        this.zoomFractal(false);
                        break;
                    case 'activateSensors':
                        this.activateSensors();
                        break;
                    case 'simulateSensorMovement':
                        this.simulateSensorMovement();
                        break;
                    case 'activateSound':
                        this.activateSound(action.params);
                        break;
                    case 'changeSoundType':
     
(Content truncated due to size limit. Use line ranges to read in chunks)