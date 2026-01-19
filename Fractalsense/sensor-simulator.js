// FractalSense EntaENGELment - Sensor Simulation Module

// Hauptklasse für die Sensorsimulation
class SensorSimulator {
    constructor() {
        // Sensordaten
        this.sensorData = {
            accelX: 0,
            accelY: 0,
            accelZ: 0,
            gyroX: 0,
            gyroY: 0,
            gyroZ: 0
        };
        
        // Simulationsparameter
        this.simulationSpeed = 5; // 1-10
        this.isSimulating = false;
        this.simulationInterval = null;
        
        // Event-Callbacks
        this.onDataUpdate = null;
        
        // UI-Elemente
        this.initializeUI();
    }
    
    // UI-Elemente initialisieren
    initializeUI() {
        // Slider-Elemente
        this.sliders = {
            accelX: document.getElementById('accel-x-slider'),
            accelY: document.getElementById('accel-y-slider'),
            accelZ: document.getElementById('accel-z-slider'),
            gyroX: document.getElementById('gyro-x-slider'),
            gyroY: document.getElementById('gyro-y-slider'),
            gyroZ: document.getElementById('gyro-z-slider')
        };
        
        // Wert-Anzeigen
        this.valueDisplays = {
            accelX: document.getElementById('accel-x-value'),
            accelY: document.getElementById('accel-y-value'),
            accelZ: document.getElementById('accel-z-value'),
            gyroX: document.getElementById('gyro-x-value'),
            gyroY: document.getElementById('gyro-y-value'),
            gyroZ: document.getElementById('gyro-z-value')
        };
        
        // Buttons
        this.startButton = document.getElementById('start-simulation');
        this.stopButton = document.getElementById('stop-simulation');
        this.randomButton = document.getElementById('random-values');
        
        // Geschwindigkeitsregler
        this.speedSlider = document.getElementById('sensor-speed');
        
        // Event-Listener hinzufügen
        this.setupEventListeners();
    }
    
    // Event-Listener einrichten
    setupEventListeners() {
        // Slider-Events
        for (const [key, slider] of Object.entries(this.sliders)) {
            slider.addEventListener('input', () => {
                const value = parseFloat(slider.value);
                this.updateSensorValue(key, value);
            });
        }
        
        // Button-Events
        this.startButton.addEventListener('click', () => this.startSimulation());
        this.stopButton.addEventListener('click', () => this.stopSimulation());
        this.randomButton.addEventListener('click', () => this.setRandomValues());
        
        // Geschwindigkeitsregler
        this.speedSlider.addEventListener('input', () => {
            this.simulationSpeed = parseInt(this.speedSlider.value);
            if (this.isSimulating) {
                this.restartSimulation();
            }
        });
    }
    
    // Sensordaten aktualisieren
    updateSensorValue(key, value) {
        // Sensordaten aktualisieren
        const sensorKey = this.mapKeyToSensorData(key);
        this.sensorData[sensorKey] = value;
        
        // UI aktualisieren
        if (this.valueDisplays[key]) {
            this.valueDisplays[key].textContent = value.toFixed(2);
        }
        
        // Event auslösen
        this.triggerDataUpdate();
    }
    
    // Schlüssel auf Sensordaten-Eigenschaft abbilden
    mapKeyToSensorData(key) {
        const mapping = {
            accelX: 'accelX',
            accelY: 'accelY',
            accelZ: 'accelZ',
            gyroX: 'gyroX',
            gyroY: 'gyroY',
            gyroZ: 'gyroZ'
        };
        return mapping[key] || key;
    }
    
    // Zufällige Werte setzen
    setRandomValues() {
        for (const key of Object.keys(this.sliders)) {
            const min = parseFloat(this.sliders[key].min);
            const max = parseFloat(this.sliders[key].max);
            const randomValue = min + Math.random() * (max - min);
            
            // Slider aktualisieren
            this.sliders[key].value = randomValue;
            
            // Sensordaten aktualisieren
            this.updateSensorValue(key, randomValue);
        }
    }
    
