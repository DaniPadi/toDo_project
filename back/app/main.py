# back/app/__init__.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from app import create_app
app = create_app()

if __name__ == "__main__":
    # DEV local: python back/app/__init__.py
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)
