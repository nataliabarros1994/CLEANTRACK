# 🚀 CleanTrack - Production Deployment Checklist

**Last Updated:** 2025-01-21
**Project:** CleanTrack GRC Platform
**Environment:** Production Ready Guide

---

## 📋 Pre-Deployment Validation Checklist

| Item | Status | Priority | Action Required |
|------|--------|----------|-----------------|
| `.env` in production | ❌ CRITICAL | HIGH | Never commit! Use platform secrets |
| `DEBUG=False` | ⚠️ TODO | HIGH | Must be False in production |
| `ALLOWED_HOSTS` | ❌ TODO | HIGH | Configure with actual domain |
| `SECRET_KEY` | ⚠️ WEAK | HIGH | Generate strong production key |
| HTTPS/SSL | ⚠️ TODO | HIGH | Required for Stripe + compliance |
| Database backups | ⚠️ TODO | HIGH | Configure automated backups |
| Static files | ⚠️ TODO | MEDIUM | Configure WhiteNoise or CDN |
| Media uploads | ⚠️ TODO | MEDIUM | Configure S3 or persistent storage |
| Email service | ✅ OK | MEDIUM | Resend configured |
| Stripe webhooks | ⚠️ TODO | HIGH | Configure production endpoint |
| Admin permissions | ❌ TODO | HIGH | Implement multi-tenant filters |
| Audit logging | ⚠️ PARTIAL | MEDIUM | CleaningLog exists, add more |
| Error monitoring | ❌ TODO | MEDIUM | Sentry recommended |
| Performance monitoring | ❌ TODO | LOW | APM tool recommended |

---

## 🔐 Security Checklist

### 1. Environment Variables (CRITICAL)

#### ❌ Current Issues:
```python
# cleantrack/settings.py - Line 13
ALLOWED_HOSTS = ['*']  # ⚠️ INSECURE! Accepts any host

# cleantrack/settings.py - Line 73-74
'PASSWORD': 'secure_password_123',  # ⚠️ Hardcoded password
'HOST': 'db',  # ⚠️ Won't work in production
```

#### ✅ Production Fix:

**Update `cleantrack/settings.py`:**

```python
# Security Settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS - Must be configured in production
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database - Use environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='cleantrack'),
        'USER': config('DB_USER', default='cleantrack_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

**Production `.env` (example - DO NOT COMMIT):**

```bash
# Django Settings
DEBUG=False
SECRET_KEY=<generate-new-strong-key>
ALLOWED_HOSTS=cleantrack.com,www.cleantrack.com,cleantrack.onrender.com

# Database (from hosting provider)
DB_NAME=cleantrack_production
DB_USER=cleantrack_prod_user
DB_PASSWORD=<strong-random-password>
DB_HOST=<provider-hostname>
DB_PORT=5432

# Resend
RESEND_API_KEY=<production-key>

# Stripe (PRODUCTION KEYS)
STRIPE_LIVE_SECRET_KEY=sk_live_...
STRIPE_LIVE_PUBLIC_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_LIVE_MODE=True
```

### 2. Generate Strong SECRET_KEY

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Save this in your hosting platform's environment variables, **NEVER** in `.env` file in git.

### 3. HTTPS Configuration (REQUIRED)

Add to `cleantrack/settings.py`:

```python
# Security settings for HTTPS
if not DEBUG:
    # Force HTTPS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Additional security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

    # Proxy headers (for Render, Heroku, etc.)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

---

## 📦 Static Files & Media

### 1. Install WhiteNoise (Recommended)

```bash
pip install whitenoise
```

**Update `requirements.txt`:**
```
whitenoise==6.6.0
```

**Update `cleantrack/settings.py`:**

```python
# Middleware - Add WhiteNoise AFTER SecurityMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest
]

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Media Files (User Uploads)

**Option A: Use AWS S3 (Recommended for production)**

```bash
pip install django-storages boto3
```

```python
# settings.py
if not DEBUG:
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

**Option B: Use persistent volume (Render/Fly.io)**

Configure persistent disk mount in your hosting platform.

---

## 🗄️ Database Backups

### Render.com (Recommended Platform)

Render automatically backs up PostgreSQL databases:
- Daily backups retained for 7 days (Starter plan)
- Point-in-time recovery available (Pro plan)

### Manual Backup Script

