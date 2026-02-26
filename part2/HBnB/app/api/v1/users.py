from flask import Blueprint, request, jsonify # noqa: F401
from app.services.facade import HBnBFacade

bp = Blueprint("users", __name__, url_prefix="/api/v1/users") # Create a Blueprint for the users API with the prefix /api/v1/users
facade = HBnBFacade() # Create an instance of the HBnBFacade to interact with the business logic layer

# GET /api/v1/users
# This new endpoint will return a list of all users in the system.

@bp.get("/") # Define a route for the GET request to list all users
def list_users(): # This function will handle the GET request to list all users
    users = facade.get_all_users() # This method should return a list of user objects from the database
    sanitized = [] # This will hold the sanitized user data to return in the response

    for user in users: # Iterate through each user object in the list of users
        data = user.to_dict() # Convert the user object to a dictionary
        data.pop("password", None) # Remove the password field for security reasons
        sanitized.append(data) # Add the sanitized user data to the list

    return jsonify(sanitized), 200 # Return the list of sanitized user data with a 200 OK status code

#Put /api/v1/users/<user_id>
# This new endpoint will allow updating a user's information based on their user ID.
@bp.put("/<user_id>") # Define a route for the PUT request to update a user with a specific user ID
def update_user(user_id): # This function will handle the PUT request to update a user's information based on their user ID
    payload = request.get_json() # Get the JSON payload from the request body

    if not payload: # Check if the payload is empty or not valid JSON
        return jsonify({"error": "Invalid JSON payload"}), 400 # Return a 400 Bad Request if the payload is not valid JSON
    try:
        updated_user = facade.update_user(user_id, payload) # This method should update the user in the database and return the updated user object
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 # Return a 404 Not Found if the user ID does not exist or any other error occurs
    data = updated_user.to_dict() # Convert the updated user object to a dictionary
    data.pop("password", None) # Remove the password field for security reasons

    return jsonify(data), 200 # Return the updated user data with a 200 OK status code
