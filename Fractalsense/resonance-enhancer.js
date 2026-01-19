// FractalSense EntaENGELment - Resonance Enhancer Module

// Hauptklasse für den ResonanceEnhancer
class ResonanceEnhancer {
    constructor() {
        // Audio-Kontext
        this.audioContext = null;
        this.oscillator = null;
        this.gainNode = null;
        this.isPlaying = false;
        
        // Klangparameter
        this.soundParams = {
            type: 'harmonic',     // harmonic, fractal, resonant, spectral
            baseFrequency: 220,   // Hz
            volume: 0.5,          // 0-1
            harmonics: []         // Wird basierend auf Typ generiert
        };
        
        // Farbparameter
        this.colorParams = {
            mode: 'resonant',     // resonant, harmonic, spectral, fractal, cosmic
            speed: 5,             // 1-10
            intensity: 7          // 1-10
        };
        
        // Animation
        this.colorAnimationId = null;
        
        // UI-Elemente
        this.initializeUI();
        
        // Audio-Kontext initialisieren
        this.initAudio();
    }
    
    // UI-Elemente initialisieren
    initializeUI() {
        // Klang-Steuerelemente
        this.soundTypeSelect = document.getElementById('sound-type');
        this.baseFrequencySlider = document.getElementById('base-frequency');
        this.volumeSlider = document.getElementById('volume');
        this.playButton = document.getElementById('play-sound');
        this.soundWave = document.getElementById('sound-wave');
        
        // Farb-Steuerelemente
        this.colorModeSelect = document.getElementById('color-mode');
        this.colorSpeedSlider = document.getElementById('color-speed');
        this.colorIntensitySlider = document.getElementById('color-intensity');
        this.colorPreview = document.getElementById('color-preview');
        
        // Event-Listener hinzufügen
        this.setupEventListeners();
    }
    
    // Audio-Kontext initialisieren
    initAudio() {
        // AudioContext erst bei Benutzerinteraktion erstellen (Browser-Richtlinie)
        document.addEventListener('click', () => {
            if (!this.audioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                this.setupAudioNodes();
            }
        }, { once: true });
    }
    
    // Audio-Knoten einrichten
    setupAudioNodes() {
        // Gain-Node für Lautstärkeregelung
        this.gainNode = this.audioContext.createGain();
        this.gainNode.gain.value = this.soundParams.volume;
        this.gainNode.connect(this.audioContext.destination);
    }
    
    // Event-Listener einrichten
    setupEventListeners() {
        // Klang-Events
        this.soundTypeSelect.addEventListener('change', () => {
            this.soundParams.type = this.soundTypeSelect.value;
            this.updateSound();
        });
        
        this.baseFrequencySlider.addEventListener('input', () => {
            this.soundParams.baseFrequency = parseFloat(this.baseFrequencySlider.value);
            this.updateSound();
        });
        
        this.volumeSlider.addEventListener('input', () => {
            this.soundParams.volume = parseFloat(this.volumeSlider.value) / 100;
            if (this.gainNode) {
                this.gainNode.gain.value = this.soundParams.volume;
            }
        });
        
        this.playButton.addEventListener('click', () => {
            if (this.isPlaying) {
                this.stopSound();
            } else {
                this.playSound();
            }
        });
        
        // Farb-Events
        this.colorModeSelect.addEventListener('change', () => {
            this.colorParams.mode = this.colorModeSelect.value;
            this.updateColorPreview();
        });
        
        this.colorSpeedSlider.addEventListener('input', () => {
            this.colorParams.speed = parseInt(this.colorSpeedSlider.value);
        });
        
        this.colorIntensitySlider.addEventListener('input', () => {
            this.colorParams.intensity = parseInt(this.colorIntensitySlider.value);
            this.updateColorPreview();
        });
        
        // Sensor-Daten-Event
        document.addEventListener('sensor-data-updated', (event) => {
            this.onSensorDataUpdate(event.detail);
        });
        
        // Fraktal-Update-Event
        document.addEventListener('fractal-updated', (event) => {
            this.onFractalUpdate(event.detail);
        });
    }
    
    // Klang abspielen
    playSound() {
        if (this.isPlaying || !this.audioContext) return;
        
        // Oszillator erstellen
        this.oscillator = this.audioContext.createOscillator();
        
        // Typ basierend auf soundParams.type setzen
        switch (this.soundParams.type) {
            case 'harmonic':
                this.setupHarmonicSound();
                break;
            case 'fractal':
                this.setupFractalSound();
                break;
            case 'resonant':
                this.setupResonantSound();
                break;
            case 'spectral':
                this.setupSpectralSound();
                break;
            default:
                this.oscillator.type = 'sine';
                this.oscillator.frequency.value = this.soundParams.baseFrequency;
        }
        
        // Mit Gain-Node verbinden und starten
        this.oscillator.connect(this.gainNode);
        this.oscillator.start();
        
        this.isPlaying = true;
        this.playButton.innerHTML = '<div class="play-icon" style="border-width: 0 8px 0 8px;"></div> Stop';
        
        // Wellenform-Animation starten
        this.animateSoundWave();
    }
    
