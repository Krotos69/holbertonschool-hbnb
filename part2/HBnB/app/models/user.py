from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, email, password, first_name="", last_name=""):
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
