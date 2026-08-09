from app.extensions import db
from app.models.base import BaseModel


# Association table for many-to-many Place ↔ Amenity
place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True),
)


class Place(BaseModel):
    """
    SQLAlchemy-mapped Place model.
    Supports:
    - owner relationship
    - amenities many-to-many
    - reviews one-to-many
    """

    __tablename__ = "places"

    # Columns
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Foreign key → User.id
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    # Relationships
    owner = db.relationship("User", backref="places", lazy=True)

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
        lazy=True
    )


    reviews = db.relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_dict(self):
        """Return a safe dictionary representation of the Place."""
        data = super().to_dict()
        data.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [a.id for a in self.amenities],
            "reviews": [r.id for r in self.reviews],
        })
        return data
