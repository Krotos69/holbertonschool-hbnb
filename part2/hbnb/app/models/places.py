from app.models.base import BaseModel

class Place(BaseModel):
    """
    Represents a place listed by a user.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.owner_id = kwargs.get("owner_id")  # User.id
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.city = kwargs.get("city")
        self.price_per_night = kwargs.get("price_per_night", 0)

        # Relationship: list of amenity IDs
        self.amenity_ids = kwargs.get("amenity_ids", [])

        self._validate()

    def _validate(self):
        if not self.owner_id:
            raise ValueError("Place must have an owner_id.")
        if not self.name:
            raise ValueError("Place name is required.")
        if self.price_per_night < 0:
            raise ValueError("price_per_night cannot be negative.")
