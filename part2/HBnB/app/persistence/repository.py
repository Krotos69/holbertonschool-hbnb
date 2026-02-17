class InMemoryRespository:
    def __init__(self):
        self.storage = {}

    def save(self, obj):
        cls =obj.__class__.__name__
        if cls not in self.storage:
            self.storage[cls] = {}
        self.storage[cls][obj.id] = obj
        return obj

    def get(self, cls, obj_if):
        return self.storage.get(cls.__name__, {}).get(obj_id)

    def all(self, cls):
        return list(self.storage.get(cls.__name__, {}).values())

    def delete(self, cls, obj_id):
        if cls.__name__ in self.storage:
            self.storage[cls.__name__].pop(obj_id, None)
