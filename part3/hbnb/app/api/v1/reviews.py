from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.marshal_list_with(review_model)
    def get(self):
        """ List all reviews"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT

        return facade.get_all_reviews()

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """ Create a new review"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        claims = get_jwt()  # contains is_admin and other claims task2

        payload = api.payload
        
        # Optional: enforce that the logged-in user must match review.user_id
        # if str(current_user_id) != str(data.get("user_id")) and not claims.get("is_admin"):
        #     return {"error": "You can only create reviews for yourself unless you are an admin"}, 403
        
        try:
            review = facade.create_review(payload)
        except ValueError as e:
            api.abort(400, str(e))
        return review.to_dict(), 201


@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewItem(Resource):
    
    @jwt_required()
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get a review by ID"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        
        review = facade.get_review(review_id)
        if review is None:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review by ID"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        claims = get_jwt()  # contains is_admin and other claims task2
        
        payload = api.payload
        review = facade.update_review(review_id, payload)
        if review is None:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review by ID"""
        current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
        claims = get_jwt()  # contains is_admin and other claims task2

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        # Only owner or admin can delete
        if str(current_user_id) != str(review.user_id) and not claims.get("is_admin"):
            return {"error": "You can only delete your own reviews unless you are an admin"}, 403

        deleted = facade.delete_review(review_id)
        if not deleted:
            api.abort(404, "Review not found")
        return {"message": "Review deleted"}, 200
