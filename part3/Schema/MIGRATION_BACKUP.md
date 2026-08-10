# Migration and Backup Procedures

## Database Initialization and Migration

This document provides comprehensive procedures for database initialization, migration, backup, and recovery operations.

## Database Initialization

### Automated Initialization Script
**File**: `init_db.py`

```python
#!/usr/bin/env python3
"""
Database initialization script for the HBnB application.
Creates all database tables and optionally populates with initial data.
"""

import os
import sys
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import UserDB, PlaceDB, ReviewDB, AmenityDB

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    db.create_all()
    print("✓ Database tables created successfully!")

def populate_initial_data():
    """Populate the database with initial data."""
    print("Populating initial data...")
    
    try:
        # Create admin user
        admin = UserDB(
            first_name='System',
            last_name='Administrator',
            email='admin@hbnb.com',
            password='admin123',
            is_admin=True
        )
        db.session.add(admin)
        
        # Create sample amenities
        amenities_data = [
            'WiFi', 'Air Conditioning', 'Swimming Pool', 'Parking',
            'Kitchen', 'TV', 'Heating', 'Balcony'
        ]
        
        amenities = []
        for amenity_name in amenities_data:
            amenity = AmenityDB(name=amenity_name)
            amenities.append(amenity)
            db.session.add(amenity)
        
        # Commit to get IDs
        db.session.commit()
        print("✓ Initial data populated successfully!")
        
    except Exception as e:
        print(f"✗ Error populating initial data: {e}")
        db.session.rollback()
        raise

def main():
    """Main function to initialize the database."""
    print("=== HBnB Database Initialization ===\n")
    
    # Create app with development config
    app = create_app('development')
    
    with app.app_context():
        try:
            # Create tables
            create_tables()
            
            # Ask user if they want to populate initial data
            response = input("\nWould you like to populate the database with initial data? (y/n): ")
            if response.lower() in ['y', 'yes']:
                populate_initial_data()
            
            print("\n=== Database initialization completed! ===")
            print(f"Database file: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
        except Exception as e:
            print(f"\n✗ Database initialization failed: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
```

### Manual Initialization Commands

#### Create Tables Only
```bash
python -c "
from app import create_app, db
app = create_app('development')
with app.app_context():
    db.create_all()
    print('Tables created successfully!')
"
```

#### Drop and Recreate Tables
```bash
python -c "
from app import create_app, db
app = create_app('development')
with app.app_context():
    db.drop_all()
    db.create_all()
    print('Tables recreated successfully!')
"
```

### Flask CLI Commands
**File**: `app/__init__.py` (additional setup)

```python
@app.cli.command()
def init_db():
    """Initialize the database with tables."""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    print('Database tables dropped!')

@app.cli.command()
@click.option('--with-data', is_flag=True, help='Include sample data')
def reset_db(with_data):
    """Reset database (drop and recreate)."""
    db.drop_all()
    db.create_all()
    
    if with_data:
        # Add sample data
        from app.models import UserDB, AmenityDB
        
        # Create admin user
        admin = UserDB(
            first_name='Admin',
            last_name='User',
            email='admin@hbnb.com',
            password='admin123',
            is_admin=True
        )
        db.session.add(admin)
        
        # Create basic amenities
        amenities = ['WiFi', 'Kitchen', 'Parking', 'Pool']
        for name in amenities:
            amenity = AmenityDB(name=name)
            db.session.add(amenity)
        
        db.session.commit()
        print('Database reset with sample data!')
    else:
        print('Database reset!')
```

**Usage**:
```bash
flask init-db
flask drop-db
flask reset-db --with-data
```

## Migration Procedures

### Development Migration Workflow

#### 1. Model Changes
When you modify SQLAlchemy models:

```python
# Example: Adding a new field to PlaceDB
class PlaceDB(db.Model):
    # ... existing fields ...
    featured = Column(Boolean, default=False, nullable=False)  # New field
```

#### 2. Development Database Update
```bash
# For development: Drop and recreate (loses data)
flask drop-db
flask init-db

# Or use the reset command
flask reset-db --with-data
```

#### 3. Test the Changes
```bash
# Run tests to ensure everything works
python -m pytest

# Test the application
python run.py
```

### Production Migration Strategy

For production systems, use Flask-Migrate for safer migrations:

#### 1. Install Flask-Migrate
```bash
pip install Flask-Migrate
```

#### 2. Setup Migration Support
**File**: `app/__init__.py`

```python
from flask_migrate import Migrate

def create_app(config_name='development'):
    app = Flask(__name__)
    # ... existing setup ...
    
    # Initialize migrate after db
    migrate = Migrate(app, db)
    
    return app
```

