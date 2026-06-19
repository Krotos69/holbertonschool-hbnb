from app.models.base import BaseModel

class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with a place.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name")

        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("Amenity name is required.")
