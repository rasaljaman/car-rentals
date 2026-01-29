# Supabase Setup Guide - Queries & RLS Policies

## 1. Enable RLS for All Tables

```sql
-- After Django creates tables via migrations, enable RLS on all tables
ALTER TABLE accounts_customuser ENABLE ROW LEVEL SECURITY;
ALTER TABLE cars_car ENABLE ROW LEVEL SECURITY;
ALTER TABLE cars_carimage ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings_booking ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_userdocument ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_cardocument ENABLE ROW LEVEL SECURITY;
ALTER TABLE core_auditlog ENABLE ROW LEVEL SECURITY;
```

---

## 2. Row Level Security (RLS) Policies

### **A. Users Table (accounts_customuser)**

```sql
-- Policy 1: Users can view their own profile
CREATE POLICY "users_view_own_profile"
ON accounts_customuser
FOR SELECT
USING (auth.uid()::text = id::text OR is_staff = true);

-- Policy 2: Users can update their own profile
CREATE POLICY "users_update_own_profile"
ON accounts_customuser
FOR UPDATE
USING (auth.uid()::text = id::text)
WITH CHECK (auth.uid()::text = id::text);

-- Policy 3: Admin can view all users
CREATE POLICY "admin_view_all_users"
ON accounts_customuser
FOR SELECT
USING (is_staff = true);

-- Policy 4: Public can view limited user info (for car listings)
CREATE POLICY "public_view_user_info"
ON accounts_customuser
FOR SELECT
USING (is_public_profile = true);
```

### **B. Cars Table (cars_car)**

```sql
-- Policy 1: Owners can view their own cars
CREATE POLICY "owners_view_own_cars"
ON cars_car
FOR SELECT
USING (owner_id = auth.uid()::text OR is_verified = true);

-- Policy 2: Owners can manage their own cars
CREATE POLICY "owners_manage_own_cars"
ON cars_car
FOR UPDATE
USING (owner_id = auth.uid()::text)
WITH CHECK (owner_id = auth.uid()::text);

-- Policy 3: Owners can insert cars
CREATE POLICY "owners_create_cars"
ON cars_car
FOR INSERT
WITH CHECK (owner_id = auth.uid()::text);

-- Policy 4: Owners can delete their cars
CREATE POLICY "owners_delete_own_cars"
ON cars_car
FOR DELETE
USING (owner_id = auth.uid()::text);

-- Policy 5: Public can view verified cars
CREATE POLICY "public_view_verified_cars"
ON cars_car
FOR SELECT
USING (is_verified = true AND is_active = true);

-- Policy 6: Admin manages all cars
CREATE POLICY "admin_manage_all_cars"
ON cars_car
FOR ALL
USING (auth.jwt() ->> 'user_role' = 'admin');
```

### **C. Car Images (cars_carimage)**

```sql
-- Policy 1: Car owners can manage images
CREATE POLICY "owners_manage_car_images"
ON cars_carimage
FOR ALL
USING (
  car_id IN (
    SELECT id FROM cars_car WHERE owner_id = auth.uid()::text
  )
)
WITH CHECK (
  car_id IN (
    SELECT id FROM cars_car WHERE owner_id = auth.uid()::text
  )
);

-- Policy 2: Public can view images of verified cars
CREATE POLICY "public_view_car_images"
ON cars_carimage
FOR SELECT
USING (
  car_id IN (
    SELECT id FROM cars_car WHERE is_verified = true
  )
);
```

### **D. Bookings Table (bookings_booking)**

