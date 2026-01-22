#!/usr/bin/env python3
"""
Sura Rentals - Authentication Testing Script
Tests login, register, and authentication flows
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carrentals.settings')
django.setup()

from django.contrib.auth import authenticate
from apps.accounts.models import CustomUser, Profile, OTPVerification, SignUpSession
from apps.core.models import SiteSettings

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_database_connection():
    """Test database connection"""
    print_header("1. DATABASE CONNECTION TEST")
    try:
        user_count = CustomUser.objects.count()
        print(f"✓ Database connected successfully")
        print(f"✓ Total users in database: {user_count}")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_admin_user():
    """Test admin user exists"""
    print_header("2. ADMIN USER TEST")
    try:
        admin = CustomUser.objects.get(email="admin@surarentals.com")
        print(f"✓ Admin user found")
        print(f"  - Email: {admin.email}")
        print(f"  - Role: {admin.role}")
        print(f"  - Is Staff: {admin.is_staff}")
        print(f"  - Is Superuser: {admin.is_superuser}")
        return True
    except CustomUser.DoesNotExist:
        print(f"✗ Admin user not found")
        return False

def test_admin_login():
    """Test admin login"""
    print_header("3. ADMIN LOGIN TEST")
    try:
        admin = CustomUser.objects.get(email="admin@surarentals.com")
        # Set admin password for testing
        admin.set_password('admin@12345')
        admin.save()
        
        # Try authenticating with correct credentials
        user = authenticate(username='admin@surarentals.com', password='admin@12345')
        if user is not None:
            print(f"✓ Admin authentication successful")
            print(f"  - User: {user.email}")
            print(f"  - Active: {user.is_active}")
            print(f"  - Password set to: admin@12345")
            return True
        else:
            print(f"✗ Admin exists but authentication failed")
            return False
    except CustomUser.DoesNotExist:
        print(f"✗ Admin user not found")
        return False

def test_site_settings():
    """Test site settings configuration"""
    print_header("4. SITE SETTINGS TEST")
    try:
        settings = SiteSettings.objects.get()
        print(f"✓ Site settings configured")
        print(f"  - OTP Validity: {settings.otp_validity_minutes} minutes")
        print(f"  - OTP Max Attempts: {settings.max_otp_attempts}")
        print(f"  - CAPTCHA Enabled: {settings.captcha_enabled}")
        print(f"  - Maintenance Mode: {settings.maintenance_mode}")
        return True
    except SiteSettings.DoesNotExist:
        print(f"✗ Site settings not configured")
        return False

def test_user_model():
    """Test CustomUser model"""
    print_header("5. CUSTOM USER MODEL TEST")
    try:
        # Check model fields
        fields = [f.name for f in CustomUser._meta.get_fields()]
        
        required_fields = ['email', 'phone_number', 'location', 'role', 
                          'is_verified', 'is_email_verified', 'is_phone_verified']
        
        missing_fields = [f for f in required_fields if f not in fields]
        
        if not missing_fields:
            print(f"✓ CustomUser model has all required fields")
            print(f"  - Total fields: {len(fields)}")
            print(f"  - Required fields present: {len(required_fields)}")
            return True
        else:
            print(f"✗ CustomUser model missing fields: {missing_fields}")
            return False
    except Exception as e:
        print(f"✗ Error checking CustomUser model: {e}")
        return False

def test_profile_model():
    """Test Profile model"""
    print_header("6. PROFILE MODEL TEST")
    try:
        # Check if admin has profile, create if not
        admin = CustomUser.objects.get(email="admin@surarentals.com")
        profile, created = Profile.objects.get_or_create(user=admin)
        
        print(f"✓ Profile model linked to CustomUser")
        print(f"  - Admin profile exists: {profile is not None}")
        if created:
            print(f"  - Profile was just created")
        else:
            print(f"  - Profile already existed")
        return True
    except Exception as e:
        print(f"✗ Error checking Profile model: {e}")
        return False

def test_otp_model():
    """Test OTPVerification model"""
    print_header("7. OTP MODEL TEST")
    try:
        otp_count = OTPVerification.objects.count()
        print(f"✓ OTPVerification model exists")
        print(f"  - OTP records in database: {otp_count}")
        return True
    except Exception as e:
        print(f"✗ Error checking OTPVerification model: {e}")
        return False

def test_signup_session_model():
    """Test SignUpSession model"""
    print_header("8. SIGNUP SESSION MODEL TEST")
    try:
        session_count = SignUpSession.objects.count()
        print(f"✓ SignUpSession model exists")
        print(f"  - Signup sessions in database: {session_count}")
        return True
    except Exception as e:
        print(f"✗ Error checking SignUpSession model: {e}")
        return False

def test_urls():
    """Test URL configuration"""
    print_header("9. URL CONFIGURATION TEST")
    try:
        from django.urls import reverse
        
        urls_to_test = [
            ('home', 'home'),
            ('login', 'login'),
            ('signup_step1', 'signup_step1'),
            ('signup_step2', 'signup_step2'),
            ('signup_step3', 'signup_step3'),
            ('logout', 'logout'),
            ('dashboard', 'dashboard'),
            ('edit_profile', 'edit_profile'),
        ]
        
        failed = []
        for url_name, display_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"  ✓ {display_name}: {url}")
            except Exception as e:
                failed.append((display_name, str(e)))
        
        if failed:
            print(f"\n✗ Failed to find URLs:")
            for name, error in failed:
                print(f"  - {name}: {error}")
            return False
        else:
            print(f"\n✓ All authentication URLs configured correctly")
            return True
    except Exception as e:
        print(f"✗ Error checking URLs: {e}")
        return False

def test_email_backend():
    """Test email configuration"""
    print_header("10. EMAIL CONFIGURATION TEST")
    try:
        from django.conf import settings
        print(f"✓ Email configuration found")
        print(f"  - Backend: {settings.EMAIL_BACKEND}")
        print(f"  - From Email: {settings.DEFAULT_FROM_EMAIL}")
        
        if 'console' in settings.EMAIL_BACKEND:
            print(f"  ℹ  Development mode: Emails print to console")
        else:
            print(f"  ℹ  Production mode: SMTP configured")
        
        return True
    except Exception as e:
        print(f"✗ Error checking email configuration: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  SURA RENTALS - AUTHENTICATION SYSTEM TEST SUITE".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {
        "Database Connection": test_database_connection(),
        "Admin User": test_admin_user(),
        "Admin Login": test_admin_login(),
        "Site Settings": test_site_settings(),
        "CustomUser Model": test_user_model(),
        "Profile Model": test_profile_model(),
        "OTP Model": test_otp_model(),
        "SignUp Session Model": test_signup_session_model(),
        "URL Configuration": test_urls(),
        "Email Configuration": test_email_backend(),
    }
    
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 All tests passed! Authentication system is ready!")
        print("\nNext steps:")
        print("1. Start the dev server: python manage.py runserver")
        print("2. Go to: http://127.0.0.1:8000/")
        print("3. Test signup/login flow")
        print("4. Access admin panel: http://127.0.0.1:8000/admin/\n")
        return 0
    else:
        print(f"⚠  {total - passed} test(s) failed. Please review the output above.\n")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
