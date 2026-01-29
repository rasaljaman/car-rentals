# Admin Access & Testing Guide

## 🔐 Admin Login Credentials

**Email:** `admin@surarentals.com`  
**Password:** `admin@12345`  
**Status:** Must be created via `python manage.py createsuperuser`

---

## 🔗 Admin Panel Links (Protected - Login Required)

| Feature | URL | Description |
|---------|-----|-------------|
| **Admin Dashboard** | `/admin-panel/dashboard/` | Main admin hub - view stats & manage cars |
| **Add Test Car** | `/admin-panel/add-car/` | Quickly add cars for testing (auto-verified) |
| **View Users** | `/admin-panel/users/` | See all registered users & verification status |
| **Approve Car** | `/admin-panel/approve-car/{car_id}/` | Approve pending car listings |
| **Reject Car** | `/admin-panel/reject-car/{car_id}/` | Reject pending cars |
| **Delete Car** | `/admin-panel/delete-car/{car_id}/` | Remove cars from system |

---

## 🚀 Quick Start (5 Steps)

### Step 1: Create Admin User
```bash
python manage.py createsuperuser
# Email: admin@surarentals.com
# Password: admin@12345
# First Name: Admin
# Last Name: User
# Phone: +1234567890
# Location: System
```

### Step 2: Run Migrations
```bash
python manage.py migrate
```

### Step 3: Start Server
```bash
python manage.py runserver
# Server running at http://localhost:8000
```

### Step 4: Login
```
URL: http://localhost:8000/login/
Email: admin@surarentals.com
Password: admin@12345
```

### Step 5: Access Admin Panel
```
URL: http://localhost:8000/admin-panel/dashboard/
```

---

## 🚗 Sample Test Cars

Quick-add these cars to test browsing & booking:

### Car 1: Toyota Innova (Premium)
```
Make: Toyota
Model: Innova
Year: 2024
Fuel: Petrol
Transmission: Manual
Seats: 5
Location: Mumbai
Price: ₹2000/day
Reg: MH02AB1234
```

### Car 2: Honda City (Budget-Friendly)
```
Make: Honda
Model: City
Year: 2023
Fuel: Petrol
Transmission: Automatic
Seats: 5
Location: Delhi
Price: ₹1200/day
Reg: DL01CD5678
```

### Car 3: Hyundai Creta (Mid-Range)
```
Make: Hyundai
Model: Creta
Year: 2024
Fuel: Diesel
Transmission: Manual
Seats: 5
Location: Bangalore
Price: ₹1800/day
Reg: KA02EF9012
```

### Car 4: Maruti Swift (Economy)
```
Make: Maruti
Model: Swift
Year: 2023
Fuel: Petrol
Transmission: Manual
Seats: 5
Location: Pune
Price: ₹800/day
Reg: MH04GH3456
```

---

## 📊 Admin Dashboard Features

### Statistics Cards
- **Total Cars**: Count of all cars in system
- **Verified Cars**: Cars ready for booking
- **Pending Cars**: Awaiting approval
- **Total Users**: All registered users

### Cars Management Table
Shows all cars with:
- Car details (Make, Model, Year, Fuel)
- Owner name
- Location
- Daily price
- Status badge (Verified/Pending/Rejected)
- Action buttons (Approve/Reject/Delete)

### User Management
View all users with:
- Full name
- Email & Phone
- Location
- Verification status ✓/⏳
- User role (User/Admin/Superuser)
- Join date

---

## ✅ Testing Workflow

### 1. **As Admin**
```
1. Go to: http://localhost:8000/login/
2. Login: admin@surarentals.com / admin@12345
3. Click: Dashboard (or go to /admin-panel/dashboard/)
4. Add test cars via "➕ Add Test Car" button
```

### 2. **Browse Cars (as Admin)**
```
1. Logged in as admin
2. Go to: http://localhost:8000/cars/browse/
3. See all verified cars you added
4. Click on car detail to view full info
```

### 3. **Create Test User**
```
1. Go to: http://localhost:8000/signup/step1/
2. Fill signup form
3. Complete OTP verification
4. Verify phone number
5. Create account
```

### 4. **Book a Car (as Regular User)**
```
1. Login with test user account
2. Go to: /cars/browse/
3. Click on a car
4. Click "Request Booking"
5. Select dates & submit
```

### 5. **Approve Booking (as Admin)**
```
1. Login as admin again
2. Go to: /admin/ (Django admin panel)
3. Find booking in Bookings table
4. Change status to "confirmed"
5. Save
```

---

## 🔒 Security Features

✅ **Login Required** - Can't access admin panel without authentication  
✅ **Admin Only** - Checked via `is_staff=True` flag  
✅ **CSRF Protection** - All forms have CSRF tokens  
✅ **URL Protection** - URLs start with `/admin-panel/` to distinguish from public routes  
✅ **Email/Password** - Uses Django's built-in authentication  

---

## 🎯 Key Endpoints Summary

| Method | Endpoint | Purpose | Access |
|--------|----------|---------|--------|
| GET | `/login/` | Admin login | Public |
| GET | `/admin-panel/dashboard/` | View stats & cars | Admin only |
| GET/POST | `/admin-panel/add-car/` | Add test cars | Admin only |
| POST | `/admin-panel/approve-car/{id}/` | Approve pending cars | Admin only |
| POST | `/admin-panel/reject-car/{id}/` | Reject cars | Admin only |
| POST | `/admin-panel/delete-car/{id}/` | Delete cars | Admin only |
| GET | `/admin-panel/users/` | Manage users | Admin only |
| GET | `/cars/browse/` | Browse cars | Authenticated users |

---

## 📱 Mobile Testing

Admin panel is responsive and works on:
- ✅ Desktop (1920px+)
- ✅ Tablet (768px-1024px)
- ✅ Mobile (320px+)

---

## 🔧 Troubleshooting

### "Unauthorized access" message?
- Make sure you're logged in as admin
- Check if user has `is_staff=True`
- Verify `is_superuser=True` or `is_staff=True` is set

### Can't login?
- Check email/password are correct
- Make sure superuser was created: `python manage.py createsuperuser`
- Check user exists in database: `python manage.py shell`
  ```python
  from apps.accounts.models import CustomUser
  admin = CustomUser.objects.filter(email='admin@surarentals.com').first()
  print(admin)  # Should show admin user
  ```

### Add car button not working?
- Check if logged in as admin (`is_staff=True`)
- Check if car form has all required fields
- Check Django logs for errors

### Cars not showing in browse?
- Make sure cars have `status='verified'`
- Check `is_available=True`
- Try adding cars via admin panel (auto-verified)

---

## 📞 Next Steps

1. ✅ Create admin user
2. ✅ Add 4 test cars
3. ✅ Create test user accounts
4. ✅ Book cars
5. 🚀 Ready for Supabase integration!

