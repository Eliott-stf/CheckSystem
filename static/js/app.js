document.addEventListener("DOMContentLoaded", function(){
    loadQuickStats();
    setInterval(loadQuickStats, 5000)
})


/**
 * 
 * @returns méthode qui affiche les stats rapide
 */
async function loadQuickStats(){
    try {
        const response = await fetch("/api/quick-stats");
        const data = await response.json();
        document.getElementById("cpuQuick").textContent = data.cpu + "%"
        document.getElementById("ramQuick").textContent = data.ram + "%"
        document.getElementById("diskQuick").textContent = data.disk + "%"
    } catch (error) {
        console.log(error);
    }
}

/**
 * méthode qui permet de switch entre commande et monitoring 
 */
function switchView(view){
    //on récupère les éléments du DOM
    const commandsView = document.getElementById("commandsView");
    const liveView = document.getElementById("liveView");
    const btnCommands = document.getElementById("btnCommands");
    const btnLive = document.getElementById("btnLive");

    if (view == "live") {
        commandsView.style.display = "none";
        liveView.style.display = "block"
        btnCommands.classList.remove("active");
        btnLive.classList.add("active")
    } else {
        commandsView.style.display = "block";
        liveView.style.display = "none"
        btnCommands.classList.add("active");
        btnLive.classList.remove("active")
    }

}