    // Klang stoppen
    stopSound() {
        if (!this.isPlaying || !this.oscillator) return;
        
        this.oscillator.stop();
        this.oscillator.disconnect();
        this.oscillator = null;
        
        this.isPlaying = false;
        this.playButton.innerHTML = '<div class="play-icon"></div> Klang abspielen';
        
        // Wellenform-Animation stoppen
        if (this.waveAnimationId) {
            cancelAnimationFrame(this.waveAnimationId);
            this.waveAnimationId = null;
        }
    }
    
    // Harmonischen Klang einrichten (basierend auf goldenem Schnitt)
    setupHarmonicSound() {
        // Grundfrequenz
        this.oscillator.type = 'sine';
        this.oscillator.frequency.value = this.soundParams.baseFrequency;
        
        // Harmonische Obertöne basierend auf goldenem Schnitt
        const goldenRatio = 1.61803398875;
        const harmonics = [];
        
        // Mehrere Oszillatoren für Obertöne
        for (let i = 1; i <= 5; i++) {
            const harmonic = this.audioContext.createOscillator();
            harmonic.type = 'sine';
            
            // Frequenz basierend auf goldenem Schnitt
            const freq = this.soundParams.baseFrequency * Math.pow(goldenRatio, i % 3);
            harmonic.frequency.value = freq;
            
            // Gain für jeden Oberton
            const harmonicGain = this.audioContext.createGain();
            harmonicGain.gain.value = 0.15 / (i * 0.8); // Abnehmende Lautstärke
            
            harmonic.connect(harmonicGain);
            harmonicGain.connect(this.gainNode);
            harmonic.start();
            
            harmonics.push({ oscillator: harmonic, gain: harmonicGain });
        }
        
        this.soundParams.harmonics = harmonics;
    }
    
    // Fraktalen Klang einrichten (selbstähnliche Struktur)
    setupFractalSound() {
        // Grundfrequenz
        this.oscillator.type = 'sawtooth'; // Sägezahn für reichhaltigeres Spektrum
        this.oscillator.frequency.value = this.soundParams.baseFrequency;
        
        // Fraktale Modulation mit Feedback
        const feedbackDelay = this.audioContext.createDelay();
        feedbackDelay.delayTime.value = 0.1 + (Math.random() * 0.2);
        
        const feedbackGain = this.audioContext.createGain();
        feedbackGain.gain.value = 0.4;
        
        // Feedback-Schleife
        this.oscillator.connect(feedbackDelay);
        feedbackDelay.connect(feedbackGain);
        feedbackGain.connect(feedbackDelay);
        feedbackGain.connect(this.gainNode);
        
        // Zusätzliche Modulation
        const modulator = this.audioContext.createOscillator();
        modulator.type = 'sine';
        modulator.frequency.value = this.soundParams.baseFrequency / 4;
        
        const modulationGain = this.audioContext.createGain();
        modulationGain.gain.value = 20;
        
        modulator.connect(modulationGain);
        modulationGain.connect(this.oscillator.frequency);
        modulator.start();
        
        this.soundParams.harmonics = [
            { oscillator: modulator, gain: modulationGain },
            { delay: feedbackDelay, gain: feedbackGain }
        ];
    }
    
    // Resonanten Klang einrichten (basierend auf Resonanzfrequenzen)
    setupResonantSound() {
        // Grundfrequenz
        this.oscillator.type = 'sine';
        this.oscillator.frequency.value = this.soundParams.baseFrequency;
        
        // Resonanzfilter
        const filters = [];
        const resonanceFreqs = [
            this.soundParams.baseFrequency * 1.5,
            this.soundParams.baseFrequency * 2.0,
            this.soundParams.baseFrequency * 2.5
        ];
        
        // Noise-Generator für Anregung der Resonanzfilter
        const noiseBuffer = this.createNoiseBuffer();
        const noiseSource = this.audioContext.createBufferSource();
        noiseSource.buffer = noiseBuffer;
        noiseSource.loop = true;
        
        const noiseGain = this.audioContext.createGain();
        noiseGain.gain.value = 0.2;
        noiseSource.connect(noiseGain);
        
        // Resonanzfilter erstellen
        for (let i = 0; i < resonanceFreqs.length; i++) {
            const filter = this.audioContext.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.value = resonanceFreqs[i];
            filter.Q.value = 20; // Hohe Resonanz
            
            noiseGain.connect(filter);
            filter.connect(this.gainNode);
            
            filters.push(filter);
        }
        
        noiseSource.start();
        
        this.soundParams.harmonics = [
            { source: noiseSource, gain: noiseGain, filters: filters }
        ];
    }
    
