/** @type {import('jest').Config} */
module.exports = {
  // Use jsdom for browser-like environment
  testEnvironment: 'jsdom',

  // Test file locations.
  //
  // Fractalsense/ is listed here even though it holds no test files: Jest only
  // crawls the paths under `roots`, and `collectCoverageFrom` can report on a
  // file only if the crawl found it. With `roots` limited to __tests__/ the
  // coverage table came back EMPTY ("All files 0%", zero rows) and the
  // `coverageThreshold` below passed vacuously against "0 of 0" — a green gate
  // that measured nothing. `testMatch` keeps test discovery unchanged, since
  // Fractalsense/ contains no *.test.js.
  // See OUT/test_coverage_analysis_2026-07-30.md (P0-1).
  roots: ['<rootDir>/__tests__', '<rootDir>/Fractalsense'],
  testMatch: ['**/*.test.js'],

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/__tests__/setup.js'],

  // Module path mapping
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/Fractalsense/$1'
  },

  // Coverage configuration
  collectCoverageFrom: [
    'Fractalsense/**/*.js',
    '!Fractalsense/**/*.min.js',
    '!**/node_modules/**'
  ],
  coverageDirectory: 'coverage/js',
  coverageReporters: ['text', 'lcov', 'html'],

  // Coverage thresholds — HONEST BASELINE, bewusst auf 0.
  //
  // Die vorherigen Werte (branches 50 / functions 60 / lines 60 / statements 60)
  // haben NIE gegriffen: durch das zu enge `roots` wurde keine Datei
  // instrumentiert, und Jest prueft den Threshold dann gegen "0 von 0" — gruen,
  // ohne zu messen. Mit korrigiertem `roots` wird jetzt real gemessen, und das
  // gemessene Ergebnis ist 0 %:
  //
  //   - Kein Test importiert die Fractalsense-Quellen. __tests__/unit/
  //     fractal-math.test.js re-implementiert `calculateMandelbrot` inline
  //     statt `fractal-visualizer.js` zu laden.
  //   - 3 der 5 Dateien sind ausserdem syntaktisch unvollstaendig und lassen
  //     sich nicht parsen ("Failed to collect coverage from ..." im Log):
  //     fractal-visualizer.js, presentation-mode.js, resonance-enhancer.js.
  //
  // 0 ist daher der einzige Wert, der die Lage nicht falsch darstellt. Er ist
  // als Ratchet-Boden gedacht, nicht als Zielwert: sobald echte Tests gegen die
  // Quellen laufen, hier auf den dann gemessenen Ist-Wert anheben.
  // See OUT/test_coverage_analysis_2026-07-30.md (P0-1).
  coverageThreshold: {
    global: {
      branches: 0,
      functions: 0,
      lines: 0,
      statements: 0
    }
  },

  // Timeout for async tests
  testTimeout: 10000,

  // Verbose output
  verbose: true
};
