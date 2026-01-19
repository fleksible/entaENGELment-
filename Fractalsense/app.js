// FractalSense EntaENGELment - Main Application

// Warten, bis das DOM vollständig geladen ist
document.addEventListener('DOMContentLoaded', () => {
    // Module initialisieren
    initializeApp();
});

// Hauptanwendung initialisieren
function initializeApp() {
    // Module instanziieren
    const fractalVisualizer = new FractalVisualizer('fractal-canvas');
    const sensorSimulator = new SensorSimulator();
    const resonanceEnhancer = new ResonanceEnhancer();
    const presentationMode = new PresentationMode();
    
    // Module miteinander verbinden
    connectModules(fractalVisualizer, sensorSimulator, resonanceEnhancer, presentationMode);
    
    // Tab-Navigation einrichten
    setupTabNavigation();
}

// Module miteinander verbinden
function connectModules(fractalVisualizer, sensorSimulator, resonanceEnhancer, presentationMode) {
    // Präsentationsmodus mit Modulen verbinden
    presentationMode.registerModules(fractalVisualizer, sensorSimulator, resonanceEnhancer);
    
    // Sensordaten mit Fraktal verbinden
    sensorSimulator.registerDataUpdateCallback((sensorData) => {
        // Sensordaten in Fraktalparameter umwandeln
        const fractalParams = mapSensorDataToFractalParams(sensorData);
        
        // Fraktal aktualisieren
        updateFractalWithSensorData(fractalVisualizer, fractalParams);
    });
    
    // Fraktal-Events für ResonanceEnhancer
    fractalVisualizer.canvas.addEventListener('mousemove', () => {
        // Fraktalparameter abrufen
        const params = fractalVisualizer.getParams();
        
        // Benutzerdefiniertes Event auslösen
        const event = new CustomEvent('fractal-updated', {
            detail: params
        });
        document.dispatchEvent(event);
    });
    
    // UI-Steuerelemente mit Modulen verbinden
    connectUIControls(fractalVisualizer, sensorSimulator, resonanceEnhancer, presentationMode);
}

// Sensordaten in Fraktalparameter umwandeln
function mapSensorDataToFractalParams(sensorData) {
    // Beschleunigung zu Zoom-Änderung
    const zoomFactor = 1.0 + sensorData.accelZ * 0.1;
    
    // Gyroskop zu Position
    const positionDeltaX = sensorData.gyroY * 0.05;
    const positionDeltaY = -sensorData.gyroX * 0.05;
    
    return {
        zoomFactor,
        positionDeltaX,
        positionDeltaY
    };
}

// Fraktal mit Sensordaten aktualisieren
function updateFractalWithSensorData(fractalVisualizer, fractalParams) {
    // Aktuelle Parameter abrufen
    const currentParams = fractalVisualizer.getParams();
    
    // Neue Parameter berechnen
    const newZoom = currentParams.zoom * fractalParams.zoomFactor;
    const newCenter = {
        x: currentParams.center.x + fractalParams.positionDeltaX,
        y: currentParams.center.y + fractalParams.positionDeltaY
    };
    
    // Parameter aktualisieren
    fractalVisualizer.updateParams({
        center: newCenter,
        zoom: newZoom
    });
}

