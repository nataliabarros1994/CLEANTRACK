# 📦 CleanTrack Installation Guide

Complete step-by-step installation guide for CleanTrack healthcare compliance platform.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Setup](#docker-setup)
4. [Configuration](#configuration)
5. [Database Setup](#database-setup)
6. [Running the Application](#running-the-application)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

**Python 3.10 or higher**
```bash
# Check Python version
python3 --version

# If not installed, download from python.org
# or use package manager:
sudo apt install python3.10 python3-pip python3-venv  # Ubuntu/Debian
brew install python@3.10  # macOS
```

**PostgreSQL 15+ (Production)**
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql@15

# Start PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql@15  # macOS
```

**Git**
```bash
# Check if installed
git --version

# Install if needed
sudo apt install git  # Ubuntu/Debian
brew install git  # macOS
```

### Optional but Recommended

- **virtualenv**: Python environment isolation
- **Docker & Docker Compose**: Containerized deployment
- **Redis**: Caching and background tasks (optional)

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
# Clone from GitHub (replace with your repo URL)
git clone https://github.com/yourusername/cleantrack.git

# Navigate to project directory
cd CleanTrack

# Check directory contents
ls -la
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Verify activation (you should see (venv) in prompt)
which python  # Should point to venv/bin/python
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages:**
- Django 5.0.6
- psycopg2-binary 2.9.9
- dj-stripe 2.8.3
- Pillow 10.2.0
- qrcode 7.4.2
- reportlab 4.1.0
- resend 0.8.0
- And more...

### Step 4: Configure Environment Variables

Create `.env` file in project root:

```bash
# Copy example file
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

**Minimum required variables:**

```bash
# Django Core
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Email (Resend API)
RESEND_API_KEY=re_your_api_key_here
DEFAULT_FROM_EMAIL=noreply@cleantrack.com
SERVER_EMAIL=server@cleantrack.com

# Stripe (Test Mode)
STRIPE_TEST_PUBLIC_KEY=pk_test_51xxxxx
STRIPE_TEST_SECRET_KEY=sk_test_51xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
STRIPE_LIVE_MODE=False

# Site Configuration
SITE_URL=http://localhost:8000
SITE_ID=1
LANGUAGE_CODE=en-us
TIME_ZONE=America/Sao_Paulo
```

**Generate SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 5: Database Setup

**For SQLite (Development):**
```bash
# Run migrations (creates db.sqlite3 automatically)
python manage.py migrate
```

**For PostgreSQL (Production-like):**
```bash
# Create database
sudo -u postgres psql
CREATE DATABASE cleantrack;
CREATE USER cleantrack_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE cleantrack TO cleantrack_user;
\q

# Update .env
DATABASE_URL=postgresql://cleantrack_user:your_password@localhost:5432/cleantrack

# Run migrations
python manage.py migrate
```

### Step 6: Create Superuser

```bash
python manage.py createsuperuser

# Enter details:
Email: admin@cleantrack.com
First name: Admin
Last name: User
Password: ********
Password (again): ********
```

### Step 7: Load Test Data (Optional)

```bash
# Generate test facilities, equipment, and logs
python create_test_data.py

# This creates:
# - 2 test facilities
# - 5 equipment items per facility
# - Sample cleaning logs
```

### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 9: Start Development Server

```bash
# Start on localhost only
python manage.py runserver

# Or start on all interfaces (for mobile testing)
python manage.py runserver 0.0.0.0:8000
```

### Step 10: Access the Application

Open your browser:

- **Admin Panel:** http://localhost:8000/admin/
- **Homepage:** http://localhost:8000/
- **API Docs:** http://localhost:8000/api/

**Login with superuser credentials:**
- Email: admin@cleantrack.com
- Password: (your password from Step 6)

---

## Docker Setup

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Step 1: Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: cleantrack
      POSTGRES_USER: cleantrack
      POSTGRES_PASSWORD: cleantrack_password
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn cleantrack.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Step 2: Create Dockerfile

```dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "cleantrack.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Step 3: Build and Run

```bash
# Build images
docker-compose build

# Start containers
docker-compose up -d

# Check logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access application
# http://localhost:8000/admin/
```

### Docker Commands Reference

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v

# Rebuild containers
docker-compose up --build

# View logs
docker-compose logs web

# Execute commands in container
docker-compose exec web python manage.py shell

# Restart specific service
docker-compose restart web
```

---

## Configuration

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG` | Enable debug mode | `False` | Yes |
| `SECRET_KEY` | Django secret key | - | Yes |
| `ALLOWED_HOSTS` | Comma-separated hostnames | `localhost` | Yes |
| `DATABASE_URL` | Database connection string | - | Yes |
| `RESEND_API_KEY` | Resend email API key | - | Yes |
| `STRIPE_TEST_PUBLIC_KEY` | Stripe public key | - | Yes |
| `STRIPE_TEST_SECRET_KEY` | Stripe secret key | - | Yes |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook secret | - | No |
| `STRIPE_LIVE_MODE` | Use live Stripe keys | `False` | No |
| `SITE_URL` | Full site URL | `http://localhost:8000` | Yes |
| `LANGUAGE_CODE` | Default language | `en-us` | No |
| `TIME_ZONE` | Default timezone | `UTC` | No |

### Settings Files

**Development:** `cleantrack/settings.py`
- DEBUG=True
- SQLite database
- Console email backend
- Detailed error pages

**Production:** `cleantrack/settings_production.py`
- DEBUG=False
- PostgreSQL database
- Resend email backend
- Security headers enabled
- Static files via WhiteNoise

**Switch to production settings:**
```bash
export DJANGO_SETTINGS_MODULE=cleantrack.settings_production
python manage.py runserver
```

---

## Database Setup

### SQLite (Development)

**Pros:**
- Zero configuration
- File-based (db.sqlite3)
- Perfect for development

**Cons:**
- Not suitable for production
- Limited concurrent writes

```bash
# Already configured by default
DATABASE_URL=sqlite:///db.sqlite3
```

### PostgreSQL (Production)

**Pros:**
- Production-ready
- Supports concurrent connections
- Advanced features (JSONB, full-text search)

**Cons:**
- Requires separate installation
- More complex setup

**Local PostgreSQL Setup:**

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Access PostgreSQL prompt
sudo -u postgres psql

# Create database and user
CREATE DATABASE cleantrack;
CREATE USER cleantrack_user WITH PASSWORD 'secure_password';
ALTER ROLE cleantrack_user SET client_encoding TO 'utf8';
ALTER ROLE cleantrack_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cleantrack_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cleantrack TO cleantrack_user;
\q

# Update .env
DATABASE_URL=postgresql://cleantrack_user:secure_password@localhost:5432/cleantrack

# Run migrations
python manage.py migrate
```

### Database Migrations

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name migration_name

# Create empty migration
python manage.py makemigrations --empty app_name
```

---

## Running the Application

### Development Server

```bash
# Default (localhost only)
python manage.py runserver

# Specify port
python manage.py runserver 8080

# Allow external connections
python manage.py runserver 0.0.0.0:8000

# With production settings
DJANGO_SETTINGS_MODULE=cleantrack.settings_production python manage.py runserver
```

### Production Server (Gunicorn)

```bash
# Install Gunicorn (already in requirements.txt)
pip install gunicorn

# Start Gunicorn
gunicorn cleantrack.wsgi:application --bind 0.0.0.0:8000

# With workers
gunicorn cleantrack.wsgi:application --bind 0.0.0.0:8000 --workers 4

# With config file
gunicorn -c gunicorn_config.py cleantrack.wsgi:application
```

**gunicorn_config.py:**
```python
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "-"
accesslog = "-"
loglevel = "info"
```

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'django'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

#### 2. Database Connection Error

**Error:**
```
django.db.utils.OperationalError: connection to server failed
```

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Verify DATABASE_URL in .env
echo $DATABASE_URL
```

#### 3. Static Files Not Loading

**Error:**
Static files (CSS/JS) not loading in browser

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT in settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_ROOT)
```

#### 4. Migration Conflicts

**Error:**
```
django.db.migrations.exceptions.InconsistentMigrationHistory
```

**Solution:**
```bash
# Option 1: Fake migrations (development only)
python manage.py migrate --fake

# Option 2: Reset migrations (WARNING: data loss)
python manage.py migrate app_name zero
python manage.py migrate

# Option 3: Delete db.sqlite3 and restart
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### 5. Port Already in Use

**Error:**
```
Error: That port is already in use.
```

**Solution:**
```bash
# Find process using port 8000
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)

# Or use different port
python manage.py runserver 8080
```

#### 6. Permission Denied on build.sh

**Error:**
```
Permission denied: ./build.sh
```

**Solution:**
```bash
# Make executable
chmod +x build.sh

# Run script
./build.sh
```

---

## Verification Checklist

After installation, verify everything works:

- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file configured
- [ ] Database migrations applied
- [ ] Superuser created
- [ ] Development server starts without errors
- [ ] Admin panel accessible at /admin/
- [ ] Can login with superuser account
- [ ] Static files loading correctly
- [ ] Test data generated (optional)

---

## Next Steps

After successful installation:

1. **Read the [User Guide](USER_GUIDE.md)** to understand features
2. **Review [API Documentation](API_DOCUMENTATION.md)** for integration
3. **Check [Deployment Guide](DEPLOYMENT_GUIDE.md)** for production setup
4. **Explore Admin Panel** to create facilities and equipment

---

## Getting Help

**Issues:**
- Check [Troubleshooting](#troubleshooting) section above
- Search [GitHub Issues](https://github.com/yourusername/cleantrack/issues)
- Contact support: natyssis23@gmail.com

**Contributing:**
- See [Contributing Guidelines](CONTRIBUTING.md)
- Review code standards
- Submit pull requests

---

*Last Updated: January 2025 | CleanTrack v1.0.0*
