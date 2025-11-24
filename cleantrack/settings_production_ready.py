"""
CleanTrack Production Settings for Render Deployment
====================================================
Optimized production settings for Render.com with Docker.
"""
from .settings import *
import os
import dj_database_url

# ============================================================================
# CORE SETTINGS
# ============================================================================

DEBUG = False

# Secret key from environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

# Allowed hosts
ALLOWED_HOSTS = [
    '.onrender.com',
    'cleantrack.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Add Render hostname dynamically
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ============================================================================
# SECURITY SETTINGS
# ============================================================================

# HTTPS/SSL settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://cleantrack.onrender.com',
]

# ============================================================================
# DATABASE
# ============================================================================

# Parse database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback to SQLite for testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# WhiteNoise for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ensure WhiteNoise is in middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# ============================================================================
# EMAIL CONFIGURATION (Resend)
# ============================================================================

RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@cleantrack.com')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'server@cleantrack.com')

if RESEND_API_KEY:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.resend.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'resend'
    EMAIL_HOST_PASSWORD = RESEND_API_KEY
else:
    # Console backend for testing
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================================================
# STRIPE CONFIGURATION
# ============================================================================

STRIPE_TEST_PUBLIC_KEY = os.environ.get('STRIPE_TEST_PUBLIC_KEY', '')
STRIPE_TEST_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY', '')
STRIPE_LIVE_PUBLIC_KEY = os.environ.get('STRIPE_LIVE_PUBLIC_KEY', '')
STRIPE_LIVE_SECRET_KEY = os.environ.get('STRIPE_LIVE_SECRET_KEY', '')
STRIPE_LIVE_MODE = os.environ.get('STRIPE_LIVE_MODE', 'False').lower() == 'true'

# Set Stripe API key
import stripe
if STRIPE_LIVE_MODE and STRIPE_LIVE_SECRET_KEY:
    stripe.api_key = STRIPE_LIVE_SECRET_KEY
elif STRIPE_TEST_SECRET_KEY:
    stripe.api_key = STRIPE_TEST_SECRET_KEY

DJSTRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_USE_NATIVE_JSONFIELD = True

# ============================================================================
# LOGGING
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ============================================================================
# CACHING (Optional - Redis)
# ============================================================================

REDIS_URL = os.environ.get('REDIS_URL', '')

if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'KEY_PREFIX': 'cleantrack',
            'TIMEOUT': 300,
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    # Use database cache as fallback
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cleantrack_cache_table',
        }
    }

# ============================================================================
# ADMIN CONFIGURATION
# ============================================================================

ADMINS = [
    ('CleanTrack Admin', os.environ.get('ADMIN_EMAIL', 'natyssis23@gmail.com')),
]

MANAGERS = ADMINS

# ============================================================================
# SITE CONFIGURATION
# ============================================================================

SITE_URL = os.environ.get('SITE_URL', 'https://cleantrack.onrender.com')
SITE_ID = 1

# Language and timezone
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.environ.get('TIME_ZONE', 'America/Sao_Paulo')

# ============================================================================
# CORS (for API access)
# ============================================================================

CORS_ALLOWED_ORIGINS = [
    'https://cleantrack.onrender.com',
]

# Add custom origins from environment
CORS_ORIGINS_ENV = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if CORS_ORIGINS_ENV:
    CORS_ALLOWED_ORIGINS.extend(CORS_ORIGINS_ENV.split(','))

CORS_ALLOW_CREDENTIALS = True

# ============================================================================
# TEMPLATE OPTIMIZATIONS
# ============================================================================

# Enable template caching in production
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
    TEMPLATES[0]['OPTIONS']['debug'] = False

# ============================================================================
# RENDER-SPECIFIC SETTINGS
# ============================================================================

# Port configuration for Render
PORT = os.environ.get('PORT', '10000')

# Python unbuffered for better logging
os.environ.setdefault('PYTHONUNBUFFERED', '1')

print(f"""
================================================================================
CleanTrack Production Settings Loaded
================================================================================
DEBUG: {DEBUG}
ALLOWED_HOSTS: {ALLOWED_HOSTS}
DATABASE: {'PostgreSQL' if DATABASE_URL else 'SQLite'}
STATIC_ROOT: {STATIC_ROOT}
MEDIA_ROOT: {MEDIA_ROOT}
PORT: {PORT}
================================================================================
""")
