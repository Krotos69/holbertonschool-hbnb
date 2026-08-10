"""
Amenity model for the HBnB application.

This module defines the Amenity class which represents amenities
that can be associated with places (e.g., Wi-Fi, Parking, Pool).
"""

from .base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class representing an amenity in the HBnB application.
    
    Amenities are features or services that places can offer to guests,
    such as Wi-Fi, parking, swimming pool, etc.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        name (str): The name of the amenity (max 50 chars, required)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """
    
    def __init__(self, name):
        """
        Initialize a new Amenity instance.
        
        Args:
            name (str): The name of the amenity
            
        Raises:
            ValueError: If validation fails for the name
        """
        super().__init__()
        self.name = self._validate_name(name)
    
    def _validate_name(self, name):
        """
        Validate the amenity name.
        
        Args:
            name (str): The name to validate
            
        Returns:
            str: The validated name
            
        Raises:
            ValueError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        
        name = name.strip()
        if not name:
            raise ValueError("Amenity name cannot be empty or just whitespace")
        
        if len(name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")
        
        return name
    
    def update(self, data):
        """
        Update amenity attributes with validation.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
            
        Raises:
            ValueError: If validation fails for any attribute
        """
        # Validate name if it's being updated
        if 'name' in data:
            data['name'] = self._validate_name(data['name'])
        
        # Call parent update method
        super().update(data)
    
    def to_dict(self):
        """
        Convert the Amenity object to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all amenity attributes
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        """String representation of the Amenity."""
        return f"Amenity({self.name})"
    
    def __eq__(self, other):
        """
        Check equality with another Amenity object.
        
        Args:
            other: Object to compare with
            
        Returns:
            bool: True if amenities are equal, False otherwise
        """
        if not isinstance(other, Amenity):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """
        Make Amenity objects hashable for use in sets and as dict keys.
        
        Returns:
            int: Hash value based on the amenity ID
        """
        return hash(self.id)