import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instanciar la base de datos
db = SQLAlchemy()


def create_app(script_info=None):
    # App 'Factory'

    # Instanciar la aplicacion
    app = Flask(__name__)

    # Configuracion
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # Enlazar la base de datos
    db.init_app(app)

    import_blueprints(app)

    # Contexto de la 'shell' para flask cli
    # Registra las instancias app y db en la 'shell'.
    # Permite trabajar con el contexto de la aplicacion
    # y la base de datos sin tener que importarlos
    # directamente en la 'shell'
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app


def import_blueprints(app):
    from .api.projects_list_api import projects_list_api
    app.register_blueprint(projects_list_api)
    from .api.project_api import project_api
    app.register_blueprint(project_api)
