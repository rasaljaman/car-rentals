"""
Supabase initialization script.
Run this after setting up Supabase credentials in .env

Usage:
    python manage.py shell
    from apps.core.supabase_init import initialize_supabase_db
    initialize_supabase_db()
"""

import os
from django.db import connection
from apps.core.supabase_config import get_supabase_client, test_supabase_connection
import sys


def check_supabase_credentials():
    """Check if Supabase credentials are properly set."""
    from decouple import config
    
    supabase_url = config('SUPABASE_URL', default=None)
    supabase_key = config('SUPABASE_KEY', default=None)
    
    if not supabase_url or not supabase_key:
        print("❌ SUPABASE_URL and SUPABASE_KEY not set in .env")
        print("\nTo get these credentials:")
        print("1. Go to Supabase Dashboard → https://supabase.com/dashboard")
        print("2. Create a new project or select existing one")
        print("3. Go to Settings → API")
        print("4. Copy the following to .env:")
        print("   SUPABASE_URL=https://your-project.supabase.co")
        print("   SUPABASE_KEY=your-anon-key")
        return False
    
    print("✅ Supabase credentials found")
    print(f"   URL: {supabase_url}")
    return True


def check_database_connection():
    """Check if Django can connect to Supabase database."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Database connected: {version[0][:50]}...")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("\nSetup Supabase PostgreSQL connection in .env:")
        print("   DATABASE_URL=postgresql://user:password@host:port/database")
        return False


def verify_tables():
    """Check if required tables exist in Supabase."""
    try:
        client = get_supabase_client()
        
        required_tables = [
            'accounts_customuser',
            'cars_car',
            'cars_carimage',
            'bookings_booking',
            'verification_userdocument',
            'verification_cardocument',
            'core_auditlog',
        ]
        
        missing_tables = []
        
        for table in required_tables:
            try:
                response = client.table(table).select('*').limit(1).execute()
                print(f"✅ Table exists: {table}")
            except Exception as e:
                if 'does not exist' in str(e).lower() or 'relation' in str(e).lower():
                    missing_tables.append(table)
                    print(f"⚠️  Table missing: {table}")
        
        if missing_tables:
            print(f"\n❌ Missing {len(missing_tables)} tables. Run migrations:")
            print("   python manage.py migrate")
            return False
        
        print(f"\n✅ All {len(required_tables)} tables exist")
        return True
        
    except Exception as e:
        print(f"❌ Error checking tables: {str(e)}")
        return False


def create_storage_buckets():
    """Create required storage buckets in Supabase."""
    try:
        client = get_supabase_client()
        storage = client.storage
        
        buckets_to_create = [
            {
                'name': 'car-images',
                'public': True,
                'description': 'Car listing images'
            },
            {
                'name': 'car-documents',
                'public': False,
                'description': 'Car documents (RC, Insurance)'
            },
            {
                'name': 'user-documents',
                'public': False,
                'description': 'User verification documents'
            },
        ]
        
        print("\nChecking storage buckets...")
        
        for bucket in buckets_to_create:
            try:
                # Try to get bucket info
                buckets = storage.list_buckets()
                bucket_names = [b.name for b in buckets]
                
                if bucket['name'] in bucket_names:
                    print(f"✅ Bucket exists: {bucket['name']}")
                else:
                    print(f"⚠️  Bucket missing: {bucket['name']}")
                    print(f"   Create manually in Supabase Dashboard → Storage")
            except Exception as e:
                print(f"⚠️  Could not check bucket {bucket['name']}: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking storage buckets: {str(e)}")
        return False


def setup_rls_policies():
    """Print instructions for setting up RLS policies."""
    print("\n" + "="*60)
    print("ENABLE ROW LEVEL SECURITY (RLS)")
    print("="*60)
    print("""
1. Go to Supabase Dashboard → SQL Editor
2. Create a new query and run:

-- Enable RLS on all tables
ALTER TABLE accounts_customuser ENABLE ROW LEVEL SECURITY;
ALTER TABLE cars_car ENABLE ROW LEVEL SECURITY;
ALTER TABLE cars_carimage ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings_booking ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_userdocument ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_cardocument ENABLE ROW LEVEL SECURITY;
ALTER TABLE core_auditlog ENABLE ROW LEVEL SECURITY;

3. Setup policies (see SUPABASE_SETUP.md for full policies)
4. Create storage buckets with appropriate policies
""")


def initialize_supabase_db():
    """
    Complete Supabase initialization.
    Checks credentials, connections, tables, and storage.
    """
    print("\n" + "="*60)
    print("🚀 SUPABASE INITIALIZATION")
    print("="*60 + "\n")
    
    # Step 1: Check credentials
    print("Step 1: Checking Supabase credentials...")
    if not check_supabase_credentials():
        return False
    
    # Step 2: Check database connection
    print("\nStep 2: Checking database connection...")
    db_connected = check_database_connection()
    
    if not db_connected:
        print("\n📝 To enable Supabase PostgreSQL:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Select your project → Settings → Database")
        print("3. Copy connection string to DATABASE_URL in .env")
        print("4. Run: python manage.py migrate")
    
    # Step 3: Check tables
    print("\nStep 3: Checking database tables...")
    tables_exist = verify_tables()
    
    if not tables_exist:
        return False
    
    # Step 4: Check storage
    print("\nStep 4: Checking storage buckets...")
    create_storage_buckets()
    
    # Step 5: RLS policies
    setup_rls_policies()
    
    print("\n" + "="*60)
    print("✅ INITIALIZATION COMPLETE")
    print("="*60)
    print("""
Next steps:
1. Update storage bucket policies (Supabase Dashboard → Storage)
2. Set up RLS policies (see above)
3. Create superuser: python manage.py createsuperuser
4. Run server: python manage.py runserver
5. Visit: http://localhost:8000/admin/
""")
    
    return True


if __name__ == '__main__':
    initialize_supabase_db()
