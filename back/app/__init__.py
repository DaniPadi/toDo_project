# back/app/__init__.py
import os
import atexit
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)

    # Config por entorno (con defaults sensatos)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    app.config["MONGO_DB"]  = os.getenv("MONGO_DB",  "todo_db")

    # Habilita CORS para tu API
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Cliente Mongo para toda la vida de la app (pool reutilizable)
    app.mongo_client = MongoClient(app.config["MONGO_URI"])
    app.db = app.mongo_client[app.config["MONGO_DB"]]

    # Cierra el cliente al terminar el proceso (no en cada request)
    atexit.register(app.mongo_client.close)

    # Blueprints
    from .routes.task_routes import task_bp
    app.register_blueprint(task_bp, url_prefix="/api/tasks")

    @app.get("/api/hello")
    def hello():
        return jsonify(message="Hola desde Flask + Mongo 👋")

    return app

# Exporta el WSGI app (para gunicorn o flask run)
app = create_app()
