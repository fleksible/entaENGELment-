/** @type {import('jest').Config} */
module.exports = {
  // Use jsdom for browser-like environment
  testEnvironment: 'jsdom',

  // Test file locations
  roots: ['<rootDir>/__tests__'],
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

  // Coverage thresholds
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 60,
      lines: 60,
      statements: 60
    }
  },

  // Timeout for async tests
  testTimeout: 10000,

  // Verbose output
  verbose: true
};
