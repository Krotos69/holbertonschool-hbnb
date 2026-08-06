from app.persistence.repository import InMemoryRepository
from app.models import storage
from app.models.places import Place
from app.models.user import User
from app.models.amenities import Amenity
from app.models.reviews import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

# ------------------------------
# User Endpoints Methods
# ------------------------------

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(data)
        return user
# ------------------------------
# Amenity Endpoints Methods
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
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        return amenity

# ------------------------------
# Place Endpoints methods (task 04)
# ------------------------------

    def create_place(self, place_data):
        # validate owner
        owner = storage.get(User, place_data.get("owner_id"))
        if owner is None:
            raise ValueError("Owner not found")

        # validate amenities IDs
        amenity_ids = place_data.get("amenities", [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is None:
                raise ValueError(f"Amenity not found: {amenity_id}")
            amenities.append(amenity)

        # create place (validation happens in setters)
        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner_id=owner.id,
        )

        # attach amenities (depending on your relationship model)
        place.amenities = amenities

        storage.new(place)
        storage.save()
        return place

    def get_place(self, place_id):
        place = storage.get(Place, place_id)
        if place is None:
            return None

        owner = storage.get(User, place.owner_id) if place.owner_id else None
        amenities = list(place.amenities) if getattr(place, "amenities", None) else []

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            } if owner else None,
            "amenities": [
                {"id": a.id, "name": a.name} for a in amenities
            ],
        }

    def get_all_places(self):
        places = storage.all(Place).values()
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude,
            }
            for p in places
        ]

    def update_place(self, place_id, place_data):
        place = storage.get(Place, place_id)
        if place is None:
            return None

        # only update provided fields
        for field in ("title", "description", "price", "latitude", "longitude"):
            if field in place_data:
                setattr(place, field, place_data[field])

        # optionally update amenities
        if "amenities" in place_data:
            amenity_ids = place_data["amenities"]
            amenities = []
            for amenity_id in amenity_ids:
                amenity = storage.get(Amenity, amenity_id)
                if amenity is None:
                    raise ValueError(f"Amenity not found: {amenity_id}")
                amenities.append(amenity)
            place.amenities = amenities

        storage.save()
        return place

#------------------------------
# Review Endpoints methods (task 05)
#------------------------------

    def create_review(self, review_data): 
		# Validate user
        user = storage.get(User, review_data.get("user_id"))
        if user is None:
            raise ValueError("User not found")

		# Validate place
        place = storage.get(Place, review_data.get("place_id"))
        if place is None:
            raise ValueError("Place not found")

        # validate text
        if not review_data.get("text"):
            raise ValueError("Review text is required")

        # validate rating
        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

		# Create review
        review = Review(
			text=review_data.get("text"),
            rating=rating,
			user_id=user.id,
			place_id=place.id,
		)

        storage.new(review)
        storage.save()
        return review

    def get_review(self, review_id):
        return storage.get(Review, review_id)

    def get_all_reviews(self):
        reviews = storage.all(Review).values()
        return [
			{
				"id": r.id,
				"text": r.text,
                "rating": r.rating,
				"user_id": r.user_id,
				"place_id": r.place_id,
			}
			for r in reviews
		]

    def get_reviews_by_place(self, place_id):
        place = storage.get(Place, place_id)
        if place is None:
            return None

        reviews = storage.all(Review).values()
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user_id,
                "place_id": r.place_id,
            }
            for r in reviews if r.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = storage.get(Review, review_id)
        if review is None:
            return None

		# only update provided fields
        for field in ("text", "rating"):
            if field in review_data:
                setattr(review, field, review_data[field])

        storage.save()
        return review

    def delete_review(self, review_id):
        review = storage.get(Review, review_id)
        if review is None:
            return None

        storage.delete(review)
        storage.save()
        return True
