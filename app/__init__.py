from pathlib import Path # pour gerer les chemins de fichiers dans l'appli

from flask import Flask # framwork web principal

from config import Config # Configuration centralisée de l'application

from .routes.api import api_blueprint #Routes API (endpoint JSON)
from .routes.web import web_blueprint # Routes web (pages HTML)

# configuration des chemin
BASE_DIR = Path(__file__).resolve().parent.parent # etre a la racine du projet (parent du dossier app)

#dossier pour les templates html et fichiers statiques
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# FACTORY PATTERN
def create_app() -> Flask:
  # Crée l'instance Flask avec les emplacements des template et des fichiers statiques
  app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR)
  )

  # charge la configuration depuis config.py
  app.config.from_object(Config)

  #on enregistre les routes web (page HTML)
  app.register_blueprint(web_blueprint)

  #enregistre les route d'API (endpoint JSON)
  app.register_blueprint(api_blueprint)

  # retourne l'application configurée et prête à être utilisée
  return app
