from app.models.base import BaseModel

class Place(BaseModel):
    """
    Represents a place listed by a user.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Required attributes
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.owner_id = kwargs.get("owner_id")  # User.id
        
        # these will be validates through property setters
        self._price = kwargs.get("price")
        self._latitude =kwargs.get("latitude")
        self._longitude = kwargs.get("longitude")

        # Relationship: list of amenity IDs
        self.amenity_ids = kwargs.get("amenity_ids", [])

        self._validate()

# Validation method to ensure required attributes are present and valid
    def _validate(self):
        if not self.owner_id:
            raise ValueError("Place must have an owner_id.")
        if not self.title:
            raise ValueError("Place title is required.")
        if self._price is None:
            raise ValueError("Place price is required.")
        if self._latitude is None:
            raise ValueError("Place latitude is required.")
        if self._longitude is None:
            raise ValueError("Place longitude is required.")

# Property setters and getters for price, latitude, and longitude with validation

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

# latitude and longitude properties with validation

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

# longitude property with validation
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
