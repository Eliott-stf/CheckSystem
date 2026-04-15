from .diagnostic import battery_command, logs_command, security_command, temperature_command, users_command

from .monitoring import (
    cpu_command,
    dashboard_command,
    disk_space_command,
    health_command,
    ram_command,
    system_info_command,
    uptime_command
)

from .network import network_command, ping_command, ports_command
from .process import kill_command, process_command, services_command

STATIC_COMMAND = {
    "cpu": cpu_command,
    "ram": ram_command,
    "espace": disk_space_command,
    "uptime": uptime_command,
    "processus": process_command,
    "network": network_command,
    "temp": temperature_command,
    "users": users_command,
    "battery": battery_command,
    "sysinfo": system_info_command,
    "dashboard": dashboard_command,
    "ports": ports_command,
    "services": services_command,
    "security": security_command,
    "logs": logs_command,
    "health": health_command
}

PREFIX_COMMAND = {
    "ping ": ping_command,
    "kill ": kill_command
}

def help_command() -> str:
    return (
        "💡 COMMANDES DISPONIBLES:\n\n"
        "📊 MONITORING:\n"
        "  dashboard    - Vue d'ensemble complète du système\n"
        "  cpu          - Utilisation détaillée du processeur\n"
        "  ram          - Utilisation de la mémoire\n"
        "  espace       - État détaillé des disques\n"
        "  health       - Santé globale du système avec score\n\n"
        "🌐 RÉSEAU:\n"
        "  ping <hôte>  - Teste la connectivité réseau\n"
        "  network      - Informations et statistiques réseau\n"
        "  ports        - Liste des ports TCP/UDP actifs\n\n"
        "🔄 PROCESSUS:\n"
        "  processus    - Top 10 des processus par CPU\n"
        "  services     - Services système actifs\n"
        "  kill <PID>   - Arrêter un processus (admin requis)\n\n"
        "� SÉCURITÉ:\n"
        "  users        - Utilisateurs connectés\n"
        "  security     - Audit de sécurité basique\n"
        "  logs         - Derniers événements système\n\n"
        "� DIAGNOSTIC:\n"
        "  sysinfo      - Informations complètes du système\n"
        "  uptime       - Date de démarrage et durée\n"
        "  temp         - Températures des composants\n"
        "  battery      - État de la batterie\n\n"
        "❓ AIDE:\n"
        "  help ou ?    - Affiche cette aide\n\n"
        "💡 ASTUCES:\n"
        "  • Utilisez les boutons de commande pour exécution rapide\n"
        "  • Ctrl+Enter pour exécuter, Ctrl+K pour effacer\n"
        "  • Flèches ↑↓ pour naviguer dans l'historique\n"
        "  • Cliquez sur 📋 pour copier les résultats"
    )