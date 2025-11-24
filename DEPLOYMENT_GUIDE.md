# 🚀 CleanTrack Deployment Guide

Complete production deployment guide for CleanTrack.

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Deploy to Render.com](#deploy-to-rendercom)
3. [Deploy to Railway](#deploy-to-railway)
4. [Deploy to Fly.io](#deploy-to-flyio)
5. [Deploy to Heroku](#deploy-to-heroku)
6. [Deploy to AWS](#deploy-to-aws)
7. [Post-Deployment](#post-deployment)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Pre-Deployment Checklist

### 1. Code Preparation

- [ ] All tests passing: `python manage.py test`
- [ ] No DEBUG mode: `DEBUG=False` in production settings
- [ ] Secret key generated and secure
- [ ] Database migrations up to date
- [ ] Static files collected
- [ ] Requirements.txt updated
- [ ] .gitignore configured (no secrets in Git)

### 2. Configuration Files

- [ ] `requirements.txt` - Python dependencies
- [ ] `build.sh` - Build script for deployment
- [ ] `render.yaml` - Render infrastructure config (if using Render)
- [ ] `.env.example` - Environment variables template
- [ ] `gunicorn_config.py` - Gunicorn configuration

### 3. Environment Variables

- [ ] `SECRET_KEY` - Django secret (never commit!)
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `ALLOWED_HOSTS` - Production domain(s)
- [ ] `RESEND_API_KEY` - Email service
- [ ] `STRIPE_TEST/LIVE_KEYS` - Payment integration
- [ ] `STRIPE_WEBHOOK_SECRET` - Webhook verification

### 4. Security Review

- [ ] HTTPS enforced (`SECURE_SSL_REDIRECT=True`)
- [ ] HSTS enabled (`SECURE_HSTS_SECONDS=31536000`)
- [ ] CSRF trusted origins configured
- [ ] XSS protection headers enabled
- [ ] No sensitive data in logs
- [ ] Password validation enabled

---

## Deploy to Render.com

**Recommended for:** Quick deployment, free tier available, PostgreSQL included

### Method 1: One-Click Deploy (Blueprint)

**Step 1: Push to GitHub**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**Step 2: Connect Render to GitHub**
1. Go to [render.com](https://render.com)
2. Sign up / Log in
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will detect `render.yaml` and auto-configure

**Step 3: Review Configuration**
Render will create:
- PostgreSQL database (`cleantrack-db`)
- Web service (`cleantrack-api`)
- Environment variables (auto-populated)

**Step 4: Deploy**
- Click "Apply"
- Wait 5-10 minutes for initial deployment
- Access: `https://cleantrack-api.onrender.com`

### Method 2: Manual Setup

**Step 1: Create PostgreSQL Database**
1. Dashboard → "New" → "PostgreSQL"
2. Name: `cleantrack-db`
3. Region: Oregon (US West)
4. Plan: Free
5. Click "Create Database"
6. Copy `Internal Database URL`

**Step 2: Create Web Service**
1. Dashboard → "New" → "Web Service"
2. Connect GitHub repository
3. Configure:
   - **Name:** cleantrack-api
   - **Region:** Oregon (US West)
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn cleantrack.wsgi:application`
   - **Plan:** Free (or Starter $7/month for production)

**Step 3: Add Environment Variables**
Go to "Environment" tab and add:

```bash
# Django
DJANGO_SETTINGS_MODULE=cleantrack.settings_production
DEBUG=False
SECRET_KEY=  # Click "Generate Value"
ALLOWED_HOSTS=.onrender.com
PYTHON_VERSION=3.10.0

# Database
DATABASE_URL=  # Paste Internal Database URL from Step 1

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://*.onrender.com

# Site
SITE_URL=https://cleantrack-api.onrender.com
SITE_ID=1

# Email (Resend)
RESEND_API_KEY=re_your_key_here
DEFAULT_FROM_EMAIL=noreply@cleantrack.com

# Stripe
STRIPE_TEST_PUBLIC_KEY=pk_test_xxx
STRIPE_TEST_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_LIVE_MODE=False

# Locale
LANGUAGE_CODE=en-us
TIME_ZONE=America/Sao_Paulo
```

**Step 4: Deploy**
1. Click "Create Web Service"
2. Deployment starts automatically
3. View logs in real-time
4. Access: `https://cleantrack-api.onrender.com`

**Step 5: Create Superuser**
```bash
# Open Shell from Render Dashboard
python manage.py createsuperuser
```

### build.sh Content
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput --clear
```

### render.yaml Content
```yaml
databases:
  - name: cleantrack-db
    databaseName: cleantrack
    user: cleantrack
    region: oregon

services:
  - type: web
    name: cleantrack-api
    runtime: python
    region: oregon
    plan: free
    branch: main
    buildCommand: "./build.sh"
    startCommand: "gunicorn cleantrack.wsgi:application"
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: cleantrack.settings_production
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: cleantrack-db
          property: connectionString
      - key: PYTHON_VERSION
        value: 3.10.0
```

---

## Deploy to Railway

**Recommended for:** Simple deployment, PostgreSQL plugin, generous free tier

### Step 1: Install Railway CLI
```bash
# macOS
brew install railway

# npm
npm i -g @railway/cli

# Verify
railway --version
```

### Step 2: Login
```bash
railway login
```

### Step 3: Initialize Project
```bash
cd CleanTrack
railway init
```

### Step 4: Add PostgreSQL
```bash
railway add postgresql
```

### Step 5: Create Procfile
```bash
echo "web: gunicorn cleantrack.wsgi:application" > Procfile
```

### Step 6: Set Environment Variables
```bash
railway variables set DJANGO_SETTINGS_MODULE=cleantrack.settings_production
railway variables set DEBUG=False
railway variables set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
railway variables set RESEND_API_KEY=re_your_key_here
# ... add all other variables
```

### Step 7: Deploy
```bash
railway up
```

### Step 8: Get URL
```bash
railway domain
```

### Step 9: Run Migrations
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

## Deploy to Fly.io

**Recommended for:** Global edge deployment, Dockerfile-based

### Step 1: Install Fly CLI
```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Sign Up / Login
```bash
fly auth signup
# or
fly auth login
```

### Step 3: Launch App
```bash
cd CleanTrack
fly launch

# Answer prompts:
# App name: cleantrack-api
# Region: Choose closest to users
# PostgreSQL: Yes (create Postgres cluster)
# Redis: Optional (for caching)
```

### Step 4: Configure fly.toml
```toml
app = "cleantrack-api"
primary_region = "sjc"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"
  DJANGO_SETTINGS_MODULE = "cleantrack.settings_production"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

### Step 5: Set Secrets
```bash
fly secrets set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
fly secrets set RESEND_API_KEY=re_your_key_here
fly secrets set STRIPE_TEST_SECRET_KEY=sk_test_xxx
# ... other secrets
```

### Step 6: Deploy
```bash
fly deploy
```

### Step 7: Scale (if needed)
```bash
# Scale to 2 instances
fly scale count 2

# Scale VM size
fly scale vm shared-cpu-1x --memory 1024
```

### Step 8: Open App
```bash
fly open
```

---

## Deploy to Heroku

**Recommended for:** Traditional PaaS, many addons available

### Step 1: Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Other platforms
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login
```bash
heroku login
```

### Step 3: Create App
```bash
cd CleanTrack
heroku create cleantrack-api
```

### Step 4: Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

### Step 5: Create Procfile
```bash
echo "web: gunicorn cleantrack.wsgi:application --log-file -" > Procfile
```

### Step 6: Create runtime.txt
```bash
echo "python-3.10.13" > runtime.txt
```

### Step 7: Set Config Vars
```bash
heroku config:set DJANGO_SETTINGS_MODULE=cleantrack.settings_production
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set RESEND_API_KEY=re_your_key_here
# ... other variables
```

### Step 8: Deploy
```bash
git push heroku main
```

### Step 9: Run Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Step 10: Open App
```bash
heroku open
```

---

## Deploy to AWS

**Recommended for:** Enterprise deployment, full control, scalability

### Architecture Options

#### Option 1: Elastic Beanstalk (Simple)
- Managed service (like Heroku)
- Auto-scaling
- Load balancing
- RDS PostgreSQL integration

#### Option 2: ECS Fargate (Container)
- Docker-based
- Serverless containers
- More control than Beanstalk

#### Option 3: EC2 + nginx (Full Control)
- Maximum flexibility
- Requires manual setup
- Custom configuration

### Deploy to Elastic Beanstalk

**Step 1: Install EB CLI**
```bash
pip install awsebcli
```

**Step 2: Initialize**
```bash
cd CleanTrack
eb init

# Select:
# - Application name: cleantrack
# - Platform: Python 3.10
# - Region: us-west-2
```

**Step 3: Create Environment**
```bash
eb create cleantrack-production \
  --database.engine postgres \
  --database.instance db.t3.micro \
  --envvars DJANGO_SETTINGS_MODULE=cleantrack.settings_production,DEBUG=False
```

**Step 4: Configure .ebextensions**
Create `.ebextensions/django.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: cleantrack.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: cleantrack.settings_production
    DEBUG: False

container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate --noinput"
    leader_only: true
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"
```

**Step 5: Deploy**
```bash
eb deploy
```

**Step 6: Open**
```bash
eb open
```

---

## Post-Deployment

### 1. Configure Custom Domain

**Render.com:**
1. Dashboard → Web Service → Settings
2. Add custom domain: `app.cleantrack.com`
3. Add DNS records (provided by Render)
4. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`

**DNS Records:**
```
Type: CNAME
Name: app
Value: cleantrack-api.onrender.com
TTL: 3600
```

### 2. Configure Stripe Webhooks

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://app.cleantrack.com/webhooks/stripe/`
3. Select events:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
4. Copy webhook secret
5. Update environment variable: `STRIPE_WEBHOOK_SECRET`

### 3. Test Stripe Webhook

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Forward webhooks to local
stripe listen --forward-to https://app.cleantrack.com/webhooks/stripe/

# Trigger test event
stripe trigger customer.subscription.created
```

### 4. Create Superuser

```bash
# Render
# Use Shell from dashboard

# Railway
railway run python manage.py createsuperuser

# Fly.io
fly ssh console -C "python manage.py createsuperuser"

# Heroku
heroku run python manage.py createsuperuser
```

### 5. Verify Deployment

- [ ] Homepage loads: `https://app.cleantrack.com`
- [ ] Admin login works: `https://app.cleantrack.com/admin/`
- [ ] Static files load (CSS/JS)
- [ ] Database queries work
- [ ] Email sending works (test registration)
- [ ] Stripe webhooks work
- [ ] QR code generation works
- [ ] File uploads work (cleaning photos)

---

## Monitoring & Maintenance

### Application Monitoring

**Sentry (Error Tracking)**
```bash
pip install sentry-sdk

# In settings_production.py
import sentry_sdk
sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    traces_sample_rate=1.0,
)
```

**New Relic (APM)**
```bash
pip install newrelic

# Start with New Relic
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn cleantrack.wsgi:application
```

### Database Backups

**Render.com:**
- Automatic daily backups (free tier: 7 days retention)
- Manual backup: Dashboard → Database → Backups → Create Backup

**Railway:**
```bash
railway run pg_dump $DATABASE_URL > backup.sql
```

**Fly.io:**
```bash
fly postgres backup create
fly postgres backup list
```

### Log Monitoring

**View Logs:**
```bash
# Render
# Dashboard → Logs

# Railway
railway logs

# Fly.io
fly logs

# Heroku
heroku logs --tail
```

**Log Aggregation:**
- Papertrail (free tier available)
- Logtail
- Datadog

### Uptime Monitoring

**Services:**
- [UptimeRobot](https://uptimerobot.com) - Free for 50 monitors
- [Pingdom](https://pingdom.com)
- [StatusCake](https://statuscake.com)

**Configuration:**
- Monitor URL: `https://app.cleantrack.com/health/`
- Check interval: 5 minutes
- Alert: Email + SMS

### Performance Monitoring

**Database Query Optimization:**
```bash
# Enable query logging in production
# settings_production.py
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
}
```

**Use Django Debug Toolbar (staging only):**
```bash
pip install django-debug-toolbar
```

---

## Scaling

### Horizontal Scaling

**Render:**
- Dashboard → Service → Scaling
- Increase instance count

**Railway:**
```bash
railway scale --replicas 3
```

**Fly.io:**
```bash
fly scale count 3
```

### Vertical Scaling

**Render:**
- Upgrade to Starter plan ($7/month)
- More CPU + RAM

**Fly.io:**
```bash
fly scale vm shared-cpu-2x --memory 2048
```

### Database Scaling

- Read replicas (for heavy read workloads)
- Connection pooling (PgBouncer)
- Query optimization (indexes, select_related)

---

## Rollback

### Render.com
1. Dashboard → Deploys
2. Click "Rollback" on previous successful deploy

### Railway
```bash
railway rollback
```

### Fly.io
```bash
fly releases
fly deploy --image registry.fly.io/cleantrack-api:v2
```

### Heroku
```bash
heroku releases
heroku rollback v42
```

---

## Security Checklist

- [ ] HTTPS enforced
- [ ] Security headers enabled (HSTS, X-Frame-Options, CSP)
- [ ] CSRF protection enabled
- [ ] SQL injection protection (use ORM)
- [ ] XSS protection (escape user input)
- [ ] Secrets in environment variables (not in code)
- [ ] Database backups enabled
- [ ] Monitoring and alerting configured
- [ ] Rate limiting enabled
- [ ] Regular dependency updates (`pip-audit`)

---

## Troubleshooting

### Static Files Not Loading

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Verify STATIC_ROOT in settings
# Ensure WhiteNoise is in MIDDLEWARE
```

### Database Connection Error

**Solution:**
```bash
# Verify DATABASE_URL
echo $DATABASE_URL

# Check database is running
# Render: Dashboard → Database → Status

# Test connection
python manage.py dbshell
```

### Application Crashes

**Solution:**
```bash
# View logs
# Render: Dashboard → Logs
# Railway: railway logs
# Fly.io: fly logs

# Check for errors in:
# - Migrations
# - Environment variables
# - Dependencies
```

---

## Support

**Need help with deployment?**
- Email: natyssis23@gmail.com
- Documentation: https://cleantrack.com/docs
- GitHub Issues: https://github.com/yourusername/cleantrack/issues

---

*Last Updated: January 2025 | CleanTrack Deployment Guide v1.0*