#### 3. Initialize Migration Repository
```bash
flask db init
```

#### 4. Create Migration Scripts
```bash
# Generate migration after model changes
flask db migrate -m "Add featured field to places"

# Review the generated migration file in migrations/versions/
```

#### 5. Apply Migrations
```bash
# Apply migrations to database
flask db upgrade

# Rollback if needed
flask db downgrade
```

### Migration Best Practices

#### Safe Migration Patterns
```python
# Good: Add nullable column
featured = Column(Boolean, nullable=True)

# Good: Add column with default
featured = Column(Boolean, default=False, nullable=False)

# Risky: Add non-nullable column without default
# featured = Column(Boolean, nullable=False)  # May fail on existing data
```

#### Data Migration Example
```python
# Migration file: Add data transformation
def upgrade():
    # Add new column
    op.add_column('places', sa.Column('featured', sa.Boolean(), nullable=True))
    
    # Update existing records
    connection = op.get_bind()
    connection.execute(
        "UPDATE places SET featured = 0 WHERE featured IS NULL"
    )
    
    # Make column non-nullable
    op.alter_column('places', 'featured', nullable=False)
```

## Backup Procedures

### SQLite Backup

#### Simple File Copy
```bash
#!/bin/bash
# Simple backup script

DB_FILE="hbnb_prod.db"
BACKUP_DIR="/backup/hbnb"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/hbnb_backup_${TIMESTAMP}.db"

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Copy database file
cp "${DB_FILE}" "${BACKUP_FILE}"

# Compress backup
gzip "${BACKUP_FILE}"

echo "Backup created: ${BACKUP_FILE}.gz"

# Cleanup old backups (keep last 30 days)
find "${BACKUP_DIR}" -name "hbnb_backup_*.db.gz" -mtime +30 -delete
```

#### SQLite Backup Command
```bash
# Using SQLite backup command (safer for active databases)
sqlite3 hbnb_prod.db ".backup hbnb_backup_$(date +%Y%m%d_%H%M%S).db"
```

#### Automated Backup Script
**File**: `backup_db.py`

```python
#!/usr/bin/env python3
"""
Automated database backup script.
"""

import os
import sqlite3
import shutil
import gzip
from datetime import datetime, timedelta

def backup_sqlite_database(db_path, backup_dir):
    """Create a backup of SQLite database."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"hbnb_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        # Use SQLite backup API for consistent backup
        source_conn = sqlite3.connect(db_path)
        backup_conn = sqlite3.connect(backup_path)
        
        source_conn.backup(backup_conn)
        
        source_conn.close()
        backup_conn.close()
        
        # Compress the backup
        with open(backup_path, 'rb') as f_in:
            with gzip.open(f"{backup_path}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove uncompressed backup
        os.remove(backup_path)
        
        print(f"Backup created: {backup_path}.gz")
        return f"{backup_path}.gz"
        
    except Exception as e:
        print(f"Backup failed: {e}")
        return None

def cleanup_old_backups(backup_dir, days_to_keep=30):
    """Remove backup files older than specified days."""
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    for filename in os.listdir(backup_dir):
        if filename.startswith('hbnb_backup_') and filename.endswith('.db.gz'):
            file_path = os.path.join(backup_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            if file_time < cutoff_date:
                os.remove(file_path)
                print(f"Removed old backup: {filename}")

if __name__ == '__main__':
    DB_PATH = 'hbnb_prod.db'
    BACKUP_DIR = '/backup/hbnb'
    
    backup_file = backup_sqlite_database(DB_PATH, BACKUP_DIR)
    if backup_file:
        cleanup_old_backups(BACKUP_DIR)
```

### PostgreSQL/MySQL Backup

#### PostgreSQL Backup
```bash
#!/bin/bash
# PostgreSQL backup script

DB_NAME="hbnb_prod"
DB_USER="hbnb_user"
DB_HOST="localhost"
BACKUP_DIR="/backup/hbnb"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "${BACKUP_DIR}"

# Create SQL dump
pg_dump -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" \
    > "${BACKUP_DIR}/hbnb_backup_${TIMESTAMP}.sql"

# Compress backup
gzip "${BACKUP_DIR}/hbnb_backup_${TIMESTAMP}.sql"

echo "PostgreSQL backup created: hbnb_backup_${TIMESTAMP}.sql.gz"
```

#### MySQL Backup
```bash
#!/bin/bash
# MySQL backup script

DB_NAME="hbnb_prod"
DB_USER="hbnb_user"
DB_HOST="localhost"
BACKUP_DIR="/backup/hbnb"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "${BACKUP_DIR}"

# Create SQL dump
mysqldump -h "${DB_HOST}" -u "${DB_USER}" -p "${DB_NAME}" \
    > "${BACKUP_DIR}/hbnb_backup_${TIMESTAMP}.sql"

# Compress backup
gzip "${BACKUP_DIR}/hbnb_backup_${TIMESTAMP}.sql"

echo "MySQL backup created: hbnb_backup_${TIMESTAMP}.sql.gz"
```

