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

  // Coverage thresholds — split ratchet after #345 recovery.
  //
  // The global uncovered-count budget remains unchanged for the pre-existing
  // instrumentable surface (app.js + sensor-simulator.js). Jest subtracts files
  // with path-specific thresholds from the global calculation, so restoring the
  // previously non-parseable browser modules does not silently loosen that guard.
  //
  // The three recovered modules use floor percentages from the first successful
  // characterization run on 2026-09-23:
  //   fractal-visualizer.js 66.39/59.37/60.86/65.94
  //   presentation-mode.js  57.94/45.26/54.83/62.08
  //   resonance-enhancer.js  46.33/31.25/35.48/47.05
  // (statements/branches/functions/lines). Future changes may tighten these
  // numbers, but should not reduce them without an explicit coverage review.
  coverageThreshold: {
    global: {
      branches: -28,
      functions: -51,
      lines: -170,
      statements: -181
    },
    './Fractalsense/fractal-visualizer.js': {
      statements: 66,
      branches: 59,
      functions: 60,
      lines: 65
    },
    './Fractalsense/presentation-mode.js': {
      statements: 57,
      branches: 45,
      functions: 54,
      lines: 62
    },
    './Fractalsense/resonance-enhancer.js': {
      statements: 46,
      branches: 31,
      functions: 35,
      lines: 47
    }
  },

  // Timeout for async tests
  testTimeout: 10000,

  // Verbose output
  verbose: true
};