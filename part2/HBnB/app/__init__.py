from flask import Flask
from app.api.v1 import users, places, reviews, amenities

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(users.bp)
    app.register_blueprint(places.bp)
    app.register_blueprint(reviews.bp)
    app.register_blueprint(amenities.bp)

    return app
