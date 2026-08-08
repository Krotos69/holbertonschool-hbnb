from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
})


@api.route('/')
class ReviewList(Resource):

    @jwt_required()
    @api.expect(review_model)
    def post(self):
        """Create a review"""
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}

        data["user_id"] = current_user_id

        review = facade.create_review(data)
        return review.to_dict(), 201

    @jwt_required()
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):

    @jwt_required()
    def get(self, review_id):
        review = facade.get_review(review_id)
        if review is None:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model)
    def put(self, review_id):
        data = request.get_json() or {}
        updated = facade.update_review(review_id, data)
        if updated is None:
            return {"error": "Review not found"}, 404
        return updated.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted"}, 200
