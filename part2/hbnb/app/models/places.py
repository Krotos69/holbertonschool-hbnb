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


    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is None:
            raise ValueError("price is required")
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("price must be a float")
        if value < 0:
            raise ValueError("price must be non-negative")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("latitude must be a float")
        if value < -90 or value > 90:
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("longitude must be a float")
        if value < -180 or value > 180:
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = value
