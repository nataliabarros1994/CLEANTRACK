"""
Django settings for cleantrack project.
"""

import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security Settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['*']  # Ajuste em produção

# Application definition
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party apps
    'djstripe',

    # CleanTrack apps (all enabled)
    'apps.accounts',
    'apps.facilities',
    'apps.equipment',
    'apps.cleaning_logs',
    'apps.billing',
    'apps.notifications',
    'apps.documentation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cleantrack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cleantrack.wsgi.application'

# Database
# Use SQLite for local development (change to PostgreSQL for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Uncomment for PostgreSQL (Docker)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'cleantrack',
#         'USER': 'cleantrack_user',
#         'PASSWORD': 'secure_password_123',
#         'HOST': 'db',
#         'PORT': '5432',
#     }
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Sites framework
SITE_ID = 1

# Authentication Backends
# EmailBackend primeiro - permite login por email ou username
AUTHENTICATION_BACKENDS = [
    'apps.accounts.backends.EmailBackend',  # Custom backend - prioridade
    'django.contrib.auth.backends.ModelBackend',  # Fallback
]

# Authentication URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Resend
RESEND_API_KEY = config('RESEND_API_KEY', default='')

# Stripe
STRIPE_LIVE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY', default="")
STRIPE_TEST_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY', default='')
STRIPE_LIVE_MODE = False  # Altere em produção
DJSTRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default="")
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_USE_NATIVE_JSONFIELD = True

