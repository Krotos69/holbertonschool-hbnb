import uuid 
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.update_at = datetime.utcnow()

    def to_dict(self):
        return self.__dict__
