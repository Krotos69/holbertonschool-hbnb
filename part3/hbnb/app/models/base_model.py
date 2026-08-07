"""
Base model class for all HBnB entities.

This module provides the BaseModel class that serves as the foundation
for all business logic entities in the HBnB application.
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for all HBnB entities.
    
    Provides common attributes and methods for:
    - Unique identifier generation (UUID)
    - Timestamp management (created_at, updated_at)
    - Update functionality
    """
    
    def __init__(self):
        """
        Initialize a new BaseModel instance.
        
        Sets:
        - id: Unique UUID string identifier
        - created_at: Current timestamp
        - updated_at: Current timestamp
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        """
        Update the updated_at timestamp whenever the object is modified.
        
        This method should be called whenever the object's state changes
        to maintain accurate modification timestamps.
        """
        self.updated_at = datetime.now()
    
    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
            
        Note:
            - Only updates attributes that exist on the object
            - Automatically calls save() to update the timestamp
            - Ignores 'id', 'created_at', and 'updated_at' to maintain integrity
        """
        protected_attributes = {'id', 'created_at', 'updated_at'}
        
        for key, value in data.items():
            if key not in protected_attributes and hasattr(self, key):
                setattr(self, key, value)
        
        self.save()  # Update the updated_at timestamp
    
    def to_dict(self):
        """
        Convert the object to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all object attributes
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
    
    def __str__(self):
        """String representation of the object."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
    
    def __repr__(self):
        """Detailed string representation of the object."""
        return self.__str__()