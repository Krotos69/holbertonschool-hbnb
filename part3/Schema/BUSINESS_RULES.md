# Business Rules and Constraints

## Application Business Logic

This document outlines the business rules, validation constraints, and application logic enforced by the HBnB system.

## User Management Rules

### User Registration
- ✅ **Admin-Only Registration**: Only existing admin users can create new accounts
- ✅ **Email Uniqueness**: Each email address can only be associated with one account
- ✅ **Password Requirements**: Minimum 6 characters, bcrypt hashed storage
- ✅ **Default Role**: New users are created as regular users (not admins) unless explicitly specified

### User Authentication
- ✅ **Email-Based Login**: Users authenticate using email address and password
- ✅ **Password Verification**: Bcrypt hash comparison for secure authentication
- ✅ **JWT Token Generation**: Successful login generates JWT with user identity and admin status

### User Profile Management
- ✅ **Self-Service Updates**: Users can update their own profile information
- ✅ **Admin Override**: Admins can update any user's profile
- ✅ **Protected Fields**: User ID, creation date, and update date cannot be modified
- ✅ **Password Changes**: Special handling for password updates with re-hashing

### User Account Deletion
- ✅ **Admin-Only Deletion**: Only admins can delete user accounts
- ✅ **Cascade Deletion**: When user is deleted, all their places and reviews are automatically removed
- ✅ **Data Integrity**: Foreign key constraints ensure no orphaned records

## Place Management Rules

### Place Creation
- ✅ **Authenticated Users Only**: Must be logged in to create places
- ✅ **Automatic Ownership**: Creator automatically becomes the owner
- ✅ **Required Information**: Title, price, and location coordinates must be provided
- ✅ **Location Validation**: Latitude must be -90 to 90, longitude must be -180 to 180

### Place Information Requirements
- ✅ **Title**: Required, maximum 100 characters
- ✅ **Description**: Optional, unlimited text length
- ✅ **Price**: Required, must be positive number (> 0)
- ✅ **Coordinates**: Both latitude and longitude required and validated
- ✅ **Owner**: Automatically set, cannot be changed after creation

### Place Modification
- ✅ **Owner Permission**: Only the place owner can modify place details
- ✅ **Admin Override**: Admins can modify any place
- ✅ **Protected Fields**: Owner ID, creation date, and update date cannot be modified
- ✅ **Validation**: All updates must pass the same validation as creation

### Place Deletion
- ✅ **Owner Permission**: Only the place owner can delete their places
- ✅ **Admin Override**: Admins can delete any place
- ✅ **Cascade Deletion**: When place is deleted, all associated reviews are automatically removed
- ✅ **Amenity Cleanup**: Place-amenity associations are automatically removed

## Review System Rules

### Review Creation
- ✅ **Authenticated Users Only**: Must be logged in to write reviews
- ✅ **One Review Per User Per Place**: Users can only write one review for each place
- ✅ **Required Information**: Review text and rating (1-5) must be provided
- ✅ **No Self-Review**: Users cannot review their own places (validation in API layer)

### Review Content Requirements
- ✅ **Review Text**: Required, unlimited length
- ✅ **Rating**: Required integer between 1 and 5 (inclusive)
- ✅ **User Association**: Automatically linked to authenticated user
- ✅ **Place Association**: Must reference valid, existing place

### Review Modification
- ✅ **Author Permission**: Only the review author can modify their reviews
- ✅ **Admin Override**: Admins can modify any review
- ✅ **Protected Fields**: User ID, place ID, creation date, and update date cannot be modified
- ✅ **Content Updates**: Text and rating can be updated with same validation rules

### Review Deletion
- ✅ **Author Permission**: Only the review author can delete their reviews
- ✅ **Admin Override**: Admins can delete any review
- ✅ **Automatic Cleanup**: Reviews automatically deleted when user or place is removed

## Amenity System Rules

### Amenity Management
- ✅ **Admin-Only Operations**: Only admins can create, update, or delete amenities
- ✅ **Name Uniqueness**: Each amenity name must be unique across the system
- ✅ **Required Name**: Amenity name is required, maximum 50 characters
- ✅ **Case Sensitivity**: Amenity names are case-sensitive for uniqueness

