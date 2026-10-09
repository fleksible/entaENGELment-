import nextJest from 'next/jest.js';

const createJestConfig = nextJest({ dir: './' });

export default createJestConfig({
  testEnvironment: 'jsdom',
  testMatch: ['<rootDir>/test/**/*.test.jsx'],
  moduleNameMapper: { '^@/(.*)$': '<rootDir>/$1' },
});
