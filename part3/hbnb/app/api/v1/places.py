#!/usr/bin/python3
"""Place API endpoints for management of Place resources."""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(required=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Amenity name')
})

user_model = api.model('User', {
    'id': fields.String(required=True, description='User ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address')
})

review_model = api.model('Review', {
    'id': fields.String(required=True, description='Review ID'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Review rating'),
    'user_id': fields.String(required=True, description='User ID who wrote the review')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'number_rooms': fields.Integer(required=True, description='Number of rooms'),
    'number_bathrooms': fields.Integer(required=True, description='Number of bathrooms'),
    'max_guest': fields.Integer(required=True, description='Maximum number of guests'),
    'price_by_night': fields.Integer(required=True, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        data = api.payload
        try:
            place = facade.create_place(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'id': place.id, 'title': place.title}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{'id': p.id, 'title': p.title} for p in places], 200
    
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'number_rooms': place.number_rooms,
            'number_bathrooms': place.number_bathrooms,
            'max_guest': place.max_guest,
            'price_by_night': place.price_by_night,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities],
            'reviews': [{'id': r.id, 'text': r.text, 'rating': r.rating, 'user_id': r.user_id} for r in place.reviews]
        }, 200
    
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200
    
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload
        try:
            updated = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not updated:
            return {'error': 'Place not found'}, 404

        return {'message': 'Place updated successfully'}, 200