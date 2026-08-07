from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from app.api.v1.reviews import review_model
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'reviews': fields.List(fields.Nested(review_model))
})

@api.route('/')
class PlaceList(Resource):

    @jwt_required()  # Require JWT for creating place this endpoint task2
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    def post(self):
        """Create a new place"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        claims = get_jwt()  # contains is_admin and other claims task2
        place_data = api.payload
        
        # optional: enforce admin-only creation of places
        # if not claims.get('is_admin'):
        #     return {'error': 'Admin privileges required'}, 403
        
        # Rule: owner_id Must be the authenticated user
        place_data["owner_id"] = current_user_id

        data = request.get_json() or {}
        try:
            place = facade.create_place(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "amenities": [a.id for a in place.amenities],
            "reviews": []
        }, 201

    @jwt_required()  # Require JWT for getting places listing this endpoint task2
    def get(self):
        """Get a list of all places"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        return facade.get_all_places(), 200

@api.route('/<place_id>')
class PlaceResource(Resource):

    @jwt_required()  # Require JWT for getting place details this endpoint task2
    def get(self, place_id):
        """Get place details by ID"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        return place, 200

    @jwt_required()  # Require JWT for updating place this endpoint task2
    @api.expect(place_model)
    def put(self, place_id):
        """Update place details by ID"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        claims = get_jwt()  # contains is_admin and other claims task2

        # Rule: only owner can update
        if str(place["owner"]["id"]) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403

        data = request.get_json() or {}
        try:
            place = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400
        if place is None:
            return {"error": "Place not found"}, 404
        return {"message": "Place updated successfully"}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):

    @api.marshal_list_with(review_model)
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            api.abort(404, "Place not found")
        return reviews, 200
