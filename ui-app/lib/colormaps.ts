/**
 * FractalSense Colormaps - TypeScript port of Fractalsense/color_generator.py
 *
 * Implements φ-based (golden ratio) color palettes for fractal visualization.
 */

// Types
export type RGB = { r: number; g: number; b: number };
export type ColorPalette = RGB[];
export type ColormapName =
  | 'resonant'
  | 'harmonic'
  | 'spectral'
  | 'fractal'
  | 'mereotopological'
  | 'quantum'
  | 'goldenRatio';

// Golden Ratio constant
export const PHI = (1 + Math.sqrt(5)) / 2;

/**
 * Convert HSV to RGB
 * @param h Hue (0-1)
 * @param s Saturation (0-1)
 * @param v Value (0-1)
 */
export function hsvToRgb(h: number, s: number, v: number): RGB {
  // Normalize h to [0, 1)
  h = ((h % 1) + 1) % 1;

  const i = Math.floor(h * 6);
  const f = h * 6 - i;
  const p = v * (1 - s);
  const q = v * (1 - f * s);
  const t = v * (1 - (1 - f) * s);

  let r: number, g: number, b: number;

  switch (i % 6) {
    case 0: r = v; g = t; b = p; break;
    case 1: r = q; g = v; b = p; break;
    case 2: r = p; g = v; b = t; break;
    case 3: r = p; g = q; b = v; break;
    case 4: r = t; g = p; b = v; break;
    case 5: r = v; g = p; b = q; break;
    default: r = 0; g = 0; b = 0;
  }

  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255),
  };
}

/**
 * Convert RGB to CSS color string
 */
export function rgbToCss(rgb: RGB): string {
  return `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
}

/**
 * Convert RGB to hex color string
 */
export function rgbToHex(rgb: RGB): string {
  const toHex = (n: number) => n.toString(16).padStart(2, '0');
  return `#${toHex(rgb.r)}${toHex(rgb.g)}${toHex(rgb.b)}`;
}

/**
 * Resonant colormap: Violet (270°) to Gold (45°)
 * HSV: h = (270 - t * 225) / 360, s = 0.8, v = 0.9
 */
export function generateResonantPalette(size: number = 256): ColorPalette {
  const colors: ColorPalette = [];

  for (let i = 0; i < size; i++) {
    const t = i / (size - 1);
    // HSV gradient from Violet (270°) to Gold (45°)
    const h = (270 - t * 225) / 360;
    const s = 0.8;
    const v = 0.9;
    colors.push(hsvToRgb(h, s, v));
  }

  return colors;
}

/**
 * Harmonic colormap: Golden ratio based color distribution
 * h = (t * PHI) % 1, s/v modulated with sin/cos
 */
export function generateHarmonicPalette(size: number = 256): ColorPalette {
  const colors: ColorPalette = [];

  for (let i = 0; i < size; i++) {
    const t = i / (size - 1);
    // Use golden ratio for harmonic color shift
    const h = (t * PHI) % 1.0;
    const s = 0.7 + 0.3 * Math.sin(t * PHI * Math.PI);
    const v = 0.8 + 0.2 * Math.cos(t * PHI * Math.PI);
    colors.push(hsvToRgb(h, s, v));
  }

  return colors;
}

/**
 * Spectral colormap: Physical wavelength (380-750nm) to RGB
 */
export function generateSpectralPalette(size: number = 256): ColorPalette {
  const colors: ColorPalette = [];

  for (let i = 0; i < size; i++) {
    const t = i / (size - 1);
    // Wavelength from 380nm (violet) to 750nm (red)
    const wavelength = 380 + (750 - 380) * t;

    let r: number, g: number, b: number;

    // Simplified wavelength to RGB conversion
    if (wavelength < 440) {
      r = -(wavelength - 440) / (440 - 380);
      g = 0.0;
      b = 1.0;
    } else if (wavelength < 490) {
      r = 0.0;
      g = (wavelength - 440) / (490 - 440);
      b = 1.0;
    } else if (wavelength < 510) {
      r = 0.0;
      g = 1.0;
      b = -(wavelength - 510) / (510 - 490);
    } else if (wavelength < 580) {
      r = (wavelength - 510) / (580 - 510);
      g = 1.0;
      b = 0.0;
    } else if (wavelength < 645) {
      r = 1.0;
      g = -(wavelength - 645) / (645 - 580);
      b = 0.0;
    } else {
      r = 1.0;
      g = 0.0;
      b = 0.0;
    }

    // Intensity adjustment at spectrum edges
    let factor: number;
    if (wavelength < 420) {
      factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380);
    } else if (wavelength < 700) {
      factor = 1.0;
    } else {
      factor = 0.3 + 0.7 * (750 - wavelength) / (750 - 700);
    }

    r *= factor;
    g *= factor;
    b *= factor;

    colors.push({
      r: Math.round(r * 255),
      g: Math.round(g * 255),
      b: Math.round(b * 255),
    });
  }

  return colors;
}

/**
 * Fractal colormap: Non-linear distribution with sin waves
 * t = sqrt(i/255), h/s/v modulated with sin waves
 */
export function generateFractalPalette(size: number = 256): ColorPalette {
  const colors: ColorPalette = [];

  for (let i = 0; i < size; i++) {
    // Non-linear distribution based on square root
    const t = Math.sqrt(i / (size - 1));

    // Hue based on Mandelbrot-like iteration
    const h = (0.5 + 0.5 * Math.sin(t * 20 * Math.PI)) % 1.0;

    // Saturation and value with fractal patterns
    const s = 0.6 + 0.4 * Math.sin(t * 10 * Math.PI);
    const v = 0.7 + 0.3 * Math.cos(t * 15 * Math.PI);

    colors.push(hsvToRgb(h, s, v));
  }

  return colors;
}

