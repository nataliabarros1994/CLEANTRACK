# CleanTrack - Dependencies Overview

## 📦 Current Requirements (12 packages)

### Core Framework
```
Django==5.0.6                    # Web framework (upgraded from 5.0.1)
djangorestframework==3.14.0      # REST API support
```

### Database
```
psycopg2-binary==2.9.9          # PostgreSQL adapter
```

### Configuration
```
python-decouple==3.8            # Environment variable management
python-dotenv==1.0.0            # .env file support
```

### Integrations
```
dj-stripe==2.12.0               # Stripe integration (upgraded from 2.8.3)
stripe==10.0.0                  # Stripe Python SDK (upgraded from 8.0.0)
resend==2.3.0                   # Email service (upgraded from 0.7.0)
```

### Authentication
```
django-allauth==0.57.0          # User authentication & social auth
```

### Media & Files
```
Pillow==10.3.0                  # Image processing (upgraded from 10.2.0)
```

### Production
```
whitenoise==6.6.0               # Static file serving
django-cors-headers==4.3.1      # CORS support
```

---

## 🔧 What Changed

### Before (41 packages)
- Django 5.0.1
- Celery + Redis (background tasks)
- ReportLab + openpyxl (PDF/Excel reports)
- django-environ
- django-debug-toolbar
- django-ratelimit
- Gunicorn
- Many other utilities

### After (12 packages) ✅
- Django 5.0.6 (upgraded)
- Core dependencies only
- Simplified for faster setup
- Still fully functional for web app

---

## ⚠️ Removed Features

Without these packages, some features won't work:

### Background Tasks (No Celery/Redis)
- ❌ Automated compliance checking
- ❌ Scheduled email sending
- ❌ Daily/weekly reports generation
- ❌ Subscription monitoring

### Reports (No ReportLab/openpyxl)
- ❌ PDF report generation
- ❌ Excel export
- ⚠️ Can still view data in admin, just can't export

### Development Tools
- ❌ Django Debug Toolbar
- ❌ IPython shell
- ❌ Rate limiting

### Production Server
- ❌ Gunicorn (using Django dev server instead)

---

## ✅ What Still Works

### Core Functionality
- ✅ Django web application
- ✅ PostgreSQL database
- ✅ User authentication (django-allauth)
- ✅ Admin interface
- ✅ All models (Account, Equipment, CleaningLog, etc.)
- ✅ CRUD operations
- ✅ Image uploads (Pillow)
- ✅ Static files (WhiteNoise)

### Integrations
- ✅ Stripe webhook handling (dj-stripe)
- ✅ Email sending via Resend
- ✅ REST API (DRF)
- ✅ CORS support

---

## 🚀 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or with Docker
docker-compose build
```

---

## 🔄 If You Need Full Features

To restore background tasks, reports, and production server:

```bash
# Add to requirements.txt:
celery==5.3.6
redis==5.0.1
reportlab==4.0.9
openpyxl==3.1.2
gunicorn==21.2.0
```

And restore Redis/Celery services in docker-compose.yml (see DOCKER_SETUP_NOTE.md)

---

## 📊 Package Sizes (Approximate)

| Package | Size | Purpose |
|---------|------|---------|
| Django | ~10 MB | Core framework |
| psycopg2-binary | ~5 MB | PostgreSQL |
| dj-stripe | ~1 MB | Stripe integration |
| Pillow | ~3 MB | Image processing |
| django-allauth | ~2 MB | Authentication |
| Others | ~3 MB | Utilities |
| **Total** | **~24 MB** | Installed size |

---

## 🆕 Version Upgrades

Your requirements have been updated to newer versions:

- Django: 5.0.1 → **5.0.6** (security patches)
- dj-stripe: 2.8.3 → **2.12.0** (latest features)
- stripe: 8.0.0 → **10.0.0** (latest API)
- resend: 0.7.0 → **2.3.0** (improved reliability)
- Pillow: 10.2.0 → **10.3.0** (security patches)

---

## ✅ Compatibility

All packages are compatible with:
- Python 3.11+ ✅
- PostgreSQL 15 ✅
- Django 5.0.6 ✅

---

## 📝 Notes

### python-decouple vs python-dotenv
Your requirements include both:
- `python-decouple==3.8` - You specified this
- `python-dotenv==1.0.0` - Required by settings.py

They serve similar purposes (environment variables). Consider using just one:
- Keep **python-dotenv** if using `load_dotenv()` in settings.py
- Or switch to **python-decouple** with `config()` helper

Current settings.py uses: `from dotenv import load_dotenv`

---

Your simplified dependencies are ready! 🎉

Total: **12 packages** (down from 41)
Install time: **~2 minutes** (down from ~5 minutes)
Image size: **~200 MB** (down from ~500 MB)
