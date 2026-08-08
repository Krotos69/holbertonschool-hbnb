# app.api package
from flask import Flask
from app.api.v1 import v1 as api_v1

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    return app
