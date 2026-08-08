from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt #task2

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()  # Require JWT for creating user this endpoint task2
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        current_user_id = get_jwt_identity()  # Get the current user ID from the JWT token task2
        user_data = api.payload

        #Check if  email already exists in the database task1
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create user (this will hash the password inside the model) task1
        new_user = facade.create_user(user_data)

        #Return safe response (no password) task1 part3
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @jwt_required()  # Require JWT for getting users listing this endpoint task2
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        current_user_id = get_jwt_identity()  # Get the current user ID from the JWT token task2
        users = facade.get_all_users()
        result = [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ]
        return result, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()  # Require JWT for getting user details this endpoint task2
    def get(self, user_id):
        """Get user details by ID"""
        current_user_id = get_jwt_identity()  # Get the current user ID from the JWT token task2
        claims = get_jwt()  # contains is_admin and other claims task2
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()  # Require JWT for updating user this endpoint task2
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user information"""
        current_user_id = get_jwt_identity()  # Get the current user ID from the JWT token task2

        # Rule: user can only modify their own profile
        if str(current_user_id) != str(user_id):
            return {"error": "Unauthorized action"}, 403

        data = api.payload
        
        # Rule: cannot modify email or password here
        if 'email' in data or 'password' in data:
            return {"error": " You cannot modify email or password here"}, 400

        user = facade.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
