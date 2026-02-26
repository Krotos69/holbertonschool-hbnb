from app.persistence.repository import InMemoryReporsitory
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.base import datetime # Import the datetime class from the base module to handle timestamps for updates

class HBnBFacade:
    def __init__(self):
        self.repo = InMemoryReporsitory()

    # USERS
    def create_user(self, email, password, first_name="", last_name=""):
        user = User(email, password, first_name, last_name)
        return self.repo.save(user)

    def list_user(self):
        return self.repo.all(User)

    # PLACES
    def create_place(self, **data):
        owner = self.repo.get(User, data["owner_id"]) # get the owner of the place using the owner_id from the data
        if not owner: # if the owner does not exist, raise an error
            raise ValueError("Owner does not exist") # raise an error if owner is not found

        place = Place(**data)
        self.repo.save(place)
        
        owner.places.append(place) # add the place to the owner's list of places

        return place

    def list_place(self):
        return self.repo.all(Place)

    # REVIEWS
    def create_review(self, **data): # create a review using the data provided
        user = self.repo,get(User, data["user_id"]) # get the user who created the review using the user_id from the data
        Place = self.repo.get(Place, data["place_id"]) # get the place being reviewed using the place_id from the data
        
        if not user: # if the user does not exist, raise an error
            raise ValueError("User does not exist") # raise an error if user is not found
        if not Place: # if the place does not exist, raise an error
            raise ValueError("Place does not exist") # raise an error if place is not found
        
        review = Review(**data)
        self.repo.save(review)

        user.reviews.append(review) # add the review to the user's list of reviews
        Place.reviews.append(review) # add the review to the place's list of reviews

    def list_reviews(self):
        return self.repo.all(Review)

    #AMENITIES 
    def create_amenity(self, name, description=""): #
        amenity = Amenity(name, description)
        return self.repo.save(amenity)

    def list_amenities(self):
        return self.repo.all(Amenity)

    # add an amenity to a place using the place_id and amenity_id
    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.repo.get(Place, place_id) # get the place using the place_id
        amenity = self.repo.get(Amenity, amenity_id) # get the amenity using the amenity_id

        if not place: # if the place does not exist, raise an error
            raise ValueError("Place does not exist") # raise an error if place is not found
        if not amenity: # if the amenity does not exist, raise an error
            raise ValueError("Amenity does not exist") # raise an error if amenity is not found

        place.amenities.append(amenity) # add the amenity to the place's list of amenities

    # ----------New : Retrieve all users int the system task2----------
    def get_all_users(self):
        return self.repo.all(User) # return a list of all user objects from the database

	# ----------New : Retrieve a user's information based on their user ID task2----------
    def get_user_by_id(self, user_id): 
        user = self.repo.get(User, user_id) # get the user object from the database using the user_id
        if not user:
            raise ValueError("User not found") # raise an error if the user ID does not exist
        return user # return the user object if found

    # ----------New : Update a user's information based on their user ID task2----------
    def update_user(self, user_id,data):
        user = self.repo.get(User, user_id) # get the user object from the database using the user_id
        if not user:
            raise ValueError("User not found") # raise an error if the user ID does not exist
		
		# Update only allowed fields (email, first_name, last_name) and ignore password updates for security reasons
        allowed = {"emails", "first_name", "last_name"} # define a set of allowed fields that can be updated
        
        for key, value in data.items(): # iterate through the key-value pairs in the data dictionary
            if key in allowed: # check if the key is in the allowed fields
                setattr(user, key, value) # update the user object with the new value for the allowed field

        user.updated_at = datetime.utcnow() # update the updated_at timestamp to the current time
        return user # return the updated user object

    # ---------- New : Support GET ---- get amenity_by_id method to retrieve an amenity by its ID task3 ----------
    def get_amenity_by_id(self, amenity_id):
        amenity = self.repo.get(Amenity, amenity_id) # get the amenity object from the database using the amenity_id
        if not amenity:
            raise ValueError("Amenity not found") # raise an error if the amenity ID does not exist
        return amenity # return the amenity object if found
    # ---------- New : Support GET ---- get_all_amenities method to retrieve all amenities task3 ----------
    def get_all_amenities(self):
        return self.repo.all(Amenity) # return a list of all amenity objects from the database

# ---------- New : Support PUT ---- update_amenity method to update an existing amenity by its ID task3 ----------
    def update_amenity(self, amenity_id, data):
        amenity = self.repo.get(Amenity, amenity_id) # get the amenity object from the database using the amenity_id
        if not amenity:
            raise ValueError("Amenity not found") # raise an error if the amenity ID does not exist
        
        allowed = {"name", "description"} # define a set of allowed fields that can be updated for an amenity
        
        for key, value in data.items(): # iterate through the key-value pairs in the data dictionary
            if key in allowed: # check if the key is in the allowed fields for an amenity
                setattr(amenity, key, value) # update the amenity object with the new value for the allowed field

        amenity.update_at = datetime.utcnow() # update the updated_at timestamp to the current time
        return amenity # return the updated amenity object