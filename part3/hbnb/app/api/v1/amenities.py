from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Create a new amenity and get all amenities
@api.route('/')
class AmenityList(Resource):
    @jwt_required() # Require JWT for creating amenity this endpoint task2
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        claims = get_jwt()  # contains is_admin and other claims task2

        # optional: enforce admin-only creation of amenities
		# if not claims.get('is_admin'):
        #     return {'error': 'Admin privileges required'}, 403

        data = api.payload
        new_amenity = facade.create_amenity(data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

# Get all amenities
    @jwt_required() # Require JWT for getting amenities listing this endpoint task2
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get a list of all amenities"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT

        amenities = facade.get_all_amenities()
        result = [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in amenities
        ]
        return result, 200

# Get a specific amenity by ID and update an existing amenity
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @jwt_required() # Require JWT for getting amenity details this endpoint task2
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

# Update an existing amenity
    @jwt_required() # Require JWT for updating amenity this endpoint task2
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update amenity details by ID"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        claims = get_jwt()  # contains is_admin and other claims task2

        # optional: enforce admin-only updates to amenities
        # if not claims.get('is_admin'):
        #     return {'error': 'Admin privileges required'}, 403

        data = api.payload
        amenity = facade.update_amenity(amenity_id, data)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200
