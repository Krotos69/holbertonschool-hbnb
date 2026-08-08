from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Request models
user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@api.route('/')
class UserList(Resource):

    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user and return a JWT token."""
        data = request.get_json() or {}

        # Check if email already exists
        existing = facade.get_user_by_email(data.get("email"))
        if existing:
            return {"error": "Email already registered"}, 400

        # Create user (Facade handles hashing)
        user = facade.create_user(data)

        # Create JWT token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        return {
            "user": user.to_dict(),
            "access_token": access_token
        }, 201

    @jwt_required()
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users."""
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200


@api.route('/login')
class UserLogin(Resource):

    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token."""
        data = request.get_json() or {}

        user = facade.get_user_by_email(data.get("email"))
        if not user or not user.verify_password(data.get("password")):
            return {"error": "Invalid credentials"}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        return {
            "user": user.to_dict(),
            "access_token": access_token
        }, 200


@api.route('/<user_id>')
class UserResource(Resource):

    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID."""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information."""
        data = request.get_json() or {}

        user = facade.update_user(user_id, data)
        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200
