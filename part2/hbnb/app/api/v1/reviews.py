from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

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

    @api.marshal_list_with(review_model)
    def get(self):
        return facade.get_all_reviews()

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        payload = api.payload
        try:
            review = facade.create_review(payload)
        except ValueError as e:
            api.abort(400, str(e))
        return review.to_dict(), 201


@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewItem(Resource):

    @api.marshal_with(review_model)
    def get(self, review_id):
        review = facade.get_review(review_id)
        if review is None:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        payload = api.payload
        review = facade.update_review(review_id, payload)
        if review is None:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            api.abort(404, "Review not found")
        return {"message": "Review deleted"}, 200
