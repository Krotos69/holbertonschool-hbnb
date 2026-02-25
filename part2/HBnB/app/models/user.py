from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, email, password, first_name="", last_name=""):
        super().__init__()

        if not email: # Check if the email is provided, if not, raise a ValueError
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required") # Set the email, password, first name, and last name attributes of the User instance based on the provided arguments

        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

        # Relationship: user -> Place, reviews
        self.places = [] # Initialize an empty list to hold the places associated with the user
        self.reviews = [] # Initialize an empty list to hold the reviews associated with the user
