"""
User model for the HBnB application.

This module defines the User class which represents users in the system,
including both regular users and administrators.
"""

import re
from .base_model import BaseModel


class User(BaseModel):
    """
    User class representing a user in the HBnB application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        first_name (str): User's first name (max 50 chars, required)
        last_name (str): User's last name (max 50 chars, required)
        email (str): User's email address (unique, required, valid format)
        is_admin (bool): Administrative privileges flag (default: False)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User instance.
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email address
            is_admin (bool, optional): Admin privileges. Defaults to False.
            
        Raises:
            ValueError: If validation fails for any attribute
        """
        super().__init__()
        
        # Validate and set attributes
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = bool(is_admin)
    
    def _validate_name(self, name, field_name):
        """
        Validate a name field (first_name or last_name).
        
        Args:
            name (str): The name to validate
            field_name (str): The field name for error messages
            
        Returns:
            str: The validated name
            
        Raises:
            ValueError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        
        name = name.strip()
        if not name:
            raise ValueError(f"{field_name} cannot be empty or just whitespace")
        
        if len(name) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        
        return name
    
    def _validate_email(self, email):
        """
        Validate an email address.
        
        Args:
            email (str): The email to validate
            
        Returns:
            str: The validated email
            
        Raises:
            ValueError: If email is invalid
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        email = email.strip().lower()
        if not email:
            raise ValueError("Email cannot be empty or just whitespace")
        
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Email must be in a valid format")
        
        return email
    
    def update(self, data):
        """
        Update user attributes with validation.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
            
        Raises:
            ValueError: If validation fails for any attribute
        """
        # Validate fields before updating
        if 'first_name' in data:
            data['first_name'] = self._validate_name(data['first_name'], "First name")
        
        if 'last_name' in data:
            data['last_name'] = self._validate_name(data['last_name'], "Last name")
        
        if 'email' in data:
            data['email'] = self._validate_email(data['email'])
        
        if 'is_admin' in data:
            data['is_admin'] = bool(data['is_admin'])
        
        # Call parent update method
        super().update(data)
    
    def to_dict(self):
        """
        Convert the User object to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all user attributes
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        """String representation of the User."""
        return f"User({self.first_name} {self.last_name}, {self.email})"