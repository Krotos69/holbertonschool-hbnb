# Database Configuration

## Environment-Specific Database Settings

This document outlines the database configuration for different environments in the HBnB application.

## Configuration Structure

### Base Configuration
**File**: `config.py`

```python
import os

class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    TESTING = False
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hbnb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = False  # For simplicity, tokens don't expire
```

## Environment Configurations

### Development Environment
**Purpose**: Local development and testing
**Database**: SQLite file-based storage

```python
class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///hbnb_dev.db')
```

**Connection Details**:
- **Type**: SQLite
- **File**: `hbnb_dev.db` (in project root)
- **Location**: Local filesystem
- **Persistence**: File-based, survives application restarts
- **Concurrency**: Single connection, suitable for development

**Usage**:
```bash
export FLASK_ENV=development
python run.py
```

### Testing Environment
**Purpose**: Automated testing and continuous integration
**Database**: In-memory SQLite

```python
class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    WTF_CSRF_ENABLED = False
```

**Connection Details**:
- **Type**: SQLite
- **Location**: Memory (RAM)
- **Persistence**: Temporary, destroyed after tests
- **Speed**: Fastest for testing
- **Isolation**: Fresh database for each test run

**Usage**:
```bash
export FLASK_ENV=testing
python -m pytest
```

### Production Environment
**Purpose**: Live production deployment
**Database**: Configurable via environment variables

```python
class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hbnb_prod.db')
```

**Connection Options**:

#### SQLite Production
```bash
export DATABASE_URL="sqlite:///hbnb_prod.db"
```

#### PostgreSQL Production
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/hbnb_prod"
```

#### MySQL Production
```bash
export DATABASE_URL="mysql://username:password@localhost:3306/hbnb_prod"
```

## Database Connection Management

### SQLAlchemy Integration
**File**: `app/__init__.py`

```python
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    
    return app
```

### Connection Pool Settings
For production databases that support connection pooling:

```python
# Additional configuration for production
class ProductionConfig(Config):
    # PostgreSQL/MySQL specific settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True,
        'max_overflow': 20
    }
```

## Environment Variables

### Required Variables
- `FLASK_ENV`: Environment name (development/testing/production)
- `SECRET_KEY`: Flask application secret key
- `JWT_SECRET_KEY`: JWT token signing key

### Optional Variables
- `DATABASE_URL`: Full database connection string
- `DEV_DATABASE_URL`: Development-specific database URL

### Environment File Example
**File**: `.env` (for development)

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration
DEV_DATABASE_URL=sqlite:///hbnb_dev.db

# Optional: Override default settings
DEBUG=True
```

## Database Initialization

### Manual Initialization
```bash
# Create all tables
python -c "
from app import create_app, db
app = create_app('development')
with app.app_context():
    db.create_all()
    print('Database tables created!')
"
```

### Automated Initialization Script
**File**: `init_db.py`

```bash
# Initialize database with sample data
python init_db.py
```

### Flask CLI Commands
**File**: `app/__init__.py` (additional setup)

```python
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    print('Database tables dropped!')
```

**Usage**:
```bash
flask init-db
flask drop-db
```

## Database Migration Strategy

### Development Workflow
1. **Model Changes**: Modify SQLAlchemy models
2. **Drop and Recreate**: In development, drop and recreate tables
3. **Test Data**: Use initialization script to populate test data

### Production Considerations
For production deployments, consider using Flask-Migrate:

```bash
pip install Flask-Migrate
```

**Setup**:
```python
from flask_migrate import Migrate

migrate = Migrate(app, db)
```

**Commands**:
```bash
flask db init      # Initialize migration repository
flask db migrate   # Generate migration script
flask db upgrade   # Apply migrations
```

## Security Considerations

### Database Access
- ✅ **Environment Variables**: Sensitive credentials in environment, not code
- ✅ **Restricted Permissions**: Database user with minimal required permissions
- ✅ **Network Security**: Database server firewall and access controls
- ✅ **SSL/TLS**: Encrypted connections for remote databases

### SQLite Security
- ✅ **File Permissions**: Restrict database file access to application user
- ✅ **Backup Security**: Secure backup storage and access
- ✅ **WAL Mode**: Write-Ahead Logging for better concurrency

### Connection String Security
```python
# Good: Use environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Bad: Hardcoded credentials
DATABASE_URL = 'postgresql://user:password@host/db'
```

## Monitoring and Maintenance

### Database Health Checks
```python
@app.route('/health/db')
def database_health():
    try:
        db.session.execute('SELECT 1')
        return {'status': 'healthy'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

### Performance Monitoring
- **Query Timing**: Monitor slow queries
- **Connection Usage**: Track connection pool utilization
- **Index Usage**: Analyze query execution plans
- **Storage Growth**: Monitor database size and growth patterns

### Backup Procedures
```bash
# SQLite backup
cp hbnb_prod.db hbnb_backup_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL backup
pg_dump hbnb_prod > hbnb_backup_$(date +%Y%m%d_%H%M%S).sql

# MySQL backup
mysqldump hbnb_prod > hbnb_backup_$(date +%Y%m%d_%H%M%S).sql
```

## Troubleshooting

### Common Issues

#### Database Connection Errors
```python
# Check database file permissions (SQLite)
ls -la hbnb_dev.db

# Test database connection
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.session.execute('SELECT 1')
    print('Database connection successful!')
"
```

#### Table Creation Issues
```python
# Force table recreation
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    print('Tables recreated!')
"
```

#### Migration Problems
```bash
# Reset migrations (development only)
rm -rf migrations/
flask db init
flask db migrate -m 'Initial migration'
flask db upgrade
```

This configuration system provides flexibility for different deployment scenarios while maintaining security and performance considerations.