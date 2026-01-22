# Sura Rentals - Peer-to-Peer Car Rental Platform

A production-ready, modern full-stack web application for peer-to-peer car rentals, built with Django, Django REST Framework, and Tailwind CSS.

## 🎯 Features

### Authentication & Security
- ✅ Multi-step signup with email and phone OTP verification
- ✅ Email-based login with session management
- ✅ Custom user model with role-based access control
- ✅ CSRF protection and secure password handling
- ✅ JWT support (optional)

### User Roles
- **Regular User**: Can rent cars and list cars
- **Admin**: Can verify users, verify cars, and manage platform

### Car Listings
- 📋 Create, edit, and delete car listings
- 🖼️ Upload multiple car images
- 📄 Upload RC and insurance documents
- ✓ Automatic verification workflow
- 🏷️ Filter by location, fuel type, and price

### Bookings & Rentals
- 📅 Browse available cars with date filters
- 🎫 Request bookings (pending → approved → active → completed)
- 💰 Integrated payment tracking
- 📝 Booking history and management

### Verification System
- 👤 User document verification (driving license + photo)
- 🚗 Car verification (RC, insurance, owner verification)
- 🔍 Admin dashboard for verification management
- 📋 Audit logs for all admin actions

### Dashboard
- 👤 User profile management
- 🚗 My cars listing and management
- 📅 My bookings (as renter and owner)
- ✓ Verification status tracking

## 🛠️ Tech Stack

**Backend:**
- Django 4.2 LTS
- Django REST Framework
- PostgreSQL (production) / SQLite (development)
- Celery (optional, for async tasks)

**Frontend:**
- Django Templates
- Tailwind CSS
- Alpine.js
- Font Awesome Icons

**Storage:**
- Local filesystem (development)
- AWS S3 / Supabase (production)

**Deployment:**
- Gunicorn
- WhiteNoise
- Docker-ready

## 📦 Installation

### Prerequisites
- Python 3.9+
- PostgreSQL (for production)
- pip / virtualenv

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/sura-rentals.git
cd sura-rentals
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
```

7. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

8. **Run development server:**
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 🗄️ Database Schema

### Core Models
- **CustomUser**: Email-based user authentication
- **Profile**: Extended user information (rating, photo, bio)
- **OTPVerification**: OTP records for email/phone verification
- **SignUpSession**: Multi-step signup tracking

### Car Models
- **Car**: Car listing details
- **CarImage**: Multiple images per car
- **Review**: User reviews for cars

### Booking Models
- **Booking**: Rental request/agreement
- **Payment**: Payment tracking

### Verification Models
- **UserVerification**: User document verification
- **CarVerification**: Car document verification
- **AuditLog**: Admin action logs

## 📝 API Endpoints

```
AUTH:
POST   /signup/step1/           - Start signup
POST   /signup/step2/           - Verify email
POST   /signup/step3/           - Verify phone
POST   /login/                  - Login
POST   /logout/                 - Logout

CARS:
GET    /cars/browse/            - List cars with filters
GET    /cars/<id>/              - Car details
POST   /cars/create/            - Create listing
PUT    /cars/<id>/edit/         - Edit listing
DELETE /cars/<id>/delete/       - Delete listing
POST   /cars/<id>/review/       - Add review

BOOKINGS:
POST   /bookings/create/<car>/  - Create booking
GET    /bookings/<id>/          - Booking details
POST   /bookings/<id>/approve/  - Approve booking
POST   /bookings/<id>/reject/   - Reject booking
GET    /bookings/my-bookings/   - List user's bookings

VERIFICATION:
POST   /verify/upload/          - Upload verification docs
GET    /verify/status/          - Check verification status

ADMIN:
/admin/                         - Django admin panel
```

## 🔐 Security Features

- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS protection via template escaping
- Secure password hashing (PBKDF2)
- Session-based authentication
- HTTPS enforced in production
- File upload validation
- Rate limiting (optional)

## 📂 Project Structure

```
sura-rentals/
├── apps/
│   ├── accounts/           # User authentication
│   ├── cars/               # Car listings
│   ├── bookings/           # Rental bookings
│   ├── verification/       # Document verification
│   └── core/               # Site settings
├── carrentals/             # Project settings
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads
├── requirements.txt        # Dependencies
├── manage.py              # Django CLI
└── .env.example           # Environment template
```

## 🚀 Deployment

### Production Checklist
- [ ] Set DEBUG = False
- [ ] Configure SECRET_KEY from environment
- [ ] Set up PostgreSQL database
- [ ] Configure email backend
- [ ] Set up AWS S3 or Supabase storage
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS/SSL
- [ ] Set up security headers
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets

### Deploy to Render/Railway

```bash
# Create Procfile
echo "web: gunicorn carrentals.wsgi" > Procfile

# Push to Git
git add .
git commit -m "Ready for deployment"
git push heroku main
```

### Deploy to VPS

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3-pip postgresql nginx

# Clone repository
git clone <your-repo>
cd sura-rentals

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Gunicorn and Nginx
gunicorn --bind 0.0.0.0:8000 carrentals.wsgi

# Use systemd or supervisor for process management
```

## 👥 Admin Panel

Access the admin panel at `/admin/`

**Features:**
- User management and verification
- Car listing management
- Booking approval/rejection
- Payment tracking
- Audit logs
- Site settings

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔧 Customization

### Customize Theme Colors
Edit `templates/base.html` to change Tailwind color scheme.

### Add SMS Provider
Update `apps/accounts/utils.py` with your SMS provider API.

### Add Payment Gateway
Implement payment integration in `apps/bookings/views.py`.

### Extend Admin
Add custom admin actions in `apps/*/admin.py`.

## 📚 Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Alpine.js](https://alpinejs.dev/)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@surarentals.com or open an issue on GitHub.

## ⚡ Performance Optimization

- Use database indexing (configured in models)
- Enable query result caching
- Compress images for uploads
- Use CDN for static files
- Implement pagination (20 items per page)
- Add lazy loading for images

## 🔄 Future Enhancements

- [ ] Real-time notifications
- [ ] Payment gateway integration
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Vehicle insurance integration
- [ ] GPS tracking
- [ ] Video verification
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Search suggestions/autocomplete

---

Built with ❤️ by the Sura Rentals Team
