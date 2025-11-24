# 🚀 CleanTrack Production Deployment Guide

Complete guide to deploy CleanTrack Django application to production using **Nginx + Gunicorn + PostgreSQL + Redis** on Ubuntu/Debian Linux.

---

## 📋 Table of Contents

1. [Server Requirements](#server-requirements)
2. [Initial Server Setup](#initial-server-setup)
3. [Database Setup (PostgreSQL)](#database-setup-postgresql)
4. [Redis Setup](#redis-setup)
5. [Application Deployment](#application-deployment)
6. [Nginx Configuration](#nginx-configuration)
7. [SSL Certificate (Let's Encrypt)](#ssl-certificate-lets-encrypt)
8. [Systemd Service](#systemd-service)
9. [Post-Deployment](#post-deployment)
10. [Maintenance & Updates](#maintenance--updates)

---

## 🖥️ Server Requirements

### Minimum Specifications:
- **CPU**: 2 cores
- **RAM**: 2 GB
- **Storage**: 20 GB SSD
- **OS**: Ubuntu 22.04 LTS or Debian 11+

### Required Software:
- Python 3.10+
- PostgreSQL 14+
- Redis 6+
- Nginx 1.18+
- Git

---

## 🔧 Initial Server Setup

### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Required Packages

```bash
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    redis-server \
    nginx \
    git \
    build-essential \
    libpq-dev \
    python3-dev \
    supervisor \
    certbot \
    python3-certbot-nginx
```

### 3. Create CleanTrack User

```bash
sudo useradd -m -s /bin/bash cleantrack
sudo usermod -aG sudo cleantrack  # Optional: for deployment tasks
```

### 4. Create Required Directories

```bash
sudo mkdir -p /opt/cleantrack
sudo mkdir -p /var/log/cleantrack
sudo mkdir -p /var/run/cleantrack
sudo chown -R cleantrack:cleantrack /opt/cleantrack
sudo chown -R cleantrack:cleantrack /var/log/cleantrack
sudo chown -R cleantrack:cleantrack /var/run/cleantrack
```

---

## 🗄️ Database Setup (PostgreSQL)

### 1. Switch to PostgreSQL User

```bash
sudo -u postgres psql
```

### 2. Create Database and User

```sql
CREATE DATABASE cleantrack_prod;
CREATE USER cleantrack_user WITH PASSWORD 'your_strong_password_here';

-- Grant privileges
ALTER ROLE cleantrack_user SET client_encoding TO 'utf8';
ALTER ROLE cleantrack_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cleantrack_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE cleantrack_prod TO cleantrack_user;

-- Exit
\q
```

### 3. Test Connection

```bash
psql -U cleantrack_user -d cleantrack_prod -h localhost
# Enter password when prompted
# If successful, type \q to exit
```

---

## 🔴 Redis Setup

### 1. Start and Enable Redis

```bash
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 2. Verify Redis is Running

```bash
redis-cli ping
# Should return: PONG
```

### 3. Configure Redis (Optional)

Edit `/etc/redis/redis.conf`:

```bash
sudo nano /etc/redis/redis.conf
```

Set:
```
maxmemory 256mb
maxmemory-policy allkeys-lru
```

Restart:
```bash
sudo systemctl restart redis-server
```

---

## 📦 Application Deployment

### 1. Clone Repository

```bash
cd /opt/cleantrack
sudo -u cleantrack git clone https://github.com/yourusername/cleantrack.git .
```

### 2. Create Virtual Environment

```bash
sudo -u cleantrack python3.10 -m venv venv
sudo -u cleantrack venv/bin/pip install --upgrade pip
```

### 3. Install Dependencies

```bash
sudo -u cleantrack venv/bin/pip install -r requirements.txt
```

### 4. Create Production Environment File

```bash
sudo -u cleantrack cp .env.production.example .env.production
sudo -u cleantrack nano .env.production
```

**Fill in all values:**
```env
DEBUG=False
SECRET_KEY=<generate-new-secret-key>
ALLOWED_HOSTS=cleantrack.com,www.cleantrack.com,your-server-ip
DJANGO_SETTINGS_MODULE=cleantrack.settings_production

DB_NAME=cleantrack_prod
DB_USER=cleantrack_user
DB_PASSWORD=your_strong_password_here
DB_HOST=localhost
DB_PORT=5432

# ... (complete all other values)
```

### 5. Generate New SECRET_KEY

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run Migrations

```bash
cd /opt/cleantrack
sudo -u cleantrack venv/bin/python manage.py migrate --settings=cleantrack.settings_production
```

### 7. Collect Static Files

```bash
sudo -u cleantrack venv/bin/python manage.py collectstatic --noinput --settings=cleantrack.settings_production
```

### 8. Create Superuser

```bash
sudo -u cleantrack venv/bin/python manage.py createsuperuser --settings=cleantrack.settings_production
```

---

## 🌐 Nginx Configuration

### 1. Copy Nginx Configuration

```bash
sudo cp /opt/cleantrack/nginx_cleantrack.conf /etc/nginx/sites-available/cleantrack
```

### 2. Create Symlink

```bash
sudo ln -s /etc/nginx/sites-available/cleantrack /etc/nginx/sites-enabled/
```

### 3. Remove Default Site

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

### 4. Test Nginx Configuration

```bash
sudo nginx -t
```

### 5. Reload Nginx

```bash
sudo systemctl reload nginx
```

---

## 🔒 SSL Certificate (Let's Encrypt)

### 1. Obtain SSL Certificate

```bash
sudo certbot --nginx -d cleantrack.com -d www.cleantrack.com
```

Follow the prompts:
- Enter your email
- Agree to terms of service
- Choose whether to redirect HTTP to HTTPS (recommended: Yes)

### 2. Test Auto-Renewal

```bash
sudo certbot renew --dry-run
```

### 3. Certificate Auto-Renewal

Certbot automatically sets up a cron job. Verify:

```bash
sudo systemctl list-timers | grep certbot
```

---

## ⚙️ Systemd Service

### 1. Copy Service File

```bash
sudo cp /opt/cleantrack/cleantrack.service /etc/systemd/system/
```

### 2. Reload Systemd

```bash
sudo systemctl daemon-reload
```

### 3. Enable and Start Service

```bash
sudo systemctl enable cleantrack
sudo systemctl start cleantrack
```

### 4. Check Service Status

```bash
sudo systemctl status cleantrack
```

Expected output:
```
● cleantrack.service - CleanTrack Django Application
     Loaded: loaded (/etc/systemd/system/cleantrack.service)
     Active: active (running)
```

### 5. View Logs

```bash
# Service logs
sudo journalctl -u cleantrack -f

# Application logs
tail -f /var/log/cleantrack/gunicorn_error.log
tail -f /var/log/cleantrack/gunicorn_access.log
```

---

## ✅ Post-Deployment

### 1. Verify Application is Running

```bash
# Check if gunicorn socket exists
ls -la /var/run/cleantrack/cleantrack.sock

# Test nginx upstream
sudo nginx -T | grep cleantrack
```

### 2. Access Admin Panel

Open browser: `https://cleantrack.com/admin/`

Login with the superuser credentials you created.

### 3. Configure Stripe Webhooks

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://cleantrack.com/billing/webhooks/stripe/`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
4. Copy webhook signing secret
5. Update `.env.production`:
   ```
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
   ```
6. Restart service:
   ```bash
   sudo systemctl restart cleantrack
   ```

### 4. Test Email Sending

```bash
sudo -u cleantrack venv/bin/python manage.py shell --settings=cleantrack.settings_production
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email from CleanTrack',
    'This is a test email.',
    'noreply@cleantrack.com',
    ['your@email.com'],
    fail_silently=False,
)
```

### 5. Monitor Resources

```bash
# Check disk usage
df -h

# Check memory
free -h

# Check running processes
ps aux | grep gunicorn
```

---

## 🔄 Maintenance & Updates

### Deploy Updates (Using deploy.sh)

```bash
cd /opt/cleantrack
sudo ./deploy.sh
```

### Manual Update Steps

```bash
# 1. Pull latest code
cd /opt/cleantrack
sudo -u cleantrack git pull origin main

# 2. Activate venv
source venv/bin/activate

# 3. Update dependencies
pip install -r requirements.txt --upgrade

# 4. Run migrations
python manage.py migrate --settings=cleantrack.settings_production

# 5. Collect static files
python manage.py collectstatic --noinput --settings=cleantrack.settings_production

# 6. Restart service
sudo systemctl restart cleantrack
```

### Database Backup

```bash
# Create backup
sudo -u postgres pg_dump cleantrack_prod > /opt/cleantrack/backups/cleantrack_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
sudo -u postgres psql cleantrack_prod < /opt/cleantrack/backups/cleantrack_20250101_120000.sql
```

### View Application Logs

```bash
# Django application logs
tail -f /opt/cleantrack/logs/app.log
tail -f /opt/cleantrack/logs/error.log

# Gunicorn logs
tail -f /var/log/cleantrack/gunicorn_access.log
tail -f /var/log/cleantrack/gunicorn_error.log

# Nginx logs
tail -f /var/log/nginx/cleantrack_access.log
tail -f /var/log/nginx/cleantrack_error.log

# Systemd service logs
sudo journalctl -u cleantrack -f
```

### Restart Services

```bash
# Restart CleanTrack
sudo systemctl restart cleantrack

# Restart Nginx
sudo systemctl restart nginx

# Restart Redis
sudo systemctl restart redis-server

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## 📁 Folder Structure

```
/opt/cleantrack/
├── cleantrack/              # Django project settings
│   ├── settings.py          # Base settings
│   ├── settings_production.py  # Production settings
│   ├── urls.py
│   └── wsgi.py
├── apps/                    # Django applications
│   ├── accounts/
│   ├── facilities/
│   ├── equipment/
│   ├── cleaning_logs/
│   ├── billing/
│   ├── notifications/
│   └── documentation/
├── staticfiles/             # Collected static files
├── media/                   # User uploads
├── logs/                    # Application logs
│   ├── app.log
│   └── error.log
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── gunicorn_config.py       # Gunicorn configuration
├── .env.production          # Environment variables (SECRET!)
├── manage.py                # Django management script
└── deploy.sh                # Deployment script

/etc/nginx/
└── sites-available/
    └── cleantrack           # Nginx configuration

/etc/systemd/system/
└── cleantrack.service       # Systemd service file

/var/log/cleantrack/
├── gunicorn_access.log
└── gunicorn_error.log

/var/run/cleantrack/
├── cleantrack.sock          # Unix socket
└── gunicorn.pid             # PID file
```

---

## 🆘 Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status cleantrack

# View detailed logs
sudo journalctl -xe -u cleantrack

# Check permissions
ls -la /opt/cleantrack
ls -la /var/run/cleantrack
```

### 502 Bad Gateway

```bash
# Check if gunicorn is running
ps aux | grep gunicorn

# Check socket file exists
ls -la /var/run/cleantrack/cleantrack.sock

# Verify nginx can connect
sudo nginx -t

# Check nginx error log
tail -f /var/log/nginx/cleantrack_error.log
```

### Static Files Not Loading

```bash
# Collect static files again
sudo -u cleantrack venv/bin/python manage.py collectstatic --clear --noinput --settings=cleantrack.settings_production

# Check permissions
ls -la /opt/cleantrack/staticfiles/

# Verify nginx can read static files
sudo -u www-data ls /opt/cleantrack/staticfiles/
```

### Database Connection Errors

```bash
# Test database connection
sudo -u cleantrack venv/bin/python manage.py dbshell --settings=cleantrack.settings_production

# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify credentials in .env.production
```

---

## 🎉 Success!

Your CleanTrack application is now running in production!

- **Website**: https://cleantrack.com
- **Admin Panel**: https://cleantrack.com/admin/
- **API**: https://cleantrack.com/api/ (if enabled)

---

## 📞 Support

For issues or questions:
- Check logs first (see Maintenance section)
- Review Django documentation: https://docs.djangoproject.com/
- Contact support: admin@cleantrack.com

---

**Last Updated**: 2025-11-24
**Version**: 1.0.0
