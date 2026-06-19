

---

# **Task 01 — Core Business Logic Classes**

## **Objective**

Implement the core business logic classes for the HBnB application:

- Define the main entities: **User**, **Place**, **Review**, **Amenity**
- Implement shared behavior using a **BaseModel**
- Ensure relationships between entities are represented cleanly
- Add validation and update logic
- Ensure compatibility with the Facade and repository layer

This task transforms your Part 1 design into real, functional Python classes.

---

# **1. Design Principles Used**

### **✓ UUIDs for IDs**  
As recommended in RFC 4122, UUIDs ensure global uniqueness and avoid collisions.

### **✓ BaseModel for shared attributes**  
All entities share:

- `id`
- `created_at`
- `updated_at`

### **✓ Encapsulation & Validation**  
Each model validates its own attributes and exposes an `update()` method used by the repository.

### **✓ Lightweight relationships**  
Since persistence is in‑memory for now, relationships are represented using **IDs**, not foreign keys.

### **✓ Future‑proof for SQLAlchemy**  
The structure is intentionally simple so it can be replaced with SQLAlchemy models in Part 3.

---

# **2. File: `app/models/base.py`**

```python
import uuid
from datetime import datetime

class BaseModel:
    """
    Base class for all HBnB models.
    Provides id, created_at, updated_at, and update() behavior.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at", datetime.utcnow())
        self.updated_at = kwargs.get("updated_at", datetime.utcnow())

    def update(self, data: dict):
        """
        Update model attributes and refresh updated_at timestamp.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = datetime.utcnow()
```

---

# **3. File: `app/models/user.py`**

```python
from app.models.base import BaseModel

class User(BaseModel):
    """
    Represents a user in the HBnB application.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")  # Will be hashed in Part 3

        self._validate()

    def _validate(self):
        if not self.email:
            raise ValueError("User email is required.")
        if not self.first_name:
            raise ValueError("User first_name is required.")
        if not self.last_name:
            raise ValueError("User last_name is required.")
```

---

# **4. File: `app/models/place.py`**

```python
from app.models.base import BaseModel

class Place(BaseModel):
    """
    Represents a place listed by a user.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.owner_id = kwargs.get("owner_id")  # User.id
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.city = kwargs.get("city")
        self.price_per_night = kwargs.get("price_per_night", 0)

        # Relationship: list of amenity IDs
        self.amenity_ids = kwargs.get("amenity_ids", [])

        self._validate()

    def _validate(self):
        if not self.owner_id:
            raise ValueError("Place must have an owner_id.")
        if not self.name:
            raise ValueError("Place name is required.")
        if self.price_per_night < 0:
            raise ValueError("price_per_night cannot be negative.")
```

---

# **5. File: `app/models/review.py`**

```python
from app.models.base import BaseModel

class Review(BaseModel):
    """
    Represents a review written by a user for a place.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get("user_id")
        self.place_id = kwargs.get("place_id")
        self.rating = kwargs.get("rating")
        self.comment = kwargs.get("comment", "")

        self._validate()

    def _validate(self):
        if not self.user_id:
            raise ValueError("Review must have a user_id.")
        if not self.place_id:
            raise ValueError("Review must have a place_id.")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
```

---

# **6. File: `app/models/amenity.py`**

```python
from app.models.base import BaseModel

class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with a place.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name")

        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("Amenity name is required.")
```

---

# **7. Relationship Summary**

| Entity | Relationships |
|--------|--------------|
| **User** | Owns many Places, writes many Reviews |
| **Place** | Belongs to User, has many Reviews, has many Amenities |
| **Review** | Belongs to User and Place |
| **Amenity** | Many‑to‑many with Places (via amenity_ids list) |

These relationships will be enforced in the **Facade layer** in Task 02.

---

# **8. How These Models Integrate With Your Facade**

Your Facade will:

- Validate cross‑entity relationships  
- Use repositories to store and retrieve objects  
- Provide high‑level operations like:  
  - `create_user()`  
  - `create_place()`  
  - `add_amenity_to_place()`  
  - `create_review()`  

The Facade acts as the **single entry point** for all business logic, consistent with the Facade pattern:

> “The Facade class provides a simple interface to the complex logic of one or several subsystems… shielding the client from undesired complexity.”

---

# **Author**

**Eugenio Martinez**