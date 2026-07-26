const path = require('node:path');

function resolveDependency(parentEntry, dependency) {
  return require.resolve(dependency, {
    paths: [path.dirname(parentEntry)],
  });
}

function packagingMinimatchEntries() {
  const electronBuilder = require.resolve('electron-builder');
  const appBuilderLib = resolveDependency(electronBuilder, 'app-builder-lib');
  const asar = resolveDependency(appBuilderLib, '@electron/asar');
  const universal = resolveDependency(appBuilderLib, '@electron/universal');
  const ejs = resolveDependency(appBuilderLib, 'ejs');
  const jake = resolveDependency(ejs, 'jake');
  const filelist = resolveDependency(jake, 'filelist');

  return [
    ['@electron/asar', resolveDependency(asar, 'minimatch')],
    ['@electron/universal', resolveDependency(universal, 'minimatch')],
    ['filelist', resolveDependency(filelist, 'minimatch')],
    ['app-builder-lib', resolveDependency(appBuilderLib, 'minimatch')],
  ];
}

const globCases = [
  ['app/main.js', '**/*.js', true],
  ['app/main.txt', '**/*.js', false],
  ['app/main.ts', '**/*.{js,ts}', true],
  ['dist/linux/app', 'dist/{linux,win}/**', true],
  ['dist/mac/app', 'dist/{linux,win}/**', false],
  ['resources/app.asar', 'resources/**/app.asar', true],
  ['.hidden/config.json', '**/*.json', true],
  ['foo7.txt', 'foo{1..9}.txt', true],
];

describe('Electron packaging glob compatibility', () => {
  test.each(packagingMinimatchEntries())(
    '%s accepts the security-fixed brace-expansion API',
    (_consumer, minimatchEntry) => {
      const minimatchModule = require(minimatchEntry);
      const minimatch =
        typeof minimatchModule === 'function'
          ? minimatchModule
          : minimatchModule.minimatch;

      expect(typeof minimatch).toBe('function');
      for (const [input, pattern, expected] of globCases) {
        expect(minimatch(input, pattern, { dot: true })).toBe(expected);
      }

      const braceExpansionEntry = resolveDependency(
        minimatchEntry,
        'brace-expansion'
      );
      const braceExpansion = require(braceExpansionEntry);
      expect(typeof braceExpansion).toBe('function');
      expect(braceExpansion.expand).toBe(braceExpansion);
    }
  );
});
