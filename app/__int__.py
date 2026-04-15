from pathlib import Path # pour gerer les chemins de fichier dans l'apli

from flask import Flask

from config import Config #Config centralisée de l'app

from .routes.api import api_blueprint #RouteAPI (endpoint JSON)
from .routes.web import web_blueprint #Routes web (page HTML)

#config 
BASE_DIR = Path(__file__).resolve().parent.parent #racine du projet

#dossier dpour les templay=tes html et fichier statiques
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

#Factory Patter
def create_app() -> Flask:
    #Crée l'instance Flask avec les emplacements des templates et des fichiers statiques
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR)
    )

    