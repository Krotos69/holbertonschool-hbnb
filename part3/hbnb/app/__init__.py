from flask import Flask
from flask_restx import Api


# Import extensions (NOT from app)
from app.extensions import db, bcrypt, jwt

# Import API blueprint
from app.api.v1 import v1 as api_v1


def create_app():
    """
    Application Factory for HBnB Part 3.
    Initializes extensions, loads configuration, and registers blueprints.
    """
    app = Flask(__name__)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register API blueprint
    app.register_blueprint(api_v1)

    return app
