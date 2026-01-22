# SETUP GUIDE - Sura Rentals

Complete setup guide for the Sura Rentals peer-to-peer car rental platform.

## Prerequisites

- Python 3.9+
- pip and virtualenv
- PostgreSQL 12+ (for production)
- Git
- Redis (optional, for caching)

## Quick Start (5 minutes)

### 1. Clone & Setup Environment

```bash
cd /home/ccf/carrentals

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Django

```bash
# Create .env file
cp .env.example .env

# Edit .env with your settings
nano .env
```

Key settings to update:
- `SECRET_KEY`: Generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `DEBUG=True` (for development only)
- `DATABASE_URL`: SQLite will work for development

### 3. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Email: admin@surarentals.com
# Password: your-secure-password

# Initialize default data
python manage.py init_data
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Open: http://localhost:8000

### Admin Panel
http://localhost:8000/admin/
- Email: admin@surarentals.com
- Password: (as set above)

## Project Structure

```
sura-rentals/
├── apps/
│   ├── accounts/          # User authentication & profiles
│   │   ├── models.py      # Custom user model, OTP
│   │   ├── views.py       # Auth views (login, signup)
│   │   ├── forms.py       # Auth forms
│   │   ├── urls.py        # Auth routes
│   │   ├── admin.py       # Admin configuration
│   │   └── utils.py       # OTP utilities
│   │
│   ├── cars/              # Car listings
│   │   ├── models.py      # Car, CarImage, Review
│   │   ├── views.py       # Browse, detail, create listing
│   │   ├── urls.py        # Car routes
│   │   ├── admin.py       # Admin configuration
│   │   └── api.py         # Serializers
│   │
│   ├── bookings/          # Rental bookings & payments
│   │   ├── models.py      # Booking, Payment
│   │   ├── views.py       # Booking management
│   │   ├── urls.py        # Booking routes
│   │   ├── admin.py       # Admin configuration
│   │   └── api.py         # Serializers
│   │
│   ├── verification/      # Document verification
│   │   ├── models.py      # UserVerification, CarVerification, AuditLog
│   │   ├── views.py       # Verification upload/status
│   │   ├── urls.py        # Verification routes
│   │   └── admin.py       # Admin configuration
│   │
│   └── core/              # Global settings
│       ├── models.py      # SiteSettings
│       └── admin.py       # Admin configuration
│
├── carrentals/            # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL routing
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
│
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── login.html        # Login page
│   ├── dashboard.html    # User dashboard
│   ├── signup/           # Signup step templates
│   ├── cars/             # Car listing templates
│   ├── bookings/         # Booking templates
│   └── includes/         # Navbar, footer, etc.
│
├── static/                # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                 # User uploads
│   ├── profile_photos/
│   ├── car_images/
│   ├── car_documents/
│   └── verification/
│
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker compose
├── nginx.conf            # Nginx configuration
├── README.md             # Full documentation
└── DEPLOYMENT.md         # Deployment guide
```

## Key Features Implemented

### ✅ Authentication
- [x] Multi-step signup (3 steps)
- [x] Email OTP verification
- [x] Phone OTP verification
- [x] Login with email/password
- [x] Session management
- [x] Custom user model

### ✅ Car Listings
- [x] Create/edit/delete listings
- [x] Multiple image upload
- [x] Document upload (RC, insurance)
- [x] Filter by location, fuel type, price
- [x] Car details page
- [x] Reviews & ratings

### ✅ Bookings
- [x] Request booking
- [x] Approve/reject booking
- [x] Payment tracking
- [x] Booking history
- [x] Status management

### ✅ Verification
- [x] User document verification
- [x] Car document verification
- [x] Admin approval workflow
- [x] Audit logging

### ✅ User Dashboard
- [x] Profile management
- [x] My cars
- [x] My bookings
- [x] Verification status
- [x] Quick actions

### ✅ Admin Panel
- [x] User management
- [x] Car verification
- [x] Booking management
- [x] Verification approvals
- [x] Audit logs

## Common Tasks

### Add a New User (Admin)

```bash
python manage.py shell
>>> from apps.accounts.models import CustomUser, Profile
>>> user = CustomUser.objects.create_user(
...     email='user@example.com',
...     password='secure_password',
...     first_name='John',
...     last_name='Doe',
...     phone_number='+911234567890',
...     location='Mumbai',
...     role='user'
... )
>>> Profile.objects.create(user=user)
>>> exit()
```

### Create Test Data

```bash
# Run in shell
python manage.py shell
>>> from apps.cars.models import Car
>>> from apps.accounts.models import CustomUser
>>> user = CustomUser.objects.first()
>>> Car.objects.create(
...     owner=user,
...     title='Honda City 2020',
...     brand='Honda',
...     model='City',
...     year=2020,
...     fuel_type='petrol',
...     price_per_day=1500,
...     location='Mumbai',
...     registration_number='MH01AB1234',
...     mileage=50000,
...     transmission='automatic',
...     seats=5,
...     color='Silver',
...     description='Great car for rent'
... )
```

### Reset Database

```bash
python manage.py flush  # ⚠️ Deletes all data
python manage.py migrate
python manage.py createsuperuser
python manage.py init_data
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.accounts

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput

# Development: automatic with runserver
# Production: collectstatic in CI/CD
```

## Environment Variables

### Development
```
DEBUG=True
SECRET_KEY=django-insecure-dev-key
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production
```
DEBUG=False
SECRET_KEY=your-long-random-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/db
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Troubleshooting

### Migration Issues
```bash
python manage.py showmigrations
python manage.py migrate --fake apps.accounts 0001_initial
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Port Already in Use
```bash
python manage.py runserver 0.0.0.0:8001
```

### Module Not Found Errors
```bash
pip install -r requirements.txt --upgrade
```

## Performance Tips

1. **Enable Database Connection Pooling** (production)
2. **Use CDN for Static Files**
3. **Enable Gzip Compression**
4. **Implement Caching** (Redis)
5. **Use Database Indexes**
6. **Optimize Images**

## Security Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False (production)
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS
- [ ] Set CSRF_COOKIE_SECURE
- [ ] Set SESSION_COOKIE_SECURE
- [ ] Use strong database password
- [ ] Enable security headers
- [ ] Regular dependency updates
- [ ] Monitor error logs

## Next Steps

1. **Customize Branding**
   - Update logo in templates
   - Change color scheme in CSS
   - Update site name/description

2. **Configure Email**
   - Set up Gmail/SendGrid
   - Create email templates
   - Test OTP delivery

3. **Set Up Payment Gateway**
   - Integrate Razorpay/Stripe
   - Implement payment processing
   - Add payment confirmation emails

4. **Deploy to Production**
   - Follow DEPLOYMENT.md
   - Set up domain
   - Configure SSL certificate
   - Monitor application

5. **Add Advanced Features**
   - Real-time notifications
   - GPS tracking
   - Video verification
   - Insurance integration
   - Multi-language support

## Support & Documentation

- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [Tailwind Docs](https://tailwindcss.com/)
- [GitHub Issues](https://github.com/yourusername/sura-rentals/issues)

---

**Questions?** Check the README.md or DEPLOYMENT.md for more information.

**Ready to deploy?** See DEPLOYMENT.md for production setup.
