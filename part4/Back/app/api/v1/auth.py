#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('auth', description='Authentication operations')

# Input model for login credentials
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        #retrieves the user by email
        user = facade.get_user_by_email(credentials['email'])

        #verify user exists and password match
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # create JWT token with string subject (user id) and is_admin as additional claim
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user_id = get_jwt_identity()
        return {'message': f'Hello, user {current_user_id}'}, 200

register_model = api.model('Register', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """Register a new user"""
        data = api.payload

        try:
            user = facade.create_user(data)
            return {
                'id': str(user.id),
                'email': user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400