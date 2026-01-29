# Migration Guide: Django SQLite → Supabase PostgreSQL

## 📊 Current Status

- ✅ Admin panel working (SQLite local)
- ✅ Test cars can be added
- ✅ Users can register & login
- ⏭️ Ready to migrate to Supabase

---

## 🔄 STEP-BY-STEP MIGRATION

### STEP 1: Setup Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get these credentials from **Settings → API**:
   - Project URL
   - Anon Key
   - Service Role Key
   - Database Password

### STEP 2: Create Database Tables

1. Go to **SQL Editor** in Supabase
2. Copy and run all queries from `SUPABASE_SCHEMA.md`:
   - Create tables (Step 1)
   - Enable RLS (Step 2)
   - Add policies (Step 3)

### STEP 3: Migrate Data from SQLite

```bash
# Export from SQLite
python3 manage.py dumpdata > backup.json

# Migrate to Supabase (we'll create a script for this)
python3 manage.py loaddata backup.json
```

### STEP 4: Update Django Settings

Update `.env`:
```
DATABASE_URL=postgresql://postgres:PASSWORD@PROJECT.supabase.co:5432/postgres
SUPABASE_URL=https://PROJECT.supabase.co
SUPABASE_KEY=anon_key_here
SUPABASE_SERVICE_ROLE=service_role_key_here
```

Update `settings.py`:
```python
# Remove SQLite, use PostgreSQL via Supabase
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

### STEP 5: Run Migrations on Supabase

```bash
python3 manage.py migrate
```

### STEP 6: Create Superuser on Supabase

```bash
python3 manage.py createsuperuser
```

### STEP 7: Test Everything

```bash
python3 manage.py runserver

# Test:
# 1. Login works
# 2. Admin panel accessible
# 3. Can add cars
# 4. Cars are stored in Supabase
```

---

## 📁 FILES TO UPDATE

| File | Changes |
|------|---------|
| `.env` | Add Supabase credentials |
| `settings.py` | Update DATABASE_URL |
| `requirements.txt` | Already has `dj-database-url`, `psycopg2-binary` |
| `apps/accounts/models.py` | May need adjustments for Supabase Auth |
| `apps/admin_panel/views.py` | Should work as-is |

---

## ⚠️ BREAKING CHANGES

### User Model
- **Current**: Django `CustomUser` with email field
- **Supabase**: Uses `auth.users` table (Supabase Auth)
- **Solution**: Create `accounts_users` table linked to Supabase Auth

### File Storage
- **Current**: Local `/media/` folder
- **Supabase**: Cloud storage buckets
- **Solution**: Use Supabase Storage API for uploads

### Sessions
- **Current**: Django session cookies
- **Supabase**: JWT tokens
- **Solution**: Keep Django sessions for now, add JWT later

---

## 🚀 QUICK MIGRATION (5 STEPS)

1. **Create Supabase Project** (5 min)
2. **Run SQL queries** from SUPABASE_SCHEMA.md (2 min)
3. **Update .env & settings.py** (2 min)
4. **Run migrations** (1 min)
5. **Test admin panel** (2 min)

**Total time: ~15 minutes** ⏱️

---

## ✅ VERIFICATION

After migration, verify:

```bash
# Check database connection
python3 manage.py dbshell
# Should connect to Supabase PostgreSQL

# Check tables exist
\dt
# Should show all 5 tables

# Check RLS enabled
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname='public';
# Should show "ON" for all tables

# Check policies
SELECT * FROM pg_policies;
# Should show all RLS policies
```

---

## 🔐 Security Checklist

- [ ] RLS enabled on all tables
- [ ] Policies restrict access correctly
- [ ] Service Role Key kept private (.env only)
- [ ] Anon Key has minimal permissions
- [ ] Storage bucket access controls set
- [ ] Database password is strong
- [ ] HTTPS enforced in production

---

## 📞 TROUBLESHOOTING

### "Connection refused"
- Check DATABASE_URL is correct
- Verify Supabase database is online
- Ensure IP is whitelisted (if needed)

### "Policy violation"
- Check RLS policies are applied
- Verify user is authenticated
- Check `auth.uid()` returns correct user

### "Table doesn't exist"
- Ensure SQL queries were run in SQL Editor
- Check table names match (lowercase)
- Verify no errors during table creation

---

## 📚 REFERENCES

- Supabase Docs: https://supabase.com/docs
- Django Docs: https://docs.djangoproject.com
- dj-database-url: https://github.com/jacobian/dj-database-url
- psycopg2: https://www.psycopg.org/

---

## 🎯 WHAT'S NEXT

1. Migrate to Supabase (this guide)
2. Add JWT authentication
3. Build REST API endpoints
4. Create mobile app
5. Deploy to production

