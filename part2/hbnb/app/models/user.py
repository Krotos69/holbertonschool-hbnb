from app.models.base import BaseModel

class User(BaseModel):
    """
    Represents a user in the HBnB application.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")  # Will be hashed in Part 3

        self._validate()

    def _validate(self):
        if not self.email:
            raise ValueError("User email is required.")
        if not self.first_name:
            raise ValueError("User first_name is required.")
        if not self.last_name:
            raise ValueError("User last_name is required.")
