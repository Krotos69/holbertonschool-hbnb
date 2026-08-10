# Database Tables Schema

## Complete SQL Table Definitions

This document contains the complete SQL table definitions with all constraints, indexes, and relationships.

## Users Table

Stores user account information and authentication data.

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
```

### Constraints
- **Primary Key**: `id` (UUID string)
- **Unique**: `email` (for authentication)
- **Not Null**: `first_name`, `last_name`, `email`, `password_hash`, `is_admin`, `created_at`, `updated_at`
- **Default**: `is_admin = FALSE`

### Data Types
- **id**: VARCHAR(36) - UUID string format
- **first_name**: VARCHAR(50) - User's first name
- **last_name**: VARCHAR(50) - User's last name
- **email**: VARCHAR(120) - Email address for login
- **password_hash**: VARCHAR(128) - Bcrypt hash of password
- **is_admin**: BOOLEAN - Admin privileges flag
- **created_at**: DATETIME - Account creation timestamp
- **updated_at**: DATETIME - Last modification timestamp

## Places Table

Stores property/place listings with location and pricing information.

```sql
CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    owner_id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (price > 0),
    CHECK (latitude >= -90 AND latitude <= 90),
    CHECK (longitude >= -180 AND longitude <= 180)
);

-- Indexes for performance
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_places_location ON places(latitude, longitude);
CREATE INDEX idx_places_price ON places(price);
```

### Constraints
- **Primary Key**: `id` (UUID string)
- **Foreign Key**: `owner_id` → `users(id)` with CASCADE DELETE
- **Not Null**: `title`, `price`, `latitude`, `longitude`, `owner_id`, `created_at`, `updated_at`
- **Check Constraints**:
  - `price > 0` (positive pricing only)
  - `latitude BETWEEN -90 AND 90` (valid latitude range)
  - `longitude BETWEEN -180 AND 180` (valid longitude range)

### Data Types
- **id**: VARCHAR(36) - UUID string format
- **title**: VARCHAR(100) - Place title/name
- **description**: TEXT - Optional detailed description
- **price**: REAL - Price per night (must be positive)
- **latitude**: REAL - GPS latitude coordinate
- **longitude**: REAL - GPS longitude coordinate
- **owner_id**: VARCHAR(36) - Reference to users table
- **created_at**: DATETIME - Listing creation timestamp
- **updated_at**: DATETIME - Last modification timestamp

## Reviews Table

Stores user reviews for places with ratings and text feedback.

```sql
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    place_id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    UNIQUE(user_id, place_id),
    CHECK (rating >= 1 AND rating <= 5)
);

-- Indexes for performance
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
```

### Constraints
- **Primary Key**: `id` (UUID string)
- **Foreign Keys**:
  - `user_id` → `users(id)` with CASCADE DELETE
  - `place_id` → `places(id)` with CASCADE DELETE
- **Unique**: `(user_id, place_id)` - One review per user per place
- **Not Null**: `text`, `rating`, `user_id`, `place_id`, `created_at`, `updated_at`
- **Check Constraint**: `rating BETWEEN 1 AND 5` (valid rating range)

### Data Types
- **id**: VARCHAR(36) - UUID string format
- **text**: TEXT - Review text content
- **rating**: INTEGER - Rating from 1 to 5
- **user_id**: VARCHAR(36) - Reference to users table
- **place_id**: VARCHAR(36) - Reference to places table
- **created_at**: DATETIME - Review creation timestamp
- **updated_at**: DATETIME - Last modification timestamp

## Amenities Table

Stores available amenities that can be associated with places.

```sql
CREATE TABLE amenities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_amenities_name ON amenities(name);
```

### Constraints
- **Primary Key**: `id` (UUID string)
- **Unique**: `name` (amenity names must be unique)
- **Not Null**: `name`, `created_at`, `updated_at`

### Data Types
- **id**: VARCHAR(36) - UUID string format
- **name**: VARCHAR(50) - Amenity name (e.g., "WiFi", "Pool")
- **created_at**: DATETIME - Amenity creation timestamp
- **updated_at**: DATETIME - Last modification timestamp

## Place-Amenity Association Table

Many-to-many relationship between places and amenities.

```sql
CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- No additional indexes needed - primary key covers common queries
```

### Constraints
- **Composite Primary Key**: `(place_id, amenity_id)`
- **Foreign Keys**:
  - `place_id` → `places(id)` with CASCADE DELETE
  - `amenity_id` → `amenities(id)` with CASCADE DELETE

### Data Types
- **place_id**: VARCHAR(36) - Reference to places table
- **amenity_id**: VARCHAR(36) - Reference to amenities table

## Performance Indexes

### Primary Indexes (Automatic)
- `users.id` (PRIMARY KEY)
- `places.id` (PRIMARY KEY)
- `reviews.id` (PRIMARY KEY)
- `amenities.id` (PRIMARY KEY)
- `place_amenity(place_id, amenity_id)` (COMPOSITE PRIMARY KEY)

### Secondary Indexes (Explicit)
- `idx_users_email` - Fast email lookups for authentication
- `idx_places_owner_id` - Owner-based place queries
- `idx_places_location` - Location-based searches
- `idx_places_price` - Price range filtering
- `idx_reviews_user_id` - User's review history
- `idx_reviews_place_id` - Place review aggregation
- `idx_reviews_rating` - Rating-based filtering
- `idx_amenities_name` - Amenity name lookups

### Unique Indexes (Constraint Enforcement)
- `users.email` (UNIQUE constraint)
- `amenities.name` (UNIQUE constraint)
- `reviews(user_id, place_id)` (UNIQUE constraint)

## Table Relationships Summary

```sql
-- One-to-Many Relationships
places.owner_id → users.id (CASCADE DELETE)
reviews.user_id → users.id (CASCADE DELETE)
reviews.place_id → places.id (CASCADE DELETE)

-- Many-to-Many Relationships
place_amenity.place_id → places.id (CASCADE DELETE)
place_amenity.amenity_id → amenities.id (CASCADE DELETE)
```

## Storage Considerations

### SQLite-Specific Features
- **DATETIME**: Stored as TEXT in ISO8601 format
- **BOOLEAN**: Stored as INTEGER (0/1)
- **REAL**: IEEE floating point numbers
- **TEXT**: Variable length strings
- **VARCHAR(n)**: TEXT with length limit (advisory in SQLite)

### Size Estimates (Approximate)
- **users**: ~200 bytes per record
- **places**: ~300 bytes per record
- **reviews**: ~250 bytes per record + text length
- **amenities**: ~100 bytes per record
- **place_amenity**: ~80 bytes per record

### Growth Projections
- **Small deployment**: <1,000 users, <5,000 places
- **Medium deployment**: 1,000-10,000 users, 5,000-50,000 places
- **Large deployment**: >10,000 users, >50,000 places

This schema provides a robust foundation for the HBnB application with proper constraints, relationships, and performance optimizations.