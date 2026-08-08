from app.models.user import User
from app.models.places import Place
from app.models.amenities import Amenity
from app.models.reviews import Review

from app.services.repositories.user_repository import UserRepository
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    """
    Facade layer for HBnB.
    Uses SQLAlchemy repositories for all persistence operations.
    """

    def __init__(self):
        # Task 6 requirement: dedicated UserRepository
        self.user_repo = UserRepository()

        # Generic repositories for other entities
        self.place_repo = SQLAlchemyRepository(Place)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.review_repo = SQLAlchemyRepository(Review)

    # ------------------------------
    # User Methods
    # ------------------------------

    def create_user(self, user_data):
        """Create a new user with hashed password."""
        user = User(**user_data)

        # Task 6 requirement: hash password before saving
        if "password" in user_data:
            user.hash_password(user_data["password"])

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    # ------------------------------
    # Amenity Methods
    # ------------------------------

    def create_amenity(self, data):
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

    # ------------------------------
    # Place Methods
    # ------------------------------

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        return self.place_repo.update(place_id, data)

    # ------------------------------
    # Review Methods
    # ------------------------------

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [
            r for r in self.review_repo.get_all()
            if str(r.place_id) == str(place_id)
        ]

    def update_review(self, review_id, data):
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
