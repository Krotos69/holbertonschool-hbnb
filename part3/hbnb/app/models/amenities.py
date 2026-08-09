from app.extensions import db
from app.models.base import BaseModel


class Amenity(BaseModel):
    """
    SQLAlchemy-mapped Amenity model.
    Supports:
    - many-to-many relationship with Place
    """

    __tablename__ = "amenities"

    # Columns
    name = db.Column(db.String(128), nullable=False)

    # Relationship back to Place (many-to-many)
    # The association table is defined in places.py
    places = db.relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities",
        lazy=True
    )


    def to_dict(self):
        """Return a safe dictionary representation of the Amenity."""
        data = super().to_dict()
        data.update({
            "name": self.name,
            "places": [p.id for p in self.places],
        })
        return data
