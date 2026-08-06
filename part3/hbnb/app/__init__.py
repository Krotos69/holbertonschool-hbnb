from flask import Flask
from app.api.v1 import v1 as api_v1

def create_app(config_class="config.DevelopmentConfig"):
    """
    Updated create_app with configuration support, update your factory 
    so it receives a config class (or instance), loads it with from_object, 
    and defaults to config.DevelopmentConfig.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    #Initialize extensions here
    #Register blueprints here
    
    return app
