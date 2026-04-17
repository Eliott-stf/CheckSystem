let commandHistory = JSON.parse(localStorage.getItem("cmdHistory") || "[]");
let historyIndex = -1;
let isCommandListVisible = true;

let cpuChart;
let ramChart;
let diskChart;
let networkChart;
let autoRefresh = false;
let refreshInterval = 2000;
let refreshTimer = null;
let lastNetBytes = { sent: 0, recv: 0, time: Date.now() };

document.addEventListener("DOMContentLoaded", function () {
  loadCommandHistory();
  updateSystemTime();
  setInterval(updateSystemTime, 1000);
  loadQuickStats();
  setInterval(loadQuickStats, 5000);
  initAutoComplete();
  initCharts();
});

document.addEventListener("keydown", function (event) {
  const input = document.getElementById("cmdInput");

  if (event.ctrlKey && event.key === "Enter") {
    document.getElementById("commandForm").submit();
  }

  if (event.ctrlKey && event.key === "k") {
    event.preventDefault();
    input.value = "";
    input.focus();
  }

  if (input === document.activeElement) {
    if (event.key === "ArrowUp") {
      event.preventDefault();
      if (historyIndex < commandHistory.length - 1) {
        historyIndex++;
        input.value = commandHistory[historyIndex];
      }
    } else if (event.key === "ArrowDown") {
      event.preventDefault();
      if (historyIndex > 0) {
        historyIndex--;
        input.value = commandHistory[historyIndex];
      } else if (historyIndex === 0) {
        historyIndex = -1;
        input.value = "";
      }
    }
  }
});

document.addEventListener("click", function (event) {
  if (!event.target.closest("button") && !event.target.closest("a")) {
    const cmdInput = document.getElementById("cmdInput");
    if (cmdInput) {
      cmdInput.focus();
    }
  }
});

// Execute une commande rapide: normalise, historise et soumet le formulaire.
function executeCommand(cmd) {
  const normalizedCmd = (cmd || "").toLowerCase();
  saveToHistory(normalizedCmd);
  document.getElementById("cmdInput").value = normalizedCmd;
  document.getElementById("commandForm").submit();
}
// Ouvre une popup pour preparer une commande ping pre-remplie.
function fillPingCommand() {
  const host = prompt(
    "🌐 Entrez l'hôte à pinguer:\n\nExemples:\n• 8.8.8.8 (Google DNS)\n• 1.1.1.1 (Cloudflare)\n• google.com",
    "8.8.8.8",
  );
  if (host) {
    executeCommand("ping " + host);
  }
}
// Ouvre une popup pour saisir un PID puis lance la commande kill.
function fillKillCommand() {
  const pid = prompt('⚠️ Entrez le PID du processus à arrêter:\n\n(Utilisez "processus" pour voir la liste)', "");
  if (pid && !isNaN(pid)) {
    executeCommand("kill " + pid);
  }
}

// Filtre l'affichage des commandes par categorie et met a jour le bouton actif.
function filterCommands(category, sourceButton) {
  const items = document.querySelectorAll(".command-item");
  const buttons = document.querySelectorAll(".filter-btn");

  buttons.forEach((btn) => btn.classList.remove("active"));
  if (sourceButton) {
    sourceButton.classList.add("active");
  }

  items.forEach((item) => {
    if (category === "all" || item.dataset.category === category) {
      item.style.display = "flex";
    } else {
      item.style.display = "none";
    }
  });
}
// Affiche ou masque la grille des commandes (collapse/expand).
function toggleCommandList() {
  const grid = document.getElementById("commandsGrid");
  const icon = document.getElementById("toggleIcon");
  isCommandListVisible = !isCommandListVisible;
  grid.style.display = isCommandListVisible ? "grid" : "none";
  icon.textContent = isCommandListVisible ? "▼" : "▶";
}
// Ajoute une commande unique dans l'historique local (max 50 entrees).
function saveToHistory(cmd) {
  if (cmd && !commandHistory.includes(cmd)) {
    commandHistory.unshift(cmd); // unshisft: ajoute un élément au début du tableau
    if (commandHistory.length > 50) {
      commandHistory.pop(); // pop: supprime le dernier élément du tableau
    }
    localStorage.setItem("cmdHistory", JSON.stringify(commandHistory)); // localStorage: enregistre le tableau dans le localStorage
  }
}

