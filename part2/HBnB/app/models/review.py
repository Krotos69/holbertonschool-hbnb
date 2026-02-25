from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id): # Initialize Review with text, rating, user_id, and place_id
        super().__init__()

        if rating < 1 or rating > 5: # Ensure rating is between 1 and 5 
            raise ValueError("Rating must be between 1 and 5") # Validate rating value

        self.text = text # Set the review text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
