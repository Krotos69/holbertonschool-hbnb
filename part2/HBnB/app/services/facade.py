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
        place = Place(**data)
        return self.repo.save(place)

    def list_place(self):
        return self.repo.all(Place)

    # REVIEWS
    def create_review(self, **data):
        review = Review(**data)
        return self.repo.all(Review)

    def list_reviews(self):
        return self.repo.all(Review)

    #AMENITIES
    def create_amenity(self, name, description=""):
        amenity = Amenity(name, description)
        return self.repo.save(amenity)

    def list_amenities(self):
        return self.repo.all(Amenity)