```sql
-- Policy 1: Renters can view their own bookings
CREATE POLICY "renters_view_own_bookings"
ON bookings_booking
FOR SELECT
USING (renter_id = auth.uid()::text);

-- Policy 2: Owners can view booking requests for their cars
CREATE POLICY "owners_view_booking_requests"
ON bookings_booking
FOR SELECT
USING (
  car_id IN (
    SELECT id FROM cars_car WHERE owner_id = auth.uid()::text
  )
);

-- Policy 3: Renters can create bookings
CREATE POLICY "renters_create_bookings"
ON bookings_booking
FOR INSERT
WITH CHECK (renter_id = auth.uid()::text);

-- Policy 4: Owners can update booking status
CREATE POLICY "owners_update_booking_status"
ON bookings_booking
FOR UPDATE
USING (
  car_id IN (
    SELECT id FROM cars_car WHERE owner_id = auth.uid()::text
  )
)
WITH CHECK (
  car_id IN (
    SELECT id FROM cars_car WHERE owner_id = auth.uid()::text
  )
);

-- Policy 5: Renters can cancel their bookings
CREATE POLICY "renters_cancel_bookings"
ON bookings_booking
FOR UPDATE
USING (renter_id = auth.uid()::text AND status IN ('pending', 'confirmed'))
WITH CHECK (renter_id = auth.uid()::text);

-- Policy 6: Admin manages all bookings
CREATE POLICY "admin_manage_all_bookings"
ON bookings_booking
FOR ALL
USING (auth.jwt() ->> 'user_role' = 'admin');
```

### **E. Verification Documents (verification_userdocument & verification_cardocument)**

```sql
-- User Documents
-- Policy 1: Users can view their own documents
CREATE POLICY "users_view_own_documents"
ON verification_userdocument
FOR SELECT
USING (user_id = auth.uid()::text);

-- Policy 2: Users can upload documents
CREATE POLICY "users_upload_documents"
ON verification_userdocument
FOR INSERT
WITH CHECK (user_id = auth.uid()::text);

-- Policy 3: Admin can view all documents for verification
CREATE POLICY "admin_view_all_documents"
ON verification_userdocument
FOR SELECT
USING (auth.jwt() ->> 'user_role' = 'admin');

-- Policy 4: Admin can update verification status
CREATE POLICY "admin_verify_documents"
ON verification_userdocument
FOR UPDATE
USING (auth.jwt() ->> 'user_role' = 'admin')
WITH CHECK (auth.jwt() ->> 'user_role' = 'admin');

-- Car Documents
-- Policy 1: Car owners can manage their documents
CREATE POLICY "owners_manage_car_documents"
ON verification_cardocument
FOR ALL
USING (
  car_id IN (
    SELECT id FROM cars_car WHERE owner_id = auth.uid()::text
  )
)
WITH CHECK (
  car_id IN (
    SELECT id FROM cars_car WHERE owner_id = auth.uid()::text
  )
);

-- Policy 2: Admin can view all car documents
CREATE POLICY "admin_view_all_car_documents"
ON verification_cardocument
FOR SELECT
USING (auth.jwt() ->> 'user_role' = 'admin');

-- Policy 3: Admin can approve documents
CREATE POLICY "admin_approve_car_documents"
ON verification_cardocument
FOR UPDATE
USING (auth.jwt() ->> 'user_role' = 'admin')
WITH CHECK (auth.jwt() ->> 'user_role' = 'admin');
```

### **F. Audit Logs (core_auditlog)**

```sql
-- Policy 1: Only admins can view audit logs
CREATE POLICY "admin_view_audit_logs"
ON core_auditlog
FOR SELECT
USING (auth.jwt() ->> 'user_role' = 'admin');

-- Policy 2: System can insert audit logs
CREATE POLICY "system_create_audit_logs"
ON core_auditlog
FOR INSERT
WITH CHECK (true);

-- Policy 3: Audit logs are immutable
ALTER TABLE core_auditlog DISABLE ROW LEVEL SECURITY;
```

---

## 3. Helpful PostgreSQL Queries

### **A. User Management Queries**

