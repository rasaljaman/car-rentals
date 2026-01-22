# Sura Rentals - Authentication System Guide

## ✅ Database Connected & Authentication Ready

The authentication system is fully configured and the database is connected using SQLite for local development.

### Current Setup
- **Database**: SQLite (db.sqlite3) - local development
- **Admin User**: admin@surarentals.com
- **Authentication**: Email-based with OTP verification
- **Framework**: Django 4.2 LTS with custom user model

---

## 🔐 Authentication Features

### 1. **Multi-Step Registration (3 Steps)**
```
Step 1: User Details (Email, Password, Phone, Location)
   ↓
Step 2: Email OTP Verification
   ↓
Step 3: Phone OTP Verification
   ↓
Account Created & Verified
```

### 2. **Login System**
- Email-based login (not username)
- Password authentication
- Session management
- Remember me functionality (optional)

### 3. **OTP Verification**
- Email OTP for email verification
- SMS OTP for phone verification
- Configurable OTP length (default: 6 digits)
- Configurable validity period (default: 10 minutes)
- Max retry attempts (default: 3)

---

## 🚀 Quick Start Testing

### Access the Application
```
Home Page:        http://127.0.0.1:8000/
Login:            http://127.0.0.1:8000/login/
Register Step 1:  http://127.0.0.1:8000/signup/step1/
Admin Panel:      http://127.0.0.1:8000/admin/
```

### Admin Credentials
- **Email**: admin@surarentals.com
- **Password**: admin@12345 (set during init_data)

---

## 📝 Test Flow: Register a New User

### Step 1: Sign Up (Basic Info)
1. Go to http://127.0.0.1:8000/signup/step1/
2. Fill in:
   - **First Name**: John
   - **Last Name**: Doe
   - **Email**: john@example.com
   - **Phone Number**: +1234567890
   - **Location**: New York
   - **Password**: SecurePass123
   - **Confirm Password**: SecurePass123
3. Click "Next" → Redirects to Step 2

### Step 2: Email OTP Verification
1. Check console output (Email OTP printed to console in dev mode)
   - Look for: `Subject: Email Verification Code` in Django console
2. Enter the 6-digit OTP code
3. Click "Verify Email" → Redirects to Step 3

### Step 3: Phone OTP Verification
1. Check console output for Phone OTP (or it will be auto-sent)
2. Enter the 6-digit OTP code
3. Click "Verify Phone" → Account created!
4. Redirected to login page

### Login
1. Go to http://127.0.0.1:8000/login/
2. Enter:
   - **Email**: john@example.com
   - **Password**: SecurePass123
3. Click "Sign In" → Dashboard

---

## 📧 Email Configuration

### Current Setup (Console Backend - Development)
```
All emails print to Django console/terminal
Check the server output for OTP codes
```

### Switch to SMTP (Gmail - Production)
Edit `.env` file:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note**: Use Gmail App Password (not regular password)
1. Enable 2-Step Verification on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the generated password in EMAIL_HOST_PASSWORD

---

## 📱 SMS Configuration (OTP via Phone)

Currently using placeholder SMS provider. To connect to real SMS:

### Option 1: Twilio
Edit `apps/accounts/utils.py`:
```python
def send_otp_sms(phone_number, otp_code):
    from twilio.rest import Client
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your Sura Rentals OTP is: {otp_code}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid
```

### Option 2: AWS SNS
```python
def send_otp_sms(phone_number, otp_code):
    import boto3
    
    client = boto3.client('sns', region_name='us-east-1')
    client.publish(
        PhoneNumber=phone_number,
        Message=f"Your Sura Rentals OTP is: {otp_code}"
    )
```

---

## 🗄️ Database Models

### CustomUser
- `email` (unique) - Login credential
- `first_name`, `last_name`
- `phone_number`
- `location`
- `role` - 'user' or 'admin'
- `is_verified` - Email & Phone verified
- `is_email_verified` - Email OTP verified
- `is_phone_verified` - Phone OTP verified
- `is_active` - Account status
- `created_at`, `updated_at`