// UI-Steuerelemente mit Modulen verbinden
function connectUIControls(fractalVisualizer, sensorSimulator, resonanceEnhancer, presentationMode) {
    // Fraktal-Steuerelemente
    connectFractalControls(fractalVisualizer);
    
    // Sensor-Steuerelemente sind bereits in der SensorSimulator-Klasse implementiert
    
    // Resonance-Steuerelemente sind bereits in der ResonanceEnhancer-Klasse implementiert
    
    // Präsentations-Steuerelemente
    document.querySelectorAll('.presentation-button').forEach(button => {
        if (button.id === 'prev-slide') {
            button.addEventListener('click', () => presentationMode.previousSlide());
        } else if (button.id === 'next-slide') {
            button.addEventListener('click', () => presentationMode.nextSlide());
        } else if (button.id === 'pause-presentation') {
            button.addEventListener('click', () => presentationMode.togglePause());
        }
    });
    
    // Starten-Button für Präsentation hinzufügen
    const startPresentationButton = document.createElement('button');
    startPresentationButton.className = 'control-button';
    startPresentationButton.textContent = 'Präsentation starten';
    startPresentationButton.addEventListener('click', () => presentationMode.startPresentation());
    
    // Button zu allen Tab-Inhalten hinzufügen
    document.querySelectorAll('.tab-content').forEach(tabContent => {
        const controlGroups = tabContent.querySelectorAll('.control-group');
        if (controlGroups.length > 0) {
            const lastControlGroup = controlGroups[controlGroups.length - 1];
            const buttonGroup = lastControlGroup.querySelector('.button-group');
            
            if (buttonGroup) {
                const clonedButton = startPresentationButton.cloneNode(true);
                clonedButton.addEventListener('click', () => presentationMode.startPresentation());
                buttonGroup.appendChild(clonedButton);
            }
        }
    });
}

// Fraktal-Steuerelemente verbinden
function connectFractalControls(fractalVisualizer) {
    // Zoom-Slider
    const zoomSlider = document.getElementById('zoom');
    zoomSlider.addEventListener('input', () => {
        const zoomValue = Math.pow(10, parseFloat(zoomSlider.value) / 50);
        fractalVisualizer.updateParams({ zoom: zoomValue });
    });
    
    // Position X-Slider
    const positionXSlider = document.getElementById('position-x');
    positionXSlider.addEventListener('input', () => {
        const currentParams = fractalVisualizer.getParams();
        const newCenter = {
            x: parseFloat(positionXSlider.value) / 50,
            y: currentParams.center.y
        };
        fractalVisualizer.updateParams({ center: newCenter });
    });
    
    // Position Y-Slider
    const positionYSlider = document.getElementById('position-y');
    positionYSlider.addEventListener('input', () => {
        const currentParams = fractalVisualizer.getParams();
        const newCenter = {
            x: currentParams.center.x,
            y: parseFloat(positionYSlider.value) / 50
        };
        fractalVisualizer.updateParams({ center: newCenter });
    });
    
    // Reset-Button
    const resetButton = document.getElementById('reset-fractal');
    resetButton.addEventListener('click', () => {
        fractalVisualizer.reset();
        
        // Slider zurücksetzen
        zoomSlider.value = 10;
        positionXSlider.value = 0;
        positionYSlider.value = 0;
    });
    
    // Speichern-Button
    const saveButton = document.getElementById('save-fractal');
    saveButton.addEventListener('click', () => {
        // Fraktal als Bild speichern
        const canvas = fractalVisualizer.canvas;
        const link = document.createElement('a');
        link.download = 'fractalsense_' + Date.now() + '.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
    
    // Fraktaltyp-Auswahl
    const fractalTypeSelect = document.getElementById('fractal-type');
    fractalTypeSelect.addEventListener('change', () => {
        fractalVisualizer.updateParams({ fractalType: fractalTypeSelect.value });
    });
    
    // Iterationen-Slider
    const iterationsSlider = document.getElementById('iterations');
    iterationsSlider.addEventListener('input', () => {
        fractalVisualizer.updateParams({ maxIterations: parseInt(iterationsSlider.value) });
    });
    
    // Auflösung-Slider
    const resolutionSlider = document.getElementById('resolution');
    resolutionSlider.addEventListener('input', () => {
        fractalVisualizer.updateParams({ resolution: parseFloat(resolutionSlider.value) / 500 });
    });
}

// Tab-Navigation einrichten
function setupTabNavigation() {
    const tabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Aktiven Tab entfernen
            tabs.forEach(t => t.classList.remove('active'));
            
            // Angeklickten Tab aktivieren
            tab.classList.add('active');
            
            // Tab-Inhalt anzeigen
            const tabName = tab.getAttribute('data-tab');
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabName + '-tab') {
                    content.classList.add('active');
                }
            });
        });
    });
}
