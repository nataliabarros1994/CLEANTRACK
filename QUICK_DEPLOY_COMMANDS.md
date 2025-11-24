# ⚡ CleanTrack - Quick Deploy Commands

One-page reference for deploying CleanTrack to production.

---

## 🚀 Initial Setup (Run Once)

```bash
# 1. Install dependencies
sudo apt update && sudo apt install -y python3.10 python3.10-venv postgresql redis-server nginx git

# 2. Create user and directories
sudo useradd -m -s /bin/bash cleantrack
sudo mkdir -p /opt/cleantrack /var/log/cleantrack /var/run/cleantrack
sudo chown -R cleantrack:cleantrack /opt/cleantrack /var/log/cleantrack /var/run/cleantrack

# 3. Setup PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE cleantrack_prod;"
sudo -u postgres psql -c "CREATE USER cleantrack_user WITH PASSWORD 'YOUR_PASSWORD';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cleantrack_prod TO cleantrack_user;"

# 4. Clone and setup project
cd /opt/cleantrack
sudo -u cleantrack git clone YOUR_REPO_URL .
sudo -u cleantrack python3.10 -m venv venv
sudo -u cleantrack venv/bin/pip install -r requirements.txt

# 5. Configure environment
sudo -u cleantrack cp .env.production.example .env.production
sudo -u cleantrack nano .env.production  # Fill in all values

# 6. Run migrations and collect static
sudo -u cleantrack venv/bin/python manage.py migrate --settings=cleantrack.settings_production
sudo -u cleantrack venv/bin/python manage.py collectstatic --noinput --settings=cleantrack.settings_production
sudo -u cleantrack venv/bin/python manage.py createsuperuser --settings=cleantrack.settings_production

# 7. Setup Nginx
sudo cp nginx_cleantrack.conf /etc/nginx/sites-available/cleantrack
sudo ln -s /etc/nginx/sites-available/cleantrack /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 8. Setup SSL (Let's Encrypt)
sudo certbot --nginx -d cleantrack.com -d www.cleantrack.com

# 9. Setup systemd service
sudo cp cleantrack.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cleantrack
sudo systemctl start cleantrack
```

---

## 🔄 Regular Updates

```bash
cd /opt/cleantrack
sudo ./deploy.sh
```

**OR manually:**

```bash
cd /opt/cleantrack
sudo -u cleantrack git pull
sudo -u cleantrack venv/bin/pip install -r requirements.txt --upgrade
sudo -u cleantrack venv/bin/python manage.py migrate --settings=cleantrack.settings_production
sudo -u cleantrack venv/bin/python manage.py collectstatic --noinput --settings=cleantrack.settings_production
sudo systemctl restart cleantrack
```

---

## 📊 Monitor & Debug

```bash
# Service status
sudo systemctl status cleantrack

# View logs
sudo journalctl -u cleantrack -f
tail -f /var/log/cleantrack/gunicorn_error.log
tail -f /var/log/nginx/cleantrack_error.log

# Check processes
ps aux | grep gunicorn
ls -la /var/run/cleantrack/cleantrack.sock

# Test configuration
sudo nginx -t
python manage.py check --deploy --settings=cleantrack.settings_production
```

---

## 🛑 Start/Stop/Restart

```bash
# CleanTrack service
sudo systemctl start cleantrack
sudo systemctl stop cleantrack
sudo systemctl restart cleantrack

# Nginx
sudo systemctl reload nginx
sudo systemctl restart nginx

# PostgreSQL
sudo systemctl restart postgresql

# Redis
sudo systemctl restart redis-server
```

---

## 🗄️ Database Commands

```bash
# Backup
sudo -u postgres pg_dump cleantrack_prod > backup_$(date +%Y%m%d).sql

# Restore
sudo -u postgres psql cleantrack_prod < backup_20250101.sql

# Connect to database
sudo -u postgres psql cleantrack_prod
```

---

## 🔐 Security Checklist

- ✅ DEBUG=False in production
- ✅ Strong SECRET_KEY (never reuse from dev)
- ✅ ALLOWED_HOSTS configured
- ✅ SSL certificate installed
- ✅ HTTPS redirect enabled
- ✅ Database password is strong
- ✅ Firewall configured (UFW)
- ✅ Regular backups enabled
- ✅ .env.production not in git

---

## 📍 Important Paths

| Item | Path |
|------|------|
| Project | `/opt/cleantrack` |
| Venv | `/opt/cleantrack/venv` |
| Static files | `/opt/cleantrack/staticfiles` |
| Media files | `/opt/cleantrack/media` |
| Logs | `/var/log/cleantrack` |
| Socket | `/var/run/cleantrack/cleantrack.sock` |
| Nginx config | `/etc/nginx/sites-available/cleantrack` |
| Systemd service | `/etc/systemd/system/cleantrack.service` |
| SSL certs | `/etc/letsencrypt/live/cleantrack.com/` |

---

## 🆘 Emergency Fixes

**502 Bad Gateway:**
```bash
sudo systemctl restart cleantrack
sudo systemctl restart nginx
```

**Static files not loading:**
```bash
sudo -u cleantrack venv/bin/python manage.py collectstatic --clear --noinput --settings=cleantrack.settings_production
sudo systemctl restart nginx
```

**Database connection error:**
```bash
sudo systemctl status postgresql
# Check .env.production credentials
```

---

**For full documentation, see: PRODUCTION_DEPLOYMENT_GUIDE.md**
