
---

# **HBnB Technical Architecture Document**

## **1. Introduction**

### **Purpose of this Document**
This document compiles and organizes the technical architecture of the **HBnB** project, including:

- The High‑Level Package Diagram  
- The Detailed Class Diagram for the Business Logic Layer  
- The Sequence Diagrams for key API calls  

Its purpose is to serve as a **blueprint** for implementation, providing a clear view of the system’s structure, responsibilities, and interaction flows.

### **Project Overview**
HBnB is an accommodation‑listing platform where users can:

- Register an account  
- Create property listings (places)  
- Submit reviews  
- Browse and filter available places  

The architecture follows a **layered design**:

- **Presentation Layer:** API / Services  
- **Business Logic Layer:** Facade + Domain Models  
- **Persistence Layer:** Repositories + Database  

This document explains how these layers interact and how the system is structured internally.

---

## **2. High‑Level Architecture**

### **2.1 High‑Level Package Diagram (Mermaid)**

```mermaid
flowchart TB
    subgraph Presentation_Layer
        API[API Endpoints]
        Services[Services]
    end

    subgraph Business_Logic_Layer
        Facade[Facade Interface]
        UserModel[User Model]
        PlaceModel[Place Model]
        ReviewModel[Review Model]
        AmenityModel[Amenity Model]
    end

    subgraph Persistence_Layer
        Repositories[Repositories / DAOs]
        Database[(Database)]
    end

    API --> Facade
    Services --> Facade
    Facade --> UserModel
    Facade --> PlaceModel
    Facade --> ReviewModel
    Facade --> AmenityModel
    UserModel --> Repositories
    PlaceModel --> Repositories
    ReviewModel --> Repositories
    AmenityModel --> Repositories
    Repositories --> Database
```

### **2.2 Architecture Explanation**

#### **Presentation Layer**
- **API:** Exposes REST endpoints to clients.  
- **Services:** Implement application‑level logic for use cases (e.g., `UserService`, `PlaceService`).

#### **Business Logic Layer**
- **Facade:** Single entry point for the Presentation Layer.  
- **Models:** Core domain entities (`User`, `Place`, `Review`, `Amenity`).

#### **Persistence Layer**
- **Repositories:** Abstract data access operations.  
- **Database:** Stores persistent data.

### **Why the Facade Pattern?**
- Reduces coupling between API and domain models  
- Centralizes validation and orchestration  
- Allows internal changes without affecting the API  

---

## **3. Business Logic Layer – Class Diagram**

### **3.1 Class Diagram (Mermaid UML)**

```mermaid
classDiagram
    class BaseModel {
        +UUID id
        +datetime created_at
        +datetime updated_at
        +save()
        +to_dict()
    }

    class User {
        +string email
        +string password
        +string first_name
        +string last_name
        +list<Place> places
        +list<Review> reviews
        +create_place()
        +add_review()
    }

    class Place {
        +string name
        +string description
        +int rooms
        +int bathrooms
        +int max_guests
        +float price_per_night
        +string address
        +User owner
        +list<Review> reviews
        +list<Amenity> amenities
        +add_review()
        +add_amenity()
    }

    class Review {
        +string text
        +int rating
        +User author
        +Place place
        +validate_rating()
    }

    class Amenity {
        +string name
        +string description
    }

    User --|> BaseModel
    Place --|> BaseModel
    Review --|> BaseModel
    Amenity --|> BaseModel

    User "1" --> "0..*" Place : owns >
    User "1" --> "0..*" Review : writes >
    Place "1" --> "0..*" Review : receives >
    Place "1" --> "0..*" Amenity : includes >
    Review "1" --> "1" Place : about >
    Review "1" --> "1" User : by >
```

### **3.2 Entity Explanations**

#### **BaseModel**
- Provides shared attributes: `id`, `created_at`, `updated_at`  
- Provides shared methods: `save()`, `to_dict()`  
- Ensures consistency across all domain entities  

#### **User**
- Represents a platform user  
- Attributes: email, password, first/last name  
- Relationships:  
  - Owns many `Place` objects  
  - Writes many `Review` objects  
- Methods: `create_place()`, `add_review()`  

#### **Place**
- Represents a property listing  
- Attributes: name, description, rooms, bathrooms, max guests, price, address  
- Relationships:  
  - Owned by a `User`  
  - Has many `Review` objects  
  - Has many `Amenity` objects  
- Methods: `add_review()`, `add_amenity()`  

#### **Review**
- Represents a user’s review of a place  
- Attributes: text, rating  
- Relationships:  
  - Written by a `User`  
  - About a `Place`  
- Method: `validate_rating()`  

#### **Amenity**
- Represents a feature or service (WiFi, pool, etc.)  
- Attributes: name, description  
- Relationship: many‑to‑many with `Place`  

---

## **4. API Interaction Flow – Sequence Diagrams**

### **4.1 User Registration**

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API as API / Controller
    participant Service as UserService
    participant Model as User Model
    participant Repo as UserRepository
    participant DB as Database

    Client->>API: POST /users (email, password, name)
    API->>Service: validate_and_create_user(data)
    Service->>Model: new User(data)
    Model-->>Service: user instance
    Service->>Repo: save(user)
    Repo->>DB: INSERT user
    DB-->>Repo: success
    Repo-->>Service: user saved
    Service-->>API: return user DTO
    API-->>Client: 201 Created (user info)
```

---

### **4.2 Place Creation**

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API as API / Controller
    participant Service as PlaceService
    participant Model as Place Model
    participant Repo as PlaceRepository
    participant DB as Database

    Client->>API: POST /places (place data)
    API->>Service: create_place(user_id, place_data)
    Service->>Model: new Place(place_data)
    Model-->>Service: place instance
    Service->>Repo: save(place)
    Repo->>DB: INSERT place
    DB-->>Repo: success
    Repo-->>Service: place saved
    Service-->>API: return place DTO
    API-->>Client: 201 Created (place info)
```

---

### **4.3 Review Submission**

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API as API / Controller
    participant Service as ReviewService
    participant Model as Review Model
    participant Repo as ReviewRepository
    participant DB as Database

    Client->>API: POST /places/{id}/reviews (review data)
    API->>Service: create_review(user_id, place_id, data)
    Service->>Model: new Review(data)
    Model-->>Service: review instance
    Service->>Repo: save(review)
    Repo->>DB: INSERT review
    DB-->>Repo: success
    Repo-->>Service: review saved
    Service-->>API: return review DTO
    API-->>Client: 201 Created (review info)
```

---

### **4.4 Fetching a List of Places**

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API as API / Controller
    participant Service as PlaceService
    participant Repo as PlaceRepository
    participant DB as Database

    Client->>API: GET /places?filters
    API->>Service: get_places(filters)
    Service->>Repo: find_by_filters(filters)
    Repo->>DB: SELECT * FROM places WHERE filters
    DB-->>Repo: list of places
    Repo-->>Service: place objects
    Service-->>API: return list DTO
    API-->>Client: 200 OK (list of places)
```

---

## **5. How All Diagrams Fit Together**

- The **High‑Level Package Diagram** shows the overall layered architecture.  
- The **Class Diagram** details the internal structure of the Business Logic Layer.  
- The **Sequence Diagrams** show how real API calls flow through all layers.  

Together, they provide a complete architectural blueprint for HBnB.

---