### Amenity-Place Associations
- ✅ **Many-to-Many Relationship**: Places can have multiple amenities, amenities can be used by multiple places
- ✅ **Dynamic Assignment**: Place owners can add/remove amenities from their places
- ✅ **Admin Control**: Only admins control the master list of available amenities
- ✅ **Automatic Cleanup**: Associations automatically removed when place or amenity is deleted

## Authorization Hierarchy

### Permission Levels
1. **Public**: Anonymous users (read-only access to places, amenities, reviews)
2. **Authenticated**: Logged-in users (can create places and reviews)
3. **Owner**: Resource owners (can modify their own places and reviews)
4. **Admin**: System administrators (can perform any operation)

### Admin Privileges
- ✅ **User Management**: Create, update, delete any user account
- ✅ **Amenity Management**: Full control over amenity system
- ✅ **Content Moderation**: Can modify or delete any place or review
- ✅ **System Operations**: Access to all protected endpoints
- ✅ **Override Permissions**: Can bypass ownership restrictions

### Ownership Rules
- ✅ **Place Ownership**: Determined by `owner_id` field, set at creation
- ✅ **Review Ownership**: Determined by `user_id` field, set at creation
- ✅ **Transfer Restrictions**: Ownership cannot be transferred (except by admin modification)
- ✅ **Inheritance**: No ownership inheritance (each resource independently owned)

## Data Validation Rules

### Input Sanitization
- ✅ **Required Fields**: All mandatory fields validated on input
- ✅ **Data Types**: Type checking for integers, floats, booleans, strings
- ✅ **String Lengths**: Maximum length validation for all string fields
- ✅ **Value Ranges**: Numeric range validation (ratings, coordinates, prices)

### Business Logic Validation
- ✅ **Email Format**: Valid email address format required
- ✅ **Coordinate Bounds**: Geographic coordinate validation
- ✅ **Positive Pricing**: Price values must be greater than zero
- ✅ **Rating Scale**: Review ratings must be 1-5 integer values

### Uniqueness Constraints
- ✅ **User Emails**: No duplicate email addresses allowed
- ✅ **Amenity Names**: No duplicate amenity names allowed
- ✅ **User-Place Reviews**: One review per user per place combination

## Error Handling Rules

### Validation Errors
- ✅ **400 Bad Request**: Invalid input data or constraint violations
- ✅ **Detailed Messages**: Specific error descriptions for validation failures
- ✅ **Field-Level Errors**: Identification of which fields failed validation
- ✅ **Consistent Format**: Standardized error response structure

### Authorization Errors
- ✅ **401 Unauthorized**: Missing or invalid authentication
- ✅ **403 Forbidden**: Valid authentication but insufficient permissions
- ✅ **Resource Ownership**: Clear indication when ownership is required
- ✅ **Admin Requirements**: Explicit messaging for admin-only operations

### Resource Errors
- ✅ **404 Not Found**: Requested resource does not exist
- ✅ **409 Conflict**: Resource conflicts (duplicate emails, existing reviews)
- ✅ **410 Gone**: Resource has been deleted
- ✅ **422 Unprocessable Entity**: Valid format but business rule violations

## System Constraints

### Performance Limits
- ✅ **Database Indexes**: Optimized queries for common operations
- ✅ **Pagination Support**: Large result sets handled via pagination
- ✅ **Query Optimization**: Efficient relationship loading strategies
- ✅ **Connection Pooling**: Database connection management

### Scalability Considerations
- ✅ **UUID Primary Keys**: Globally unique identifiers for distributed systems
- ✅ **Stateless Authentication**: JWT tokens for horizontal scaling
- ✅ **Database Abstraction**: SQLAlchemy ORM for database independence
- ✅ **Configuration Management**: Environment-based configuration

### Security Constraints
- ✅ **Password Hashing**: Irreversible bcrypt encryption
- ✅ **Token Security**: JWT with strong secret keys
- ✅ **Input Validation**: Protection against injection attacks
- ✅ **Access Control**: Consistent authorization patterns

These business rules ensure data integrity, security, and proper application behavior while providing a clear framework for feature development and system maintenance.