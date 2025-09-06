from flask import Flask 
from flask_cors import CORS
from pymongo import MongoClient
from .config import Config

client = MongoClient(Config.MONGO_URI)
db = client.todo_db

def create_app ():
    app = Flask(__name__)
    CORS(app)

    from .routes.task_routes import task_bp
    app.register_blueprint(task_bp, url_prefix="/tasks")

    return app