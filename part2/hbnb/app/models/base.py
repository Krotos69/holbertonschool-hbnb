import uuid
from datetime import datetime

class BaseModel:
    """
    Base class for all HBnB models.
    Provides id, created_at, updated_at, and update() behavior.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at", datetime.utcnow())
        self.updated_at = kwargs.get("updated_at", datetime.utcnow())

    def update(self, data: dict):
        """
        Update model attributes and refresh updated_at timestamp.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = datetime.utcnow()