    // Simulation starten
    startSimulation() {
        if (this.isSimulating) return;
        
        this.isSimulating = true;
        
        // Intervall basierend auf Geschwindigkeit
        const intervalTime = 1000 / this.simulationSpeed;
        
        this.simulationInterval = setInterval(() => {
            this.simulateStep();
        }, intervalTime);
    }
    
    // Simulation stoppen
    stopSimulation() {
        if (!this.isSimulating) return;
        
        clearInterval(this.simulationInterval);
        this.isSimulating = false;
    }
    
    // Simulation neu starten (z.B. nach Geschwindigkeitsänderung)
    restartSimulation() {
        this.stopSimulation();
        this.startSimulation();
    }
    
    // Einen Simulationsschritt ausführen
    simulateStep() {
        // Perlin-Noise-ähnliche Bewegung simulieren
        const time = Date.now() / 1000;
        const amplitude = 0.05; // Änderungsrate
        
        for (const key of Object.keys(this.sliders)) {
            const currentValue = parseFloat(this.sliders[key].value);
            const min = parseFloat(this.sliders[key].min);
            const max = parseFloat(this.sliders[key].max);
            
            // Verschiedene Frequenzen für verschiedene Sensoren
            const frequency = 0.5 + (key.charCodeAt(0) % 5) * 0.1;
            
            // Sinuswelle mit Noise
            const noise = Math.sin(time * frequency + key.length) * amplitude;
            
            // Neuen Wert berechnen und begrenzen
            let newValue = currentValue + noise;
            newValue = Math.max(min, Math.min(max, newValue));
            
            // Slider aktualisieren
            this.sliders[key].value = newValue;
            
            // Sensordaten aktualisieren
            this.updateSensorValue(key, newValue);
        }
    }
    
    // Event für Datenaktualisierung auslösen
    triggerDataUpdate() {
        if (typeof this.onDataUpdate === 'function') {
            this.onDataUpdate(this.sensorData);
        }
        
        // Benutzerdefiniertes Event auslösen
        const event = new CustomEvent('sensor-data-updated', {
            detail: this.sensorData
        });
        document.dispatchEvent(event);
    }
    
    // Callback für Datenaktualisierung registrieren
    registerDataUpdateCallback(callback) {
        this.onDataUpdate = callback;
    }
    
    // Aktuelle Sensordaten abrufen
    getSensorData() {
        return { ...this.sensorData };
    }
    
    // Sensordaten manuell setzen
    setSensorData(data) {
        for (const [key, value] of Object.entries(data)) {
            const uiKey = this.mapSensorDataToKey(key);
            if (this.sliders[uiKey]) {
                this.sliders[uiKey].value = value;
                this.updateSensorValue(uiKey, value);
            }
        }
    }
    
    // Sensordaten-Eigenschaft auf Schlüssel abbilden
    mapSensorDataToKey(sensorKey) {
        const mapping = {
            accelX: 'accelX',
            accelY: 'accelY',
            accelZ: 'accelZ',
            gyroX: 'gyroX',
            gyroY: 'gyroY',
            gyroZ: 'gyroZ'
        };
        return mapping[sensorKey] || sensorKey;
    }
    
    // Sensordaten in Fraktalparameter umwandeln
    mapSensorDataToFractalParams() {
        // Beschleunigung zu Zoom-Änderung
        const zoomFactor = 1.0 + this.sensorData.accelZ * 0.1;
        
        // Gyroskop zu Position
        const positionDeltaX = this.sensorData.gyroY * 0.05;
        const positionDeltaY = -this.sensorData.gyroX * 0.05;
        
        return {
            zoomFactor,
            positionDeltaX,
            positionDeltaY
        };
    }
}

// Sensor-Modul exportieren
window.SensorSimulator = SensorSimulator;