/**
 * Mereotopological colormap: For hypergraphs
 * First half: Blue→Green (nodes), Second half: Red→Violet (edges)
 */
export function generateMereotopologicalPalette(size: number = 256): ColorPalette {
  const colors: ColorPalette = [];
  const half = Math.floor(size / 2);

  // First half for nodes (blue to green)
  for (let i = 0; i < half; i++) {
    const t = i / (half - 1);
    const h = 0.5 + 0.2 * t; // Blue (0.5) to Green (0.7)
    const s = 0.7 + 0.3 * t;
    const v = 0.8;
    colors.push(hsvToRgb(h, s, v));
  }

  // Second half for edges (red to violet)
  for (let i = 0; i < size - half; i++) {
    const t = i / (size - half - 1);
    const h = (0.95 + 0.15 * t) % 1.0; // Red (0.95) to Violet
    const s = 0.8 - 0.2 * t;
    const v = 0.9;
    colors.push(hsvToRgb(h, s, v));
  }

  return colors;
}

/**
 * Quantum colormap: Discrete energy levels, Red→Violet
 */
export function generateQuantumPalette(energyLevels: number = 7, size: number = 256): ColorPalette {
  // Colors for each energy level
  const levelColors: RGB[] = [];

  for (let level = 0; level < energyLevels; level++) {
    const e = level / (energyLevels - 1);
    // Hue based on energy level (red to violet)
    const h = e * 0.8; // 0.0 (red) to 0.8 (violet)
    const s = 0.8;
    const v = 0.9;
    levelColors.push(hsvToRgb(h, s, v));
  }

  // Create colormap with smooth transitions between energy levels
  const colors: ColorPalette = [];

  for (let i = 0; i < size; i++) {
    const t = (i / (size - 1)) * (energyLevels - 1);
    const level = Math.floor(t);
    const frac = t - level;

    // Interpolate between adjacent energy levels
    if (level < energyLevels - 1) {
      const c1 = levelColors[level];
      const c2 = levelColors[level + 1];
      colors.push({
        r: Math.round(c1.r * (1 - frac) + c2.r * frac),
        g: Math.round(c1.g * (1 - frac) + c2.g * frac),
        b: Math.round(c1.b * (1 - frac) + c2.b * frac),
      });
    } else {
      colors.push(levelColors[energyLevels - 1]);
    }
  }

  return colors;
}

/**
 * Golden Ratio colormap: φ-based hue distribution
 * h = (baseHue + t * PHI) % 1
 */
export function generateGoldenRatioPalette(baseHue: number = 0.0, size: number = 256): ColorPalette {
  const colors: ColorPalette = [];

  for (let i = 0; i < size; i++) {
    const t = i / (size - 1);

    // Hue based on golden ratio
    const h = (baseHue + t * PHI) % 1.0;

    // Saturation and value with Fibonacci ratios
    const s = 0.5 + 0.5 * Math.sin(t * PHI * 2 * Math.PI);
    const v = 0.5 + 0.5 * Math.cos(t * PHI * 2 * Math.PI);

    colors.push(hsvToRgb(h, s, v));
  }

  return colors;
}

/**
 * Get a colormap by name
 */
export function getColormap(name: ColormapName, size: number = 256): ColorPalette {
  switch (name) {
    case 'resonant':
      return generateResonantPalette(size);
    case 'harmonic':
      return generateHarmonicPalette(size);
    case 'spectral':
      return generateSpectralPalette(size);
    case 'fractal':
      return generateFractalPalette(size);
    case 'mereotopological':
      return generateMereotopologicalPalette(size);
    case 'quantum':
      return generateQuantumPalette(7, size);
    case 'goldenRatio':
      return generateGoldenRatioPalette(0, size);
    default:
      return generateResonantPalette(size);
  }
}

/**
 * Interpolate a color from a palette based on a value (0-1)
 */
export function interpolateColor(palette: ColorPalette, value: number): RGB {
  // Clamp value to [0, 1]
  const v = Math.max(0, Math.min(1, value));

  // Get position in palette
  const pos = v * (palette.length - 1);
  const i = Math.floor(pos);
  const frac = pos - i;

  // Handle edge case
  if (i >= palette.length - 1) {
    return palette[palette.length - 1];
  }

  // Interpolate between adjacent colors
  const c1 = palette[i];
  const c2 = palette[i + 1];

  return {
    r: Math.round(c1.r * (1 - frac) + c2.r * frac),
    g: Math.round(c1.g * (1 - frac) + c2.g * frac),
    b: Math.round(c1.b * (1 - frac) + c2.b * frac),
  };
}

/**
 * All available colormap names
 */
export const COLORMAP_NAMES: ColormapName[] = [
  'resonant',
  'harmonic',
  'spectral',
  'fractal',
  'mereotopological',
  'quantum',
  'goldenRatio',
];

/**
 * Colormap display labels
 */
export const COLORMAP_LABELS: Record<ColormapName, string> = {
  resonant: 'Resonant (Violett→Gold)',
  harmonic: 'Harmonic (φ-based)',
  spectral: 'Spectral (380-750nm)',
  fractal: 'Fractal (sin waves)',
  mereotopological: 'Mereotopological',
  quantum: 'Quantum (Energy)',
  goldenRatio: 'Golden Ratio',
};
