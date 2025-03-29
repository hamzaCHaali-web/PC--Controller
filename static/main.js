// Logging shortcut
let log = console.log;

// ---------------- Tab Navigation ----------------
const navItems = document.querySelectorAll('.nav-item');
const screens = document.querySelectorAll('.screen');

navItems.forEach(item => {
  item.addEventListener('click', () => {
    navItems.forEach(nav => nav.classList.remove('active'));
    screens.forEach(screen => screen.classList.remove('active'));

    item.classList.add('active');
    document.getElementById(`${item.dataset.tab}-screen`).classList.add('active');
  });
});

// ---------------- WebSocket Connection ----------------
let socket;

function connectWebSocket() {
  const ip = localStorage.getItem('ipAddress');
  const port = localStorage.getItem('port') || '1626';

  if (!ip) {
    log("⚠️ IP address not found in localStorage!");
    return;
  }

  const wsUrl = `ws://${ip}:${port}`;
  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    log(`✅ Connected to: ${wsUrl}`);
    log("متصل بالخادم");
  };

  socket.onmessage = event => {
    log("📩 الخادم: " + event.data);
  };

  socket.onerror = error => {
    log("❌ WebSocket Error:", error);
  };

  socket.onclose = () => {
    log("🔌 WebSocket connection closed");
  };
}

// ---------------- Remote Control Buttons ----------------
function initRemoteButtons() {
  const buttons = document.querySelectorAll('.remote-button');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      // Ripple Effect
      const ripple = document.createElement('div');
      ripple.classList.add('ripple');
      button.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);

      // Extract button type
      const buttonType = button.dataset.type || button.className.split(' ')[1].split('-')[0];
      log(`🖱️ Button pressed: ${buttonType}`);

      const command = ["btn", buttonType];

      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(command));
      } else {
        log("⚠️ WebSocket not connected. Cannot send command.");
      }
    });
  });
}

// ---------------- Theme Toggle ----------------
const themeSwitch = document.getElementById('theme-switch');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

function setTheme(isDark) {
  document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
  themeSwitch.checked = isDark;
}

setTheme(prefersDark.matches);

themeSwitch.addEventListener('change', (e) => {
  setTheme(e.target.checked);
});

prefersDark.addEventListener('change', (e) => {
  setTheme(e.matches);
});

// ---------------- Settings Save/Load ----------------
const ipInput = document.getElementById('ip-address');
const portInput = document.getElementById('port');

// Load saved settings
ipInput.value = localStorage.getItem('ipAddress') || '192.168.0.1';
portInput.value = localStorage.getItem('port') || '1626';

// Save settings and reconnect
ipInput.addEventListener('change', (e) => {
  localStorage.setItem('ipAddress', e.target.value);
  log("✅ IP saved. Reconnecting...");
  connectWebSocket();
});

portInput.addEventListener('change', (e) => {
  localStorage.setItem('port', e.target.value);
  log("✅ Port saved. Reconnecting...");
  connectWebSocket();
});

// ---------------- Initial Setup ----------------
log("📍 IP from storage:", localStorage.getItem('ipAddress'));
log("📍 Port from storage:", localStorage.getItem('port'));

connectWebSocket();
initRemoteButtons();
