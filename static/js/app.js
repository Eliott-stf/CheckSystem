//VARIABLES
let isCommandListVisible = true;
let commandHistory = JSON.parse(localStorage.getItem("cmdHistory") || []);
let historyIndex = -1;

document.addEventListener("DOMContentLoaded", function () {
  loadQuickStats();
  setInterval(loadQuickStats, 5000);
});

/**
 * methode qui affiche les stats rapide
 * @returns Object
 */
async function loadQuickStats() {
  try {
    const response = await fetch("/api/quick-stats");
    const data = await response.json();
    document.getElementById("cpuQuick").textContent = data.cpu + "%";
    document.getElementById("ramQuick").textContent = data.ram + "%";
    document.getElementById("diskQuick").textContent = data.disk + "%";
  } catch (error) {
    console.log(error);
  }
}

/**
 * méthode qui permet de switch entre commande et monitoring
 */
function switchView(view) {
  //on récupère les éléments du DOM
  const commandsView = document.getElementById("commandsView");
  const liveView = document.getElementById("liveView");
  const btnCommands = document.getElementById("btnCommands");
  const btnLive = document.getElementById("btnLive");

  if (view === "live") {
    commandsView.style.display = "none";
    liveView.style.display = "block";
    btnCommands.classList.remove("active");
    btnLive.classList.add("active");
    // TODO: start start auto refresh
  } else {
    commandsView.style.display = "block";
    liveView.style.display = "none";
    btnCommands.classList.add("active");
    btnLive.classList.remove("active");
    //TODO: stop auto refresh
  }
}

/**
 * permet de filtrer les commandes
 */
function filterCommands(category, sourceButton) {
  const buttons = document.querySelectorAll(".filter-btn");
  const items = document.querySelectorAll(".command-item");

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

/**
 * méthode qui permet de masquer toutes les cartes de commandes
 */
function toggleCommandList() {
  const grid = document.getElementById("commandsGrid");
  const icon = document.getElementById("toggleIcon");

  isCommandListVisible = !isCommandListVisible;

  grid.style.display = isCommandListVisible ? "grid" : "none";
  icon.textContent = isCommandListVisible ? "▼" : "▶";
}

/**
 * exécute une commande et l'ajoute à l'historique
 * @param {string} cmd - la commande à exécuter
 * @returns {void}
 */
function executeCommand(cmd) {
  saveToHistory(cmd);
  document.getElementById("cmdInput").value = cmd;
  document.getElementById("commandForm").onsubmit();
}

/**
 * sauvegarde une commande dans l'historique (max 50 éléments)
 * stocke les données dans le localStorage du navigateur
 * @param {string} cmd - la commande à sauvegarder
 * @returns {void}
 */
function saveToHistory(cmd) {
  if (cmd && !commandHistory.includes(cmd)) {
    commandHistory.unshift(cmd); // unshift: ajoute un element au debut du tableau
    if (commandHistory.length > 50) {
      commandHistory.pop(); //pop: supprime le dernier element du tableau
    }
    localStorage.setItem("cmdHistory", JSON.stringify(commandHistory));
  }
}
/**
 * efface tout l'historique des commandes après confirmation
 * supprime aussi les données du localStorage
 * @returns {void}
 */
function clearHistory() {
  if (confirm("Effacer tout l'historique des commandes?")) {
    commandHistory = [];
    localStorage.removeItem("cmdHistory");
    document.getElementById("commandHistory").innerHTML = "";
    alert("✅ Historique effacé");
  }
}
/**
 * exporte les résultats en téléchargeant un fichier texte
 * @returns {void}
 */
function exportResults() {
  downloadResult();
}
/**
 * copie le dernier résultat dans le presse-papier
 * affiche une notification si aucun résultat n'est disponible
 * @returns {void}
 */
function copyLastResult() {
  const result = document.getElementById("resultContent");
  if (result) {
    copyResult();
  } else {
    showNotification("⚠️ Aucun résultat à copier");
  }
}

/**
 * copie le contenu du résultat dans le presse-papier du navigateur
 * affiche une notification de confirmation
 * @returns {void}
 */
function copyResult() {
  const text = document.getElementById("resultContent").textContent;
  navigator.clipboard.writeText(text).then(() => {
    showNotification("✅ Résultat copié dans le presse-papier");
  });
}

/**
 * télécharge les résultats dans un fichier texte
 * le fichier est nommé avec un timestamp pour éviter les doublons
 * @returns {void}
 */
function downloadResult() {
  const text = document.getElementById("resultContent").textContent;
  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `check_system_${new Date().getTime()}.txt`;
  link.click();
  showNotification("💾 Résultat téléchargé");
}

/**
 * affiche une notification temporaire à l'écran
 * la notification s'affiche pendant 2 secondes avant de disparaître
 * @param {string} message - le message à afficher dans la notification
 * @returns {void}
 */
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