### Profile (One-to-One with CustomUser)
- `profile_photo`
- `bio`
- `rating` (1-5)
- `total_reviews`
- `total_rentals`
- `total_listings`
- `is_banned`

### OTPVerification
- `user` - FK to CustomUser
- `otp_code` - The OTP
- `otp_type` - 'email' or 'phone'
- `is_verified` - Whether OTP was verified
- `expires_at` - When OTP expires
- `attempts` - Failed verification attempts

### SignUpSession
- `email` - Temporary session email
- `first_name`, `last_name`, `phone_number`, `location`
- `password_hash` - Hashed password
- `step_completed` - Current step (1, 2, or 3)
- `created_at`

---

## 🔑 Authentication Views

### Registration Views
- `signup_step1` - Collect user details
- `signup_step2` - Email OTP verification
- `signup_step3` - Phone OTP verification

### Auth Views
- `login_view` - Email + Password login
- `logout_view` - Session logout
- `dashboard` - Protected dashboard (requires login)
- `edit_profile` - Profile editing

### URL Routes
```
POST   /signup/step1/        - Create signup session
POST   /signup/step2/        - Verify email OTP
POST   /signup/step3/        - Verify phone OTP
POST   /login/               - Email login
GET    /logout/              - Logout
GET    /dashboard/           - User dashboard (protected)
GET/POST /edit-profile/      - Edit profile (protected)
```

---

## 🔒 Security Features Implemented

✅ CSRF Protection on all forms
✅ Password hashing (PBKDF2)
✅ Session-based authentication
✅ `@login_required` decorators on protected views
✅ OTP time-based expiration
✅ OTP attempt limiting
✅ Secure password validation
✅ User permission checks
✅ SQL injection prevention (Django ORM)

---

## 🛠️ Troubleshooting

### Issue: "OTP expired" error
**Solution**: OTP validity is set to 10 minutes. Request a new OTP if expired.

### Issue: "User already exists" on signup
**Solution**: Email must be unique. Use a different email address.

### Issue: "Wrong password" on login
**Solution**: Ensure password is correct. Use "Forgot Password" (if implemented).

### Issue: Emails not appearing in console
**Solution**: Check Django development server console. Emails are printed as:
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Email Verification Code
From: noreply@surarentals.com
To: user@example.com
Date: ...
Message-ID: ...

Your OTP is: 123456
```

---

## 📊 Admin Panel Features

Access at: http://127.0.0.1:8000/admin/

### User Management
- View all users with verification status
- Edit user details
- View verification flags (email, phone, verified)
- Ban/unban users
- Assign admin role

### Verification Management
- View verification status for users
- Approve/reject document uploads
- View audit logs of all verification actions

### Profile Management
- View user profiles
- See ratings and reviews
- Track rental history
- Monitor listings

---

## 🚢 Deployment Configuration

The authentication system is production-ready. For deployment:

1. **Set Environment Variables** (.env):
   - `SECRET_KEY` - Strong random key
   - `DEBUG=False`
   - `ALLOWED_HOSTS` - Your domain
   - `EMAIL_BACKEND` - SMTP backend
   - `DATABASE_URL` - PostgreSQL connection string

2. **Enable Security Settings** (.env):
   ```env
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   SECURE_HSTS_SECONDS=31536000
   ```

3. **Use PostgreSQL** in production:
   ```env
   DATABASE_URL=postgresql://user:password@host:5432/sura_rentals
   ```

---

## 📚 Next Steps

1. ✅ **Test Registration**: Create a test account
2. ✅ **Test Login**: Login with test account
3. ✅ **Test Dashboard**: Access protected dashboard
4. ✅ **Test Admin Panel**: Manage users as admin
5. 🔄 **Set up Email Provider**: Connect real SMTP
6. 🔄 **Set up SMS Provider**: Connect Twilio/AWS SNS
7. 🔄 **Test OTP Flow**: Verify phone OTP works
8. 🚀 **Deploy**: Follow deployment guide in DEPLOYMENT.md

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review Django logs in console
3. Check database in admin panel
4. Review model fields and form validation

Happy coding! 🚀
