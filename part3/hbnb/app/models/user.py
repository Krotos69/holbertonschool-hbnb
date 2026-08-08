from app.extensions import db, bcrypt
from app.models.base import BaseModel


class User(BaseModel):
    """
    SQLAlchemy‑mapped User model for HBnB Part 3.
    Includes password hashing, validation, and safe serialization.
    """

    __tablename__ = "users"

    # SQLAlchemy columns
    id = db.Column(db.String(60), primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Assign fields
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.email = kwargs.get("email")
        self.is_admin = kwargs.get("is_admin", False)

        # Never store plaintext password
        raw_password = kwargs.get("password")
        if raw_password:
            self.hash_password(raw_password)

        self._validate()

    def _validate(self):
        if not self.email:
            raise ValueError("User email is required.")
        if not self.first_name:
            raise ValueError("User first_name is required.")
        if not self.last_name:
            raise ValueError("User last_name is required.")

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
