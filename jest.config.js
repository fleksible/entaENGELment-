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

  // Coverage thresholds — uncovered-count ratchet at the measured baseline.
  //
  // Jest interprets negative thresholds as the maximum number of uncovered
  // entities allowed. This preserves the honest 0%-coverage baseline without
  // using a no-op 0% percentage threshold: adding untested code, or restoring
  // one of the currently non-parseable files without tests, makes CI fail.
  // Additional tests can only improve the baseline; lowering these absolute
  // counts later tightens the gate further.
  //
  // Baseline from CI artifact on 2026-07-30 (instrumentable files only):
  //   statements 181, branches 28, functions 51, lines 170 — all uncovered.
  // Three files currently fail parsing and are therefore not counted:
  // fractal-visualizer.js, presentation-mode.js, resonance-enhancer.js.
  // See OUT/test_coverage_analysis_2026-07-30_ratchet_addendum.md.
  coverageThreshold: {
    global: {
      branches: -28,
      functions: -51,
      lines: -170,
      statements: -181
    }
  },

  // Timeout for async tests
  testTimeout: 10000,

  // Verbose output
  verbose: true
};