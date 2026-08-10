# Performance Optimization

## Database Performance Strategies

This document outlines performance optimization strategies, indexing guidelines, and query optimization techniques for the HBnB application.

## Index Strategy

### Primary Indexes (Automatic)
These indexes are automatically created by database constraints:

```sql
-- Primary key indexes (automatic)
CREATE UNIQUE INDEX users_pkey ON users(id);
CREATE UNIQUE INDEX places_pkey ON places(id);
CREATE UNIQUE INDEX reviews_pkey ON reviews(id);
CREATE UNIQUE INDEX amenities_pkey ON amenities(id);
CREATE UNIQUE INDEX place_amenity_pkey ON place_amenity(place_id, amenity_id);
```

### Secondary Indexes (Explicit)
These indexes are explicitly created for query optimization:

#### Users Table Indexes
```sql
-- Email lookup for authentication (most critical)
CREATE INDEX idx_users_email ON users(email);

-- Admin user filtering
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- User search by name
CREATE INDEX idx_users_name ON users(first_name, last_name);
```

#### Places Table Indexes
```sql
-- Owner-based queries (very common)
CREATE INDEX idx_places_owner_id ON places(owner_id);

-- Location-based searches
CREATE INDEX idx_places_location ON places(latitude, longitude);

-- Price range filtering
CREATE INDEX idx_places_price ON places(price);

-- Title search
CREATE INDEX idx_places_title ON places(title);

-- Combined location and price filtering
CREATE INDEX idx_places_location_price ON places(latitude, longitude, price);
```

#### Reviews Table Indexes
```sql
-- User's review history
CREATE INDEX idx_reviews_user_id ON reviews(user_id);

-- Place review aggregation
CREATE INDEX idx_reviews_place_id ON reviews(place_id);

-- Rating-based filtering
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- Combined place and rating queries
CREATE INDEX idx_reviews_place_rating ON reviews(place_id, rating);

-- Recent reviews (if needed)
CREATE INDEX idx_reviews_created_at ON reviews(created_at);
```

#### Amenities Table Indexes
```sql
-- Amenity name lookup
CREATE INDEX idx_amenities_name ON amenities(name);
```

### Unique Indexes (Constraint Enforcement)
```sql
-- Unique constraint indexes (automatic)
CREATE UNIQUE INDEX users_email_unique ON users(email);
CREATE UNIQUE INDEX amenities_name_unique ON amenities(name);
CREATE UNIQUE INDEX reviews_user_place_unique ON reviews(user_id, place_id);
```

## Query Optimization

### SQLAlchemy Query Patterns

#### Efficient User Queries
```python
# Good: Use indexed email lookup
user = UserDB.query.filter_by(email=email).first()

# Good: Load relationships efficiently
user = UserDB.query.options(
    joinedload(UserDB.places),
    joinedload(UserDB.reviews)
).filter_by(email=email).first()

# Avoid: N+1 query problem
users = UserDB.query.all()
for user in users:
    print(user.places)  # This triggers individual queries
```

#### Optimized Place Queries
```python
# Good: Use owner index
owner_places = PlaceDB.query.filter_by(owner_id=user_id).all()

# Good: Location-based search with bounds
nearby_places = PlaceDB.query.filter(
    PlaceDB.latitude.between(lat_min, lat_max),
    PlaceDB.longitude.between(lng_min, lng_max)
).all()

# Good: Price range with index
affordable_places = PlaceDB.query.filter(
    PlaceDB.price <= max_price,
    PlaceDB.price >= min_price
).all()

# Good: Combined filters (uses composite index)
places = PlaceDB.query.filter(
    PlaceDB.latitude.between(lat_min, lat_max),
    PlaceDB.longitude.between(lng_min, lng_max),
    PlaceDB.price <= max_price
).all()
```

#### Efficient Review Queries
```python
# Good: Use place_id index for place reviews
place_reviews = ReviewDB.query.filter_by(place_id=place_id).all()

# Good: User's review history
user_reviews = ReviewDB.query.filter_by(user_id=user_id).all()

# Good: High-rated places (uses composite index)
good_reviews = ReviewDB.query.filter(
    ReviewDB.place_id == place_id,
    ReviewDB.rating >= 4
).all()

# Good: Average rating calculation
from sqlalchemy import func
avg_rating = db.session.query(
    func.avg(ReviewDB.rating)
).filter_by(place_id=place_id).scalar()
```

#### Amenity Association Queries
```python
# Good: Places with specific amenity
places_with_wifi = PlaceDB.query.join(
    PlaceDB.amenities
).filter(
    AmenityDB.name == 'WiFi'
).all()

# Good: Amenities for a place
place_amenities = AmenityDB.query.join(
    AmenityDB.places
).filter(
    PlaceDB.id == place_id
).all()
```

### Relationship Loading Strategies

#### Lazy Loading (Default)
```python
# Lazy loading - queries executed when accessed
user = UserDB.query.get(user_id)
places = user.places  # Separate query executed here
```

#### Eager Loading
```python
# Joined loading - single query with JOIN
user = UserDB.query.options(
    joinedload(UserDB.places)
).get(user_id)

# Subquery loading - separate optimized query
user = UserDB.query.options(
    subqueryload(UserDB.places)
).get(user_id)

# Select in loading - batch loading
users = UserDB.query.options(
    selectinload(UserDB.places)
).all()
```