Create `scripts/backup_db.sh`:

```bash
#!/bin/bash
# Database backup script

BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="cleantrack_backup_${TIMESTAMP}.sql"

# Create backup directory
mkdir -p $BACKUP_DIR

# Dump database
docker-compose exec -T db pg_dump -U cleantrack_user cleantrack > "$BACKUP_DIR/$BACKUP_FILE"

# Compress
gzip "$BACKUP_DIR/$BACKUP_FILE"

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

**Set up cron job:**
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/scripts/backup_db.sh
```

---

## 🔔 Error Monitoring (Recommended)

### Install Sentry

```bash
pip install sentry-sdk
```

**Update `requirements.txt`:**
```
sentry-sdk==1.40.0
```

**Update `cleantrack/settings.py`:**

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn=config('SENTRY_DSN', default=''),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,  # 10% of transactions
        send_default_pii=False,  # Don't send PII for HIPAA compliance
        environment='production',
    )
```

---

## 💳 Stripe Configuration

### 1. Switch to Live Mode

**In `.env` (production):**
```bash
STRIPE_LIVE_MODE=True
STRIPE_LIVE_SECRET_KEY=sk_live_...
STRIPE_LIVE_PUBLIC_KEY=pk_live_...
```

**Update `cleantrack/settings.py`:**
```python
STRIPE_LIVE_MODE = config('STRIPE_LIVE_MODE', default=False, cast=bool)
```

### 2. Configure Webhook Endpoint

**In Stripe Dashboard:**
1. Go to: https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Endpoint URL: `https://yourdomain.com/billing/webhook/stripe/`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.trial_will_end`
   - `charge.refunded`
5. Copy the signing secret → Add to `.env` as `STRIPE_WEBHOOK_SECRET`

---

## 🌐 Domain & DNS Configuration

### 1. Domain Setup

**Example for Render.com:**

1. **Add custom domain in Render dashboard**
2. **Configure DNS records:**

```
Type    Name    Value                       TTL
A       @       76.76.21.21                 3600
CNAME   www     cleantrack.onrender.com     3600
```

3. **SSL Certificate:** Render automatically provisions Let's Encrypt SSL

### 2. Update ALLOWED_HOSTS

```python
ALLOWED_HOSTS = [
    'cleantrack.com',
    'www.cleantrack.com',
    'cleantrack.onrender.com',  # Render subdomain
]
```

---

## 🚢 Deployment Platforms

### Option 1: Render.com (Recommended)

**Pros:**
- ✅ Free PostgreSQL database (512 MB)
- ✅ Automatic SSL certificates
- ✅ Easy deployments from GitHub
- ✅ Automatic daily backups
- ✅ Environment variables management
- ✅ Good for Django apps

**Setup:**

1. Create `render.yaml`:

```yaml
databases:
  - name: cleantrack-db
    databaseName: cleantrack
    user: cleantrack_user
    plan: starter  # Free tier

services:
  - type: web
    name: cleantrack-web
    env: python
    plan: starter  # $7/month
    buildCommand: "./build.sh"
    startCommand: "gunicorn cleantrack.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: cleantrack-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
```

2. Create `build.sh`:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

3. Update `requirements.txt`:

```
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
```

### Option 2: Railway.app

Similar to Render, with different pricing.

### Option 3: Fly.io

More control, requires Dockerfile.

### Option 4: AWS/DigitalOcean

Full control, requires more DevOps knowledge.

---

## 🔍 Pre-Deploy Testing

### 1. Test with DEBUG=False Locally

```bash
# In .env
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Collect static files
docker-compose exec web python manage.py collectstatic --no-input

# Test
docker-compose restart web
```

Visit: http://localhost:8000

### 2. Run Django System Checks

```bash
docker-compose exec web python manage.py check --deploy
```

**Expected warnings to fix:**
- SECURE_SSL_REDIRECT
- SESSION_COOKIE_SECURE
- CSRF_COOKIE_SECURE
- SECURE_HSTS_SECONDS

### 3. Test Database Migrations

```bash
docker-compose exec web python manage.py showmigrations
docker-compose exec web python manage.py migrate --plan
```

---

## 📊 Post-Deploy Verification

### Immediate Checks (First 5 minutes)

