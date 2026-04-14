class Config:
    #config principale de l'application

    #application
    APP_NAME = "Check System"
    VERSION ="1.0"
    DEBUG = True

    #Serveur Flask
    HOST = "127.0.0.1"
    PORT = 5000

    #Monitoring
    STAT_REFRESH_INTERVALE = 3 #secondes entre les mise a jour
    CPU_INTERVAL= 1
    MAX_HISTORY_SIZE = 50

    #Limites d'affichage
    MAX_PROCESS_DISPLAY = 10
    MAX_SERVICES_DISPLAY = 20
    MAX_LOGS_DISPLAY = 10 

    #Seuil d'Alerte (en pourcentage)
    CPU_WARNING_THRESHOLD = 70
    CPU_CRITICAL_THRESHOLD = 90

    RAM_WARNING_THRESHOLD = 75
    RAM_CRITICAL_THRESHOLD = 90

    DISK_WARNING_THRESHOLD = 80
    DISK_CRITICAL_THRESHOLD = 90

    TEMP_WARNING_THRESHOLD = 75 # en C°
    TEMP_CRITICAL_THRESHOLD = 85 # en C°

    #Score Santé
    HEALTH_PENALTY_CPU_HIGH = 10
    HEALTH_PENALTY_CPU_CRITICAL = 20

    HEALTH_PENALTY_RAM_HIGH = 15
    HEALTH_PENALTY_RAM_CRITICAL = 25

    HEALTH_PENALTY_DISK_HIGH = 10
    HEALTH_PENALTY_DISK_CRITICAL = 20

    HEALTH_PENALTY_TEMP_HIGH = 15

    #ping
    PING_COUNT = 2 #nombre de pings

    #sécurité
    REQUIRE_AUTH = False
    SECRET_KEY = "changer-en-prod"

    #export
    EXPORT_DIRECTORY = "exports" #dossier pour export
    EXPORT_FORMAT = "txt"

    #interface
    COMMANDS_COLLAPSED_BY_DEFAUT = False #remplir la liste des commandes
    SHOW_QUICK_STATS = True #Afficher les stats rapides en header
    ENABLE_NOTIFICATION = True #notif javascript

    #dev
    ENABLE_PROFILING = False
    LOG_COMMANDS = True

#categories de commandes pour filtrage
COMMAND_CATEGORIES = {
    "monitoring" : ["cpu", "ram", "espace", "dashboard", "health"],
    "network" : ["ping", "network", "ports"],
    "process" : ["processus", "services", "kill"],
    "security" : ["users", "security", "logs"],
    "diagnostic" : ["sysinfo", "uptime", "temp", "battery"]
}

#message personnalisés
MESSAGES = {
    "welcome": "Bienvenue sur Check System",
    "error_permission": "Permission refusée. Droits administrateur requis",
    "error_not_found": "Ressource non trouvée",
    "error_invalid_command": "Cammande invalide. Tapez 'help' pour l'aide",
    "success_kill": "Processus arreté avec succes",
    "info_no_battery": "pas de batterie detecté"

}
    