/**
 * Jest Setup File
 * Configures the test environment before each test suite
 */

// Import jest-dom matchers
require('@testing-library/jest-dom');

// Mock window.matchMedia (required for some UI tests)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock requestAnimationFrame
global.requestAnimationFrame = callback => setTimeout(callback, 16);
global.cancelAnimationFrame = id => clearTimeout(id);

// Suppress console errors during tests (optional - comment out for debugging)
// console.error = jest.fn();
// console.warn = jest.fn();
