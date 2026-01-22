# Quick Start - Authentication Testing

## ✅ System Status
✓ Database connected (SQLite)
✓ Authentication system configured
✓ All 10 system tests passing
✓ Admin user ready (admin@surarentals.com)
✓ OTP system configured

---

## 🚀 Step 1: Verify Everything Works

Run the authentication test suite:
```bash
python3 test_auth_system.py
```

Expected output: **10/10 tests passed** ✅

---

## 🏃 Step 2: Start the Development Server

```bash
python3 manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

---

## 📋 Step 3: Test Authentication Flow

### A. Login as Admin
1. Go to: http://127.0.0.1:8000/login/
2. Enter:
   - **Email**: admin@surarentals.com
   - **Password**: admin@12345
3. Click "Sign In"
4. You should see the dashboard

### B. Create a New User (Register)
1. Go to: http://127.0.0.1:8000/signup/step1/
2. Fill in the form:
   - **First Name**: Test
   - **Last Name**: User
   - **Email**: testuser@example.com
   - **Phone**: +1234567890
   - **Location**: New York
   - **Password**: TestPass123
3. Click "Next"

### C. Verify Email (Step 2)
1. Check the Django server console for email output
2. Look for the line: **Subject: Email Verification Code**
3. Find the 6-digit OTP code in the console
4. Enter it in the form and click "Verify Email"

### D. Verify Phone (Step 3)
1. Check the Django server console again
2. Look for the OTP code
3. Enter it and click "Verify Phone"
4. Account created! You'll be redirected to login

### E. Login with New Account
1. Go to: http://127.0.0.1:8000/login/
2. Enter your credentials:
   - **Email**: testuser@example.com
   - **Password**: TestPass123
3. Click "Sign In"

---

## 🛠️ Admin Panel

Access at: http://127.0.0.1:8000/admin/

**Credentials:**
- Email: admin@surarentals.com
- Password: admin@12345

**What you can do:**
- Manage users and their verification status
- View user profiles and ratings
- Manage OTP records
- View signup sessions
- Configure site settings

---

## 📧 Email Configuration

### Current Setup (Development)
Emails are printed to the Django console. When you request an OTP, you'll see:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Email Verification Code
From: noreply@surarentals.com
To: your-email@example.com
Date: Wed, 22 Jan 2026 12:34:56 +0000
Message-ID: <...>

Your OTP is: 123456
```

Copy the 6-digit code and paste it in the form.

### For Production (Gmail)
Edit `.env` file:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

[Get Gmail App Password](https://myaccount.google.com/apppasswords)

---

## 🔐 Security Notes

✓ All passwords are hashed (PBKDF2)
✓ OTP codes expire after 10 minutes
✓ Maximum 5 failed OTP attempts
✓ Session-based authentication
✓ CSRF protection on all forms
✓ Email-based login (no usernames)

---

## 📝 Test Cases

| Feature | URL | Expected Result |
|---------|-----|-----------------|
| Home | `/` | Hero section with car search |
| Login | `/login/` | Login form with email/password |
| Sign Up Step 1 | `/signup/step1/` | User details form |
| Sign Up Step 2 | `/signup/step2/` | Email OTP verification |
| Sign Up Step 3 | `/signup/step3/` | Phone OTP verification |
| Dashboard | `/dashboard/` | User dashboard (requires login) |
| Admin Panel | `/admin/` | Django admin with customizations |
| Browse Cars | `/cars/browse/` | Car listing with filters |
| User Profile | `/profile/edit/` | Profile editing (requires login) |

---

## 🐛 Troubleshooting

### Issue: "Invalid OTP"
- **Cause**: OTP code expired or wrong
- **Solution**: Request a new OTP (OTP valid for 10 minutes)

### Issue: "User already exists"
- **Cause**: Email is already registered
- **Solution**: Use a different email or login with existing account

### Issue: "Page not found"
- **Cause**: URL doesn't exist
- **Solution**: Check URL spelling or access from home page navigation

### Issue: Email not appearing in console
- **Cause**: Email backend not configured correctly
- **Solution**: Check Django console output; emails print there in development

### Issue: "Too many attempts"
- **Cause**: Failed OTP verification 5+ times
- **Solution**: Request a new OTP or create a new signup session

---

## ✨ Next Steps

1. ✅ Test login/register flow
2. ✅ Test admin panel
3. 🔄 Connect real email provider (Gmail SMTP)
4. 🔄 Connect SMS provider (Twilio/AWS SNS)
5. 🔄 Test car listing creation
6. 🔄 Test booking workflow
7. 🚀 Deploy to production

---

## 📞 Getting Help

1. Check the AUTHENTICATION.md guide
2. Review the test output: `python3 test_auth_system.py`
3. Check Django logs in console
4. Visit the admin panel to verify data

**Database Status**: ✅ Connected
**Authentication**: ✅ Ready
**Tests**: ✅ Passing
**Server**: ✅ Running

Happy testing! 🎉
