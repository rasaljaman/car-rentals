# Admin Panel Setup Guide

## Access Admin Panel

### 🔗 Admin Links
- **Admin Dashboard**: `/admin-panel/dashboard/`
- **Add Test Car**: `/admin-panel/add-car/`
- **View Users**: `/admin-panel/users/`

---

## ✅ Quick Setup Steps

### 1. **Run Migrations**
```bash
python manage.py migrate
```

### 2. **Create Admin User** (if not already created)
```bash
python manage.py createsuperuser
```

**Admin Credentials (Example):**
- Email: `admin@surarentals.com`
- Password: `admin@12345`
- First Name: Admin
- Last Name: User
- Phone: +1234567890
- Location: System

### 3. **Start Server**
```bash
python manage.py runserver
```

### 4. **Access Admin Panel**
1. Go to: `http://localhost:8000/login/`
2. Login with admin email & password
3. Go to: `http://localhost:8000/admin-panel/dashboard/`

---

## 🚗 Add Test Cars

### Option 1: Via Admin Panel (Recommended)
1. Visit: `http://localhost:8000/admin-panel/dashboard/`
2. Click "➕ Add Test Car"
3. Fill in car details
4. Submit (auto-verified)

### Option 2: Sample Test Cars (Quick Setup)
Use these details in the Add Car form:

**Car 1 - Toyota Innova:**
- Make: Toyota
- Model: Innova
- Year: 2024
- Fuel Type: Petrol
- Transmission: Manual
- Seats: 5
- Location: Mumbai
- Price: 2000
- Registration: MH02AB1234

**Car 2 - Honda City:**
- Make: Honda
- Model: City
- Year: 2023
- Fuel Type: Petrol
- Transmission: Automatic
- Seats: 5
- Location: Delhi
- Price: 1200
- Registration: DL01CD5678

**Car 3 - Hyundai Creta:**
- Make: Hyundai
- Model: Creta
- Year: 2024
- Fuel Type: Diesel
- Transmission: Manual
- Seats: 5
- Location: Bangalore
- Price: 1800
- Registration: KA02EF9012

**Car 4 - Maruti Swift:**
- Make: Maruti
- Model: Swift
- Year: 2023
- Fuel Type: Petrol
- Transmission: Manual
- Seats: 5
- Location: Pune
- Price: 800
- Registration: MH04GH3456

---

## 👥 Admin Features

### Dashboard
- View total cars, users, pending/verified cars
- See all cars in a table
- Approve/Reject/Delete cars

### Add Test Car
- Quick add cars directly to database
- Auto-verified (no need for approval)
- Can upload images
- Pre-filled with sensible defaults

### View Users
- See all registered users
- Check verification status
- View user roles (Admin, User)
- See join date and location

---

## 🔐 Security Notes

- Only authenticated admin users can access the panel
- `is_staff=True` users can access all admin functions
- Uses Django's `@login_required` decorator
- CSRF protection enabled on all forms

---

## 🧪 Testing Flow

1. **Login as Admin**
   ```
   Email: admin@surarentals.com
   Password: admin@12345
   ```

2. **Add 4 Test Cars**
   - Use the sample car details above
   - Each car is auto-verified

3. **View Dashboard**
   - Stats show total cars, users, pending
   - All cars appear in the table

4. **Browse as Regular User**
   - Login with test user account
   - Go to `/cars/browse/`
   - All verified cars are visible

5. **Create Bookings**
   - Regular users can book verified cars
   - Admins can approve/reject bookings

---

## 📝 Supabase Integration

When you migrate to Supabase:

1. Update `DATABASE_URL` in `.env`
2. Run migrations: `python manage.py migrate`
3. Create superuser in Supabase database
4. Admin panel will work the same way

The admin panel automatically works with any database backend (SQLite, PostgreSQL, Supabase).

---

## 🚀 Production Deployment

For production, restrict admin panel access:

```python
# In settings.py
ALLOWED_ADMIN_IPS = ['your-office-ip', 'your-home-ip']

# In views.py
def admin_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        client_ip = get_client_ip(request)
        if not is_admin(request.user) or client_ip not in ALLOWED_ADMIN_IPS:
            return HttpResponseForbidden("Access Denied")
        return view_func(request, *args, **kwargs)
    return wrapped_view
```

Or use a secret token in URL:

```python
path('admin-panel/<str:token>/', views.admin_panel_login, name='admin_panel_login')
```

---

## ✨ Features

✅ Admin-only access control  
✅ Auto-verified car listings  
✅ Multiple image upload  
✅ Car approval/rejection workflow  
✅ User management view  
✅ Real-time statistics  
✅ Responsive design  
✅ CSRF protection  

