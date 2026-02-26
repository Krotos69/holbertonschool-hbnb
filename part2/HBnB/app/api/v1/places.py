from Flask import Blueprint, request, jsonify
from app.services.facade import HBnBFacade 

bp = Blueprint("places", __name__, url_prefix="/api/v1/places")
facade = HBnBFacade() # 

@bp.post("/") # task 04
def create_place():
    payload = request.get_json()

    if not payload or "name" not in payload or "owner_id" not in payload:
        return jsonify("error": "Missing required fields"}), 400 #task 04
    
    try:
        place = facade.create_place(**payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400 
    return jsonify(facade.serialize_place(place)), 201 # task 4

@bp.get("/<place_id>") # task 4
def get_place(place_id):
    try:
        place = facade.get_place_by_id(place_id)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    return jsonify(facade.serialize_place(place)), 200 # Place endpoints task4 

@bp.get("/")
def list_places():
    places = facade.get_all_places() # task 4 update list_places
    result = [facade.serialize_place(p) for p in places]
    return jsonify(result), 200

@bp.put("/place_id>") # task 4
def update_place(place_id):
    payload = request_get_json()

    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400
    
    try:
        updated = facade.update_place(place_id, payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(facade.serialize_place(updated)), 200