// Recharge l'historique depuis localStorage dans le datalist de suggestions.
function loadCommandHistory() {
  const datalist = document.getElementById("commandHistory");
  commandHistory.forEach((cmd) => {
    const option = document.createElement("option");
    option.value = cmd;
    datalist.appendChild(option);
  });
}
// Vide l'historique apres confirmation utilisateur.
function clearHistory() {
  if (confirm("Effacer tout l'historique des commandes ?")) {
    commandHistory = [];
    localStorage.removeItem("cmdHistory");
    document.getElementById("commandHistory").innerHTML = "";
    alert("✅ Historique effacé");
  }
}

// Copie le contenu du bloc de resultat dans le presse-papier.
function copyResult() {
  const text = document.getElementById("resultContent").textContent;
  navigator.clipboard.writeText(text).then(() => {
    showNotification("✅ Résultat copié dans le presse-papier");
  });
}

// Copie le dernier resultat seulement s'il existe.
function copyLastResult() {
  const result = document.getElementById("resultContent");
  if (result) {
    copyResult();
  } else {
    showNotification("⚠️ Aucun résultat à copier");
  }
}

// Exporte le resultat courant dans un fichier texte telecharge.
function downloadResult() {
  const text = document.getElementById("resultContent").textContent;
  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `sysadmin_result_${new Date().getTime()}.txt`;
  link.click();
  showNotification("💾 Résultat téléchargé");
}
// Alias ergonomique pour exporter le resultat courant.
function exportResults() {
  downloadResult();
}
// Recupere les stats rapides depuis l'API et met a jour les tuiles du header.
async function loadQuickStats() {
  try {
    const response = await fetch("/api/quick-stats");
    const data = await response.json();
    document.getElementById("cpuQuick").textContent = data.cpu + "%";
    document.getElementById("ramQuick").textContent = data.ram + "%";
    document.getElementById("diskQuick").textContent = data.disk + "%";
  } catch (error) {
    return error;
  }
}
// Met a jour l'horloge systeme affichee dans l'interface.
function updateSystemTime() {
  const now = new Date();
  document.getElementById("systemTime").textContent = now.toLocaleString("fr-FR");
}

// Affiche une notification temporaire en bas de page.
function showNotification(message) {
  const notif = document.createElement("div");
  notif.className = "notification";
  notif.textContent = message;
  document.body.appendChild(notif);
  setTimeout(() => notif.classList.add("show"), 10);
  setTimeout(() => {
    notif.classList.remove("show");
    setTimeout(() => notif.remove(), 300);
  }, 2000);
}
// Initialise l'auto-completion sur les commandes connues.
function initAutoComplete() {
  const input = document.getElementById("cmdInput");
  const hinds = document.getElementById("hinds");
  const commands = [
    "cpu",
    "ram",
    "espace",
    "dashboard",
    "ping",
    "network",
    "ports",
    "processus",
    "services",
    "kill",
    "users",
    "security",
    "logs",
    "sysinfo",
    "uptime",
    "temp",
    "battery",
    "health",
    "help",
  ];

  input.addEventListener("input", function () {
    const value = this.value.toLowerCase();
    if (value.length > 0) {
      const matches = commands.filter((cmd) => cmd.startsWith(value));
      if (matches.length > 0 && matches[0] !== value) {
        hinds.textContent = "💡 " + matches.slice(0, 3).join(", ");
        hinds.style.display = "block";
      } else {
        hinds.style.display = "none";
      }
    } else {
      hinds.style.display = "none";
    }
  });
}


