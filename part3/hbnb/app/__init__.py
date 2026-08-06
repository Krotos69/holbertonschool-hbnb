from flask import Flask
from flask_bcrypt import Bcrypt
from app.models import db
import config 
from app.api.v1 import v1 as api_v1
from flask_jwt_extended import JWTManager # task2: import JWTManager from flask_jwt_extended

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=config.DevelopmentConfig):
    """
    Updated create_app with configuration support, update your factory 
    so it receives a config class (or instance), loads it with from_object, 
    and defaults to config.DevelopmentConfig.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  #Initialize the database with the Flask app task1
    bcrypt.init_app(app)    #Register blueprints here task1
    jwt.init_app(app)       #Initialize JWT manager task2

    return app
