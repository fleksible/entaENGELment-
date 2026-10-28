'use strict';

// Inspect the actual AppImage payload over loopback; keep its sandbox enabled.
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { setTimeout: delay } = require('node:timers/promises');
const expectedElectron = require('../package.json').devDependencies.electron;
const electron = "process.getBuiltinModule('module').createRequire(process.resourcesPath + '/app.asar/package.json')('electron')";

async function main() {
  assert(process.argv[2], 'Pass the extracted AppImage AppRun path');
  assert.equal(process.platform, 'linux');
  assert.notEqual(process.getuid(), 0, 'Use a normal user; do not disable the sandbox');
  assert(!process.env.ELECTRON_RUN_AS_NODE);
  const executable = path.resolve(process.argv[2]);
  assert(fs.existsSync(executable));
  const desktopFiles = fs.readdirSync(path.dirname(executable)).filter(name => name.endsWith('.desktop'));
  assert.equal(desktopFiles.length, 1, 'Expected one distributed desktop entry');
  const desktopEntry = fs.readFileSync(path.join(path.dirname(executable), desktopFiles[0]), 'utf8');
  const desktopExec = desktopEntry.match(/^Exec=(.*)$/m)?.[1];
  assert(desktopExec && !/--(?:no-sandbox|disable-setuid-sandbox|disable-seccomp-filter-sandbox|disable-gpu-sandbox)\b/.test(desktopExec), 'Desktop entry must not disable the sandbox');
  const output = path.resolve(process.argv[3] || 'out/desktop-smoke');
  fs.mkdirSync(output, { recursive: true });
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'enta-desktop-smoke-'));
  const child = spawn(executable, ['--inspect=127.0.0.1:0', `--user-data-dir=${profile}`], {
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  let log = '', inspectorUrl, exited, startupError, socket;
  child.once('error', error => { startupError = error; });
  const exit = new Promise(resolve => child.once('exit', (code, signal) => {
    exited = { code, signal };
    resolve(exited);
  }));
  for (const stream of [child.stdout, child.stderr]) {
    stream.on('data', data => {
      log = (log + data.toString()).slice(-256 * 1024);
      inspectorUrl ||= log.match(/Debugger listening on (ws:\/\/127\.0\.0\.1:\d+\/[^\s]+)/)?.[1];
    });
  }
  try {
    const deadline = Date.now() + 90000;
    while (!inspectorUrl) {
      if (startupError) throw startupError;
      assert(!exited, `Application exited during startup: ${JSON.stringify(exited)}`);
      assert(Date.now() < deadline, 'Application debugger startup timed out');
      await delay(100);
    }
    socket = new WebSocket(inspectorUrl);
    const pending = new Map();
    let nextId = 0;
    socket.addEventListener('message', event => {
      const message = JSON.parse(event.data), request = pending.get(message.id);
      if (!request) return;
      pending.delete(message.id);
      clearTimeout(request.timer);
      if (message.error) request.reject(new Error(JSON.stringify(message.error)));
      else request.resolve(message.result);
    });
    socket.addEventListener('close', () => {
      for (const request of pending.values()) {
        clearTimeout(request.timer);
        request.reject(new Error('Application debugger disconnected'));
      }
      pending.clear();
    });
    await new Promise((resolve, reject) => {
      socket.addEventListener('open', resolve, { once: true });
      socket.addEventListener('error', reject, { once: true });
    });
    async function evaluate(expression) {
      const result = await new Promise((resolve, reject) => {
        const id = ++nextId;
        const timer = setTimeout(() => {
          pending.delete(id);
          reject(new Error('Application debugger command timed out'));
        }, 15000);
        pending.set(id, { resolve, reject, timer });
        socket.send(JSON.stringify({ id, method: 'Runtime.evaluate', params: {
          expression, awaitPromise: true, returnByValue: true,
        } }));
      });
      assert(!result.exceptionDetails, JSON.stringify(result.exceptionDetails));
      return result.result.value;
    }
    let observed;
    do {
      assert(!exited && Date.now() < deadline, 'Document/preload startup timed out');
      observed = await evaluate(`(async () => {
        const { app, BrowserWindow } = ${electron};
        await app.whenReady();
        const windows = BrowserWindow.getAllWindows();
        if (windows.length !== 1) return { pending: true };
        const contents = windows[0].webContents;
        if (contents.isLoadingMainFrame()) return { pending: true };
        const page = await contents.executeJavaScript('({ ready: document.readyState, url: location.href, container: !!document.getElementById("canvas-container"), bridge: window.entaShell, requireType: typeof require, processType: typeof process, bufferType: typeof Buffer })');
        const prefs = contents.getLastWebPreferences();
        const status = process.getBuiltinModule('fs').readFileSync('/proc/' + contents.getOSProcessId() + '/status', 'utf8');
        return {
          packaged: app.isPackaged, appPath: app.getAppPath(),
          electron: process.versions.electron, chrome: process.versions.chrome,
          sandbox: prefs.sandbox, contextIsolation: prefs.contextIsolation,
          nodeIntegration: prefs.nodeIntegration,
          disabledSandboxFlags: ['no-sandbox', 'disable-setuid-sandbox', 'disable-seccomp-filter-sandbox', 'disable-gpu-sandbox'].filter(flag => app.commandLine.hasSwitch(flag)),
          seccomp: Number(status.match(/^Seccomp:\\s+(\\d+)/m)?.[1]),
          noNewPrivileges: Number(status.match(/^NoNewPrivs:\\s+(\\d+)/m)?.[1]), page
        };
      })()`);
      if (observed.pending || observed.page.ready !== 'complete') await delay(200);
    } while (observed.pending || observed.page.ready !== 'complete');
    assert.equal(observed.packaged, true);
    assert(observed.appPath.endsWith('/resources/app.asar'));
    assert.equal(observed.electron, expectedElectron);
    assert.equal(observed.sandbox, true);
    assert.equal(observed.contextIsolation, true);
    assert.equal(observed.nodeIntegration, false);
    assert.deepEqual(observed.disabledSandboxFlags, []);
    assert.equal(observed.seccomp, 2, 'Renderer seccomp filter must be active');
    assert.equal(observed.noNewPrivileges, 1);
    assert(observed.page.url.endsWith('/resources/app.asar/Index.html'));
    assert.equal(observed.page.container, true);
    for (const key of ['requireType', 'processType', 'bufferType']) assert.equal(observed.page[key], 'undefined');
    assert.equal(observed.page.bridge.platform, 'linux');
    assert.equal(observed.page.bridge.versions.electron, expectedElectron);
    assert.equal(observed.page.bridge.versions.chrome, observed.chrome);
    assert.deepEqual(Object.keys(observed.page.bridge).sort(), ['platform', 'versions']);
    await evaluate(`(async () => {
      await (${electron}).BrowserWindow.getAllWindows()[0].webContents.executeJavaScript('window.open("file:///__enta_blocked_window__.html"); location.href = "file:///__enta_blocked_navigation__.html"; true');
      return true;
    })()`);
    await delay(300);
    const after = await evaluate(`(() => {
      const windows = (${electron}).BrowserWindow.getAllWindows();
      return { windows: windows.length, url: windows[0].webContents.getURL() };
    })()`);
    assert.equal(after.windows, 1, 'Unsafe popup must remain blocked');
    assert.equal(after.url, observed.page.url, 'Unsafe navigation must remain blocked');
    observed.blockedPopup = observed.blockedNavigation = true;
    observed.desktopExec = desktopExec;
    await evaluate(`setTimeout(() => (${electron}).app.quit(), 100); true`);
    socket.close();
    const shutdown = await Promise.race([exit, delay(10000, null, { ref: false }).then(() => { throw new Error('Application did not quit'); })]);
    assert.equal(shutdown.code, 0);
    fs.writeFileSync(path.join(output, 'runtime.json'), JSON.stringify(observed, null, 2) + '\n');
    console.log('PASS: actual AppImage payload, preload, sandbox and navigation guards');
    console.log(JSON.stringify(observed, null, 2));
  } finally {
    socket?.close();
    if (!exited && child.pid) child.kill('SIGTERM');
    fs.writeFileSync(path.join(output, 'desktop.log'), log);
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
