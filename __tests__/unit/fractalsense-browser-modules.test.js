const fs = require('fs');
const path = require('path');
const { MockCanvasRenderingContext2D } = require('../__mocks__/canvas');

function loadBrowserClass(modulePath, globalName) {
  jest.resetModules();
  delete window[globalName];
  require(modulePath);
  return window[globalName];
}

function installFractalDom() {
  document.body.innerHTML = '<div id="canvas-wrap"><canvas id="fractal-canvas"></canvas></div>';
  const canvas = document.getElementById('fractal-canvas');
  const parent = canvas.parentElement;

  Object.defineProperty(parent, 'clientWidth', { configurable: true, value: 12 });
  Object.defineProperty(parent, 'clientHeight', { configurable: true, value: 8 });

  const ctx = new MockCanvasRenderingContext2D(canvas);
  canvas.getContext = jest.fn(() => ctx);
  canvas.getBoundingClientRect = jest.fn(() => ({
    left: 0,
    top: 0,
    right: 12,
    bottom: 8,
    width: 12,
    height: 8
  }));

  return { canvas, ctx };
}

function installPresentationDom() {
  document.body.innerHTML = `
    <div class="content-area">
      <div class="nav-tab active" data-tab="fractal"></div>
      <div class="nav-tab" data-tab="sensors"></div>
      <div class="nav-tab" data-tab="resonance"></div>
      <div id="fractal-tab" class="tab-content active"></div>
      <div id="sensors-tab" class="tab-content"></div>
      <div id="resonance-tab" class="tab-content"></div>
      <button id="prev-slide"></button>
      <button id="next-slide"></button>
      <button id="pause-presentation"></button>
    </div>
  `;
}

function installResonanceDom() {
  document.body.innerHTML = `
    <select id="sound-type">
      <option value="harmonic">harmonic</option>
      <option value="fractal">fractal</option>
      <option value="resonant">resonant</option>
      <option value="spectral">spectral</option>
    </select>
    <input id="base-frequency" value="220">
    <input id="volume" value="50">
    <button id="play-sound"></button>
    <div id="sound-wave"></div>
    <select id="color-mode">
      <option value="resonant">resonant</option>
      <option value="harmonic">harmonic</option>
      <option value="spectral">spectral</option>
      <option value="fractal">fractal</option>
      <option value="cosmic">cosmic</option>
    </select>
    <input id="color-speed" value="5">
    <input id="color-intensity" value="7">
    <div id="color-preview"></div>
  `;
}

describe('Fractalsense browser source loading', () => {
  afterEach(() => {
    jest.restoreAllMocks();
    document.body.innerHTML = '';
    document.head.querySelector('#twinkle-animation')?.remove();
  });

  test.each([
    ['../../Fractalsense/fractal-visualizer.js', 'FractalVisualizer'],
    ['../../Fractalsense/presentation-mode.js', 'PresentationMode'],
    ['../../Fractalsense/resonance-enhancer.js', 'ResonanceEnhancer']
  ])('%s parses and publishes %s', (modulePath, globalName) => {
    expect(() => loadBrowserClass(modulePath, globalName)).not.toThrow();
    expect(window[globalName]).toEqual(expect.any(Function));
  });

  test('index loads globals before app.js', () => {
    const html = fs.readFileSync(
      path.join(__dirname, '../../Fractalsense/index.html'),
      'utf8'
    );
    const expectedOrder = [
      'fractal-visualizer.js',
      'sensor-simulator.js',
      'resonance-enhancer.js',
      'presentation-mode.js',
      'app.js'
    ];

    const offsets = expectedOrder.map(name => html.indexOf(`src="${name}"`));
    expect(offsets.every(offset => offset >= 0)).toBe(true);
    expect(offsets).toEqual([...offsets].sort((a, b) => a - b));
  });
});

