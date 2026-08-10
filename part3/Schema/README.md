# HBnB Database Schema Documentation

## Overview

This directory contains comprehensive documentation for the HBnB application database schema, organized into separate files for better readability and maintenance.

## Documentation Structure

📁 **SCHEMA Directory Contents:**

### 🎯 Core Documentation
- [`README.md`](README.md) - This overview file
- [`ENTITY_RELATIONSHIP_DIAGRAM.md`](ENTITY_RELATIONSHIP_DIAGRAM.md) - Complete ERD with visual representation
- [`SQLALCHEMY_MODELS.md`](SQLALCHEMY_MODELS.md) - SQLAlchemy class architecture diagrams

### 📊 Database Tables
- [`TABLES_SCHEMA.md`](TABLES_SCHEMA.md) - Complete SQL table definitions and constraints
- [`RELATIONSHIPS.md`](RELATIONSHIPS.md) - Foreign keys, associations, and relationships

### 🔐 Security & Authentication
- [`AUTHENTICATION_FLOW.md`](AUTHENTICATION_FLOW.md) - JWT authentication and authorization diagrams
- [`SECURITY_FEATURES.md`](SECURITY_FEATURES.md) - Password security, JWT configuration, authorization levels

### ⚙️ Configuration & Operations
- [`DATABASE_CONFIGURATION.md`](DATABASE_CONFIGURATION.md) - Environment settings and connection strings
- [`BUSINESS_RULES.md`](BUSINESS_RULES.md) - Application constraints and validation rules
- [`PERFORMANCE_OPTIMIZATION.md`](PERFORMANCE_OPTIMIZATION.md) - Indexes, query optimization strategies
- [`MIGRATION_BACKUP.md`](MIGRATION_BACKUP.md) - Database initialization, migration, and backup procedures

## Quick Navigation

### For Developers
Start with [`SQLALCHEMY_MODELS.md`](SQLALCHEMY_MODELS.md) to understand the code structure, then review [`BUSINESS_RULES.md`](BUSINESS_RULES.md) for application logic.

### For Database Administrators
Begin with [`ENTITY_RELATIONSHIP_DIAGRAM.md`](ENTITY_RELATIONSHIP_DIAGRAM.md) and [`TABLES_SCHEMA.md`](TABLES_SCHEMA.md) for the database structure, then check [`PERFORMANCE_OPTIMIZATION.md`](PERFORMANCE_OPTIMIZATION.md) for optimization guidelines.

### For System Architects
Review [`AUTHENTICATION_FLOW.md`](AUTHENTICATION_FLOW.md) and [`SECURITY_FEATURES.md`](SECURITY_FEATURES.md) for security architecture, then examine [`DATABASE_CONFIGURATION.md`](DATABASE_CONFIGURATION.md) for deployment considerations.

### For Project Managers
Start with this overview, then review [`BUSINESS_RULES.md`](BUSINESS_RULES.md) to understand application constraints and requirements.

## Key Features Documented

✅ **Complete Database Schema**
- All table structures with constraints
- Primary and foreign key relationships
- Indexes for performance optimization

✅ **SQLAlchemy Integration**
- Model class architecture
- Relationship mappings
- Query optimization strategies

✅ **Security Implementation**
- JWT-based authentication flow
- Password hashing with bcrypt
- Role-based authorization

✅ **Business Logic**
- User management rules
- Place ownership validation
- Review system constraints
- Admin access controls

✅ **Operational Procedures**
- Database initialization scripts
- Migration strategies
- Backup and recovery procedures

## Technology Stack

- **Database**: SQLite (dev/test), configurable for production
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: JWT with Flask-JWT-Extended
- **Password Security**: bcrypt hashing
- **API Framework**: Flask-RESTX with Swagger documentation

## Getting Started

1. **For Implementation**: Start with [`SQLALCHEMY_MODELS.md`](SQLALCHEMY_MODELS.md)
2. **For Database Setup**: Follow [`MIGRATION_BACKUP.md`](MIGRATION_BACKUP.md)
3. **For Security Understanding**: Review [`AUTHENTICATION_FLOW.md`](AUTHENTICATION_FLOW.md)
4. **For Performance**: Check [`PERFORMANCE_OPTIMIZATION.md`](PERFORMANCE_OPTIMIZATION.md)

This modular documentation structure makes it easy to find specific information while maintaining comprehensive coverage of all database-related aspects of the HBnB application.