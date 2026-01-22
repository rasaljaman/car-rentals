#!/usr/bin/env python
"""
Test script to verify database and authentication setup
Run with: python test_auth_setup.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carrentals.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.accounts.models import CustomUser, Profile
from django.db import connection

def test_database():
    """Test database connection."""
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ Database connection: SUCCESS")
        return True
    except Exception as e:
        print(f"✗ Database connection: FAILED - {e}")
        return False

def test_user_model():
    """Test CustomUser model."""
    print("\n" + "=" * 60)
    print("USER MODEL TEST")
    print("=" * 60)
    
    try:
        # Check admin user exists
        admin_user = CustomUser.objects.filter(email='admin@surarentals.com').first()
        if admin_user:
            print(f"✓ Admin user found: {admin_user.email}")
            print(f"  - Name: {admin_user.first_name} {admin_user.last_name}")
            print(f"  - Role: {admin_user.role}")
            print(f"  - Verified: {admin_user.is_verified}")
            return True
        else:
            print("✗ Admin user not found")
            return False
    except Exception as e:
        print(f"✗ User model test FAILED: {e}")
        return False

def test_create_test_user():
    """Create a test user for authentication."""
    print("\n" + "=" * 60)
    print("CREATE TEST USER")
    print("=" * 60)
    
    try:
        # Delete if exists
        CustomUser.objects.filter(email='testuser@example.com').delete()
        
        # Create new user
        user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123!',
            first_name='Test',
            last_name='User',
            phone_number='+1234567890',
            location='New York'
        )
        
        # Create profile
        profile = Profile.objects.create(user=user)
        
        print(f"✓ Test user created successfully")
        print(f"  - Email: {user.email}")
        print(f"  - Name: {user.first_name} {user.last_name}")
        print(f"  - Phone: {user.phone_number}")
        print(f"  - Location: {user.location}")
        print(f"\n  Test Credentials:")
        print(f"  Email: testuser@example.com")
        print(f"  Password: TestPassword123!")
        
        return True
    except Exception as e:
        print(f"✗ Create test user FAILED: {e}")
        return False

def test_authentication():
    """Test authentication system."""
    print("\n" + "=" * 60)
    print("AUTHENTICATION TEST")
    print("=" * 60)
    
    try:
        from django.contrib.auth import authenticate
        
        # Test with admin user
        user = authenticate(username='admin@surarentals.com', password='admin123')
        if user:
            print("✓ Admin authentication: SUCCESS")
        else:
            print("⚠ Admin authentication: Failed (password might be different)")
        
        # Test with test user
        user = authenticate(username='testuser@example.com', password='TestPassword123!')
        if user:
            print("✓ Test user authentication: SUCCESS")
            print(f"  - Authenticated as: {user.email}")
            return True
        else:
            print("✗ Test user authentication: FAILED")
            return False
    except Exception as e:
        print(f"✗ Authentication test FAILED: {e}")
        return False

def print_credentials():
    """Print login credentials."""
    print("\n" + "=" * 60)
    print("📝 LOGIN CREDENTIALS")
    print("=" * 60)
    print("\nAdmin Account (Created by init_data):")
    print("  Email: admin@surarentals.com")
    print("  Password: admin123 (change this in production!)")
    print("\nTest Account (Created by this script):")
    print("  Email: testuser@example.com")
    print("  Password: TestPassword123!")
    
def print_urls():
    """Print important URLs."""
    print("\n" + "=" * 60)
    print("🔗 IMPORTANT URLs")
    print("=" * 60)
    print("\nLocal Development:")
    print("  Home: http://127.0.0.1:8000/")
    print("  Login: http://127.0.0.1:8000/login/")
    print("  Sign Up (Step 1): http://127.0.0.1:8000/signup/step1/")
    print("  Admin Panel: http://127.0.0.1:8000/admin/")
    print("  Dashboard: http://127.0.0.1:8000/dashboard/ (after login)")
    print("\nAPI Endpoints (when configured):")
    print("  API Root: http://127.0.0.1:8000/api/")
    print("  Users: http://127.0.0.1:8000/api/users/")
    print("  Cars: http://127.0.0.1:8000/api/cars/")
    print("  Bookings: http://127.0.0.1:8000/api/bookings/")

if __name__ == '__main__':
    print("\n")
    print(" █████████████████████████████████████████████████████████ ")
    print(" ███  SURA RENTALS - AUTHENTICATION SETUP TEST  ███ ")
    print(" █████████████████████████████████████████████████████████ ")
    
    # Run tests
    db_ok = test_database()
    user_ok = test_user_model()
    create_ok = test_create_test_user()
    auth_ok = test_authentication()
    
    # Print credentials and URLs
    print_credentials()
    print_urls()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    if db_ok and user_ok and auth_ok:
        print("✓ All tests passed! Authentication is ready.")
        print("\n✅ Your Sura Rentals platform is fully operational!")
        print("\nNext Steps:")
        print("1. Start the server: python manage.py runserver")
        print("2. Visit http://127.0.0.1:8000/ in your browser")
        print("3. Try logging in with the test credentials")
        print("4. Create car listings and test the booking flow")
    else:
        print("⚠ Some tests failed. Check the output above.")
    
    print("\n")
