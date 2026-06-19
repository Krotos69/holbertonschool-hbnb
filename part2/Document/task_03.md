Perfect, **Krotos** — I’ve got you.  
Here is **Task 03 – Amenity Endpoints**, written *exactly* in the same explanatory, structured, conceptual style as **Task 00** and **Task 01**.  
No download format. No document tool.  
Just a clean, readable, instructional breakdown right here on screen.

---

# **Task 03 — Amenity Endpoints**  
### *Building the Amenity API Layer with Proper Architecture, Validation, and Integration*

---

## **1. Overview**

In this task, you extend the HBnB application by implementing the **Amenity API endpoints**, following the same architectural principles used for Users. Amenities are simple entities, but they play a key role in the HBnB domain model because they will later be associated with Places (many‑to‑many relationship).

This task focuses on:

- Designing and implementing the **Presentation Layer** (Flask‑RESTX endpoints)
- Connecting those endpoints to the **Business Logic Layer** via the **Facade**
- Ensuring proper validation, error handling, and RESTful response formats
- Preparing the system for future integration (e.g., adding amenities to places)

Just like in Task 02, the DELETE operation is **not** implemented at this stage.

---

# **2. Objectives**

By the end of Task 03, you will have:

- A complete set of Amenity endpoints:
  - **POST /amenities** — Create an amenity  
  - **GET /amenities** — List all amenities  
  - **GET /amenities/<id>** — Retrieve a single amenity  
  - **PUT /amenities/<id>** — Update an amenity  
- A fully integrated Facade layer for amenity operations  
- A consistent API interface matching the style of the User endpoints  
- Proper validation and error handling  
- A foundation for Place–Amenity relationships in future tasks  

---

# **3. Business Logic Layer (Amenity Model Recap)**

From Task 01, the **Amenity** class includes:

- `id` — UUID string  
- `name` — Required, max length 50  
- `created_at` / `updated_at` — timestamps  
- Validation for required fields  

This makes amenities simple but strict: they must always have a valid name.

---

# **4. Extending the Facade (Business Logic Integration)**

The Facade acts as the bridge between API and business logic.  
For amenities, you add four core operations:

### **Amenity‑related Facade Methods**
```python
def create_amenity(self, data):
    amenity = Amenity(**data)
    self.amenity_repo.add(amenity)
    return amenity

def get_amenity(self, amenity_id):
    return self.amenity_repo.get(amenity_id)

def get_all_amenities(self):
    return self.amenity_repo.get_all()

def update_amenity(self, amenity_id, data):
    amenity = self.get_amenity(amenity_id)
    if not amenity:
        return None
    amenity.update(data)
    return amenity
```

### **Why this matters**
- The API never touches the repository directly  
- All validation and update logic stays inside the model  
- The Facade ensures a clean, maintainable architecture  

This mirrors the structure used for Users, ensuring consistency across the project.

---

# **5. Presentation Layer (API Endpoints)**

You now create the Amenity endpoints under:

```
app/api/v1/amenities.py
```

The API uses:

- A **Namespace** (`amenities`)
- A **model** for input validation (`amenity_model`)
- Four endpoint handlers (POST, GET list, GET by ID, PUT)

---

## **5.1 Namespace and Input Model**

```python
api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})
```

This ensures:

- Input validation  
- Automatic Swagger documentation  
- Consistency with the User endpoints  

---

# **6. Endpoint Implementations**

Below is the conceptual breakdown of each endpoint, matching the style of Task 00/01.

---

## **6.1 POST /api/v1/amenities/**  
### *Create a new amenity*

### **Purpose**
- Accepts JSON input  
- Validates the amenity name  
- Creates a new Amenity instance  
- Returns the created amenity  

### **REST Behavior**
- **201 Created** on success  
- **400 Bad Request** if input is invalid  

### **Key Concept**
Amenities are simple, so no uniqueness checks are required (unlike users with email).

---

## **6.2 GET /api/v1/amenities/**  
### *Retrieve all amenities*

### **Purpose**
- Returns a list of all amenities stored in the repository  
- Useful for UI dropdowns, filters, and place creation forms  

### **REST Behavior**
- **200 OK** always (empty list is valid)

### **Key Concept**
This endpoint is foundational for future tasks where Places will reference amenities.

---

## **6.3 GET /api/v1/amenities/<amenity_id>**  
### *Retrieve a single amenity by ID*

### **Purpose**
- Fetches a specific amenity  
- Returns 404 if not found  

### **REST Behavior**
- **200 OK** if found  
- **404 Not Found** if the ID does not exist  

### **Key Concept**
This endpoint is essential for validating amenity existence when associating them with Places.

---

## **6.4 PUT /api/v1/amenities/<amenity_id>**  
### *Update an existing amenity*

### **Purpose**
- Updates the amenity’s name  
- Refreshes `updated_at` timestamp  
- Returns the updated amenity  

### **REST Behavior**
- **200 OK** on success  
- **404 Not Found** if amenity does not exist  
- **400 Bad Request** if input is invalid  

### **Key Concept**
This mirrors the update pattern used for Users, ensuring consistency across the API.

---

# **7. Registering the Namespace**

In `app/__init__.py`, you add:

```python
api.add_namespace(amenities_ns, path='/api/v1/amenities')
```

This makes all amenity endpoints available under:

```
/api/v1/amenities
```

---

# **8. Testing the Amenity Endpoints**

You can test using cURL or Postman.

### **Create an Amenity**
```
POST /api/v1/amenities/
{
  "name": "Wi-Fi"
}
```

### **Retrieve All Amenities**
```
GET /api/v1/amenities/
```

### **Retrieve One Amenity**
```
GET /api/v1/amenities/<amenity_id>
```

### **Update an Amenity**
```
PUT /api/v1/amenities/<amenity_id>
{
  "name": "Parking"
}
```

---

# **9. Expected Outcome**

After completing Task 03, you will have:

- A fully functional Amenity API  
- A clean integration between API → Facade → Business Logic  
- Consistent RESTful behavior across endpoints  
- A foundation for Place–Amenity relationships in future tasks  
- A scalable pattern you can reuse for Places and Reviews  

This completes **Task 03 — Amenity Endpoints**, written in the same conceptual, explanatory style as **Task 00** and **Task 01**.

---

If you want, I can now prepare **Task 04 – Place Endpoints** in the same style.