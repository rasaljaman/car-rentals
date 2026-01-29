# Supabase SQL Setup Script - COPY & PASTE READY

## 🚀 HOW TO USE THIS FILE

1. Create Supabase project
2. Go to **SQL Editor**
3. Copy-paste each section below
4. Run queries one by one
5. Verify no errors

---

## ✅ CREATE ALL TABLES (Copy & Paste as ONE block)

```sql
-- Create Users table
CREATE TABLE accounts_users (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name text,
  phone text,
  is_verified boolean DEFAULT false,
  is_admin boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- Create Cars table
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

-- Create Car Images table
CREATE TABLE car_images (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  car_id uuid REFERENCES cars(id) ON DELETE CASCADE,
  image_url text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create Bookings table
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

-- Create Verification Documents table
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

## ✅ ENABLE ROW LEVEL SECURITY (Copy & Paste as ONE block)

```sql
ALTER TABLE accounts_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE cars ENABLE ROW LEVEL SECURITY;
ALTER TABLE car_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_docs ENABLE ROW LEVEL SECURITY;
```

---

## ✅ ADD RLS POLICIES (Copy & Paste each section)

### SECTION 1: User Policies

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

### SECTION 2: Car Policies

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

### SECTION 3: Car Image Policies

```sql
-- Public can view images of verified cars
CREATE POLICY "public_view_car_images"
ON car_images
FOR SELECT
USING (
  car_id IN (SELECT id FROM cars WHERE is_verified = true)
);

-- Owner manages images
CREATE POLICY "owner_manage_car_images"
ON car_images
FOR ALL
USING (
  car_id IN (SELECT id FROM cars WHERE owner_id = auth.uid())
);
```

### SECTION 4: Booking Policies

```sql
-- Renter views own bookings
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

### SECTION 5: Verification Document Policies

```sql
-- User uploads own documents
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

## ✅ VERIFY SETUP (Test Queries)

### Check all tables created
```sql
SELECT * FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

### Check RLS is enabled
```sql
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname='public'
ORDER BY tablename;
```

### Check all policies
```sql
SELECT schemaname, tablename, policyname, qual, with_check
FROM pg_policies
ORDER BY tablename, policyname;
```

---

## 📊 CREATE SAMPLE DATA (Optional - For Testing)

```sql
-- Create test user (replace with your user UUID)
INSERT INTO accounts_users (id, full_name, phone, is_verified, is_admin)
VALUES (
  '11111111-1111-1111-1111-111111111111',
  'Admin User',
  '+1234567890',
  true,
  true
);

-- Create test car
INSERT INTO cars (owner_id, brand, model, fuel_type, price_per_day, location, is_verified, is_active)
VALUES (
  '11111111-1111-1111-1111-111111111111',
  'Toyota',
  'Innova',
  'petrol',
  2000,
  'Mumbai',
  true,
  true
);
```

---

## 🔄 STEP-BY-STEP EXECUTION

### In Supabase SQL Editor:

1. **Run this FIRST:**
   ```
   Copy "CREATE ALL TABLES" section
   Paste into SQL Editor
   Click "Run"
   ✅ Verify: 5 tables created
   ```

2. **Run this SECOND:**
   ```
   Copy "ENABLE ROW LEVEL SECURITY" section
   Paste into SQL Editor
   Click "Run"
   ✅ Verify: No errors
   ```

3. **Run these NEXT (one by one):**
   ```
   SECTION 1: User Policies
   SECTION 2: Car Policies
   SECTION 3: Car Image Policies
   SECTION 4: Booking Policies
   SECTION 5: Document Policies
   ✅ Verify: 14 policies created
   ```

4. **Verify with TEST queries:**
   ```
   Run "Check all tables created"
   Run "Check RLS is enabled"
   Run "Check all policies"
   ✅ All should show tables and policies
   ```

5. **Optional - Add sample data:**
   ```
   (Skip if not needed for testing)
   ```

---

## ⚠️ COMMON ERRORS & FIXES

### Error: "table already exists"
→ Drop the table first: `DROP TABLE table_name CASCADE;`

### Error: "permission denied"
→ Make sure you're using the service role key (has admin access)

### Error: "UUID doesn't exist"
→ Use actual auth.users UUIDs from Supabase Auth

### Error: "policy already exists"
→ Drop the policy: `DROP POLICY policy_name ON table_name;`

---

## 📝 NOTES

- All times use `timestamptz` (timezone aware)
- All IDs are `uuid` (Supabase standard)
- Foreign keys cascade on delete
- RLS policies use `auth.uid()` for current user
- Admin check uses `EXISTS` subquery (safe)

---

## ✅ CHECKLIST

After running all queries:

- [ ] 5 tables created
- [ ] RLS enabled on all tables
- [ ] 14 policies created
- [ ] Verification queries pass
- [ ] No error messages
- [ ] Ready to use!

---

**COPY-PASTE READY!** Just follow the step-by-step execution above. 🚀

