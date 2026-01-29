# ⚡ SUPABASE QUICK REFERENCE

## 🚀 5-Minute Setup

### Step 1: Get Credentials
```
https://supabase.com/dashboard → Settings → API
```

### Step 2: Update `.env`
```dotenv
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=sb_anon_xxxxx
```

### Step 3: Install & Migrate
```bash
pip install -r requirements.txt
python manage.py migrate
```

### Step 4: Initialize
```bash
python manage.py shell
```
```python
from apps.core.supabase_init import initialize_supabase_db
initialize_supabase_db()
```

---

## 💻 Quick Usage

### SELECT
```python
from apps.core.supabase_utils import supabase_select, supabase_get, supabase_filter

supabase_select('cars_car', limit=20)
supabase_get('cars_car', 1)
supabase_filter('cars_car', {'status': 'verified'})
```

### INSERT
```python
from apps.core.supabase_utils import supabase_insert

supabase_insert('cars_car', {
    'brand': 'Toyota',
    'model': 'Innova',
    'owner_id': 1
})
```

### UPDATE
```python
from apps.core.supabase_utils import supabase_update

supabase_update('cars_car', 1, {'price_per_day': 2000})
```

### DELETE
```python
from apps.core.supabase_utils import supabase_delete

supabase_delete('cars_car', 1)
```

### COUNT
```python
from apps.core.supabase_utils import supabase_count

supabase_count('cars_car', {'status': 'verified'})
```

### FILES
```python
from apps.core.supabase_config import upload_file_to_supabase, delete_file_from_supabase

upload_file_to_supabase('bucket', 'path', content)
delete_file_from_supabase('bucket', 'path')
```

---

## 📚 Documentation

| Need | Document |
|------|----------|
| Quick setup | [SUPABASE_CONNECTION.md](SUPABASE_CONNECTION.md) |
| Complete guide | [SUPABASE_INTEGRATION.md](SUPABASE_INTEGRATION.md) |
| What's new | [SUPABASE_STATUS.md](SUPABASE_STATUS.md) |
| Security setup | [SUPABASE_SETUP.md](SUPABASE_SETUP.md) |
| Database schema | [SUPABASE_SCHEMA.md](SUPABASE_SCHEMA.md) |
| SQL scripts | [SUPABASE_SQL_SETUP.md](SUPABASE_SQL_SETUP.md) |

---

## ✅ Verification

```bash
python manage.py shell
```
```python
from apps.core.supabase_config import test_supabase_connection
test_supabase_connection()
```

Expected: `✅ Supabase connection successful!`

---

## 🐛 Quick Troubleshooting

| Error | Fix |
|-------|-----|
| No credentials | Add SUPABASE_URL, SUPABASE_KEY to .env |
| Table not found | Run `python manage.py migrate` |
| Import failed | Run `pip install -r requirements.txt` |
| Connection error | Check DATABASE_URL or restart Django |

---

## 📁 What Was Added

**Python Modules (3):**
- `apps/core/supabase_config.py` - Client initialization
- `apps/core/supabase_utils.py` - Database utilities
- `apps/core/supabase_init.py` - Initialization script

**Documentation (8):**
- SUPABASE_CONNECTION.md (Quick start)
- SUPABASE_INTEGRATION.md (Full guide)
- SUPABASE_STATUS.md (Summary)
- SUPABASE_SETUP.md (Security)
- SUPABASE_SCHEMA.md (Database)
- SUPABASE_SQL_SETUP.md (SQL)
- SUPABASE_INDEX.md (Navigation)
- SUPABASE_SETUP_COMPLETE.md (Status)

**Modified Files (3):**
- carrentals/settings.py
- requirements.txt
- .env

---

## 🎯 Common Tasks

```python
# Get all cars
cars = supabase_select('cars_car')

# Get one car
car = supabase_get('cars_car', 1)

# Filter cars
verified = supabase_filter('cars_car', {'status': 'verified'})

# Create car
result = supabase_insert('cars_car', {...})

# Update car
result = supabase_update('cars_car', 1, {...})

# Delete car
result = supabase_delete('cars_car', 1)

# Count cars
count = supabase_count('cars_car')

# Upload image
url = upload_file_to_supabase('bucket', 'path', file)

# Delete file
delete_file_from_supabase('bucket', 'path')
```

---

## 🔑 Configuration

### Local Development
```dotenv
DATABASE_URL=sqlite:///db.sqlite3
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key
```

### Supabase PostgreSQL
```dotenv
DATABASE_URL=postgresql://user:pass@host:port/db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key
```

---

## 🎓 Resources

- [Supabase Docs](https://supabase.com/docs)
- [Python SDK](https://github.com/supabase/supabase-py)
- [Discord Community](https://discord.supabase.io)

---

**Status: ✅ Ready to Use**
