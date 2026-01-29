# Supabase Integration Setup Guide

## Overview
This document guides you through properly connecting your Django application to Supabase for database and file storage operations.

## What's Been Added

### 1. **Supabase Configuration Module** (`apps/core/supabase_config.py`)
- Client initialization
- Connection management
- Storage operations
- Error handling with detailed messages

### 2. **Supabase Utilities** (`apps/core/supabase_utils.py`)
- SupabaseDB helper class for common operations
- Convenience functions for:
  - SELECT (select_all, select_by_id, select_where)
  - INSERT (insert, insert_many)
  - UPDATE (update, update_where)
  - DELETE (delete, delete_where)
  - AGGREGATE (count)

### 3. **Initialization Script** (`apps/core/supabase_init.py`)
- Credential verification
- Database connection testing
- Table verification
- Storage bucket setup
- RLS policy configuration

### 4. **Updated Settings** (`carrentals/settings.py`)
- Automatic database selection (SQLite vs PostgreSQL)
- Supabase connection support
- Storage configuration

### 5. **Updated Requirements** (`requirements.txt`)
- Added: `supabase==2.1.1`
- Added: `python-jwt==1.7.1`

## Step-by-Step Setup

### Step 1: Get Supabase Credentials

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project or select existing one
3. Navigate to **Settings → API**
4. Copy the following:
   - **Project URL** → `SUPABASE_URL`
   - **Anon Public Key** → `SUPABASE_KEY`
   - **Service Role Key** (optional) → `SUPABASE_SERVICE_ROLE_KEY`

### Step 2: Update `.env` File

```dotenv
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key

# For PostgreSQL database (instead of SQLite):
DATABASE_URL=postgresql://postgres:password@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres

# Enable Supabase Storage (optional)
USE_SUPABASE_STORAGE=False
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations

```bash
python manage.py migrate
```

This creates all necessary tables in your database (SQLite or PostgreSQL).

### Step 5: Initialize Supabase

```bash
python manage.py shell
```

Then in the Django shell:

```python
from apps.core.supabase_init import initialize_supabase_db
initialize_supabase_db()
```

This will:
- ✅ Verify Supabase credentials
- ✅ Test database connection
- ✅ Check all tables exist
- ✅ Verify storage buckets
- ✅ Show RLS policy setup instructions

### Step 6: Create Storage Buckets (Optional)

If using Supabase Storage:

1. Go to Supabase Dashboard → **Storage**
2. Create these buckets:
   - `car-images` (public)
   - `car-documents` (private)
   - `user-documents` (private)

### Step 7: Set Up RLS Policies

Go to Supabase Dashboard → **SQL Editor** and run:

```sql
-- Enable RLS on all tables
ALTER TABLE accounts_customuser ENABLE ROW LEVEL SECURITY;
ALTER TABLE cars_car ENABLE ROW LEVEL SECURITY;
ALTER TABLE cars_carimage ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings_booking ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_userdocument ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_cardocument ENABLE ROW LEVEL SECURITY;
ALTER TABLE core_auditlog ENABLE ROW LEVEL SECURITY;
```

See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for complete RLS policies.

## Usage Examples

### Using Supabase in Your Code

#### Method 1: Using Convenience Functions

```python
from apps.core.supabase_utils import (
    supabase_select, supabase_get, supabase_insert, 
    supabase_update, supabase_delete
)

# Select all cars
cars = supabase_select('cars_car', limit=50)

# Get single car
car = supabase_get('cars_car', 1)

# Insert new car
result = supabase_insert('cars_car', {
    'brand': 'Toyota',
    'model': 'Innova',
    'owner_id': 1
})

# Update car
result = supabase_update('cars_car', 1, {
    'price_per_day': 2000
})

# Delete car
result = supabase_delete('cars_car', 1)
```

#### Method 2: Using SupabaseDB Class

```python
from apps.core.supabase_utils import db

# Select with filters
result = db.select_where('cars_car', {
    'owner_id': 1,
    'status': 'verified'
})

# Count records
count = db.count('cars_car', {'status': 'verified'})

# Batch insert
data = [
    {'brand': 'Toyota', 'model': 'Innova', 'owner_id': 1},
    {'brand': 'Honda', 'model': 'City', 'owner_id': 2},
]
result = db.insert_many('cars_car', data)
```

#### Method 3: Direct Client Access

```python
from apps.core.supabase_config import get_supabase_client

