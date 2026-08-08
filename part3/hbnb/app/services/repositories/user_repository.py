from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository dedicated to User-specific database operations.
    Extends the generic SQLAlchemyRepository with custom queries.
    """

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.model.query.filter_by(email=email).first()
