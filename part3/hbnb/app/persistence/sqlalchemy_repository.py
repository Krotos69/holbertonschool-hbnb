from app.extensions import db
from app.persistence.repository import Repository

class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy-based implementation of the Repository interface.
    Handles CRUD operations for any SQLAlchemy model.
    """

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add a new object to the database."""
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieve all objects of this model."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object with the provided data."""
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete an object by its ID."""
        obj = self.get(obj_id)
        if not obj:
            return None

        db.session.delete(obj)
        db.session.commit()
        return True

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve the first object matching a given attribute."""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
