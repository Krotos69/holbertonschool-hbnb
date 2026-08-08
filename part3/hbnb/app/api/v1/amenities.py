from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True),
})


@api.route('/')
class AmenityList(Resource):

    @jwt_required()
    @api.expect(amenity_model)
    def post(self):
        data = request.get_json() or {}
        amenity = facade.create_amenity(data)
        return amenity.to_dict(), 201

    @jwt_required()
    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    @jwt_required()
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model)
    def put(self, amenity_id):
        data = request.get_json() or {}
        updated = facade.update_amenity(amenity_id, data)
        if updated is None:
            return {"error": "Amenity not found"}, 404
        return updated.to_dict(), 200