describe('FractalVisualizer restored contract', () => {
  let FractalVisualizer;
  let visualizer;

  beforeEach(() => {
    installFractalDom();
    FractalVisualizer = loadBrowserClass(
      '../../Fractalsense/fractal-visualizer.js',
      'FractalVisualizer'
    );
    visualizer = new FractalVisualizer('fractal-canvas');
  });

  afterEach(() => {
    jest.restoreAllMocks();
    document.body.innerHTML = '';
  });

  test('getParams exposes the complete archived parameter contract', () => {
    expect(visualizer.getParams()).toEqual({
      center: { x: -0.75, y: 0 },
      zoom: 1,
      maxIterations: 100,
      resolution: 1,
      fractalType: 'mandelbrot'
    });

    visualizer.updateParams({
      center: { x: -0.2, y: 0.3 },
      zoom: 4,
      maxIterations: 32,
      resolution: 0.5,
      fractalType: 'julia'
    });

    expect(visualizer.getParams()).toEqual({
      center: { x: -0.2, y: 0.3 },
      zoom: 4,
      maxIterations: 32,
      resolution: 0.5,
      fractalType: 'julia'
    });
  });

  test('reset restores center and zoom while preserving rendering configuration', () => {
    visualizer.updateParams({
      center: { x: 0.1, y: -0.2 },
      zoom: 8,
      maxIterations: 24,
      resolution: 0.5,
      fractalType: 'burning-ship'
    });

    const renderSpy = jest.spyOn(visualizer, 'render');
    visualizer.reset();

    expect(visualizer.getParams()).toEqual({
      center: { x: -0.75, y: 0 },
      zoom: 1,
      maxIterations: 24,
      resolution: 0.5,
      fractalType: 'burning-ship'
    });
    expect(renderSpy).toHaveBeenCalled();
  });

  test('archived fractal variants still produce bounded iteration values', () => {
    for (const calculate of [
      visualizer.calculateMandelbrot.bind(visualizer),
      visualizer.calculateJulia.bind(visualizer),
      visualizer.calculateBurningShip.bind(visualizer)
    ]) {
      const value = calculate(2, 2);
      expect(Number.isFinite(value)).toBe(true);
      expect(value).toBeLessThanOrEqual(visualizer.maxIterations);
    }
  });

  test('HSL conversion preserves the archived RGB contract', () => {
    expect(visualizer.hslToRgb('hsl(0, 100%, 50%)')).toEqual({ r: 255, g: 0, b: 0 });
    expect(visualizer.hslToRgb('not-a-color')).toEqual({ r: 0, g: 0, b: 0 });
  });
});

describe('PresentationMode reconstructed action contract', () => {
  let PresentationMode;
  let presentation;
  let fractal;
  let sensor;
  let resonance;

  beforeEach(() => {
    jest.useFakeTimers();
    installPresentationDom();
    PresentationMode = loadBrowserClass(
      '../../Fractalsense/presentation-mode.js',
      'PresentationMode'
    );
    presentation = new PresentationMode();

    fractal = {
      updateParams: jest.fn(),
      getParams: jest.fn(() => ({ zoom: 2 })),
      reset: jest.fn()
    };
    sensor = {
      setRandomValues: jest.fn(),
      startSimulation: jest.fn(),
      stopSimulation: jest.fn(),
      restartSimulation: jest.fn(),
      isSimulating: false,
      speedSlider: { value: '5' },
      simulationSpeed: 5
    };
    resonance = {
      soundTypeSelect: { value: 'harmonic' },
      soundParams: { type: 'harmonic' },
      colorModeSelect: { value: 'resonant' },
      colorParams: { mode: 'resonant' },
      isPlaying: false,
      playSound: jest.fn(),
      stopSound: jest.fn(),
      updateSound: jest.fn(),
      updateColorPreview: jest.fn()
    };

    presentation.registerModules(fractal, sensor, resonance);
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
    jest.restoreAllMocks();
    document.body.innerHTML = '';
  });

  test('routes documented immediate actions to registered modules', () => {
    presentation.executeSlideActions([
      { type: 'showFractal', params: { zoom: 3 } },
      { type: 'zoomIn' },
      { type: 'zoomOut' },
      { type: 'activateSensors' },
      { type: 'simulateSensorMovement' },
      { type: 'activateSound', params: { type: 'fractal' } },
      { type: 'changeSoundType', params: { type: 'resonant' } },
      { type: 'changeColorMode', params: { mode: 'spectral' } }
    ]);

    expect(fractal.updateParams).toHaveBeenCalledWith({ zoom: 3 });
    expect(fractal.updateParams).toHaveBeenCalledWith({ zoom: 3 });
    expect(fractal.updateParams).toHaveBeenCalledWith({ zoom: 2 / 1.5 });
    expect(sensor.setRandomValues).toHaveBeenCalled();
    expect(sensor.startSimulation).toHaveBeenCalled();
    expect(sensor.restartSimulation).toHaveBeenCalled();
    expect(sensor.simulationSpeed).toBe(7);
    expect(resonance.playSound).toHaveBeenCalled();
    expect(resonance.soundParams.type).toBe('resonant');
    expect(resonance.updateSound).toHaveBeenCalled();
    expect(resonance.colorParams.mode).toBe('spectral');
    expect(resonance.updateColorPreview).toHaveBeenCalled();
  });

  test('supports delayed actions without executing them early', () => {
    presentation.executeSlideActions([
      { type: 'showFractal', params: { zoom: 9 }, delay: 100 }
    ]);

    expect(fractal.updateParams).not.toHaveBeenCalled();
    jest.advanceTimersByTime(100);
    expect(fractal.updateParams).toHaveBeenCalledWith({ zoom: 9 });
  });

  test('fails closed for unknown actions', () => {
    expect(() => presentation.executeSlideActions([{ type: 'inventedAction' }]))
      .toThrow('Unknown presentation action: inventedAction');
  });

  test('activateAllModules and resetAll preserve the archived module contract', () => {
    presentation.activateAllModules();

    expect(fractal.updateParams).toHaveBeenCalledWith({
      center: { x: -0.5, y: 0 },
      zoom: 1.5,
      fractalType: 'mandelbrot'
    });
    expect(sensor.setRandomValues).toHaveBeenCalled();
    expect(sensor.startSimulation).toHaveBeenCalled();
    expect(resonance.soundParams.type).toBe('harmonic');
    expect(resonance.colorParams.mode).toBe('resonant');

    resonance.isPlaying = true;
    presentation.resetAll();

    expect(fractal.reset).toHaveBeenCalled();
    expect(sensor.stopSimulation).toHaveBeenCalled();
    expect(resonance.stopSound).toHaveBeenCalled();
  });
});

