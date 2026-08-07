"""
Review model for the HBnB application.

This module defines the Review class which represents user reviews
for places in the system.
"""

from .base_model import BaseModel


class Review(BaseModel):
    """
    Review class representing a user review for a place in the HBnB application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        text (str): The content of the review (required)
        rating (int): Rating given to the place (1-5, required)
        place (Place): Place instance being reviewed
        user (User): User instance who wrote the review
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """
    
    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): The content of the review
            rating (int): Rating given to the place (1-5)
            place (Place): Place being reviewed
            user (User): User who wrote the review
            
        Raises:
            ValueError: If validation fails for any attribute
            TypeError: If place or user are not proper instances
        """
        super().__init__()
        
        # Validate and set attributes
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = self._validate_place(place)
        self.user = self._validate_user(user)
        
        # Validate business logic: user cannot review their own place
        self._validate_review_ownership()
    
    def _validate_text(self, text):
        """
        Validate the review text.
        
        Args:
            text (str): The text to validate
            
        Returns:
            str: The validated text
            
        Raises:
            ValueError: If text is invalid
        """
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        
        text = text.strip()
        if not text:
            raise ValueError("Review text cannot be empty or just whitespace")
        
        return text
    
    def _validate_rating(self, rating):
        """
        Validate the review rating.
        
        Args:
            rating (int): The rating to validate
            
        Returns:
            int: The validated rating
            
        Raises:
            ValueError: If rating is invalid
        """
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            raise ValueError("Rating must be a valid integer")
        
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        return rating
    
    def _validate_place(self, place):
        """
        Validate the place being reviewed.
        
        Args:
            place (Place): The place to validate
            
        Returns:
            Place: The validated place
            
        Raises:
            TypeError: If place is not a Place instance
        """
        from .place import Place  # Import here to avoid circular imports
        
        if not isinstance(place, Place):
            raise TypeError("Place must be a Place instance")
        
        return place
    
    def _validate_user(self, user):
        """
        Validate the user writing the review.
        
        Args:
            user (User): The user to validate
            
        Returns:
            User: The validated user
            
        Raises:
            TypeError: If user is not a User instance
        """
        from .user import User  # Import here to avoid circular imports
        
        if not isinstance(user, User):
            raise TypeError("User must be a User instance")
        
        return user
    
    def _validate_review_ownership(self):
        """
        Validate that a user cannot review their own place.
        
        Raises:
            ValueError: If user is trying to review their own place
        """
        if self.user.id == self.place.owner.id:
            raise ValueError("Users cannot review their own places")
    
    def update(self, data):
        """
        Update review attributes with validation.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
            
        Raises:
            ValueError: If validation fails for any attribute
        """
        # Validate fields before updating
        if 'text' in data:
            data['text'] = self._validate_text(data['text'])
        
        if 'rating' in data:
            data['rating'] = self._validate_rating(data['rating'])
        
        if 'place' in data:
            data['place'] = self._validate_place(data['place'])
        
        if 'user' in data:
            data['user'] = self._validate_user(data['user'])
        
        # If place or user are being updated, revalidate ownership
        if 'place' in data or 'user' in data:
            # Temporarily update the attributes to validate
            old_place = self.place
            old_user = self.user
            
            if 'place' in data:
                self.place = data['place']
            if 'user' in data:
                self.user = data['user']
            
            try:
                self._validate_review_ownership()
            except ValueError:
                # Restore old values if validation fails
                self.place = old_place
                self.user = old_user
                raise
        
        # Call parent update method
        super().update(data)
    
    def to_dict(self):
        """
        Convert the Review object to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all review attributes
        """
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        """String representation of the Review."""
        return f"Review({self.rating}/5 stars by {self.user.first_name})"
    
    def __eq__(self, other):
        """
        Check equality with another Review object.
        
        Args:
            other: Object to compare with
            
        Returns:
            bool: True if reviews are equal, False otherwise
        """
        if not isinstance(other, Review):
            return False
        return self.id == other.id