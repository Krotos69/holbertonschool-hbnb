from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api =Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
	'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
	'id':fields.String(description='User ID'),
    'firts_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
	'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price of the place'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description= 'Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenity ID's")
})

@api.route('/')
class PlaceList(Resource:):
    @api.expect(place_model)
    @api.response(201, 'Place Successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """REgister a new place"""
        data = request.get_json() or {}
        try:
            place =facade.create_place(data)
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
			"amenities": [amenity.id for amenity in place.amenities]
		}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """REtrieve a list of all places"""
        places = facade.get_all_places()
        return places, 200

@api.route('/place/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        return place, 200

    @api.expect(place_model)
    @api.response(200, 'Place update successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data =request.get_json() or {}
        try:
            place = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400
        if place is None:
            return {"error": "Place not found"}, 404
        return {"message": "Place updated successfully"}, 200