```sql
-- Get all active users
SELECT id, email, first_name, last_name, phone, is_verified, created_at 
FROM accounts_customuser 
WHERE is_active = true 
ORDER BY created_at DESC;

-- Get all unverified users
SELECT id, email, phone, created_at 
FROM accounts_customuser 
WHERE is_verified = false 
ORDER BY created_at DESC;

-- Get admin users
SELECT id, email, is_staff 
FROM accounts_customuser 
WHERE is_staff = true;

-- Update user verification status
UPDATE accounts_customuser 
SET is_verified = true, verified_at = NOW() 
WHERE id = 'user-uuid-here';
```

### **B. Car Management Queries**

```sql
-- Get all pending cars (awaiting approval)
SELECT id, make, model, owner_id, status, created_at 
FROM cars_car 
WHERE status = 'pending' 
ORDER BY created_at ASC;

-- Get all verified cars
SELECT id, make, model, owner_id, daily_rate, location, fuel_type 
FROM cars_car 
WHERE is_verified = true AND is_active = true 
ORDER BY created_at DESC;

-- Get cars by location
SELECT id, make, model, location, daily_rate 
FROM cars_car 
WHERE location ILIKE '%location-name%' AND is_verified = true;

-- Get cars by fuel type
SELECT id, make, model, fuel_type, daily_rate 
FROM cars_car 
WHERE fuel_type = 'petrol' AND is_verified = true;

-- Approve a car
UPDATE cars_car 
SET status = 'verified', is_verified = true, verified_at = NOW() 
WHERE id = 'car-uuid-here';

-- Reject a car
UPDATE cars_car 
SET status = 'rejected', is_verified = false 
WHERE id = 'car-uuid-here';

-- Get cars owned by a user
SELECT id, make, model, status, daily_rate 
FROM cars_car 
WHERE owner_id = 'user-uuid-here' 
ORDER BY created_at DESC;
```

### **C. Booking Management Queries**

```sql
-- Get all pending bookings
SELECT b.id, b.renter_id, b.car_id, c.make, c.model, 
       b.start_date, b.end_date, b.total_price, b.status 
FROM bookings_booking b
JOIN cars_car c ON b.car_id = c.id
WHERE b.status = 'pending' 
ORDER BY b.created_at ASC;

-- Get all confirmed bookings
SELECT b.id, b.renter_id, b.car_id, c.make, c.model,
       b.start_date, b.end_date, b.total_price
FROM bookings_booking b
JOIN cars_car c ON b.car_id = c.id
WHERE b.status = 'confirmed'
ORDER BY b.start_date ASC;

-- Get bookings for a specific car (check availability)
SELECT renter_id, start_date, end_date, status 
FROM bookings_booking 
WHERE car_id = 'car-uuid-here' AND status IN ('confirmed', 'in_progress')
ORDER BY start_date ASC;

-- Get bookings by a renter
SELECT b.id, b.car_id, c.make, c.model, b.start_date, 
       b.end_date, b.total_price, b.status 
FROM bookings_booking b
JOIN cars_car c ON b.car_id = c.id
WHERE b.renter_id = 'user-uuid-here'
ORDER BY b.created_at DESC;

-- Approve a booking
UPDATE bookings_booking 
SET status = 'confirmed', approved_at = NOW() 
WHERE id = 'booking-uuid-here';

-- Reject a booking
UPDATE bookings_booking 
SET status = 'rejected', rejected_at = NOW() 
WHERE id = 'booking-uuid-here';

-- Check for booking conflicts (date overlap)
SELECT * FROM bookings_booking 
WHERE car_id = 'car-uuid-here' 
AND status IN ('confirmed', 'in_progress')
AND (
  (start_date, end_date) OVERLAPS 
  ('2026-02-01'::date, '2026-02-10'::date)
);
```

### **D. Verification Queries**

