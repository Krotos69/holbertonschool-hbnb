from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from app.api.v1.reviews import review_model

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

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    def post(self):
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

    def get(self):
        return facade.get_all_places(), 200

@api.route('/<place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        return place, 200

    @api.expect(place_model)
    def put(self, place_id):
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
