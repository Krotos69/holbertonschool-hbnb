from app.extensions import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    """
    Abstract SQLAlchemy base model providing:
    - UUID primary key
    - created_at timestamp
    - updated_at timestamp
    - automatic updates
    - safe serialization
    """

    __abstract__ = True  # SQLAlchemy will NOT create a table for this class

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Return a dictionary representation of the model."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