#### Conditional Loading
```python
# Load relationships only when needed
if include_places:
    query = query.options(joinedload(UserDB.places))
if include_reviews:
    query = query.options(joinedload(UserDB.reviews))

user = query.get(user_id)
```

## Caching Strategies

### Application-Level Caching
```python
from functools import lru_cache
from flask import current_app
import time

class CacheManager:
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
        self.default_ttl = 300  # 5 minutes
    
    def get(self, key):
        if key in self._cache:
            if time.time() - self._timestamps[key] < self.default_ttl:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._timestamps[key]
        return None
    
    def set(self, key, value, ttl=None):
        self._cache[key] = value
        self._timestamps[key] = time.time()

# Usage example
@lru_cache(maxsize=100)
def get_popular_amenities():
    return AmenityDB.query.join(
        AmenityDB.places
    ).group_by(AmenityDB.id).all()
```

### Database-Level Caching
```python
# SQLite: Enable WAL mode for better read concurrency
def configure_sqlite_performance(app):
    @app.before_first_request
    def enable_wal_mode():
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            db.engine.execute('PRAGMA journal_mode=WAL')
            db.engine.execute('PRAGMA synchronous=NORMAL')
            db.engine.execute('PRAGMA cache_size=1000')
            db.engine.execute('PRAGMA temp_store=MEMORY')
```

## Pagination Implementation

### Efficient Pagination
```python
def get_paginated_places(page=1, per_page=20, filters=None):
    query = PlaceDB.query
    
    # Apply filters
    if filters:
        if 'owner_id' in filters:
            query = query.filter_by(owner_id=filters['owner_id'])
        if 'max_price' in filters:
            query = query.filter(PlaceDB.price <= filters['max_price'])
    
    # Use pagination
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }
```

### Cursor-Based Pagination (for large datasets)
```python
def get_places_cursor_paginated(cursor=None, limit=20):
    query = PlaceDB.query.order_by(PlaceDB.created_at.desc())
    
    if cursor:
        # Decode cursor (timestamp)
        import base64
        timestamp = base64.b64decode(cursor).decode()
        query = query.filter(PlaceDB.created_at < timestamp)
    
    places = query.limit(limit + 1).all()
    
    has_more = len(places) > limit
    if has_more:
        places = places[:-1]
    
    next_cursor = None
    if has_more and places:
        next_cursor = base64.b64encode(
            places[-1].created_at.isoformat().encode()
        ).decode()
    
    return {
        'items': places,
        'next_cursor': next_cursor,
        'has_more': has_more
    }
```

## Database Optimization

### SQLite Optimizations
```sql
-- Performance pragmas for SQLite
PRAGMA journal_mode = WAL;          -- Write-Ahead Logging
PRAGMA synchronous = NORMAL;        -- Balanced durability/performance
PRAGMA cache_size = 1000;           -- Larger page cache
PRAGMA temp_store = MEMORY;         -- Temporary tables in RAM
PRAGMA mmap_size = 268435456;       -- Memory-mapped I/O (256MB)
```

### Query Analysis
```python
# Enable query logging for development
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Analyze query performance
def analyze_query(query):
    import time
    start_time = time.time()
    result = query.all()
    execution_time = time.time() - start_time
    
    print(f"Query executed in {execution_time:.4f} seconds")
    print(f"Returned {len(result)} records")
    return result
```

### Index Usage Monitoring
```sql
-- SQLite: Check index usage
EXPLAIN QUERY PLAN SELECT * FROM places WHERE owner_id = ?;

-- Look for "USING INDEX" in the output
-- If you see "SCAN TABLE", an index might be missing
```

## Memory Optimization

### Object Loading Strategies
```python
# Load only required columns
essential_user_data = db.session.query(
    UserDB.id,
    UserDB.first_name,
    UserDB.last_name,
    UserDB.email
).all()

# Use scalar results for single values
user_count = db.session.query(func.count(UserDB.id)).scalar()

# Stream large result sets
def stream_all_places():
    query = PlaceDB.query.yield_per(100)
    for place in query:
        yield place
```

### Connection Pool Configuration
```python
# For production databases
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,           # Base connection pool size
    'max_overflow': 20,        # Additional connections beyond pool_size
    'pool_recycle': 120,       # Recycle connections after 2 minutes
    'pool_pre_ping': True,     # Validate connections before use
    'pool_timeout': 30         # Timeout for getting connection
}
```

## Performance Monitoring

### Key Metrics to Track
- **Query Execution Time**: Average and 95th percentile
- **Database Connection Usage**: Active vs available connections
- **Index Hit Ratio**: Queries using indexes vs table scans
- **Database Size Growth**: Storage usage trends
- **Slow Query Log**: Queries taking longer than threshold

### Performance Testing
```python
import time
import statistics

def benchmark_query(query_func, iterations=10):
    times = []
    for _ in range(iterations):
        start = time.time()
        result = query_func()
        end = time.time()
        times.append(end - start)
    
    return {
        'avg_time': statistics.mean(times),
        'median_time': statistics.median(times),
        'min_time': min(times),
        'max_time': max(times),
        'std_dev': statistics.stdev(times)
    }

# Usage
stats = benchmark_query(lambda: PlaceDB.query.all())
print(f"Average query time: {stats['avg_time']:.4f}s")
```

These optimization strategies ensure the HBnB application maintains good performance as data volume and user load increase.