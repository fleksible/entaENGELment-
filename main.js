const { app, BrowserWindow, shell } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      // Hardened defaults (Electron security best practice):
      // the renderer gets NO Node integration and runs isolated + sandboxed,
      // so remote/CDN scripts in Index.html cannot reach Node/Electron APIs.
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
    },
  });

  // Match the actual on-disk filename (case-sensitive on Linux): Index.html.
  win.loadFile('Index.html');
  win.setMenu(null); // Optional: Entfernt die Menüleiste

  // Defense in depth: keep the window on the local document; open any external
  // navigation attempt in the user's real browser instead of inside the shell.
  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
  win.webContents.on('will-navigate', (event, url) => {
    if (!url.startsWith('file://')) {
      event.preventDefault();
      shell.openExternal(url);
    }
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
