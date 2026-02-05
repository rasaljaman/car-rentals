"""
Django settings for Sura Rentals project.

Production-ready configuration with PostgreSQL (Supabase),
custom user model, and secure authentication.
"""

import os
from pathlib import Path
from decouple import config

# --------------------------------------------------
# BASE DIR
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# CORE SETTINGS
# --------------------------------------------------
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-change-this-in-production"
)

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")]
)

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",

    # Local apps
<<<<<<< HEAD
    'apps.accounts.apps.AccountsConfig',
    'apps.cars.apps.CarsConfig',
    'apps.bookings.apps.BookingsConfig',
    'apps.verification.apps.VerificationConfig',
    'apps.core.apps.CoreConfig',
    'apps.admin_panel',
=======
    "apps.accounts.apps.AccountsConfig",
    "apps.cars.apps.CarsConfig",
    "apps.bookings.apps.BookingsConfig",
    "apps.verification.apps.VerificationConfig",
    "apps.core.apps.CoreConfig",
>>>>>>> 9a7e9f9 (database connection started)
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# URL / WSGI
# --------------------------------------------------
ROOT_URLCONF = "carrentals.urls"
WSGI_APPLICATION = "carrentals.wsgi.application"

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

<<<<<<< HEAD
WSGI_APPLICATION = 'carrentals.wsgi.application'

# Use PostgreSQL in production, SQLite in development
DATABASE_URL = config('DATABASE_URL', default=None)
SUPABASE_URL = config('SUPABASE_URL', default=None)
SUPABASE_KEY = config('SUPABASE_KEY', default=None)

if DATABASE_URL:
    # Production: PostgreSQL (Supabase or other)
=======
# --------------------------------------------------
# DATABASE CONFIGURATION (SUPABASE)
# --------------------------------------------------
DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL:
>>>>>>> 9a7e9f9 (database connection started)
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
elif SUPABASE_URL and SUPABASE_KEY:
    # Supabase: Using Supabase's PostgreSQL database
    # Extract credentials from Supabase connection string
    supabase_user = config('SUPABASE_USER', default='postgres')
    supabase_password = config('SUPABASE_PASSWORD', default='')
    supabase_host = config('SUPABASE_HOST', default='')
    supabase_port = config('SUPABASE_PORT', default='6543', cast=int)
    supabase_db = config('SUPABASE_DB', default='postgres')
    
    if supabase_host:  # Use individual credentials if provided
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': supabase_db,
                'USER': supabase_user,
                'PASSWORD': supabase_password,
                'HOST': supabase_host,
                'PORT': supabase_port,
                'CONN_MAX_AGE': 600,
                'OPTIONS': {
                    'sslmode': 'require',
                }
            }
        }
    else:
        # Development: SQLite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --------------------------------------------------
# AUTH & USER MODEL
# --------------------------------------------------
AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# REST FRAMEWORK
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# --------------------------------------------------
# MEDIA FILES
# --------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------
# CORS
# --------------------------------------------------
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://localhost:8000",
    cast=lambda v: [s.strip() for s in v.split(",")]
)

CORS_ALLOW_CREDENTIALS = True

# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)

SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool
)
SECURE_HSTS_PRELOAD = config(
    "SECURE_HSTS_PRELOAD", default=False, cast=bool
)

# --------------------------------------------------
# SESSION
# --------------------------------------------------
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 2 weeks
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# --------------------------------------------------
# EMAIL
# --------------------------------------------------
EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="noreply@surarentals.com",
)

# --------------------------------------------------
# OTP
# --------------------------------------------------
OTP_VALIDITY_MINUTES = 10
OTP_LENGTH = 6

# --------------------------------------------------
# FILE UPLOAD LIMITS
# --------------------------------------------------
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
MAX_UPLOAD_SIZE = 10 * 1024 * 1024

<<<<<<< HEAD
# Storage Configuration (Supabase/S3 in production)
USE_SUPABASE_STORAGE = config('USE_SUPABASE_STORAGE', default=False, cast=bool)

if USE_SUPABASE_STORAGE and SUPABASE_URL and SUPABASE_KEY:
    # Use Supabase Storage
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
            'LOCATION': MEDIA_ROOT,
        },
        'supabase': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
            'LOCATION': MEDIA_ROOT,
        }
    }
    # Note: Supabase storage integration is handled via apps.core.supabase_config
    # Files are uploaded via Supabase SDK instead of Django storage
else:
    # Use local filesystem storage
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
            'LOCATION': MEDIA_ROOT,
        }
    }
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
=======
# --------------------------------------------------
# STORAGE
# --------------------------------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "LOCATION": MEDIA_ROOT,
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
>>>>>>> 9a7e9f9 (database connection started)

# --------------------------------------------------
# DEFAULT PK
# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"