client = get_supabase_client()

# Custom query
response = client.table('cars_car').select('*').eq('status', 'verified').execute()
```

### File Upload to Supabase Storage

```python
from apps.core.supabase_config import upload_file_to_supabase, delete_file_from_supabase

# Upload file
result = upload_file_to_supabase(
    bucket_name='car-images',
    file_path='cars/car_1/image.jpg',
    file_content=file.read()
)

# Delete file
success = delete_file_from_supabase(
    bucket_name='car-images',
    file_path='cars/car_1/image.jpg'
)
```

## Integration with Django Models

Your Django models automatically use the configured database (SQLite or PostgreSQL). The ORM handles the database operations:

```python
from apps.cars.models import Car

# Django ORM still works normally
car = Car.objects.create(
    brand='Toyota',
    model='Innova',
    owner=user
)

# Can also use Supabase utilities if needed
from apps.core.supabase_utils import supabase_select
all_cars = supabase_select('cars_car')
```

## Configuration Options

### Using SQLite (Local Development)
```dotenv
DATABASE_URL=sqlite:///db.sqlite3
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key
USE_SUPABASE_STORAGE=False
```

### Using Supabase PostgreSQL
```dotenv
DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key
USE_SUPABASE_STORAGE=False
```

### Using Supabase Storage
```dotenv
USE_SUPABASE_STORAGE=True
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key
```

## Troubleshooting

### ❌ "SUPABASE_URL and SUPABASE_KEY must be set"
**Solution:** Check `.env` file has correct credentials from Supabase Dashboard

### ❌ "Database connection failed"
**Solution:** 
- For SQLite: Ensure `DATABASE_URL=sqlite:///db.sqlite3`
- For PostgreSQL: Verify connection string format
- Run `python manage.py migrate` first

### ❌ "Table does not exist"
**Solution:** Run `python manage.py migrate` to create tables

### ❌ "Storage bucket not found"
**Solution:** Manually create buckets in Supabase Dashboard → Storage

## Testing Connection

Run the initialization script to test everything:

```bash
python manage.py shell
from apps.core.supabase_init import initialize_supabase_db
initialize_supabase_db()
```

Expected output:
```
============================================================
🚀 SUPABASE INITIALIZATION
============================================================

Step 1: Checking Supabase credentials...
✅ Supabase credentials found
   URL: https://your-project.supabase.co

Step 2: Checking database connection...
✅ Database connected: PostgreSQL 15...

Step 3: Checking database tables...
✅ Table exists: accounts_customuser
✅ Table exists: cars_car
...
```

## Security Best Practices

1. **Never commit `.env` file** - Keep credentials private
2. **Use Anon Key for frontend** - `SUPABASE_KEY` is safe to use in frontend
3. **Use Service Role Key for admin** - Only on backend, for admin operations
4. **Enable RLS Policies** - Restrict database access at row level
5. **Implement proper authentication** - Use Supabase Auth or your custom auth

## Files Modified/Created

```
✨ Created:
- apps/core/supabase_config.py      (Supabase client initialization)
- apps/core/supabase_utils.py       (Database operation utilities)
- apps/core/supabase_init.py        (Initialization & verification script)

📝 Modified:
- carrentals/settings.py            (Database configuration)
- requirements.txt                  (Added supabase package)
- .env                              (Updated Supabase config comments)

📖 Reference:
- SUPABASE_SETUP.md                 (RLS policies)
- SUPABASE_SCHEMA.md                (Database schema)
- SUPABASE_SQL_SETUP.md             (SQL setup script)
```

## Next Steps

1. ✅ Set Supabase credentials in `.env`
2. ✅ Run `pip install -r requirements.txt`
3. ✅ Run `python manage.py migrate`
4. ✅ Run initialization script
5. ✅ Set up storage buckets (if needed)
6. ✅ Configure RLS policies
7. ✅ Create superuser: `python manage.py createsuperuser`
8. ✅ Start server: `python manage.py runserver`
9. ✅ Access admin: `http://localhost:8000/admin/`

## Support

For more information:
- [Supabase Documentation](https://supabase.com/docs)
- [Django ORM Documentation](https://docs.djangoproject.com/en/4.2/topics/db/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Status:** ✅ Supabase integration is properly configured and ready to use!
