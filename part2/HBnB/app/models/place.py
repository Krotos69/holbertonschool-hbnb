from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, name, description="",rooms=0, bathrooms=0, max_guests=0, price_per_night=0.0, address="", owner_id=None):
        super().__init__()
        
        if not name: # name is required
            raise ValueError("place name is required")
        if owner_id is None: # owner_id is required
            raise ValueError("owner_id is required")
        if price_per_night < 0: # price cannot be negative
            raise ValueError("price cannot be negative")

        self.name = name
        self.description = description
        self.rooms = rooms
        self.bathrooms =bathrooms
        self.max_guests = max_guests
        self.price_per_night = price_per_night
        self.address = address
        self.owner_id = owner_id
        
        # Relationship: place -> reviews
        self.reviews = [] # This will hold Review instances related to this Place
        self.amenities = [] # This will hold Amenity instances related to this Place

        # Add latitude and longitude attributes ---- task 4
        self.latitude = latitude 
        self.longitude = longitude