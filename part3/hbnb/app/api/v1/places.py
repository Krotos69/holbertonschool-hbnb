from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from app.api.v1.reviews import review_model
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
})


@api.route('/')
class PlaceList(Resource):

    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    def post(self):
        """Create a new place"""
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}

        # Owner must be the authenticated user
        data["owner_id"] = current_user_id

        place = facade.create_place(data)
        return place.to_dict(), 201

    @jwt_required()
    def get(self):
        """Get a list of all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):

    @jwt_required()
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @jwt_required()
    @api.expect(place_model)
    def put(self, place_id):
        """Update place details by ID"""
        current_user_id = get_jwt_identity()

        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        # Only owner can update
        if str(place.owner_id) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403

        data = request.get_json() or {}
        updated = facade.update_place(place_id, data)

        return updated.to_dict(), 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):

    @jwt_required()
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Get all reviews for a place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [r.to_dict() for r in reviews], 200
