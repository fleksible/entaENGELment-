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
        if (this.colorAnimationId) {
            cancelAnimationFrame(this.colorAnimationId);
            this.colorAnimationId = null;
        }

        if (this.colorParams.mode === 'cosmic') {
            this.animateCosmicTheme();
            return;
        }

        this.clearCosmicTheme();

        let gradient;
        switch (this.colorParams.mode) {
            case 'resonant':
                gradient = `linear-gradient(45deg,
                    hsl(280, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(180, ${this.colorParams.intensity * 10}%, 60%),
                    hsl(45, ${this.colorParams.intensity * 10}%, 60%))`;
                break;
            case 'harmonic':
                gradient = `linear-gradient(135deg,
                    hsl(45, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(135, ${this.colorParams.intensity * 10}%, 60%),
                    hsl(225, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(315, ${this.colorParams.intensity * 10}%, 60%))`;
                break;
            case 'spectral':
                gradient = `linear-gradient(to right,
                    hsl(0, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(60, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(120, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(180, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(240, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(300, ${this.colorParams.intensity * 10}%, 50%))`;
                break;
            case 'fractal':
                gradient = `radial-gradient(circle at 30% 40%,
                    hsl(280, ${this.colorParams.intensity * 10}%, 30%),
                    hsl(220, ${this.colorParams.intensity * 10}%, 40%),
                    hsl(180, ${this.colorParams.intensity * 10}%, 20%))`;
                break;
            default:
                gradient = `linear-gradient(45deg,
                    hsl(280, ${this.colorParams.intensity * 10}%, 50%),
                    hsl(180, ${this.colorParams.intensity * 10}%, 60%),
                    hsl(45, ${this.colorParams.intensity * 10}%, 60%))`;
        }

        this.colorPreview.style.background = gradient;
    }

    clearCosmicTheme() {
        while (this.colorPreview.firstChild) {
            this.colorPreview.removeChild(this.colorPreview.firstChild);
        }

        const animationStyle = document.getElementById('twinkle-animation');
        if (animationStyle) {
            animationStyle.remove();
        }
    }

    // Kosmisches Thema animieren
    animateCosmicTheme() {
        const intensity = Math.max(
            1,
            Math.min(10, Number(this.colorParams.intensity) || 1)
        );

        this.clearCosmicTheme();

        this.colorPreview.style.background = `radial-gradient(ellipse at center,
            hsl(240, ${intensity * 10}%, 10%),
            hsl(260, ${intensity * 10}%, 5%))`;

        const numStars = 50 + intensity * 10;
        for (let i = 0; i < numStars; i++) {
            const star = document.createElement('div');
            star.className = 'star';

            const x = Math.random() * 100;
            const y = Math.random() * 100;
            const size = 1 + Math.random() * 3;
            const duration = 2 + Math.random() * 8;

            star.style.cssText = `
                position: absolute;
                left: ${x}%;
                top: ${y}%;
                width: ${size}px;
                height: ${size}px;
                background-color: white;
                border-radius: 50%;
                opacity: ${0.5 + Math.random() * 0.5};
                animation: twinkle ${duration}s infinite alternate;
            `;

            this.colorPreview.appendChild(star);
        }

        const numNebulas = 2 + Math.floor(intensity / 3);
        for (let i = 0; i < numNebulas; i++) {
            const nebula = document.createElement('div');
            nebula.className = 'nebula';

            const x = 20 + Math.random() * 60;
            const y = 20 + Math.random() * 60;
            const size = 30 + Math.random() * 40;
            const hue = 180 + Math.random() * 180;

            nebula.style.cssText = `
                position: absolute;
                left: ${x}%;
                top: ${y}%;
                width: ${size}px;
                height: ${size}px;
                background: radial-gradient(circle,
                    hsla(${hue}, 100%, 70%, 0.3),
                    hsla(${hue}, 100%, 50%, 0.1),
                    transparent 70%);
                border-radius: 50%;
                filter: blur(5px);
            `;

            this.colorPreview.appendChild(nebula);
        }

        if (!document.getElementById('twinkle-animation')) {
            const style = document.createElement('style');
            style.id = 'twinkle-animation';
            style.textContent = `
                @keyframes twinkle {
                    0% { opacity: 0.2; }
                    100% { opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // Klangwellenform visualisieren
    animateSoundWave() {
        const wavePaths = {
            harmonic: 'M0,40 C30,20 10,60 40,40 C70,20 60,60 90,40 C120,20 110,60 140,40 C170,20 160,60 190,40 C220,20 210,60 240,40 C270,20 260,60 290,40',
            fractal: 'M0,40 C10,10 20,70 30,40 C35,20 40,60 45,40 C50,30 55,50 60,40 C70,10 80,70 90,40 C100,20 110,60 120,40 C130,30 140,50 150,40',
            resonant: 'M0,40 C30,40 30,10 60,10 C90,10 90,70 120,70 C150,70 150,10 180,10 C210,10 210,70 240,70 C270,70 270,40 300,40',
            spectral: 'M0,40 C30,10 60,70 90,10 C120,70 150,10 180,70 C210,10 240,70 270,10 C300,70 330,10 360,40'
        };

        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('viewBox', '0 300 80');
        svg.setAttribute('width', '100%');
        svg.setAttribute('height', '100%');

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const soundType = this.soundParams.type in wavePaths ? this.soundParams.type : 'harmonic';
        path.setAttribute('d', wavePaths[soundType]);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', '#9d00ff');
        path.setAttribute('stroke-width', '2');

        const animate = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        animate.setAttribute('attributeName', 'd');
        animate.setAttribute('dur', '2s');
        animate.setAttribute('repeatCount', 'indefinite');

        const randomPath = wavePaths[soundType].split(' ').map(part => {
            if (part.startsWith('M') || part.startsWith('C')) {
                const command = part.substring(0, 1);
                const coordinates = part.substring(1).split(',');
                const x = coordinates[0];
                const y = parseInt(coordinates[1]) + Math.random() * 20 - 10;
                return `${command}${x},${y}`;
            }
            return part;
        }).join(' ');

        animate.setAttribute(
            'values',
            `${wavePaths[soundType]};${randomPath};${wavePaths[soundType]}`
        );
        path.appendChild(animate);
        svg.appendChild(path);

        this.soundWave.innerHTML = '';
        this.soundWave.appendChild(svg);

        this.waveAnimationId = requestAnimationFrame(() => this.animateSoundWave());
    }

    // Sensordaten in laufende Klang-/Farbausgabe einbeziehen
    onSensorDataUpdate(sensorData) {
        if (!this.isPlaying) return;

        if (this.oscillator) {
            const frequencyFactor = 1 + sensorData.accelY * 0.1;
            this.oscillator.frequency.value = this.soundParams.baseFrequency * frequencyFactor;
        }

        if (this.soundParams.harmonics.length > 0) {
            for (let i = 0; i < this.soundParams.harmonics.length; i++) {
                const harmonic = this.soundParams.harmonics[i];

                if (harmonic.oscillator) {
                    const frequencyFactor = 1 + sensorData.gyroX * 0.05;
                    const currentFrequency = harmonic.oscillator.frequency.value;
                    harmonic.oscillator.frequency.value = currentFrequency * frequencyFactor;
                }

                if (harmonic.gain) {
                    harmonic.gain.gain.value =
                        Math.max(0.1, Math.min(1, 0.5 + sensorData.gyroZ * 0.1)) * 0.2;
                }
            }
        }

        const hueRotation = sensorData.accelX * 20;
        const saturation = sensorData.gyroY * 5;
        this.colorPreview.style.filter =
            `hue-rotate(${hueRotation}deg) saturate(${100 + saturation}%)`;
    }

    // Fraktalparameter in Resonanzdarstellung abbilden
    onFractalUpdate(fractalData) {
        if (fractalData.center) {
            const x = fractalData.center.x;
            const y = fractalData.center.y;
            this.soundParams.baseFrequency = 220 * (1 + x * 0.2);

            if (y > 0.5) {
                this.soundParams.type = 'harmonic';
            } else if (y < -0.5) {
                this.soundParams.type = 'fractal';
            } else if (x > 0.5) {
                this.soundParams.type = 'resonant';
            } else if (x < -0.5) {
                this.soundParams.type = 'spectral';
            }

            this.soundTypeSelect.value = this.soundParams.type;
            this.baseFrequencySlider.value = this.soundParams.baseFrequency;

            if (this.isPlaying) {
                this.updateSound();
            }
        }

        if (fractalData.zoom) {
            const zoom = fractalData.zoom;

            if (zoom > 10) {
                this.colorParams.mode = 'cosmic';
            } else if (zoom > 5) {
                this.colorParams.mode = 'fractal';
            } else if (zoom > 2) {
                this.colorParams.mode = 'spectral';
            } else if (zoom > 1) {
                this.colorParams.mode = 'harmonic';
            } else {
                this.colorParams.mode = 'resonant';
            }

            this.colorParams.intensity = Math.min(10, Math.max(1, Math.floor(zoom)));
            this.colorModeSelect.value = this.colorParams.mode;
            this.colorIntensitySlider.value = this.colorParams.intensity;
            this.updateColorPreview();
        }
    }
}

window.ResonanceEnhancer = ResonanceEnhancer;
