from flask import Blueprint, request, jsonify
from app.services.facade import HBnBFacade # task 5

bp = Blueprint("reviews", __name__, url_prefix="/api/v1/reviews") # task 1
facade = HBnBFacade()  # Will be overridden by app/__init__.py

# implement Post--- Review task 5
@bp.post("/")
def create_review():
    payload = request.get_json()
    
    required = {"text", "rating", "user_id", "place_id"}
    if not payload or not required.issubset(payload):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        review = facade.create_review(**payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(review.to_dict()), 201

@bp.get("/<review_id>") #task 5
def get_review(review_id):
    try:
        review = facade.get_review_by_id(review_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
    return jsonify(review.to_dict()), 200

# update improve #3 review list task 5
@bp.get("/")
def list_reviews():
    reviews = facade.get_all_reviews() # task 5
    result = [r.to_dict() for r in reviews]
    return jsonify(result), 200

# improvement #4 review task 5
@bp.put("/<review_id>")
def update_review(review_id):
    payload = request.get_json()
    
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        updated = facade.update_review(review_id, payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
    return jsonify(updated.to_dict()), 200
