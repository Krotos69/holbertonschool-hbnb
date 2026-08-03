from flask import Blueprint
from flask_restx import Api

# Import the namespaces from the packages 
from app.api.v1.users import api as users_ns
from app.api.v1.places import  api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns

# Create Blueprint for version 1 of the Api
v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Create API instance and register the namespaces(objects)
api = Api(
	v1,
    version='1.0',
    title='HBnB API v1',
    description='API for HBnB project (Part2)'
)

# Register the namespaces with the API isntance (objects)
api.add_namespace(users_ns)
api.add_namespace(places_ns)
api.add_namespace(amenities_ns)
api.add_namespace(reviews_ns)
