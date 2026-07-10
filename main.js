const { app, BrowserWindow, shell } = require('electron');
const path = require('path');
const { getSafeExternalUrl } = require('./electron-url-policy');

function openExternalIfAllowed(rawUrl) {
  const safeUrl = getSafeExternalUrl(rawUrl);
  if (safeUrl) {
    void shell.openExternal(safeUrl);
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      // Hardened defaults: remote/CDN renderer content has no Node/Electron access.
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
    },
  });

  // Match the actual on-disk filename (case-sensitive on Linux): Index.html.
  win.loadFile('Index.html');
  win.setMenu(null);

  // Renderer-controlled navigation always stays out of the Electron window.
  // Only normalized HTTP(S) targets may be handed to the system browser.
  win.webContents.setWindowOpenHandler(({ url }) => {
    openExternalIfAllowed(url);
    return { action: 'deny' };
  });

  win.webContents.on('will-navigate', (event, url) => {
    event.preventDefault();
    openExternalIfAllowed(url);
  });
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