    // Spektralen Klang einrichten (basierend auf Frequenzspektrum)
    setupSpectralSound() {
        // Grundfrequenz
        this.oscillator.type = 'sine';
        this.oscillator.frequency.value = this.soundParams.baseFrequency;
        
        // Additiver Synthesizer mit vielen Frequenzen
        const oscillators = [];
        const numOscillators = 8;
        
        // Spektrale Verteilung
        for (let i = 0; i < numOscillators; i++) {
            const osc = this.audioContext.createOscillator();
            
            // Verschiedene Wellenformen
            const waveforms = ['sine', 'triangle', 'sawtooth', 'square'];
            osc.type = waveforms[i % waveforms.length];
            
            // Frequenzverteilung basierend auf Obertönen
            const freqMultiplier = i === 0 ? 1 : i * (1 + (i % 3) * 0.1);
            osc.frequency.value = this.soundParams.baseFrequency * freqMultiplier;
            
            // Individuelle Lautstärke
            const oscGain = this.audioContext.createGain();
            oscGain.gain.value = 0.15 / (i + 1);
            
            osc.connect(oscGain);
            oscGain.connect(this.gainNode);
            osc.start();
            
            oscillators.push({ oscillator: osc, gain: oscGain });
        }
        
        this.soundParams.harmonics = oscillators;
    }
    
    // Rauschen für Resonanzfilter erzeugen
    createNoiseBuffer() {
        const bufferSize = this.audioContext.sampleRate * 2; // 2 Sekunden
        const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const data = buffer.getChannelData(0);
        
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        
        return buffer;
    }
    
    // Klang aktualisieren
    updateSound() {
        if (this.isPlaying) {
            // Aktuellen Klang stoppen und neu starten
            this.stopSound();
            this.playSound();
        }
    }
    
    // Farb-Vorschau aktualisieren
    updateColorPreview() {
        // Animation stoppen, falls vorhanden
        if (this.colorAnimationId) {
            cancelAnimationFrame(this.colorAnimationId);
        }
        
        // Gradient basierend auf Modus
        let gradient;
        
        switch (this.colorParams.mode) {
            case 'resonant':
                gradient = `linear-gradient(45deg, 
                    hsl(280, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(180, ${this.colorParams.intensity * 10}%, 60%), 
                    hsl(45, ${this.colorParams.intensity * 10}%, 60%))`;
                break;
                
            case 'harmonic':
                // Basierend auf Fibonacci-Sequenz / goldenem Schnitt
                gradient = `linear-gradient(135deg, 
                    hsl(45, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(135, ${this.colorParams.intensity * 10}%, 60%), 
                    hsl(225, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(315, ${this.colorParams.intensity * 10}%, 60%))`;
                break;
                
            case 'spectral':
                // Basierend auf Lichtspektrum
                gradient = `linear-gradient(to right, 
                    hsl(0, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(60, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(120, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(180, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(240, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(300, ${this.colorParams.intensity * 10}%, 50%))`;
                break;
                
            case 'fractal':
                // Fraktale Farbgebung
                gradient = `radial-gradient(circle at 30% 40%, 
                    hsl(280, ${this.colorParams.intensity * 10}%, 30%), 
                    hsl(220, ${this.colorParams.intensity * 10}%, 40%), 
                    hsl(180, ${this.colorParams.intensity * 10}%, 20%))`;
                break;
                
            case 'cosmic':
                // Kosmisches Thema mit Sternen
                this.animateCosmicTheme();
                return;
                
            default:
                gradient = `linear-gradient(45deg, 
                    hsl(280, ${this.colorParams.intensity * 10}%, 50%), 
                    hsl(180, ${this.colorParams.intensity * 10}%, 60%), 
                    hsl(45, ${this.colorParams.intensity * 10}%, 60%))`;
        }
        
        this.colorPreview.style.background = gradient;
    }
    
    // Kosmisches Thema animieren
    animateCosmicTheme() {
        // Hintergrund
        this.colorPreview.style.background = `radial-gradient(ellipse at center, 
            hsl(240, ${this.colorParams.intensity * 10}%, 10%), 
            hsl(260, ${this.colorParams.intensity * 10}%, 5%))`;
        
        // Sterne entfernen, falls vorhanden
        while (this.colorPreview.firstChild) {
            this.colorPreview.removeChild(this.colorPreview.firstChild);
        }
        
        // Sterne hinzufügen
        const numStars = 50 + this.colorParams.intensity * 10;
        for (let i = 0; i < numStars; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            
            // Zufällige Position
   
(Content truncated due to size limit. Use line ranges to read in chunks)