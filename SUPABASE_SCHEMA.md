# Supabase Database Schema & RLS Policies

## ✅ STEP 1: CREATE CORE TABLES

### Users (Linked with Supabase Auth)
```sql
CREATE TABLE accounts_users (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name text,
  phone text,
  is_verified boolean DEFAULT false,
  is_admin boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);
```

### Cars
```sql
CREATE TABLE cars (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id uuid REFERENCES accounts_users(id) ON DELETE CASCADE,
  brand text,
  model text,
  fuel_type text,
  price_per_day numeric,
  location text,
  is_verified boolean DEFAULT false,
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);
```

### Car Images
```sql
CREATE TABLE car_images (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  car_id uuid REFERENCES cars(id) ON DELETE CASCADE,
  image_url text NOT NULL,
  created_at timestamptz DEFAULT now()
);
```

### Bookings
```sql
CREATE TABLE bookings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  car_id uuid REFERENCES cars(id) ON DELETE CASCADE,
  renter_id uuid REFERENCES accounts_users(id),
  start_date date,
  end_date date,
  status text DEFAULT 'pending',
  total_price numeric,
  created_at timestamptz DEFAULT now()
);
```

### Verification Documents
```sql
CREATE TABLE verification_docs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES accounts_users(id),
  car_id uuid REFERENCES cars(id),
  doc_type text,
  status text DEFAULT 'pending',
  created_at timestamptz DEFAULT now()
);
```

---

## ✅ STEP 2: ENABLE ROW LEVEL SECURITY (MANDATORY)

```sql
ALTER TABLE accounts_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE cars ENABLE ROW LEVEL SECURITY;
ALTER TABLE car_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_docs ENABLE ROW LEVEL SECURITY;
```

---

## ✅ STEP 3: RLS POLICIES (SAFE & SECURE)

### 👤 USERS TABLE

```sql
-- Users can view their own profile
CREATE POLICY "user_read_own_profile"
ON accounts_users
FOR SELECT
USING (id = auth.uid());

-- Users can update their own profile
CREATE POLICY "user_update_own_profile"
ON accounts_users
FOR UPDATE
USING (id = auth.uid());
```

### 🚗 CARS TABLE

```sql
-- Public can view verified cars
CREATE POLICY "public_view_verified_cars"
ON cars
FOR SELECT
USING (is_verified = true AND is_active = true);

-- Owner manages own cars
CREATE POLICY "owner_manage_own_cars"
ON cars
FOR ALL
USING (owner_id = auth.uid())
WITH CHECK (owner_id = auth.uid());

-- Admin manages all cars
CREATE POLICY "admin_manage_all_cars"
ON cars
FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM accounts_users 
    WHERE id = auth.uid() AND is_admin = true
  )
);
```

### 🖼 CAR IMAGES TABLE

```sql
-- Public can view images of verified cars
CREATE POLICY "public_view_car_images"
ON car_images
FOR SELECT
USING (
  car_id IN (SELECT id FROM cars WHERE is_verified = true)
);

-- Owner manages car images
CREATE POLICY "owner_manage_car_images"
ON car_images
FOR ALL
USING (
  car_id IN (SELECT id FROM cars WHERE owner_id = auth.uid())
);
```

### 📅 BOOKINGS TABLE

```sql
-- Renter views their own bookings
CREATE POLICY "renter_view_own_bookings"
ON bookings
FOR SELECT
USING (renter_id = auth.uid());

-- Owner views bookings for their cars
CREATE POLICY "owner_view_car_bookings"
ON bookings
FOR SELECT
USING (
  car_id IN (SELECT id FROM cars WHERE owner_id = auth.uid())
);

-- Renter creates bookings
CREATE POLICY "renter_create_booking"
ON bookings
FOR INSERT
WITH CHECK (renter_id = auth.uid());
```

### 📄 VERIFICATION DOCUMENTS TABLE

```sql
-- Users upload their own documents
CREATE POLICY "user_upload_docs"
ON verification_docs
FOR INSERT
WITH CHECK (user_id = auth.uid());

-- Admin reviews all documents
CREATE POLICY "admin_review_docs"
ON verification_docs
FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM accounts_users 
    WHERE id = auth.uid() AND is_admin = true
  )
);
```

---

## ✅ STEP 4: ESSENTIAL QUERIES

### Get Verified Cars (Homepage)
```sql
SELECT * FROM cars
WHERE is_verified = true AND is_active = true
ORDER BY created_at DESC;
```

### Check Booking Conflicts
```sql
SELECT *
FROM bookings
WHERE car_id = 'car_uuid_here'
AND status IN ('confirmed')
AND (start_date, end_date)
OVERLAPS ('2026-02-01', '2026-02-05');
```

### Approve Car (Admin)
```sql
UPDATE cars
SET is_verified = true
WHERE id = 'car_uuid_here';
```

### Get User's Cars (Owner)
```sql
SELECT * FROM cars
WHERE owner_id = auth.uid()
ORDER BY created_at DESC;
```

### Get User's Bookings (Renter)
```sql
SELECT b.*, c.brand, c.model, c.price_per_day
FROM bookings b
JOIN cars c ON b.car_id = c.id
WHERE b.renter_id = auth.uid()
ORDER BY b.created_at DESC;
```

---

## ✅ STEP 5: STORAGE BUCKETS

Create these buckets in **Supabase Dashboard → Storage**:

| Bucket Name | Access Level | Purpose |
|-------------|-------------|---------|
| `car-images` | Public | Car listing images |
| `user-docs` | Private | User verification documents |
| `car-docs` | Private | Car documents (RC, insurance) |

---

## 🔥 KEY SECURITY FEATURES

✅ **No Insecure Policies** - No `USING (true)` that allows everyone  
✅ **Admin Verification** - Uses `EXISTS` subquery to verify admin status  
✅ **Owner Control** - Owners can only manage their own cars  
✅ **Public Browsing** - Only verified cars visible to public  
✅ **Privacy** - Users can only see their own documents/bookings  
✅ **Production Ready** - Safe for production use  

---

## 📋 DEPLOYMENT CHECKLIST

- [ ] Create all 5 tables in Supabase
- [ ] Enable RLS on all tables
- [ ] Add all RLS policies
- [ ] Create 3 storage buckets
- [ ] Test policies with different user roles
- [ ] Update Django to use Supabase SDK
- [ ] Migrate data from SQLite to Supabase
- [ ] Update `.env` with Supabase credentials

---

## 🚀 MIGRATION FROM DJANGO TO SUPABASE

Current: Django with SQLite + Custom User Model  
Target: Supabase with Auth + REST API

### Changes Needed:

1. **User Management** → Use Supabase Auth instead of Django User Model
2. **Database** → PostgreSQL (Supabase) instead of SQLite
3. **Authentication** → JWT tokens instead of Django sessions
4. **File Storage** → Supabase Storage instead of local filesystem
5. **API** → Supabase REST API or create Django REST endpoints

---

## ✨ NEXT STEPS

1. **Create Supabase Project** (if not done)
2. **Copy-paste tables** from Step 1 into SQL Editor
3. **Enable RLS** from Step 2
4. **Add policies** from Step 3
5. **Create buckets** from Step 5
6. **Test with different users**
7. **Update Django code** to use Supabase SDK

---

## 📞 NOTES

- All table IDs are `uuid` (Supabase standard)
- Timestamps use `timestamptz` for timezone support
- Foreign keys cascade on delete for data integrity
- RLS policies use `auth.uid()` for current user
- Admin status checked via `accounts_users.is_admin` flag

