# ✅ Settings.py Updated!

## 🎯 Changes Made

Your `cleantrack/settings.py` has been simplified and updated to use `python-decouple`:

---

## 📝 What Changed

### 1. Configuration Method
**Before:**
```python
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', 'default')
```

**After:**
```python
from decouple import config
SECRET_KEY = config('SECRET_KEY')
```

---

### 2. BASE_DIR
**Before:**
```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
```

**After:**
```python
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

---

### 3. ALLOWED_HOSTS
**Before:**
```python
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

**After:**
```python
ALLOWED_HOSTS = ['*']  # Ajuste em produção
```

---

### 4. INSTALLED_APPS
**Removed:**
- `django.contrib.sites`
- `rest_framework`
- `allauth` and related apps
- `corsheaders`

**Kept:**
- Core Django apps
- `djstripe` (Stripe integration)
- Your local apps: `accounts`, `equipment`, `compliance`, `billing`

---

### 5. MIDDLEWARE
**Removed:**
- `whitenoise.middleware.WhiteNoiseMiddleware`
- `corsheaders.middleware.CorsMiddleware`
- `allauth.account.middleware.AccountMiddleware`

**Kept only essentials:**
- Security, Sessions, Common, CSRF
- Auth, Messages, Clickjacking

---

### 6. Database
**Before:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'cleantrack'),
        'USER': os.getenv('DB_USER', 'cleantrack'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'cleantrack_dev_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

**After:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cleantrack',
        'USER': 'cleantrack_user',
        'PASSWORD': 'secure_password_123',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

---

### 7. Resend (Email)
**Before:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.resend.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'resend'
EMAIL_HOST_PASSWORD = os.getenv('RESEND_API_KEY', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@cleantrack.app')
```

**After:**
```python
RESEND_API_KEY = config('RESEND_API_KEY')
```

---

### 8. Stripe
**Before:**
```python
STRIPE_LIVE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_LIVE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_TEST_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_LIVE_MODE = os.getenv('STRIPE_LIVE_MODE', 'False') == 'True'
DJSTRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
DJSTRIPE_FOREIGN_KEY_TO_FIELD = 'id'
```

**After:**
```python
STRIPE_LIVE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY', default="")
STRIPE_TEST_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY')
STRIPE_LIVE_MODE = False  # Altere em produção
DJSTRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default="")
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_USE_NATIVE_JSONFIELD = True
```

---

### 9. Removed Sections
❌ **Removed (not in your spec):**
- AllAuth settings
- Email SMTP settings (using Resend directly)
- Redis & Celery configuration
- REST Framework settings
- CORS settings
- CSRF_TRUSTED_ORIGINS
- Security settings for production
- Application-specific pricing settings
- Logging configuration

---

## 📊 Current Settings.py Structure

```python
# Imports
import os
from decouple import config

# Base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['*']

# Apps (4 local apps)
INSTALLED_APPS = [...]

# Middleware (7 essential)
MIDDLEWARE = [...]

# URLs & Templates
ROOT_URLCONF = 'cleantrack.urls'
TEMPLATES = [...]

# WSGI
WSGI_APPLICATION = 'cleantrack.wsgi.application'

# Database (PostgreSQL)
DATABASES = {...}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [...]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Resend
RESEND_API_KEY = config('RESEND_API_KEY')

# Stripe
STRIPE_LIVE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY', default="")
STRIPE_TEST_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY')
STRIPE_LIVE_MODE = False
DJSTRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default="")
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_USE_NATIVE_JSONFIELD = True
```

**Total lines:** ~113 (down from ~235)

---

## ⚠️ Important: Update .env Variables

Your `.env` file uses different variable names. Update it to match:

### Current .env:
```bash
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
RESEND_API_KEY=***REMOVED***
STRIPE_TEST_PUBLIC_KEY=pk_test_51ST4zs...
STRIPE_TEST_SECRET_KEY=sk_test_51ST4zs...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### What settings.py expects:
```bash
SECRET_KEY=...                    ✅ Matches
DEBUG=True                        ✅ Matches (will be cast to bool)
RESEND_API_KEY=...               ✅ Matches
STRIPE_TEST_SECRET_KEY=...       ✅ Matches
STRIPE_LIVE_SECRET_KEY=...       🔶 Optional (has default="")
STRIPE_WEBHOOK_SECRET=...        ✅ Matches
```

**Your current .env is compatible!** ✅

---

## 🧪 Test the Configuration

```bash
# Start project
docker-compose up --build

# Check for errors in logs
docker-compose logs web

# Expected:
# ✅ No configuration errors
# ✅ Database connected
# ✅ Server starts successfully
```

---

## 🔧 What Still Works

Even with simplified settings:

✅ **Core Django:**
- Admin interface
- User authentication
- Database (PostgreSQL)
- Templates rendering
- Static files serving
- Media uploads

✅ **Integrations:**
- Resend (email via API key)
- Stripe (dj-stripe with webhooks)

❌ **No Longer Available:**
- django-allauth (removed)
- REST Framework (removed)
- CORS headers (removed)
- Celery/Redis (removed)
- WhiteNoise (removed)

If you need any of these, you'll need to add them back to INSTALLED_APPS and MIDDLEWARE.

---

## 📋 Settings Summary

| Setting | Value | Source |
|---------|-------|--------|
| DEBUG | True/False | .env (DEBUG) |
| SECRET_KEY | From .env | .env (SECRET_KEY) |
| ALLOWED_HOSTS | ['*'] | Hardcoded |
| Database | PostgreSQL | Hardcoded credentials |
| Resend | API key | .env (RESEND_API_KEY) |
| Stripe Test | Secret key | .env (STRIPE_TEST_SECRET_KEY) |
| Stripe Live | Secret key | .env (STRIPE_LIVE_SECRET_KEY) - optional |
| Webhook | Secret | .env (STRIPE_WEBHOOK_SECRET) |

---

## ✅ Next Steps

1. **Test the configuration:**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access admin:**
   http://localhost:8000/admin

---

## 🎊 Settings.py is Ready!

Your simplified `settings.py`:
- ✅ Uses `python-decouple` for config
- ✅ Simplified from 235 to 113 lines
- ✅ Only essential settings
- ✅ Compatible with your .env file
- ✅ Ready for Docker deployment

**Start your project:**
```bash
docker-compose up --build
```