describe('ResonanceEnhancer reconstructed browser contract', () => {
  let ResonanceEnhancer;
  let enhancer;

  beforeEach(() => {
    installResonanceDom();
    global.requestAnimationFrame = jest.fn(() => 123);
    global.cancelAnimationFrame = jest.fn();

    ResonanceEnhancer = loadBrowserClass(
      '../../Fractalsense/resonance-enhancer.js',
      'ResonanceEnhancer'
    );
    enhancer = new ResonanceEnhancer();
  });

  afterEach(() => {
    jest.restoreAllMocks();
    document.body.innerHTML = '';
    document.head.querySelector('#twinkle-animation')?.remove();
  });

  test('cosmic mode is bounded and cleaned when switching modes', () => {
    enhancer.colorParams.intensity = 999;
    enhancer.colorParams.mode = 'cosmic';
    enhancer.updateColorPreview();

    expect(enhancer.colorPreview.querySelectorAll('.star')).toHaveLength(150);
    expect(enhancer.colorPreview.querySelectorAll('.nebula')).toHaveLength(5);
    expect(document.getElementById('twinkle-animation')).not.toBeNull();

    enhancer.colorParams.mode = 'resonant';
    enhancer.updateColorPreview();

    expect(enhancer.colorPreview.querySelectorAll('.star,.nebula')).toHaveLength(0);
    expect(document.getElementById('twinkle-animation')).toBeNull();
  });

  test('animateSoundWave creates the archived SVG representation without recursive test work', () => {
    enhancer.soundParams.type = 'spectral';
    enhancer.animateSoundWave();

    const svg = enhancer.soundWave.querySelector('svg');
    const wave = svg.querySelector('path');
    expect(svg.getAttribute('viewBox')).toBe('0 300 80');
    expect(wave.getAttribute('stroke')).toBe('#9d00ff');
    expect(global.requestAnimationFrame).toHaveBeenCalledTimes(1);
    expect(enhancer.waveAnimationId).toBe(123);
  });

  test('sensor data modulates active oscillator, harmonics and preview filter', () => {
    enhancer.isPlaying = true;
    enhancer.oscillator = { frequency: { value: 220 } };
    enhancer.soundParams.harmonics = [
      {
        oscillator: { frequency: { value: 440 } },
        gain: { gain: { value: 0 } }
      }
    ];

    enhancer.onSensorDataUpdate({
      accelX: 1,
      accelY: 0.5,
      gyroX: 0.2,
      gyroY: 2,
      gyroZ: 1
    });

    expect(enhancer.oscillator.frequency.value).toBeCloseTo(231);
    expect(enhancer.soundParams.harmonics[0].oscillator.frequency.value).toBeCloseTo(444.4);
    expect(enhancer.soundParams.harmonics[0].gain.gain.value).toBeCloseTo(0.12);
    expect(enhancer.colorPreview.style.filter)
      .toBe('hue-rotate(20deg) saturate(110%)');
  });

  test('fractal updates map center and zoom onto the archived sound/color controls', () => {
    const colorSpy = jest.spyOn(enhancer, 'updateColorPreview');

    enhancer.onFractalUpdate({
      center: { x: 0.75, y: 0 },
      zoom: 11
    });

    expect(enhancer.soundParams.baseFrequency).toBeCloseTo(253);
    expect(enhancer.soundParams.type).toBe('resonant');
    expect(enhancer.soundTypeSelect.value).toBe('resonant');
    expect(enhancer.colorParams.mode).toBe('cosmic');
    expect(enhancer.colorParams.intensity).toBe(10);
    expect(colorSpy).toHaveBeenCalled();
  });
});
