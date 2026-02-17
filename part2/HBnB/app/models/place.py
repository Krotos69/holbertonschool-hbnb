from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, name, description="",rooms=0, bathrooms=0, max_guests=0, price_per_night=0.0, address="", owner_id=None):
        super().__init__()
        self.name = name
        self.description = description
        self.rooms = rooms
        self.bathrooms =bathrooms
        self.mas_guests = mas_guests
        self.price_per_night = price_per_night
        self.address = address
        self.owner_id = owner_id
