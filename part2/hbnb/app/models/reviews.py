from app.models.base import BaseModel

class Review(BaseModel):
    """
    Represents a review written by a user for a place.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get("user_id")
        self.place_id = kwargs.get("place_id")
        self.rating = kwargs.get("rating")
        self.comment = kwargs.get("comment", "")

        self._validate()

    def _validate(self):
        if not self.user_id:
            raise ValueError("Review must have a user_id.")
        if not self.place_id:
            raise ValueError("Review must have a place_id.")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