// Bascule entre la vue "commandes" et la vue "monitoring live".
function switchView(view) {
  const commandsView = document.getElementById("commandsView");
  const liveView = document.getElementById("liveView");
  const btnCommands = document.getElementById("btnCommands");
  const btnLive = document.getElementById("btnLive");

  if (view === "live") {
    commandsView.style.display = "none";
    liveView.style.display = "block";
    btnCommands.classList.remove("active");
    btnLive.classList.add("active");
    startAutoRefresh();
  } else {
    commandsView.style.display = "block";
    liveView.style.display = "none";
    btnCommands.classList.add("active");
    btnLive.classList.remove("active");
    stopAutoRefresh();
  }
}
// Cree et configure les graphiques Chart.js (CPU, RAM, disque, reseau).
function initCharts() {
  const chartConfig = {
    type: "line",
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 750,
      },
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
          ticks: {
            color: "#94a3b8",
            callback: function (value) {
              return value + "%";
            },
          },
        },
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: "#94a3b8",
            maxTicksLimit: 10,
          },
        },
      },
    },
  };

  cpuChart = new Chart(document.getElementById("cpuChart"), {
    ...chartConfig,
    data: {
      labels: [],
      datasets: [
        {
          label: "CPU %",
          data: [],
          borderColor: "#2563eb",
          backgroundColor: "rgba(37, 99, 235, 0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
  });

  ramChart = new Chart(document.getElementById("ramChart"), {
    ...chartConfig,
    data: {
      labels: [],
      datasets: [
        {
          label: "RAM %",
          data: [],
          borderColor: "#10b981",
          backgroundColor: "rgba(16, 185, 129, 0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
  });

  diskChart = new Chart(document.getElementById("diskChart"), {
    ...chartConfig,
    data: {
      labels: [],
      datasets: [
        {
          label: "Disk %",
          data: [],
          borderColor: "#06b6d4",
          backgroundColor: "rgba(6, 182, 212, 0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
  });

  networkChart = new Chart(document.getElementById("networkChart"), {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Upload",
          data: [],
          borderColor: "#f59e0b",
          backgroundColor: "rgba(245, 158, 11, 0.1)",
          fill: true,
          tension: 0.4,
        },
        {
          label: "Download",
          data: [],
          borderColor: "#8b5cf6",
          backgroundColor: "rgba(139, 92, 246, 0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 750,
      },
      plugins: {
        legend: {
          display: true,
          labels: {
            color: "#94a3b8",
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
          ticks: {
            color: "#94a3b8",
            callback: function (value) {
              return value + " KB/s";
            },
          },
        },
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: "#94a3b8",
            maxTicksLimit: 10,
          },
        },
      },
    },
  });
}
// Interroge l'API live, met a jour les graphiques et les indicateurs detailles.
async function fetchLiveData() {
  try {
    const response = await fetch("/api/live-monitoring");
    const data = await response.json();

    updateChart(cpuChart, data.cpu);
    updateChart(ramChart, data.ram);
    updateChart(diskChart, data.disk);
    updateNetworkChart(data.network);

    document.getElementById("cpuLiveValue").textContent = data.cpu + "%";
    document.getElementById("ramLiveValue").textContent = data.ram + "%";
    document.getElementById("diskLiveValue").textContent = data.disk + "%";

    const now = Date.now();
    const timeDiff = (now - lastNetBytes.time) / 1000;
    const uploadSpeed = Math.round((data.network.sent - lastNetBytes.sent) / timeDiff / 1024);
    const downloadSpeed = Math.round((data.network.recv - lastNetBytes.recv) / timeDiff / 1024);

    document.getElementById("networkLiveValue").textContent = `↑${uploadSpeed} ↓${downloadSpeed} Mo/s`;



    lastNetBytes = {
      sent: data.network.sent,
      recv: data.network.recv,
      time: now,
    };

    updateDetailedStats(data);
  } catch (error) {
    console.error("Erreur fetch monitoring:", error);
  }
}
// Ajoute un point sur un graphique standard avec fenetre glissante.
function updateChart(chart, value) {
  const now = new Date().toLocaleTimeString("fr-FR");

  chart.data.labels.push(now);
  chart.data.datasets[0].data.push(value);

  if (chart.data.labels.length > 20) {
    chart.data.labels.shift(); // shift: supprime le premier élément du tableau
    chart.data.datasets[0].data.shift(); // shift: supprime le premier élément du tableau
  }

  chart.update("none"); // update: met à jour le graphique
}
// Calcule et trace les debits reseau upload/download en KB/s.
function updateNetworkChart(networkData) {
  const now = new Date().toLocaleTimeString("fr-FR");
  const timeDiff = (Date.now() - lastNetBytes.time) / 1000;

  const uploadSpeed = Math.round((networkData.sent - lastNetBytes.sent) / timeDiff / 1024);
  const downloadSpeed = Math.round((networkData.recv - lastNetBytes.recv) / timeDiff / 1024);

  networkChart.data.labels.push(now);
  networkChart.data.datasets[0].data.push(uploadSpeed);
  networkChart.data.datasets[1].data.push(downloadSpeed);

  if (networkChart.data.labels.length > 20) {
    networkChart.data.labels.shift();
    networkChart.data.datasets[0].data.shift();
    networkChart.data.datasets[1].data.shift();
  }

  networkChart.update("none");
}

// Met a jour le panneau de statistiques detaillees (CPU/RAM/disque/reseau).
function updateDetailedStats(data) {
  if (data.cpu_freq) {
    document.getElementById("cpuFreq").textContent = (data.cpu_freq / 1000).toFixed(2) + " GHz";
  }
  document.getElementById("cpuCores").textContent = data.cpu_cores || "--";
  document.getElementById("cpuThreads").textContent = data.cpu_threads || "--";

  document.getElementById("ramTotal").textContent = (data.ram_total / 1024 ** 3).toFixed(1) + " GB";
  document.getElementById("ramUsed").textContent = (data.ram_used / 1024 ** 3).toFixed(1) + " GB";
  document.getElementById("ramAvailable").textContent = (data.ram_available / 1024 ** 3).toFixed(1) + " GB";

  document.getElementById("diskTotal").textContent = (data.disk_total / 1024 ** 3).toFixed(1) + " GB";
  document.getElementById("diskUsed").textContent = (data.disk_used / 1024 ** 3).toFixed(1) + " GB";
  document.getElementById("diskFree").textContent = (data.disk_free / 1024 ** 3).toFixed(1) + " GB";

  document.getElementById("netSent").textContent = (data.network.sent / 1024 ** 2).toFixed(1) + " MB";
  document.getElementById("netRecv").textContent = (data.network.recv / 1024 ** 2).toFixed(1) + " MB";
}
// Active/desactive le rafraichissement automatique du monitoring.
function toggleAutoRefresh() {
  autoRefresh = !autoRefresh;
  const btn = document.getElementById("autoRefreshBtn");

  if (autoRefresh) {
    btn.textContent = "⏸️";
    btn.title = "Pause";
    startAutoRefresh();
  } else {
    btn.textContent = "▶️";
    btn.title = "Play";
    stopAutoRefresh();
  }
}
// Lance le polling live avec l'intervalle courant.
function startAutoRefresh() {
  if (!autoRefresh) {
    autoRefresh = true;
    document.getElementById("autoRefreshBtn").textContent = "⏸️";
  }

  fetchLiveData();
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }
  refreshTimer = setInterval(fetchLiveData, refreshInterval);
}


// Arrete le polling live en nettoyant le timer actif.
function stopAutoRefresh() {
  if (refreshTimer) {
    clearInterval(refreshTimer);
    refreshTimer = null;
  }
}

// Applique un nouvel intervalle puis redemarre le polling si necessaire.
function updateRefreshInterval() {
  refreshInterval = parseInt(document.getElementById("refreshInterval").value, 10);
  if (autoRefresh) {
    stopAutoRefresh();
    startAutoRefresh();
  }
}

// Reinitialise toutes les series de graphiques et les compteurs reseau.
function resetCharts() {
  [cpuChart, ramChart, diskChart, networkChart].forEach((chart) => {
    chart.data.labels = [];
    chart.data.datasets.forEach((dataset) => {
      dataset.data = [];
    });
    chart.update();
  });

  lastNetBytes = { sent: 0, recv: 0, time: Date.now() };
  showNotification("✅ Graphiques réinitialisés");
}