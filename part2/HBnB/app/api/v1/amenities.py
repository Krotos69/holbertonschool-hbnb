from flask import Blueprint, request, jsonify
from app.services.facade import HBnBFacade # Import the HBnBFacade class from the services module task 3

bp = Blueprint("amenities", __name__, url_prefix="/api/v1/amenities") # Define the blueprint for amenities with a URL prefix---task 1
facade = HBnBFacade() # Create an instance of the HBnBFacade class to use its methods---task 2

#-- Task 3: Implement the POST endpoint to create a new amenity
@bp.post("/")
def create_amenity():
    payload = request.get_json() # Get the JSON payload from the request
    
    if not payload or "name" not in payload:
        return jsonify({"error": "Missing required field: name"}), 400 # Return an error if the name field is missing

    try:
        amenity = facade.create_amenity(payload["name"], payload.get("description", "")) # Use the facade to create a new amenity with the provided name and optional description
    except ValueError as e:
        return jsonify({"error": str(e)}), 400 # Return an error if there was an issue creating the amenity
    return jsonify({amenity.to_dict()}), 201 # Return the created amenity as a JSON response with a 201 status code

# -- Task 3: Implement the GET endpoint to retrieve an amenity by its ID
@bp.get("amenity_id")
def get_amenity(amenity_id):
    try:
        amenity = facade.get_amenity_by_id(amenity_id) # Use the facade to retrieve an amenity by its ID
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 # Return an error if the amenity was not found
    return jsonify({amenity.to_dict()}), 200 # Return the retrieved amenity as a JSON response with a 200 status code

# -- Task 3: Implement the GET endpoint to retrieve all amenities
@bp.get("/")
def list_amenities():
    amenities = facade.get_all_amenities() # Use the facade to retrieve all amenities
    result = [a.to_dict() for a in amenities] # Convert each amenity to a dictionary for JSON serialization
    return jsonify(result), 200 # Return the list of amenities as a JSON response with a 200 status code

# -- Task 3: Implement the PUT endpoint to update an existing amenity by its ID
@bp.put("/<amenity_id>")
def update_amenity(amenity_id):
    payload = request.get_json() # Get the JSON payload from the request

    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400 # Return an error if the payload is not valid JSON
    try:
        updated = facade.update_amenity(amenity_id, payload) # Use the facade to update the amenity with the provided ID and payload
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 # Return an error if the amenity was not found or if there was an issue updating it
    
    return jsonify(updated.to_dict()), 200 # Return the updated amenity as a JSON response with a 200 status code