// Preload script for the EntaENGELment desktop shell.
//
// Runs in an isolated context (contextIsolation: true) with no Node integration
// in the renderer. It deliberately exposes only a minimal, read-only surface via
// contextBridge so the renderer cannot reach Node/Electron internals even if a
// (CDN) script in Index.html were compromised. Keep this surface minimal.
const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('entaShell', {
  // Non-sensitive metadata only. No fs/child_process/ipc surface is exposed.
  platform: process.platform,
  versions: {
    electron: process.versions.electron,
    chrome: process.versions.chrome,
  },
});
