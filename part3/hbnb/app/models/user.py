from app.models.base import BaseModel
from app import bcrypt

class User(BaseModel):
    """
    Represents a user in the HBnB application.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.email = kwargs.get("email")

        # Never store plaintext password task1
        self.password = None
        self.is_admin = kwargs.get("is_admin", False) # Default to False if not provided task2

        # If a password was provided, hash it immediately task1
        if "password" in kwargs and kwargs["password"] is not None:
            self.hash_password(kwargs["password"])

        self._validate()

    def _validate(self):
        if not self.email:
            raise ValueError("User email is required.")
        if not self.first_name:
            raise ValueError("User first_name is required.")
        if not self.last_name:
            raise ValueError("User last_name is required.")

        # task1 Modify the User Model to Include Password Hashing
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Return safe user data (no password)."""
        data = super().to_dict()
        data.pop("password", None)
        return data
