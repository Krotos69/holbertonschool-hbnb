import uuid 
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.update_at = datetime.utcnow()

def update(self, **kwargs):  # Update attributes of the instance based on provided keyword arguments
    for key, value in kwargs.items(): # Iterate through the provided keyword arguments and update the corresponding attributes of the instance
        if hasattr(self, key): # Check if the instance has the attribute specified by the key
            setattr(self, key, value) # Update the attribute of the instance with the new value
    self.updated_at = datetime.utcnow() # Update the 'updated_at' attribute to the current UTC time after updating the instance's attributes

    def to_dict(self):
        return self.__dict__
