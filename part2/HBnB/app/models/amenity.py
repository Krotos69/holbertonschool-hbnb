from app.models.base import BaseModel

class Amenity(BaseModel): 
    def __init__(self, name, description=""): # amenity name is required, description is optional
        super().__init__()

        if not name: # amenity name is required
            raise ValueError("Amenity name is required") # raise an error if name is not provided

        self.name = name # set the name of the amenity
        self.description = description # set the description of the amenity, default is an empty string if not provided
