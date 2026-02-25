from app.persistence.repository import InMemoryReporsitory
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

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
    def create_amenity(self, name, description=""):
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
