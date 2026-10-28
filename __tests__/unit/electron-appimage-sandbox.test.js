const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const builder = require.resolve('electron-builder');
const appBuilder = require.resolve('app-builder-lib', { paths: [path.dirname(builder)] });
const { generateAppRunScript } = require(path.join(path.dirname(appBuilder), 'targets/appimage/appImageUtil.js'));

describe('AppImage launcher preserves the renderer sandbox', () => {
  test.each([1, 127])('failed namespace probe (%i) never adds --no-sandbox', code => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'enta-apprun-'));
    try {
      const bin = path.join(dir, 'bin');
      fs.mkdirSync(bin);
      fs.writeFileSync(path.join(bin, 'unshare'), `#!/bin/sh\nexit ${code}\n`, { mode: 0o755 });
      fs.writeFileSync(path.join(dir, 'probe'), '#!/usr/bin/env node\nrequire("node:fs").writeFileSync(process.env.ENTA_ARGV_LOG, JSON.stringify(process.argv.slice(2)));\n', { mode: 0o755 });
      const launcher = path.join(dir, 'AppRun');
      fs.writeFileSync(launcher, generateAppRunScript({
        DesktopFileName: 'probe.desktop', ExecutableName: 'probe',
        ProductName: 'probe', ProductFilename: 'probe', ResourceName: 'probe',
      }), { mode: 0o755 });
      const args = ['--example=with space', 'literal;$(not-a-command)'];
      const record = path.join(dir, 'argv.json');
      const result = spawnSync('bash', [launcher, ...args], {
        encoding: 'utf8', env: {
          ...process.env, APPDIR: dir, APPIMAGE: '', APPIMAGE_EXIT_AFTER_INSTALL: '',
          ENTA_ARGV_LOG: record, PATH: bin + path.delimiter + process.env.PATH,
        },
      });
      expect(result.status).toBe(0);
      expect(JSON.parse(fs.readFileSync(record, 'utf8'))).toEqual(args);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });
});