- [ ] Site loads with HTTPS
- [ ] Admin login works
- [ ] Static files load (CSS, JS)
- [ ] Database connection works
- [ ] Can create a facility
- [ ] Can create equipment
- [ ] Can create cleaning log
- [ ] Stripe webhooks receiving events

### First Hour Checks

- [ ] Email notifications working (Resend)
- [ ] User registration works
- [ ] Password reset works
- [ ] QR codes generate correctly
- [ ] Image uploads work
- [ ] All admin pages accessible

### First Day Checks

- [ ] Monitor error logs (Sentry)
- [ ] Check database performance
- [ ] Verify backup ran successfully
- [ ] Test payment flow end-to-end
- [ ] Load test with multiple users

---

## ⚠️ Critical Issues to Fix Before Production

### 1. SECURITY: Admin Permissions NOT Implemented

**Current risk:** All users can see all data in admin

**Fix required:** Implement multi-tenant filtering

**See:** `MULTI_TENANT_PERMISSIONS_TEST_GUIDE.md`

**Priority:** 🔴 CRITICAL - Must fix before production

### 2. DATABASE: Hardcoded Credentials

**Current:**
```python
'PASSWORD': 'secure_password_123',  # ⚠️ In code
```

**Fix:** Move to environment variables (see Security section above)

**Priority:** 🔴 CRITICAL

### 3. HOSTS: Wildcard Allowed

**Current:**
```python
ALLOWED_HOSTS = ['*']  # Accepts any host
```

**Fix:** Use specific domains

**Priority:** 🔴 CRITICAL

---

## 📝 Production Environment Variables Template

Create this in your hosting platform (Render, Railway, etc.):

```bash
# ============================================
# CLEANTRACK PRODUCTION ENVIRONMENT VARIABLES
# ============================================

# Django Core
DEBUG=False
SECRET_KEY=<generate-with-get_random_secret_key>
ALLOWED_HOSTS=cleantrack.com,www.cleantrack.com,cleantrack.onrender.com

# Database (provided by hosting platform)
DB_NAME=cleantrack_production
DB_USER=cleantrack_prod_user
DB_PASSWORD=<auto-generated-by-platform>
DB_HOST=<hostname-from-platform>
DB_PORT=5432

# Email (Resend)
RESEND_API_KEY=<production-key-from-resend>

# Stripe (PRODUCTION KEYS!)
STRIPE_LIVE_MODE=True
STRIPE_LIVE_SECRET_KEY=sk_live_...
STRIPE_LIVE_PUBLIC_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# AWS S3 (if using for media)
AWS_ACCESS_KEY_ID=<your-aws-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret>
AWS_STORAGE_BUCKET_NAME=cleantrack-media
AWS_S3_REGION_NAME=us-east-1

# Sentry (error monitoring)
SENTRY_DSN=https://...@sentry.io/...

# Site Configuration
SITE_ID=1
```

---

## 🎯 Deployment Workflow

### 1. Prepare Code

```bash
# Update dependencies
pip freeze > requirements.txt

# Run tests (if you have them)
python manage.py test

# Check for issues
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --no-input
```

### 2. Push to GitHub

```bash
git add .
git commit -m "Production deployment preparation"
git push origin main
```

### 3. Deploy to Platform

**Render.com:**
- Push triggers automatic deployment
- Monitor logs in dashboard

**Manual:**
```bash
# SSH to server
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
sudo systemctl restart gunicorn
```

### 4. Run Migrations

```bash
# On platform (Render runs automatically)
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Verify Deployment

- Check HTTPS
- Test login
- Create test data
- Monitor logs

---

## 📞 Support & Next Steps

**What to do now:**

1. ✅ **Fix critical security issues** (see section above)
2. ✅ **Choose hosting platform** (Render.com recommended)
3. ✅ **Set up environment variables** (never commit secrets)
4. ✅ **Configure HTTPS** (required for Stripe)
5. ✅ **Set up database backups**
6. ✅ **Implement admin permissions** (see MULTI_TENANT_PERMISSIONS_TEST_GUIDE.md)
7. ✅ **Test thoroughly** before going live

**I can help with:**

- Updating settings.py for production
- Creating build scripts
- Setting up CI/CD
- Implementing admin permissions
- Configuring monitoring
- Performance optimization

---

**Last Updated:** 2025-01-21
**Project Status:** Ready for production prep
**Deployment Target:** Render.com, Railway, or Fly.io
