-- Initial data for HBnB Application
-- This script inserts initial data for testing and demonstration

-- Insert initial admin user
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin, created_at, updated_at) 
VALUES (
    'admin-001',
    'System',
    'Administrator',
    'admin@hbnb.com',
    '$2b$12$example_hash_here',  -- This should be replaced with actual bcrypt hash
    TRUE,
    datetime('now'),
    datetime('now')
);

-- Insert sample amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
    ('amenity-001', 'WiFi', datetime('now'), datetime('now')),
    ('amenity-002', 'Air Conditioning', datetime('now'), datetime('now')),
    ('amenity-003', 'Swimming Pool', datetime('now'), datetime('now')),
    ('amenity-004', 'Parking', datetime('now'), datetime('now')),
    ('amenity-005', 'Kitchen', datetime('now'), datetime('now')),
    ('amenity-006', 'TV', datetime('now'), datetime('now')),
    ('amenity-007', 'Heating', datetime('now'), datetime('now')),
    ('amenity-008', 'Balcony', datetime('now'), datetime('now'));

-- Insert sample regular users
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin, created_at, updated_at) 
VALUES 
    ('user-001', 'John', 'Doe', 'john@example.com', '$2b$12$example_hash_here', FALSE, datetime('now'), datetime('now')),
    ('user-002', 'Jane', 'Smith', 'jane@example.com', '$2b$12$example_hash_here', FALSE, datetime('now'), datetime('now')),
    ('user-003', 'Bob', 'Johnson', 'bob@example.com', '$2b$12$example_hash_here', FALSE, datetime('now'), datetime('now'));

-- Insert sample places
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at) VALUES
    (
        'place-001',
        'Cozy Downtown Apartment',
        'A beautiful 2-bedroom apartment in the heart of the city with modern amenities.',
        120.50,
        40.7589,
        -73.9851,
        'user-001',
        datetime('now'),
        datetime('now')
    ),
    (
        'place-002',
        'Beachfront Villa',
        'Stunning oceanview villa with private beach access and luxury furnishings.',
        450.00,
        25.7617,
        -80.1918,
        'user-002',
        datetime('now'),
        datetime('now')
    ),
    (
        'place-003',
        'Mountain Cabin Retreat',
        'Peaceful cabin in the mountains, perfect for nature lovers and hiking enthusiasts.',
        85.75,
        39.7392,
        -104.9903,
        'user-001',
        datetime('now'),
        datetime('now')
    );

-- Associate places with amenities
INSERT INTO place_amenity (place_id, amenity_id) VALUES
    -- Downtown Apartment amenities
    ('place-001', 'amenity-001'),  -- WiFi
    ('place-001', 'amenity-002'),  -- Air Conditioning
    ('place-001', 'amenity-004'),  -- Parking
    ('place-001', 'amenity-005'),  -- Kitchen
    ('place-001', 'amenity-006'),  -- TV
    
    -- Beachfront Villa amenities
    ('place-002', 'amenity-001'),  -- WiFi
    ('place-002', 'amenity-002'),  -- Air Conditioning
    ('place-002', 'amenity-003'),  -- Swimming Pool
    ('place-002', 'amenity-004'),  -- Parking
    ('place-002', 'amenity-005'),  -- Kitchen
    ('place-002', 'amenity-006'),  -- TV
    ('place-002', 'amenity-008'),  -- Balcony
    
    -- Mountain Cabin amenities
    ('place-003', 'amenity-001'),  -- WiFi
    ('place-003', 'amenity-005'),  -- Kitchen
    ('place-003', 'amenity-007');  -- Heating

-- Insert sample reviews
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at) VALUES
    (
        'review-001',
        'Amazing place! The location was perfect and the apartment was exactly as described.',
        5,
        'user-002',
        'place-001',
        datetime('now'),
        datetime('now')
    ),
    (
        'review-002',
        'Beautiful villa with incredible ocean views. Would definitely stay again!',
        5,
        'user-003',
        'place-002',
        datetime('now'),
        datetime('now')
    ),
    (
        'review-003',
        'The cabin was cozy and peaceful. Great for a weekend getaway from the city.',
        4,
        'user-003',
        'place-003',
        datetime('now'),
        datetime('now')
    );