## Recovery Procedures

### SQLite Recovery

#### Restore from Backup
```bash
#!/bin/bash
# SQLite restore script

BACKUP_FILE="$1"
DB_FILE="hbnb_prod.db"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Stop application first
echo "Stopping application..."
# systemctl stop hbnb  # Adjust based on your deployment

# Backup current database
mv "${DB_FILE}" "${DB_FILE}.before_restore"

# Restore from backup
if [[ "$BACKUP_FILE" == *.gz ]]; then
    gunzip -c "$BACKUP_FILE" > "$DB_FILE"
else
    cp "$BACKUP_FILE" "$DB_FILE"
fi

echo "Database restored from: $BACKUP_FILE"
echo "Previous database saved as: ${DB_FILE}.before_restore"

# Start application
echo "Starting application..."
# systemctl start hbnb  # Adjust based on your deployment
```

#### Point-in-Time Recovery
```python
# For SQLite with WAL mode, you can implement point-in-time recovery
def restore_to_timestamp(backup_file, target_timestamp):
    """Restore database to specific timestamp."""
    # This is a simplified example
    # In practice, you'd need WAL file analysis
    
    import sqlite3
    from datetime import datetime
    
    # Restore from backup
    shutil.copy(backup_file, 'temp_restore.db')
    
    # Connect and remove records after timestamp
    conn = sqlite3.connect('temp_restore.db')
    cursor = conn.cursor()
    
    # Remove records created after target timestamp
    tables = ['users', 'places', 'reviews', 'amenities']
    for table in tables:
        cursor.execute(f"""
            DELETE FROM {table} 
            WHERE created_at > ?
        """, (target_timestamp,))
    
    conn.commit()
    conn.close()
    
    # Replace current database
    shutil.move('temp_restore.db', 'hbnb_prod.db')
```

### PostgreSQL/MySQL Recovery

#### PostgreSQL Restore
```bash
#!/bin/bash
# PostgreSQL restore script

BACKUP_FILE="$1"
DB_NAME="hbnb_prod"
DB_USER="hbnb_user"

# Drop and recreate database
dropdb -U "$DB_USER" "$DB_NAME"
createdb -U "$DB_USER" "$DB_NAME"

# Restore from backup
if [[ "$BACKUP_FILE" == *.gz ]]; then
    gunzip -c "$BACKUP_FILE" | psql -U "$DB_USER" -d "$DB_NAME"
else
    psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"
fi

echo "PostgreSQL database restored from: $BACKUP_FILE"
```

#### MySQL Restore
```bash
#!/bin/bash
# MySQL restore script

BACKUP_FILE="$1"
DB_NAME="hbnb_prod"
DB_USER="hbnb_user"

# Drop and recreate database
mysql -u "$DB_USER" -p -e "DROP DATABASE IF EXISTS $DB_NAME; CREATE DATABASE $DB_NAME;"

# Restore from backup
if [[ "$BACKUP_FILE" == *.gz ]]; then
    gunzip -c "$BACKUP_FILE" | mysql -u "$DB_USER" -p "$DB_NAME"
else
    mysql -u "$DB_USER" -p "$DB_NAME" < "$BACKUP_FILE"
fi

echo "MySQL database restored from: $BACKUP_FILE"
```

## Automated Backup Schedule

### Cron Job Setup
```bash
# Edit crontab
crontab -e

# Add backup schedule (daily at 2 AM)
0 2 * * * /path/to/backup_db.py

# Weekly full backup (Sundays at 1 AM)
0 1 * * 0 /path/to/full_backup.sh

# Cleanup old backups (monthly)
0 3 1 * * find /backup/hbnb -name "*.gz" -mtime +30 -delete
```

### Systemd Timer (Alternative to Cron)
**File**: `/etc/systemd/system/hbnb-backup.service`

```ini
[Unit]
Description=HBnB Database Backup
After=network.target

[Service]
Type=oneshot
User=hbnb
ExecStart=/usr/local/bin/backup_hbnb.py
```

**File**: `/etc/systemd/system/hbnb-backup.timer`

```ini
[Unit]
Description=Run HBnB backup daily
Requires=hbnb-backup.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

**Enable Timer**:
```bash
sudo systemctl enable hbnb-backup.timer
sudo systemctl start hbnb-backup.timer
```

This comprehensive migration and backup strategy ensures data safety and smooth deployments for the HBnB application.