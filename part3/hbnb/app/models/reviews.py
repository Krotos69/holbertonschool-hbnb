from app.extensions import db
from app.models.base import BaseModel


class Review(BaseModel):
    """
    SQLAlchemy-mapped Review model.
    Supports:
    - user relationship
    - place relationship
    """

    __tablename__ = "reviews"

    # Columns
    text = db.Column(db.String(512), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    # No Relationships


    def to_dict(self):
        """Return a safe dictionary representation of the Review."""
        data = super().to_dict()
        data.update({
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
        })
        return data
