// FractalSense EntaENGELment - Fractal Visualization Module

// Hauptklasse für die Fraktalvisualisierung
class FractalVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // Standardparameter
        this.center = { x: -0.75, y: 0 };
        this.zoom = 1.0;
        this.maxIterations = 100;
        this.resolution = 1.0; // Auflösungsfaktor (1.0 = volle Auflösung)
        this.fractalType = 'mandelbrot';
        
        // Farbpalette
        this.colorPalette = this.generateColorPalette();
        
        // Initialisierung
        this.resizeCanvas();
        this.render();
        
        // Event-Listener für Größenänderungen
        window.addEventListener('resize', () => this.resizeCanvas());
        
        // Interaktivität
        this.setupInteractivity();
    }
    
    // Canvas an Containergröße anpassen
    resizeCanvas() {
        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;
        this.render();
    }
    
    // Farbpalette generieren
    generateColorPalette() {
        const palette = [];
        const paletteSize = 256;
        
        // Violett zu Gold Gradient (EntaENGELment-Thema)
        for (let i = 0; i < paletteSize; i++) {
            const t = i / paletteSize;
            
            // HSL-Farbverlauf von Violett (270°) zu Gold (45°)
            const h = 270 - t * 225;
            const s = 80;
            const l = 50 + t * 20;
            
            palette.push(`hsl(${h}, ${s}%, ${l}%)`);
        }
        
        return palette;
    }
    
    // Fraktal rendern
    render() {
        const { width, height } = this.canvas;
        const imageData = this.ctx.createImageData(width, height);
        const data = imageData.data;
        
        // Skalierungsfaktor für die Auflösung
        const scaleFactor = this.resolution;
        const scaledWidth = Math.floor(width * scaleFactor);
        const scaledHeight = Math.floor(height * scaleFactor);
        
        // Bereich im komplexen Zahlenraum
        const xRange = 3.0 / this.zoom;
        const yRange = (height / width) * xRange;
        const xMin = this.center.x - xRange / 2;
        const yMin = this.center.y - yRange / 2;
        const dx = xRange / scaledWidth;
        const dy = yRange / scaledHeight;
        
        // Für jeden Pixel das Fraktal berechnen
        for (let y = 0; y < scaledHeight; y++) {
            for (let x = 0; x < scaledWidth; x++) {
                // Komplexe Zahl c = a + bi
                const a = xMin + x * dx;
                const b = yMin + y * dy;
                
                // Iterationen berechnen je nach Fraktaltyp
                let iterations;
                switch (this.fractalType) {
                    case 'julia':
                        iterations = this.calculateJulia(a, b);
                        break;
                    case 'burning-ship':
                        iterations = this.calculateBurningShip(a, b);
                        break;
                    case 'mandelbrot':
                    default:
                        iterations = this.calculateMandelbrot(a, b);
                        break;
                }
                
                // Farbe basierend auf Iterationen bestimmen
                const color = this.getColor(iterations);
                
                // Bei niedrigerer Auflösung Pixel mehrfach setzen
                const pixelX = Math.floor(x / scaleFactor);
                const pixelY = Math.floor(y / scaleFactor);
                
                if (pixelX < width && pixelY < height) {
                    const pixelIndex = (pixelY * width + pixelX) * 4;
                    data[pixelIndex] = color.r;     // R
                    data[pixelIndex + 1] = color.g; // G
                    data[pixelIndex + 2] = color.b; // B
                    data[pixelIndex + 3] = 255;     // A
                }
            }
        }
        
        this.ctx.putImageData(imageData, 0, 0);
    }
    
    // Mandelbrot-Berechnung
    calculateMandelbrot(a, b) {
        let ca = a;
        let cb = b;
        let za = 0;
        let zb = 0;
        
        let i;
        for (i = 0; i < this.maxIterations; i++) {
            // z = z² + c
            const temp = za * za - zb * zb + ca;
            zb = 2 * za * zb + cb;
            za = temp;
            
            // Wenn |z| > 2, dann divergiert die Folge
            if (za * za + zb * zb > 4) {
                break;
            }
        }
        
        // Smooth coloring
        if (i < this.maxIterations) {
            // Logarithmische Glättung
            const log_zn = Math.log(za * za + zb * zb) / 2;
            const nu = Math.log(log_zn / Math.log(2)) / Math.log(2);
            i = i + 1 - nu;
        }
        
        return i;
    }
    
    // Julia-Berechnung
    calculateJulia(a, b) {
        // Julia-Set Parameter (kann dynamisch geändert werden)
        const ca = -0.7;
        const cb = 0.27;
        
        let za = a;
        let zb = b;
        
        let i;
        for (i = 0; i < this.maxIterations; i++) {
            // z = z² + c
            const temp = za * za - zb * zb + ca;
            zb = 2 * za * zb + cb;
            za = temp;
            
            if (za * za + zb * zb > 4) {
                break;
            }
        }
        
        // Smooth coloring
        if (i < this.maxIterations) {
            const log_zn = Math.log(za * za + zb * zb) / 2;
            const nu = Math.log(log_zn / Math.log(2)) / Math.log(2);
            i = i + 1 - nu;
        }
        
        return i;
    }
    
    // Burning Ship Fraktal
    calculateBurningShip(a, b) {
        let ca = a;
        let cb = b;
        let za = 0;
        let zb = 0;
        
        let i;
        for (i = 0; i < this.maxIterations; i++) {
            // Burning Ship verwendet |Re(z)| + i|Im(z)| statt z
            za = Math.abs(za);
            zb = Math.abs(zb);
            
            // z = z² + c
            const temp = za * za - zb * zb + ca;
            zb = 2 * za * zb + cb;
            za = temp;
            
            if (za * za + zb * zb > 4) {
                break;
            }
        }
        
        // Smooth coloring
        if (i < this.maxIterations) {
            const log_zn = Math.log(za * za + zb * zb) / 2;
            const nu = Math.log(log_zn / Math.log(2)) / Math.log(2);
            i = i + 1 - nu;
        }
        
        return i;
    }
    
    // Farbe basierend auf Iterationen bestimmen
    getColor(iterations) {
        if (iterations >= this.maxIterations) {
            // Punkte in der Menge sind schwarz
            return { r: 0, g: 0, b: 0 };
        } else {
            // Normalisierte Iteration für Farbindex
            const normalizedI = iterations / this.maxIterations;
            const colorIndex = Math.floor(normalizedI * (this.colorPalette.length - 1));
            
            // Farbe aus der Palette holen
            const colorStr = this.colorPalette[colorIndex];
            
            // HSL zu RGB konvertieren
            return this.hslToRgb(colorStr);
        }
    }
    
    // HSL-String zu RGB-Objekt konvertieren
    hslToRgb(hslStr) {
        // HSL-String parsen (Format: "hsl(h, s%, l%)")
        const hslRegex = /hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)/;
        const match = hslStr.match(hslRegex);
        
        if (!match) {
            return { r: 0, g: 0, b: 0 };
        }
        
        let h = parseInt(match[1]) / 360;
        let s = parseInt(match[2]) / 100;
        let l = parseInt(match[3]) / 100;
        
        let r, g, b;
        
        if (s === 0) {
            r = g = b = l; // Graustufe
        } else {
            const hue2rgb = (p, q, t) => {
                if (t < 0) t += 1;
                if (t > 1) t -= 1;
                if (t < 1/6) return p + (q - p) * 6 * t;
                if (t < 1/2) return q;
                if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
                return p;
            };
            
            const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            const p = 2 * l - q;
            
            r = hue2rgb(p, q, h + 1/3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1/3);
        }
        
        return {
            r: Math.round(r * 255),
            g: Math.round(g * 255),
            b: Math.round(b * 255)
        };
    }
    
    // Interaktivität einrichten
    setupInteractivity() {
        // Maus-Interaktion für Zoom und Pan
        let isDragging = false;
        let lastX, lastY;
        
        this.canvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            lastX = e.offsetX;
            lastY = e.offsetY;
        });
        
        this.canvas.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const dx = e.offsetX - lastX;
            const dy = e.offsetY - lastY;
            
            // Umrechnung von Pixeln in komplexe Zahlen
            const xRange = 3.0 / this.zoom;
            const yRange = (this.canvas.height / this.canvas.width) * xRange;
            
            // Verschiebung des Zentrums
            this.center.x -= dx * xRange / this.canvas.width;
            this.center.y -= dy * yRange / this.canvas.height;
            
            lastX = e.offsetX;
            lastY = e.offsetY;
            
            this.render();
        });
        
        this.canvas.addEventListener('mouseup', () => {
            isDragging = false;
        });
        
        this.canvas.addEventListener('mouseleave', () => {
            isDragging = false;
        });
        
        // Zoom mit Mausrad
        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            
            // Mausposition im Canvas
            const rect = this.canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            
            // Umrechnung von Pixeln in komplexe Zahlen
            const xRange = 3.0 / this.zoom;
            const yRange = (this.canvas.height / this.canvas.width) * xRange;
            const xMin = this.center.x - xRange / 2;
            const yMin = this.center.y - yRange / 2;
            
            // Position im komplexen Zahlenraum
            const mouseRealX = xMin + (mouseX / this.canvas.width) * xRange;
            const mouseRealY = yMin + (mouseY / this.canvas.height) * yRange;
            
            // Zoom-Faktor
            const zoomFactor = e.deltaY < 0 ? 1.2 : 0.8;
            
            // Zoom anpassen
            this.zoom *= zoomFactor;
            
            // Neues Zentrum berechnen, um an der Mausposition zu zoomen
            const newXRange = 3.0 / this.zoom;
            const newYRange = (this.canvas.height / this.canvas.width) * newXRange;
            
            this.center.x = mouseRealX - (mouseX / this.canvas.width - 0.5) * newXRange;
            this.center.y = mouseRealY - (mouseY / this.canvas.height - 0.5) * newYRange;
            
            this.render();
        });
        
        // Touch-Interaktion für mobile Geräte
        let lastTouchDistance = 0;
        
        this.canvas.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                isDragging = true;
                lastX = e.touches[0].clientX;
                lastY = e.touches[0].clientY;
            } else if (e.touches.length === 2) {
                // Zwei-Finger-Zoom
                const touch1 = e.touches[0];
                const touch2 = e.touches[1];
                lastTouchDistance = Math.hypot(
                    touch2.clientX - touch1.clientX,
                    touch2.clientY - touch1.clientY
                );
            }
        });
        
        this.canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            
            if (e.touches.length === 1 && isDragging) {
                const touch = e.touches[0];
                const dx = touch.clientX - lastX;
                const dy = touch.clientY - lastY;
                
                // Umrechnung von Pixeln in komplexe Zahlen
                const xRange = 3.0 / this.zoom;
                const yRange = (this.canvas.height / this.canvas.width) * xRange;
                
                // Verschiebung des Zentrums
                this.center.x -= dx * xRange / this.canvas.width;
                this.center.y -= dy * yRange / this.canvas.height;
                
                lastX = touch.clientX;
                lastY = touch.clientY;
                
                this.render();
            } else if (e.touches.length === 2) {
                // Zwei-Finger-Zoom
                const touch1 = e.touches[0];
                const touch2 = e.touches[1];
                const currentDistance = Math.hypot(
                    touch2.clientX - touch1.clientX,
                    touch2.clientY - touch1.clientY
                );
                
                if (lastTouchDistance > 0) {
                    // Mittelpunkt der beiden Finger
                    const centerX = (touch1.clientX + touch2.clientX) / 2;
                    const centerY = (touch1.clientY + touch2.clientY) / 2;
                    
                    // Umrechnung von Pixeln in komplexe Zahlen
                    const rect = this.canvas.getBoundingClientRect();
                    const mouseX = centerX - rect.left;
                    const mouseY = centerY - rect.top;
                    
                    const xRange = 3.0 / this.zoom;
                    const yRange = (this.canvas.height / this.canvas.width) * xRange;
                    const xMin = this.center.x - xRange / 2;
                    const yMin = this.center.y - yRange / 2;
                    
                    // Position im komplexen Zahlenraum
                    const mouseRealX = xMin + (mouseX / this.canvas.width) * xRange;
                    const mouseRealY = yMin + (mouseY / this.canvas.height) * yRange;
                    
                    // Zoom-Faktor
                    const zoomFactor = currentDistance / lastTouchDistance;
                    
                    // Zoom anpassen
                    this.zoom *= zoomFactor;
                    
                    // Neues Zentrum berechnen, um an der Mausposition zu zoomen
                    const newXRange = 3.0 / this.zoom;
                    const newYRange = (this.canvas.height / this.canvas.width) * newXRange;
                    
                    this.center.x = mouseRealX - (mouseX / this.canvas.width - 0.5) * newXRange;
                    this.center.y = mouseRealY - (mouseY / this.canvas.height - 0.5) * newYRange;
                    
                    this.render();
                }
                
                lastTouchDistance = currentDistance;
            }
        });
        
        this.canvas.addEventListener('touchend', () => {
            isDragging = false;
            lastTouchDistance = 0;
        });
    }
    
    // Parameter aktualisieren
    updateParams(params) {
        if (params.center) this.center = params.center;
        if (params.zoom) this.zoom = params.zoom;
        if (params.maxIterations) this.maxIterations = params.maxIterations;
        if (params.resolution) this.resolution = params.resolution;
        if (params.fractalType) this.fractalType = params.fractalType;
        
        this.render();
    }
    
    // Aktuelle Parameter abrufen
    getParams() {
        return {
            center: this.center,
            zoom: this.zoom,
            maxIterations: this.maxIterations,
            resolution: this.resol
(Content truncated due to size limit. Use line ranges to read in chunks)