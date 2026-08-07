"""
Place model for the HBnB application.

This module defines the Place class which represents rental properties
in the system, including their details, location, and relationships.
"""

from .base_model import BaseModel


class Place(BaseModel):
    """
    Place class representing a rental property in the HBnB application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        title (str): The title of the place (max 100 chars, required)
        description (str): Detailed description of the place (optional)
        price (float): Price per night (must be positive)
        latitude (float): Latitude coordinate (-90.0 to 90.0)
        longitude (float): Longitude coordinate (-180.0 to 180.0)
        owner (User): User instance who owns the place
        reviews (list): List of Review instances for this place
        amenities (list): List of Amenity instances for this place
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place instance.
        
        Args:
            title (str): The title of the place
            description (str): Description of the place
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner (User): User who owns the place
            
        Raises:
            ValueError: If validation fails for any attribute
            TypeError: If owner is not a User instance
        """
        super().__init__()
        
        # Validate and set attributes
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = self._validate_owner(owner)
        
        # Initialize relationship lists
        self.reviews = []
        self.amenities = []
    
    def _validate_title(self, title):
        """
        Validate the place title.
        
        Args:
            title (str): The title to validate
            
        Returns:
            str: The validated title
            
        Raises:
            ValueError: If title is invalid
        """
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty or just whitespace")
        
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        
        return title
    
    def _validate_description(self, description):
        """
        Validate the place description.
        
        Args:
            description (str): The description to validate
            
        Returns:
            str: The validated description
        """
        if description is None:
            return ""
        
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        
        return description.strip()
    
    def _validate_price(self, price):
        """
        Validate the price per night.
        
        Args:
            price (float): The price to validate
            
        Returns:
            float: The validated price
            
        Raises:
            ValueError: If price is invalid
        """
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a valid number")
        
        if price <= 0:
            raise ValueError("Price must be a positive value")
        
        return price
    
    def _validate_latitude(self, latitude):
        """
        Validate the latitude coordinate.
        
        Args:
            latitude (float): The latitude to validate
            
        Returns:
            float: The validated latitude
            
        Raises:
            ValueError: If latitude is invalid
        """
        try:
            latitude = float(latitude)
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a valid number")
        
        if not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        
        return latitude
    
    def _validate_longitude(self, longitude):
        """
        Validate the longitude coordinate.
        
        Args:
            longitude (float): The longitude to validate
            
        Returns:
            float: The validated longitude
            
        Raises:
            ValueError: If longitude is invalid
        """
        try:
            longitude = float(longitude)
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a valid number")
        
        if not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        
        return longitude
    
    def _validate_owner(self, owner):
        """
        Validate the place owner.
        
        Args:
            owner (User): The owner to validate
            
        Returns:
            User: The validated owner
            
        Raises:
            TypeError: If owner is not a User instance
        """
        from .user import User  # Import here to avoid circular imports
        
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance")
        
        return owner
    
    def add_review(self, review):
        """
        Add a review to the place.
        
        Args:
            review (Review): The review to add
            
        Raises:
            TypeError: If review is not a Review instance
            ValueError: If review is already associated with this place
        """
        from .review import Review  # Import here to avoid circular imports
        
        if not isinstance(review, Review):
            raise TypeError("Review must be a Review instance")
        
        if review in self.reviews:
            raise ValueError("Review is already associated with this place")
        
        self.reviews.append(review)
        self.save()
    
    def remove_review(self, review):
        """
        Remove a review from the place.
        
        Args:
            review (Review): The review to remove
            
        Returns:
            bool: True if review was removed, False if not found
        """
        if review in self.reviews:
            self.reviews.remove(review)
            self.save()
            return True
        return False
    
    def add_amenity(self, amenity):
        """
        Add an amenity to the place.
        
        Args:
            amenity (Amenity): The amenity to add
            
        Raises:
            TypeError: If amenity is not an Amenity instance
            ValueError: If amenity is already associated with this place
        """
        from .amenity import Amenity  # Import here to avoid circular imports
        
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an Amenity instance")
        
        if amenity in self.amenities:
            raise ValueError("Amenity is already associated with this place")
        
        self.amenities.append(amenity)
        self.save()
    
    def remove_amenity(self, amenity):
        """
        Remove an amenity from the place.
        
        Args:
            amenity (Amenity): The amenity to remove
            
        Returns:
            bool: True if amenity was removed, False if not found
        """
        if amenity in self.amenities:
            self.amenities.remove(amenity)
            self.save()
            return True
        return False
    
    def update(self, data):
        """
        Update place attributes with validation.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
            
        Raises:
            ValueError: If validation fails for any attribute
        """
        # Validate fields before updating
        if 'title' in data:
            data['title'] = self._validate_title(data['title'])
        
        if 'description' in data:
            data['description'] = self._validate_description(data['description'])
        
        if 'price' in data:
            data['price'] = self._validate_price(data['price'])
        
        if 'latitude' in data:
            data['latitude'] = self._validate_latitude(data['latitude'])
        
        if 'longitude' in data:
            data['longitude'] = self._validate_longitude(data['longitude'])
        
        if 'owner' in data:
            data['owner'] = self._validate_owner(data['owner'])
        
        # Call parent update method
        super().update(data)
    
    def to_dict(self):
        """
        Convert the Place object to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all place attributes
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id,
            'reviews': [review.id for review in self.reviews],
            'amenities': [amenity.id for amenity in self.amenities],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        """String representation of the Place."""
        return f"Place({self.title}, ${self.price}/night)"