```sql
-- Get pending user verifications
SELECT id, user_id, document_type, status, created_at 
FROM verification_userdocument 
WHERE status = 'pending' 
ORDER BY created_at ASC;

-- Get pending car verifications
SELECT id, car_id, document_type, status, created_at 
FROM verification_cardocument 
WHERE status = 'pending' 
ORDER BY created_at ASC;

-- Approve user verification
UPDATE verification_userdocument 
SET status = 'approved', approved_at = NOW() 
WHERE id = 'doc-uuid-here';

-- Reject user verification
UPDATE verification_userdocument 
SET status = 'rejected', rejected_reason = 'reason-here' 
WHERE id = 'doc-uuid-here';

-- Get verified users
SELECT DISTINCT u.id, u.email, u.first_name, u.last_name 
FROM accounts_customuser u
JOIN verification_userdocument v ON u.id = v.user_id
WHERE v.status = 'approved';

-- Get verified cars
SELECT DISTINCT c.id, c.make, c.model, c.owner_id 
FROM cars_car c
JOIN verification_cardocument v ON c.id = v.car_id
WHERE v.status = 'approved';
```

### **E. Analytics Queries**

```sql
-- Total users
SELECT COUNT(*) as total_users 
FROM accounts_customuser 
WHERE is_active = true;

-- Total cars available
SELECT COUNT(*) as available_cars 
FROM cars_car 
WHERE is_verified = true AND is_active = true;

-- Total bookings this month
SELECT COUNT(*) as monthly_bookings 
FROM bookings_booking 
WHERE EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM NOW());

-- Total revenue this month
SELECT SUM(total_price) as monthly_revenue 
FROM bookings_booking 
WHERE status = 'completed' 
AND EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM NOW());

-- Cars by owner (top listers)
SELECT owner_id, COUNT(*) as car_count 
FROM cars_car 
WHERE is_verified = true
GROUP BY owner_id 
ORDER BY car_count DESC 
LIMIT 10;

-- Average booking duration
SELECT AVG(EXTRACT(DAY FROM (end_date - start_date))) as avg_duration_days 
FROM bookings_booking 
WHERE status = 'completed';

-- Most booked cars
SELECT car_id, c.make, c.model, COUNT(*) as booking_count 
FROM bookings_booking b
JOIN cars_car c ON b.car_id = c.id
WHERE b.status = 'completed'
GROUP BY b.car_id, c.make, c.model
ORDER BY booking_count DESC 
LIMIT 10;
```

### **F. Data Cleanup Queries**

```sql
-- Deactivate inactive user accounts (30+ days no login)
UPDATE accounts_customuser 
SET is_active = false 
WHERE last_login < NOW() - INTERVAL '30 days' 
AND is_staff = false;

-- Cancel pending bookings older than 7 days
UPDATE bookings_booking 
SET status = 'cancelled' 
WHERE status = 'pending' 
AND created_at < NOW() - INTERVAL '7 days';

-- Soft delete old cars
UPDATE cars_car 
SET is_active = false 
WHERE is_active = true 
AND created_at < NOW() - INTERVAL '1 year';

-- Delete old audit logs (older than 90 days)
DELETE FROM core_auditlog 
WHERE created_at < NOW() - INTERVAL '90 days';
```

---

## 4. Supabase SQL Editor Setup

1. Go to Supabase Dashboard → SQL Editor
2. Copy and paste each section above
3. Run queries one by one
4. Test policies with different user roles

---

## 5. Testing RLS Policies

```sql
-- Test if user can only see their data
SET request.jwt.claim.sub = 'user-uuid-here';
SELECT * FROM accounts_customuser;

-- Test admin access
SET request.jwt.claim.user_role = 'admin';
SELECT * FROM cars_car;

-- Reset
RESET request.jwt.claim.sub;
RESET request.jwt.claim.user_role;
```

---

## 6. Storage Buckets (Optional)

```sql
-- Create storage buckets in Supabase Dashboard:
-- 1. car-images (public)
-- 2. car-documents (private)
-- 3. user-documents (private)
-- 4. profile-pictures (public)
```

