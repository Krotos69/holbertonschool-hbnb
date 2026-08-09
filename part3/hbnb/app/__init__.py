from flask import Flask
from flask_restx import Api
from app.extensions import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    # Basic configuration (no external config.py needed)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hbnb.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register API blueprint
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1)

    return app
