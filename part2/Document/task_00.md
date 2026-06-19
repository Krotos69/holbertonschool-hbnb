

---

# **HBnB – Project Setup and Package Initialization**  
## **Task 00: Initial Project Structure, Package Setup, and In‑Memory Persistence Layer**

## **Overview**

This task establishes the foundation of the **HBnB application**, preparing the codebase for the implementation of the Business Logic and API layers in later tasks. The goal is to create a clean, modular, and scalable project structure following Python best practices, while also setting up the initial components required for the Facade pattern and the in‑memory persistence layer.

Although the full Persistence layer will be implemented in **Part 3** using SQLAlchemy, this task includes the **complete implementation of an in‑memory repository** to support object storage, retrieval, and validation during development.

This setup ensures that the application is ready for the upcoming implementation of business logic, API endpoints, and future integration with a database-backed repository.

---

## **Objectives**

By completing this task, you will:

### **1. Create the Project Directory Structure**
Organize the application into a modular architecture with clear separation of concerns:

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

This structure prepares the application for:

- **Presentation Layer** (Flask + Flask‑RESTX)
- **Business Logic Layer** (domain models)
- **Persistence Layer** (in‑memory repository → SQLAlchemy in Part 3)
- **Facade Pattern** (centralized communication between layers)

---

## **2. Initialize Python Packages**

Each directory intended to function as a Python package must include an empty `__init__.py` file:

- `app/`
- `api/`
- `api/v1/`
- `models/`
- `services/`
- `persistence/`

This enables clean imports and modular organization.

---

## **3. Set Up the Flask Application**

Inside `app/__init__.py`, create the Flask application and initialize Flask‑RESTX:

```python
from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Namespaces will be added in later tasks

    return app
```

This prepares the API layer for future endpoints.

---

## **4. Implement the In‑Memory Repository**

The in‑memory repository provides temporary storage for all entities until SQLAlchemy is introduced.

`app/persistence/repository.py`:

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name) == attr_value),
            None
        )
```

This repository will be used by the Facade to manage Users, Places, Reviews, and Amenities.

---

## **5. Prepare the Facade Pattern**

The Facade centralizes interactions between the API, business logic, and persistence layers.

`app/services/facade.py`:

```python
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder for future logic
    def create_user(self, user_data):
        pass

    def get_place(self, place_id):
        pass
```

Create a singleton instance in `app/services/__init__.py`:

```python
from app.services.facade import HBnBFacade

facade = HBnBFacade()
```

This ensures a single shared Facade instance across the application.

---

## **6. Create the Application Entry Point**

`run.py`:

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

---

## **7. Add Basic Configuration**

`config.py`:

```python
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
```

---

## **8. Install Dependencies**

`requirements.txt`:

```
flask
flask-restx
```

Install them:

```
pip install -r requirements.txt
```

---

## **9. Test the Setup**

Run the application:

```
python run.py
```

You should see Flask start successfully.  
No routes exist yet — that’s expected.  
This confirms the structure is correct and ready for the next tasks.

---

## **Author**
   **Eugenio Martinez**

---