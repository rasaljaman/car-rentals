# Sura Rentals - Deployment Guide

## Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Initialize data
python manage.py init_data

# 7. Run development server
python manage.py runserver
```

Visit: http://localhost:8000

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
http://localhost
```

## Production Deployment on Render

1. **Create Render account** and connect GitHub repository
2. **Create PostgreSQL database**
3. **Configure environment variables:**
   - `DEBUG=False`
   - `SECRET_KEY=your-secret-key`
   - `DATABASE_URL=postgresql://...`
   - `ALLOWED_HOSTS=your-domain.onrender.com`
   - `EMAIL_HOST_USER=your-email@gmail.com`
   - `EMAIL_HOST_PASSWORD=app-password`

4. **Create Web Service:**
   - Runtime: Python 3.11
   - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn carrentals.wsgi:application`

5. **Configure Static Files:**
   - Add static file path: `/staticfiles`
   - Add media file path: `/media`

## Production Deployment on AWS/GCP

### RDS Database
- Create PostgreSQL instance
- Update `DATABASE_URL` environment variable

### S3/Cloud Storage
- Create bucket for media files
- Configure Django storage settings
- Update AWS credentials in environment

### Application Server
- Use EC2/Compute Engine instance
- Install nginx and gunicorn
- Use systemd or supervisor for process management

### SSL Certificate
- Use Let's Encrypt for free SSL
- Configure with nginx

## Environment Variables (Production)

```
DEBUG=False
SECRET_KEY=your-very-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/sura_rentals

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-specific-password

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# AWS S3 (if using)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1

# Supabase (if using)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key
```

## Health Check

```bash
# Check application status
curl http://localhost:8000/

# Check admin panel
curl http://localhost:8000/admin/
```

## Monitoring & Logging

```bash
# View logs (Docker)
docker-compose logs -f web

# View logs (systemd)
sudo journalctl -u sura-rentals -f

# Monitor application
# Use tools like: DataDog, New Relic, Sentry
```

## Backup Strategy

### Database Backup
```bash
# PostgreSQL backup
pg_dump sura_rentals > backup.sql

# Restore
psql sura_rentals < backup.sql
```

### Media Files Backup
```bash
# Backup media folder
tar -czf media_backup.tar.gz media/
```

## Scaling Considerations

1. **Database**: Use read replicas, connection pooling
2. **Static Files**: Use CDN (Cloudflare, AWS CloudFront)
3. **Application**: Use load balancer with multiple instances
4. **Caching**: Implement Redis for session/cache
5. **Queue**: Use Celery for async tasks

## Security Checklist

- [ ] Set DEBUG=False
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set secure headers
- [ ] Enable CSRF protection
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Monitor for vulnerabilities
- [ ] Implement rate limiting
- [ ] Enable audit logging

## Performance Optimization

```bash
# Enable caching
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('key', 'value', timeout=300)

# Database query optimization
# Use select_related, prefetch_related
# Add appropriate indexes

# Static file compression
COMPRESS_OFFLINE = True
```

---

For issues or questions, refer to Django documentation or GitHub issues.
