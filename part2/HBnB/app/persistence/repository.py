class InMemoryRepository:
    def __init__(self):
        self.storage = {}
# --- Task 2: Implement the save method to store an object in the repository
    def save(self, obj):
        cls =obj.__class__.__name__
        if cls not in self.storage:
            self.storage[cls] = {}
        self.storage[cls][obj.id] = obj
        return obj
# --- Task 3: Implement the get method to retrieve an object by its class and ID
    def get(self, cls, obj_id):
        return self.storage.get(cls.__name__, {}).get(obj_id)
# --- Task 3: Implement the all method to retrieve all objects of a given class
    def all(self, cls):
        return list(self.storage.get(cls.__name__, {}).values())

    def delete(self, cls, obj_id):
        if cls.__name__ in self.storage:
            self.storage[cls.__name__].pop(obj_id, None)
